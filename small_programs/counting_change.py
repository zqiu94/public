# Change making program
def print_change(change_list):
    """
    Prints out the change in the form:
    d dollars, q quarters, m dimes, n nickels, p pennies
    :param change_list: A list in the form [dollars, quarters, dimes,
    nickels, pennies]
    :return: None

    doctests:
    >>> print_change([7, 2, 0, 1, 2])
    7 dollars, 2 quarters, 0 dimes, 1 nickel, 2 pennies

    >>> print_change([1, 1, 1, 1, 1])
    1 dollar, 1 quarter, 1 dime, 1 nickel, 1 penny
    """
    print_list = ""
    change_names = ["dollar", "quarter", "dime", "nickel"]
    for change, change_name in zip(change_list, change_names):
        if change == 1:
            print_list += f"{change} {change_name}, "
        else:
            print_list += f"{change} {change_name}s, "
    if change_list[4] == 1:
        print_list += f"{change_list[4]} penny"
    else:
        print_list += f"{change_list[4]} pennies"

    print(print_list)


def print_dollars_cents(change_list):
    """
    Combines and prints a list in the form [dollars, quarters, dimes, nickels,
    pennies] into a form: $XX.yy.
    :param change_list:
    :return: None

    doctests:
    >>> print_dollars_cents([7, 2, 0, 1, 2])
    $7.57
    >>> print_dollars_cents([124, 1, 1, 0, 0])
    $124.35
    """
    total_cents = 0
    coin_values = [100, 25, 10, 5, 1]
    for change, value in zip(change_list, coin_values):
        total_cents += change * value
    d, c = divmod(total_cents, 100)
    print(f"${d}.{c:02d}")


def make_change(bill_amount_in_dollars, dollars_cost, cents_cost):
    """
    Calculates the change required for a bill in the amount of bill_amount,
    given that the item costs dollars_cost and cents_cost
    e.g., if bill_amount is 20, and the item has a dollars_cost of 12 and a
    cents_cost of 43, the change would be (in cents): 2000 - 1243 = 757 cents,
    which is 7 dollars and 57 cents. The return value would be [7, 2, 0, 1,
    2] for 7 dollars, 2 quarters, 0 dimes, 1 nickel, and 2 pennies.
    :param bill_amount_in_dollars: integer bill denomination in dollars
    :param dollars_cost: integer amount of dollars the item costs
    :param cents_cost: integer amount of cents the item costs
    :return: a list in the form of [dollars, quarters, dimes, nickels, pennies]

    doctests:
    >>> make_change(20, 12, 43)
    [7, 2, 0, 1, 2]
    >>> make_change(100, 99, 99)
    [0, 0, 0, 0, 1]
    """

    bill_cents = bill_amount_in_dollars * 100
    change_cents = bill_cents - dollars_cost * 100 - cents_cost
    change_d, change_c = divmod(change_cents, 100)

    quarter_amount = change_c // 25
    remainder = change_c - quarter_amount * 25
    dime_amount = remainder // 10
    remainder -= dime_amount * 10
    nickel_amount = remainder // 5
    remainder -= nickel_amount * 5
    penny_amount = remainder
    change_list = [change_d, quarter_amount, dime_amount, nickel_amount, penny_amount]
    return change_list


if __name__ == "__main__":
    change = make_change(20, 12, 43)
    print_change(change)
    print_dollars_cents(change)

    change = make_change(50, 28, 14)
    print_change(change)
    print_dollars_cents(change)

# end starter code
