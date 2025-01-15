def dfs(graph, start, end):
    """
    Compute dfs for a graph
    :param graph: The given graph
    :param start: Node to start bfs
    :param end: Goal-node
    """
    frontier = [start, ]
    global explored
    explored = []

    while True:
        if len(frontier) == 0:
            raise Exception("No way Exception")
        current_node = frontier.pop()
        explored.append(current_node)

        # Check if node is goal-node
        if current_node == end:
            return

        # expanding nodes
        for node in reversed(graph[current_node]):
            if node not in explored:
                frontier.append(node)