
def ucs_weight(from_node, to_node, weights=None):
    """
    Returns the UCS weight for a edge between from and to
    Assumption: There is no edge with weight >= 10e100 (You can change it)
    :param from_node: The node edge starts from
    :param to_node: The node edge ends to
    :param weights: Dictionary of weights; maps `(from, to) -> weight`
    :return: Returns the weight of edge between from and to.
    """
    return weights.get((from_node, to_node), 10e100) if weights else 1


def ucs(graph, start, end, weights=None):
    """
    Function to compute UCS(Uniform Cost Search) for a graph
    :param graph: The graph to compute UCS for
    :param start: start node
    :param end: end node
    :param weights: A dictionary of weights; maps (start_node, end_node) -> weight
    """
    frontier = PriorityQueue()
    frontier.put((0, start))  # (priority, node)
    global explored
    explored = []

    while True:
        if frontier.empty():
            raise Exception("No way Exception")

        ucs_w, current_node = frontier.get()
        explored.append(current_node)

        if current_node == end:
            return

        for node in graph[current_node]:
            if node not in explored:
                frontier.put((
                    ucs_w + ucs_weight(current_node, node, weights),
                    node
                ))