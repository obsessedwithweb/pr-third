import heapq
from collections import deque
from model import Node
from deadlocks import get_static_deadlocks, is_deadlock

def BFS(initial_state):
    root = Node(initial_state)
    if initial_state.isGoal():
        return root, 0

    open_queue = deque([root])
    open_states = {initial_state.to_tuple()}
    closed_set = set()
    explored_nodes = 0

    while open_queue:
        current_node = open_queue.popleft()
        current_tuple = current_node.state.to_tuple()
        open_states.discard(current_tuple)
        closed_set.add(current_tuple)
        explored_nodes += 1

        for action, successor_state in current_node.state.successorFunction():
            succ_tuple = successor_state.to_tuple()
            if succ_tuple in closed_set or succ_tuple in open_states:
                continue

            child_node = Node(successor_state, parent=current_node, action=action)
            if successor_state.isGoal():
                return child_node, explored_nodes

            open_queue.append(child_node)
            open_states.add(succ_tuple)

    return None, explored_nodes


def A_Star(initial_state, heuristic):
    root = Node(initial_state)
    root.setF(heuristic(initial_state))

    if initial_state.isGoal():
        return root, 0

    open_heap = []
    counter = 0
    heapq.heappush(open_heap, (root.f, counter, root))

    closed_set = set()
    g_costs = {initial_state.to_tuple(): 0}
    explored_nodes = 0

    while open_heap:
        f, _, current_node = heapq.heappop(open_heap)
        current_tuple = current_node.state.to_tuple()

        if current_tuple in closed_set:
            continue

        closed_set.add(current_tuple)
        explored_nodes += 1

        if current_node.state.isGoal():
            return current_node, explored_nodes

        for action, successor_state in current_node.state.successorFunction():
            succ_tuple = successor_state.to_tuple()
            new_g = current_node.g + 1

            if succ_tuple in closed_set and new_g >= g_costs.get(succ_tuple, float('inf')):
                continue

            if new_g < g_costs.get(succ_tuple, float('inf')):
                g_costs[succ_tuple] = new_g
                child_node = Node(successor_state, parent=current_node, action=action, step_cost=1)
                child_node.setF(heuristic(successor_state))
                counter += 1
                heapq.heappush(open_heap, (child_node.f, counter, child_node))

    return None, explored_nodes


def Improved_A_Star(initial_state, heuristic, static_deadlocks=None):
    if static_deadlocks is None:
        static_deadlocks = get_static_deadlocks(initial_state)

    root = Node(initial_state)
    root.setF(heuristic(initial_state))

    if initial_state.isGoal():
        return root, 0

    open_heap = []
    counter = 0
    heapq.heappush(open_heap, (root.f, counter, root))

    closed_set = set()
    g_costs = {initial_state.to_tuple(): 0}
    explored_nodes = 0

    while open_heap:
        f, _, current_node = heapq.heappop(open_heap)
        current_tuple = current_node.state.to_tuple()

        if current_tuple in closed_set:
            continue

        closed_set.add(current_tuple)
        explored_nodes += 1

        if current_node.state.isGoal():
            return current_node, explored_nodes

        for action, successor_state in current_node.state.successorFunction():
            if is_deadlock(successor_state, static_deadlocks):
                continue

            succ_tuple = successor_state.to_tuple()
            new_g = current_node.g + 1

            if succ_tuple in closed_set and new_g >= g_costs.get(succ_tuple, float('inf')):
                continue

            if new_g < g_costs.get(succ_tuple, float('inf')):
                g_costs[succ_tuple] = new_g
                child_node = Node(successor_state, parent=current_node, action=action, step_cost=1)
                child_node.setF(heuristic(successor_state))
                counter += 1
                heapq.heappush(open_heap, (child_node.f, counter, child_node))

    return None, explored_nodes
