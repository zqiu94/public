# There are some trees, where each tree is represented by (x,y) coordinate in a two-dimensional garden.
# Your job is to fence the entire garden using the minimum length of rope as it is expensive.
# The garden is well fenced only if all the trees are enclosed.
# Your task is to help find the coordinates of trees which are exactly located on the fence perimeter.


def outer_trees(points):
    stack = []
    if len(points) <= 3:
        for p in points:
            stack.append(p)
        return stack
    # sort by minimum y-coordinate
    points = sorted(points, key=lambda x: x[1])
    p0 = points[0]
    points = points[1:]
    points_sequence = []
    # sorted by polar angle in counterclockwise, I used slope in this case
    for i in range(len(points)):
        if points[i][1] - p0[1] != 0:
            # slope will be 0 if they have the same x-coordinate
            slope = (points[i][0] - p0[0]) / (points[i][1] - p0[1])
        else:
            # slope will set to infinity it they have the same y-coordinate
            slope = float("inf")
        # xDistanceToRoot and yDistanceToRoot are used for generating preferred sorting result
        x_distance2root = points[i][0] - p0[0]
        y_distance2root = points[i][1] - p0[1]
        points_sequence.append([slope, - x_distance2root, - y_distance2root, points[i]])
    points = [p0]
    # first sort, everything is almost in place
    points_sequence = sorted(points_sequence, reverse=True)
    # if the fence is right above the root point
    # that means there are some points along the fence share the same x-coordinate
    # these points are sorted by the y-coordinate distance to the root
    # the fence is ether draw from the root or draw to the root
    # if these points are draw to the root
    # reverse yDistanceToRoot to make them sorted appropriate: farthest visited first
    if points_sequence[0][1] != points_sequence[1][1]:
        for i in points_sequence:
            i[2] = - i[2]
    # do the second sort, and the result will be perfect to input to the algorithm
    points_sequence = sorted(points_sequence, reverse=True)
    for i in points_sequence:
        points.append(i[3])
    stack.append(points[0])
    stack.append(points[1])
    stack.append(points[2])
    for i in range(3, len(points)):
        while cross_product(i, stack, points) < 0:
            stack.pop()
        stack.append(points[i])
    return stack


def cross_product(i, stack, points):
    x1 = stack[-1][0]
    x0 = stack[-2][0]
    y2 = points[i][1]
    y0 = stack[-2][1]
    x2 = points[i][0]
    y1 = stack[-1][1]
    return (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)


lst = [[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]]
print(outer_trees(lst))
lst = [[1, 2], [2, 2], [4, 2]]
print(outer_trees(lst))
