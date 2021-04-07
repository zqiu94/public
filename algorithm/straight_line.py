# You are given an array coordinates, coordinates[i] = [x, y], where [x, y] represents the coordinate of a point.
# Check if these points make a straight line in the XY plane.

def check_straight_line(coordinates):
    straight = True
    for i in range(2, len(coordinates)):
        x1 = coordinates[i - 1][0]
        x0 = coordinates[i - 2][0]
        y2 = coordinates[i][1]
        y0 = coordinates[i - 2][1]
        x2 = coordinates[i][0]
        y1 = coordinates[i - 1][1]
        cross_product = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if cross_product != 0:
            straight = False
            break
    return straight


coordinates = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
print(check_straight_line(coordinates))
coordinates = [[1, 1], [2, 2], [3, 4], [4, 5], [5, 6], [7, 7]]
print(check_straight_line(coordinates))
