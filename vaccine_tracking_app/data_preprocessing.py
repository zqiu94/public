import requests
import json
from bs4 import BeautifulSoup
import re
import pandas as pd
import io
from sodapy import Socrata
import boto3
import config
from decimal import Decimal

class preprocessing:
    def __init__(self):
        # connect to dynamodb
        self.dynamodb = boto3.resource('dynamodb',
                                       aws_access_key_id=config.AWS_KEY,
                                       aws_secret_access_key=config.AWS_SECRET,
                                       region_name=config.REGION)

    def connect_tables(self):
        self.abbr_connection = self.dynamodb.Table('state_name_abbr')
        self.location_connection = self.dynamodb.Table('location')
        self.county_mapping_connection = self.dynamodb.Table('county_mapping')
        self.covid_visited = self.dynamodb.Table('covid_visited')
        self.vac_visited = self.dynamodb.Table('vac_visited')
        self.covid_data_con = self.dynamodb.Table('covid_data')
        self.vac_data_con = self.dynamodb.Table('vac_data')
        self.load_lookup_tables()

    def load_lookup_tables(self):
        self.full_state_set = [x['full_state_name'] for x in self.abbr_connection.scan()['Items']]

        self.state_name_abbr = {}
        for item in self.abbr_connection.scan()['Items']:
            self.state_name_abbr[item['full_state_name']] = item['abbreviation']

        self.location_mapping = {}
        for item in self.location_connection.scan()['Items']:
            self.location_mapping[item['county_state']] = int(item['location_id'])

        self.county_mapping = {}
        for item in self.county_mapping_connection.scan()['Items']:
            self.county_mapping[item['county_name']] = item['simplified_name']

    def update_all(self):
        self.update_covid_data()
        self.update_vac_data()

    def update_covid_data(self):
        # github covid data repo url
        repo = "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"

        # get all file names from meta data
        meta_info = requests.get(repo)
        soup = BeautifulSoup(meta_info.text, 'html.parser')
        csvfiles = soup.find_all(title=re.compile("\.csv$"))

        # raw file url
        covid_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

        covid_df = pd.DataFrame()

        # column white list
        covid_col_list = ['Admin2', 'Province_State', 'Last_Update', 'Confirmed', 'Deaths', 'Recovered', 'Active']

        # for file in csvfiles:
        # * for testing purpose only *
        # for file in csvfiles[:1]:
        for file in csvfiles:
            file = file.extract().get_text()
            visited = self.covid_visited.get_item(Key={'file_address': file})
            # if not visited
            if 'Item' not in visited.keys():
                self.covid_visited.put_item(Item={'file_address': file})
                file_url = covid_url + file
                download = requests.get(file_url).content
                # data before 03-21-2020 are not formated
                try:
                    df = pd.read_csv(io.StringIO(download.decode('utf-8')), usecols=covid_col_list)
                    covid_df = covid_df.append(df)
                except:
                    pass
            else:
                pass
        if covid_df.shape[0] > 0:
            covid_df = self.preprocess(covid_df, 'covid_df')

        # push preprocessed data to danamodb
        with self.covid_data_con.batch_writer() as batch:
            for index, row in covid_df.iterrows():
                batch.put_item(json.loads(row.to_json(), parse_float=Decimal))

    def update_vac_data(self):
        vac_df = pd.DataFrame()
        # 51 US states
        state_str = ', '.join(['"' + x + '"' for x in list(self.state_name_abbr.values())])

        # socrata API
        client = Socrata("data.cdc.gov", None)
        # API query
        dates = client.get("8xkx-amqh", select='distinct date')

        # for date in dates:
        # * for testing purpose only *
        # for date in dates[:1]:
        for date in dates:
            date = date['date']
            visited = self.vac_visited.get_item(Key={'date_visited': date})
            # if not visited
            if 'Item' not in visited.keys():
                self.vac_visited.put_item(Item={'date_visited': date})
                results = client.get("8xkx-amqh",
                                     select='date, recip_county, recip_state, series_complete_yes, series_complete_pop_pct',
                                     where=f'date = "{date}" AND recip_state in ({state_str})', limit=2000000)
                vac_df = vac_df.append(pd.DataFrame.from_records(results))
            else:
                pass
        if vac_df.shape[0] > 0:
            vac_df = self.preprocess(vac_df, 'vac_df')

        # push preprocessed data to danamodb
        with self.vac_data_con.batch_writer() as batch:
            for index, row in vac_df.iterrows():
                batch.put_item(json.loads(row.to_json(), parse_float=Decimal))

    def preprocess(self, df, data_name):
        if data_name == 'covid_df':
            # strip time from date
            df['Last_Update'] = df['Last_Update'].str[:10]
            # filter US only states
            df = df[df['Province_State'].isin(self.full_state_set)]
            # repalce full state name to abbreviation
            df = df.replace({'Province_State': self.state_name_abbr})
            # concatenate county and state
            df['Location'] = df['Admin2'] + ', ' + df['Province_State']
            df = df.replace({'Location': self.location_mapping})
            df = df[["Last_Update", "Confirmed", 'Deaths', 'Recovered', 'Active', 'Location']]
            # assign an uuid, which is the concatenation of date and location
            df['uuid'] = df['Last_Update'] + '-' + df['Location'].map(str)

        elif data_name == 'vac_df':
            # strip time from date
            df['date'] = df['date'].str[:10]
            df = df.replace({"recip_county": self.county_mapping})
            # concatenate county and state
            df['location'] = df['recip_county'] + ', ' + df['recip_state']
            df = df.replace({'location': self.location_mapping})
            df = df[["date", "series_complete_yes", 'series_complete_pop_pct', 'location']]
            # assign an uuid, which is the concatenation of date and location
            df['uuid'] = df['date'] + '-' + df['location'].map(str)

        df.columns = df.columns.str.lower()
        return df