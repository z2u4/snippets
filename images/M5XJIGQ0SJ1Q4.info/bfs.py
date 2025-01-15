from queue import Queue, PriorityQueue

explored = []

def bfs(graph, start, end):
    """
    Compute DFS(Depth First Search) for a graph
    :param graph: The given graph
    :param start: Node to start BFS
    :param end: Goal-node
    """
    frontier = Queue()
    frontier.put(start)
    global explored
    explored = []

    while True:
        if frontier.empty():
            raise Exception("No way Exception")
        current_node = frontier.get()
        explored.append(current_node)

        # Check if node is goal-node
        if current_node == end:
            return

        for node in graph[current_node]:
            if node not in explored:
                frontier.put(node)