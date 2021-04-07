# There is an undirected graph with n nodes, where each node is numbered between 0 and n - 1. You are given a 2D array
# graph, where graph[u] is an array of nodes that node u is adjacent to. More formally, for each v in graph[u],
# there is an undirected edge between node u and node v. The graph has the following properties:
#
# There are no self-edges (graph[u] does not contain u).
# There are no parallel edges (graph[u] does not contain duplicate values).
# If v is in graph[u], then u is in graph[v] (the graph is undirected).
# The graph may not be connected, meaning there may be two nodes u and v such that there is no path between them.
# A graph is bipartite if the nodes can be partitioned into two independent sets A and B such that every edge in
# the graph connects a node in set A and a node in set B.
#
# Return true if and only if it is bipartite.


def is_bipartite(graph):
    bipartite = True
    red_list = []
    blue_list = []
    # while not all vertexes have been discovered
    while (len(red_list) + len(blue_list)) < len(graph):
        complement = [item for item in range(len(graph)) if item not in red_list and item not in blue_list]
        # bfs the next undiscovered item
        source = complement[0]
        bfs(source, red_list, blue_list, graph)
    # connected vertexes can't be in the same list
    for i in range(len(graph)):
        for j in graph[i]:
            if i in red_list and j in red_list:
                bipartite = False
            elif i in blue_list and j in blue_list:
                bipartite = False
    return bipartite


def bfs(source, red_list, blue_list, graph):
    # always append the source into the red list
    red_list.append(source)
    queue = [source]
    while len(queue) > 0:
        # dequeue
        u = queue.pop(0)
        for i in graph[u]:
            # if not discovered
            if i not in red_list and i not in blue_list:
                # if its parent in red list
                if u in red_list:
                    blue_list.append(i)
                # else its parent in blue list
                else:
                    red_list.append(i)
                # enqueue
                queue.append(i)


graph = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]
print(is_bipartite(graph))
graph = [[1, 3], [0, 2], [1, 3], [0, 2]]
print(is_bipartite(graph))
