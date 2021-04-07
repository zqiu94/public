# There are a total of numCourses courses you have to take, labeled from 0 to num_courses - 1.
# You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course
# bi first if you want to take course ai.

# For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
# Return true if you can finish all courses. Otherwise, return false.


def can_finish(num_courses, prerequisites):
    back_edges = []
    color = []
    for i in range(num_courses):
        color.append("white")
    for u in range(num_courses):
        if color[u] == "white":
            dfs_visit(prerequisites, u, color, back_edges)
    if len(back_edges) > 0:
        return False
    else:
        return True


def dfs_visit(p, u, color, back_edges):
    color[u] = "grey"
    for e in p:
        if e[1] == u:
            if color[e[0]] == "white":
                dfs_visit(p, e[0], color, back_edges)
            elif color[e[0]] == "grey":
                back_edges.append([e[0], e[1]])
    color[u] = "black"


num_courses = 2
prerequisites = [[1, 0]]
print(can_finish(num_courses, prerequisites))

num_courses = 2
prerequisites = [[1, 0], [0, 1]]
print(can_finish(num_courses, prerequisites))
