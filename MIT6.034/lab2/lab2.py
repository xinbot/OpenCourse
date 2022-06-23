# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.
def bfs(graph, start, goal):
    # Form a one-element queue consisting of a zero-length path that contains only the root node.
    queue = [[start]]
    # Avoid extending the same node multiple times.
    extended = set()
    extended.add(start)
    # Until the first path in the queue terminates at the goal node or the queue is empty
    while len(queue) > 0:
        # Remove the first path from the queue
        path = queue.pop(0)
        # The terminal node
        if path[-1] == goal:
            # The goal node is found
            return path
        else:
            # Extending the first path to all the neighbors of the terminal node
            for node in graph.get_connected_nodes(path[-1]):
                # Reject all new paths with loops
                if node not in extended:
                    extended.add(node)
                    # Add new paths, if any, to the back of the queue
                    queue.append(path + [node])
    return []

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    # Form a one-element queue consisting of a zero-length path that contains only the root node.
    queue = [[start]]
    # Avoid extending the same node multiple times.
    extended = set()
    extended.add(start)
    # Until the first path in the queue terminates at the goal node or the queue is empty
    while len(queue) > 0:
        # Remove the first path from the queue
        path = queue.pop(0)
        # The terminal node
        if path[-1] == goal:
            # The goal node is found
            return path
        else:
            # Extending the first path to all the neighbors of the terminal node
            for node in graph.get_connected_nodes(path[-1]):
                # Reject all new paths with loops
                if node not in extended:
                    extended.add(node)
                    # Add new paths, if any, to the front of the queue
                    queue.insert(0,  path + [node])
    return []

## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def get_heuristic(graph, goal, node):
    if node:
        return graph.get_heuristic(node, goal)
    else:
        return 9223372036854775807 # Max_Integer

def hill_climbing(graph, start, goal):
    # Form a one-element queue consisting of a zero-length path that contains only the root node.
    queue = [[start]]
    # Until the queue is empty
    while len(queue) > 0:
        # Remove the first path from the queue
        path = queue.pop(0)
        # The terminal node
        if path[-1] == goal:
            # The goal node is found
            return path
        else:
            new_paths = []
            # Extending the first path to all the neighbors of the terminal node
            for node in graph.get_connected_nodes(path[-1]):
                # Reject all new paths with loops
                if node not in path:
                    new_paths.append(path + [node])
            # Sort the new paths, if any, by the estimated distance between their terminal nodes and the goal
            new_paths = sorted(new_paths, key=lambda path : get_heuristic(graph, goal, path[-1]))
            # Add the new paths, if any, to the front of the queue
            queue = new_paths + queue
    return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    # Form a one-element queue consisting of a zero-length path that contains only the root node.
    # Beam Search does not use an extended-set
    queue = [[start]]
    while len(queue) > 0:
        new_paths = []
        # Pop the entire level n of the search graph
        while len(queue) > 0:
            # Remove path from the queue
            path = queue.pop()
            if path[-1] == goal:
                # The goal node is found
                return path
            else:
                # Extending the path to all the neighbors of the terminal node
                for node in graph.get_connected_nodes(path[-1]):
                    # Reject all new paths with loops
                    if node not in path:
                        new_paths.append(path + [node])
        # Sort the new paths at level n
        new_paths = sorted(new_paths, key=lambda path : get_heuristic(graph, goal, path[-1]))
        # Make sure that there are noly beam_width paths at entire level (No Backtracing)
        while len(new_paths) > beam_width:
            new_paths.pop()
        # Refresh agenda
        queue = new_paths
    return []

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    if len(node_names) > 0:
        last_node = None
        for index in range(0, len(node_names)):
            node = node_names[index]
            if last_node == None:
                last_node = node
            else:
                edge = graph.get_edge(last_node, node)
                if edge != None:
                    length += edge.length
                last_node = node
        return length
    else:
        return length

def branch_and_bound(graph, start, goal):
    # Form a one-element queue consisting of a zero-length path that contains only the root node.
    # Branch-and-bound does not use an extended-set
    queue = [[start]]
    # Until the queue is empty
    while len(queue) > 0:
        # Remove the first path from the queue
        path = queue.pop(0)
        # Until the first path in the queue terminates at the goal node
        if path[-1] == goal:
            return path
        else:
            # Extending the path to all the neighbors of the terminal node
            for node in graph.get_connected_nodes(path[-1]):
                # Reject all new paths with loops
                if node not in path:
                    # Add the remaining new paths, if any. to the queue
                    queue.append(path + [node])
            # Sort the entire queue by path length with least-cost paths in front
            queue = sorted(queue, key=lambda node_names : path_length(graph, node_names))
    return []

def a_star_heuristic(graph, goal, node_names):
    length = path_length(graph, node_names)
    heuristic = graph.get_heuristic(node_names[-1], goal)
    return length + heuristic

def a_star(graph, start, goal):
    # Form a one-element queue consisting of a zero-length path that contains only the root node.
    queue = [[start]]
    extended_set = {start : path_length(graph, [start])}
     # Until the queue is empty
    while len(queue) > 0:
        # Remove the first path from the queue
        path = queue.pop(0)
        # Until the first path in the queue terminates at the goal node
        if path[-1] == goal:
            return path
        else:
            # Extending the path to all the neighbors of the terminal node
            for node in graph.get_connected_nodes(path[-1]):
                # Reject all new paths with loops
                if node not in path:
                    new_path = path + [node]
                    # If two or more paths reach a common node, delete all those paths except the one that
                    # reaches the common node with the minimum cost
                    if node in extended_set:
                        new_path_length = path_length(graph, new_path)
                        record_path_length  = path_length(graph, extended_set[node])
                        if new_path_length < record_path_length:
                            extended_set[node] = new_path
                            for i in xrange(len(queue)):
                                if queue[i][-1] == node:
                                    queue[i] = new_path
                    else:
                        extended_set[node] = new_path
                        queue.append(new_path)
            # Sort the entire queue by the sum of the path length and a lower-bound estimate
            # of the cost remaining, with least-cost paths in front.
            queue = sorted(queue, key=lambda node_names : a_star_heuristic(graph, goal, node_names))
    return []

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?
def dijkstra(graph, start):
    distance = {start : 0} 
    previous = {start : None}
    queue = [(0, start)] # (distance, node_name)
    extended_set = {}
    while len(queue) > 0:
        node = queue.pop(0)
        extended_set[node[1]] = True
        for new_node in graph.get_connected_nodes(node[1]):
            if new_node not in extended_set:
                new_distance = node[0] + graph.get_edge(node[1], new_node).length
                if new_node in distance:
                    if new_distance < distance[new_node]:
                       distance[new_node] = new_distance
                       previous[new_node] = node[1]
                       queue.append((new_distance, new_node))
                else:
                   distance[new_node] = new_distance
                   previous[new_node] = node[1]
                   queue.append((new_distance, new_node))
    return (distance, previous)

def is_admissible(graph, goal):
    distance, previous = dijkstra(graph, goal)
    for node in graph.nodes:
        if distance[node] < graph.get_heuristic(node, goal):
            return False
    return True

def is_consistent(graph, goal):
    for edge in graph.edges:
        if edge.length < abs(graph.get_heuristic(edge.node1, goal) - graph.get_heuristic(edge.node2, goal)):
            return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '24'
WHAT_I_FOUND_INTERESTING = 'Optimal Searching'
WHAT_I_FOUND_BORING = 'Debugging'