import heapq


def find_cycle(graph):
    state = {}
    path = []
    position = {}

    for node in graph:
        state[node] = 0

    def dfs(node):
        state[node] = 1
        position[node] = len(path)
        path.append(node)

        for next_node in sorted(graph[node]):
            if state[next_node] == 0:
                result = dfs(next_node)
                if result:
                    return result
            elif state[next_node] == 1:
                return path[position[next_node]:] + [next_node]

        path.pop()
        position.pop(node)
        state[node] = 2
        return None

    for node in sorted(graph):
        if state[node] == 0:
            result = dfs(node)
            if result:
                return result

    return []


def main():
    try:
        n, e = map(int, input().split())
        modules = []

        for _ in range(n):
            modules.append(input().strip())

        graph = {}
        for module in modules:
            graph[module] = set()

        for _ in range(e):
            a, b = input().split()
            graph[a].add(b)

        dependency_count = {}
        reverse_graph = {}

        for module in modules:
            dependency_count[module] = len(graph[module])
            reverse_graph[module] = set()

        for module in graph:
            for dependency in graph[module]:
                reverse_graph[dependency].add(module)

        heap = []
        for module in modules:
            if dependency_count[module] == 0:
                heapq.heappush(heap, module)

        order = []

        while heap:
            module = heapq.heappop(heap)
            order.append(module)

            for next_module in reverse_graph[module]:
                dependency_count[next_module] -= 1
                if dependency_count[next_module] == 0:
                    heapq.heappush(heap, next_module)

        if len(order) == n:
            print(*order)
        else:
            cycle = find_cycle(graph)
            print("CYCLE")
            print(*cycle)

    except (ValueError, KeyError, EOFError):
        print("INVALID INPUT")


if __name__ == "__main__":
    main()
