import boto3
import config
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix
from sklearn.model_selection import train_test_split
from boto3.dynamodb.conditions import Key


class predictor():
    def __init__(self):
        # db connection
        self.dynamodb = boto3.resource('dynamodb',
                                       aws_access_key_id=config.AWS_KEY,
                                       aws_secret_access_key=config.AWS_SECRET,
                                       region_name=config.REGION)

        # table connection
        self.covid_data = self.dynamodb.Table('covid_data')
        self.vac_data = self.dynamodb.Table('vac_data')
        self.location = self.dynamodb.Table('location')
        # *add in the future
        # self.distribution = self.dynamodb.Table('distribution')

        self.training_days = 30

    def location_filter(self, data_name, state, county):
        # load full location table
        location_ids = []
        location_scan = self.location.scan()

        # future work: if we reform location table on AWS, it will have a better performance
        if not state and not county:
            for item in location_scan['Items']:
                location_ids.append(int(item['location_id']))

        elif state:
            if not county:
                for item in location_scan['Items']:
                    if item['county_state'].split(', ')[1] == state:
                        location_ids.append(int(item['location_id']))

            elif county:
                for item in location_scan['Items']:
                    if item['county_state'].split(', ')[1] == state and item['county_state'].split(', ')[0] == county:
                        location_ids.append(int(item['location_id']))
        else:
            # add error handling
            pass

        filtered_data = []

        # query data by location id
        # AWS has 1 mb limit on return items, so a for loop has been used to make sure all records are returned
        if data_name == 'covid':
            for location_id in location_ids:
                response = self.covid_data.query(KeyConditionExpression=Key('location').eq(str(location_id)))
                filtered_data += response['Items']
        elif data_name == 'vac':
            for location_id in location_ids:
                response = self.vac_data.query(KeyConditionExpression=Key('location').eq(str(location_id)))
                filtered_data += response['Items']
        elif data_name == 'coefficient':
            filtered_data2 = []
            for location_id in location_ids:
                response = self.vac_data.query(KeyConditionExpression=Key('location').eq(str(location_id)))
                response2 = self.covid_data.query(KeyConditionExpression=Key('location').eq(str(location_id)))
                filtered_data += response['Items']
                filtered_data2 += response2['Items']
                filtered_data = (filtered_data, filtered_data2)

        return filtered_data

    def load_data(self, data_name, state, county):
        # key is date, value is data for that date
        dates = {}
        response = self.location_filter(data_name, state, county)
        x_axis = []
        y_axis = []

        # x_axis = distribution data
        # y_axis = covid_confirmed
        if data_name == 'coefficient':
            distribution = response[0]
            confirmed = response[1]
            for item in distribution:
                dates[item['date']] = {'distribution': item['series_complete_yes']}
            for item in confirmed:
                dates[item['last_update']] = {'confirmed': item['confirmed']}
            for k, v in dates.items():
                if len(v) == 2:
                    x_axis.append(v['distribution'])
                    y_axis.append(v['confirmed'])

        else:

            if data_name == 'covid':
                for item in response:
                    if item['last_update'] in dates:
                        dates[item['last_update']] += int(item['confirmed'])
                    else:
                        dates[item['last_update']] = int(item['confirmed'])

            elif data_name == 'vac':
                for item in response:
                    if item['series_complete_yes']:
                        if item['date'] in dates:
                            dates[item['date']] += int(item['series_complete_yes'])
                        else:
                            dates[item['date']] = int(item['series_complete_yes'])

            keys = list(dates.keys())
            formatted_keys = []
            # early data is not formatted, so they are removed
            for k in keys:
                try:
                    datetime.strptime(k, '%Y-%m-%d')
                    formatted_keys.append(k)
                except:
                    pass

            # sort by date from earliest to latest
            sorted_date = sorted(formatted_keys, key=lambda d: datetime.strptime(d, '%Y-%m-%d'))[-self.training_days:]

            # return confirmed cases time series

            # x_axis = date(0, 1, 2, 3, 4, 5 ...)
            # y_axis = covid_confirmed/vac_completed
            for i in range(len(sorted_date)):
                x_axis.append(i)
                y_axis.append(dates[sorted_date[i]])

        x_axis = np.array(x_axis).reshape(-1, 1)
        y_axis = np.array(y_axis).reshape(-1, 1)
        return x_axis, y_axis

    def train_linear_regr(self, data_name, state=None, county=None):
        x_axis, y_axis = self.load_data(data_name, state, county)
        x_train, x_test, y_train, y_test = train_test_split(x_axis, y_axis, test_size=0.2)
        self.regr = linear_model.LinearRegression()

        # Train the model using the training sets
        self.regr.fit(x_train, y_train)

    def predict_one_week(self):
        predicted_results = []
        for i in range(self.training_days, self.training_days + 7):
            predicted_results.append(int(self.regr.predict(np.array([i]).reshape(-1, 1))))
        return predicted_results

    def predict_coefficient(self, distribution_amount):
        return int(self.regr.predict(np.array([distribution_amount]).reshape(-1, 1)))


test = predictor()
test.train_linear_regr('covid', 'CA', 'Santa Clara')
print(test.predict_one_week())


# test.train_linear_regr('coefficient', 'CA', 'Santa Clara')
# print(test.predict_coefficient(100000))
