# A city's skyline is the outer contour of the silhouette formed by all the buildings in that city when viewed from
# a distance. Given the locations and heights of all the buildings, return the skyline formed by these buildings
# collectively.
#
# The geometric information of each building is given in the array buildings where buildings[i] =
# [lefti, righti, heighti]:
#
# lefti is the x coordinate of the left edge of the ith building.
# righti is the x coordinate of the right edge of the ith building.
# heighti is the height of the ith building.
# You may assume all buildings are perfect rectangles grounded on an absolutely flat surface at height 0.
#
# The skyline should be represented as a list of "key points" sorted by their x-coordinate in the form
# [[x1,y1],[x2,y2],...]. Each key point is the left endpoint of some horizontal segment in the skyline except
# the last point in the list, which always has a y-coordinate 0 and is used to mark the skyline's termination
# where the rightmost building ends. Any ground between the leftmost and rightmost buildings should be part of
# the skyline's contour.
#
# Note: There must be no consecutive horizontal lines of equal height in the output skyline. For instance,
# [...,[2 3],[4 5],[7 5],[11 5],[12 7],...] is not acceptable; the three lines of height 5 should be merged
# into one in the final output as such: [...,[2 3],[4 5],[12 7],...]

def get_skyline(buildings):
    heap = []
    points = []
    key_points = []
    # extract the value of the upper left point and upper tight point of the building
    # "0" means it is the starting point and "1" means it is an ending point
    # for sorting purpose
    for b in buildings:
        points.append([b[0], "0", b[2]])
        points.append([b[1], "1", b[2]])
    # sort by x coordinates, then by "0"/"1"
    points = sorted(points)
    # use lastPoint to track the last highest value
    # lastPoint is also the default/first point to put in the heap
    last_point = [- 1, 0, 0]
    heap_insert(heap, last_point)
    for p in points:
        # if p is a start point
        if p[1] == "0":
            # then put it into the heap
            heap_insert(heap, p)
            # if the highest value changes, then we record the key point
            if heap[0][2] > last_point[2] and heap[0][0] > last_point[0]:
                key_points.append([heap[0][0], heap[0][2]])
                last_point = heap[0]
            # else if multiple changes found on the same x coordinate
            elif heap[0][2] > last_point[2] and heap[0][0] == last_point[0]:
                key_points.pop()
                key_points.append([heap[0][0], heap[0][2]])
                last_point = heap[0]
        # if p is an ending point then remove it from the heap
        elif p[1] == "1":
            # if p is the root, it can be done in O(log(n)) time
            if p[2] == heap[0][2]:
                heap_extract_max(heap)
                if heap[0][2] != last_point[2]:
                    key_points.append([p[0], heap[0][2]])
            # else p isn't the root, then it can be done in O(n) time
            else:
                for i in range(len(heap)):
                    if heap[i][1] == "0" and heap[i][2] == p[2]:
                        found = i
                        break
                heap[found], heap[-1] = heap[-1], heap[found]
                heap.pop()
                max_heapify(heap, found)
            last_point = heap[0]
    return sorted(key_points)


def heap_insert(A, key):
    A.append(key)
    index = len(A) - 1
    while A[index][2] > A[(index + 1) // 2 - 1][2] and index > 0:
        A[index], A[(index + 1) // 2 - 1] = A[(index + 1) // 2 - 1], A[index]
        index = (index + 1) // 2 - 1


def heap_extract_max(A):
    A[0] = A[-1]
    A.pop()
    max_heapify(A, 0)


def max_heapify(A, i):
    l = 2 * (i + 1) - 1
    r = 2 * (i + 1)
    if l <= (len(A) - 1) and A[l][2] > A[i][2]:
        largest = l
    else:
        largest = i
    if r <= (len(A) - 1) and A[r][2] > A[largest][2]:
        largest = r
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, largest)


buildings = [[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]
print(get_skyline(buildings))
buildings = [[0, 2, 3], [2, 5, 3]]
print(get_skyline(buildings))
