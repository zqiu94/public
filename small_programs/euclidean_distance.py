from math import sqrt


def distance(x1, y1, x2, y2):
    """
    Calculates the euclidean distance between two points on a plane
    :param x1: The x-coordinate of the first point
    :param y1: The y-coordinate of the first point
    :param x2: The x-coordinate of the second point
    :param y2: The y-coordinate of the second point
    :return: a float that is the euclidean distance between the two points

    >>> distance(1,2,3,4)
    2.8284271247461903
    >>> distance(8,6,4,2)
    5.656854249492381
    >>> distance(0.5,1.5,2.5,3.5)
    2.8284271247461903
    """
    euclidean_distance = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    return euclidean_distance


if __name__ == '__main__':
    print("Calculating Euclidean Distance")
    x_1 = float(input("x1: "))
    y_1 = float(input("y1: "))
    x_2 = float(input("x2: "))
    y_2 = float(input("y2: "))
    print(distance(x_1, y_1, x_2, y_2))
