import copy
import itertools

import networkx as nx


class GraphTraversal:
    def __init__(self, graph: list[list[int] | list[list[int | str]]]):
        self._graph_nodes = graph[0]
        self._graph_edges = graph[1]
        self._in_degree = [0 for _ in range(len(self._graph_nodes))]
        self._out_degree = [0 for _ in range(len(self._graph_nodes))]
        self._visited = [False for _ in range(len(self._graph_nodes))]
        self._forward_paths = []
        self._loops = []
        self._loops_without_duplicates = []
        self._double_non_touching_loops = []
        self._loops_not_touching_forward_paths = []
        self._non_touching_loops = []

        self._adj_list = self._create_adj_list_representation()
        if not self._is_valid_graph(self._generate_forward_paths_and_loops()):
            return
        self._loops_without_duplicates = self._remove_duplicates(self._loops)
        self._graph_of_non_touching_loops = self._get_graph_of_non_touching_loops()
        self._non_touching_loops = self._get_all_non_touching_loops()
        self._get_loops_after_removing_forward_paths()

    def get_forward_paths(self):
        return self._forward_paths

    def get_loops(self):
        return self._loops_without_duplicates

    def get_non_touching_loops(self):
        return self._non_touching_loops

    def get_loops_not_touching_forward_paths(self):
        return self._loops_not_touching_forward_paths

    def _is_valid_graph(self, flag):
        if not flag:
            print("Invalid graph")
            return False
        for i in range(len(self._out_degree)):
            if self._out_degree[i] == 0:
                if self._in_degree[i] == 0:
                    print("Invalid graph")
                    return False
                return True
        print("Invalid graph")
        return False

    def _create_adj_list_representation(self):
        adj_list = []
        for _ in self._graph_nodes:
            adj_list.append([])
        for edge in self._graph_edges:
            adj_list[edge[0]].append([])
            adj_list[edge[0]][-1].append(edge[1])
            adj_list[edge[0]][-1].append(edge[2])
            self._in_degree[edge[1]] += 1
            self._out_degree[edge[0]] += 1
        return adj_list

    def _get_forward_paths_and_loops(self, path, node):
        path[0].append(node[0])  # Append node name
        path[1].append(node[1])  # Append node gain
        if self._out_degree[node[0]] == 0:
            copied_path = copy.deepcopy(path)
            self._forward_paths.append(copied_path)
            path[0].pop()
            path[1].pop()
        elif self._visited[node[0]]:
            path[0].pop()
            copied_path = copy.deepcopy(path)
            self._handle_loops(copied_path, node)
            self._loops.append(copied_path)
            path[1].pop()
        else:
            self._visited[node[0]] = True
            for child in self._adj_list[node[0]]:
                self._get_forward_paths_and_loops(path, child)
            path[0].pop()
            path[1].pop()
            self._visited[node[0]] = False

    def _handle_loops(self, path, node):
        for i in range(len(path[0])):
            if path[0][i] == node[0]:
                path[0] = path[0][i:]
                path[1] = path[1][i:]
                return

    def _get_start_node(self):
        for i in range(len(self._in_degree)):
            if self._in_degree[i] == 0:
                return i
        return -1  # Error

    def _get_graph_of_non_touching_loops(self):
        adj_list = []
        for i in range(len(self._loops_without_duplicates)):
            adj_list.append([])
        for i in range(len(self._loops_without_duplicates)):
            for j in range(i + 1, len(self._loops_without_duplicates)):
                if not self._check_if_loops_touch(self._loops_without_duplicates[i], self._loops_without_duplicates[j]):
                    adj_list[i].append(j)
                    adj_list[j].append(i)
                    self._double_non_touching_loops.append([i, j])
        return adj_list

    def _check_if_loops_touch(self, loop1, loop2):
        for node in loop1[0]:
            if node in loop2[0]:
                return True
        return False

    def _get_all_non_touching_loops(self):
        cliques = []
        vertices = set(range(len(self._graph_of_non_touching_loops)))
        self._bron_kerbosch([], vertices, set(), self._graph_of_non_touching_loops, cliques)
        return self._get_all_combinations(cliques)

    def _bron_kerbosch(self, r, p, x, graph, cliques):
        if not p and not x:
            cliques.append(r)
            return
        pivot = max(p.union(x), key=lambda y: len(set(graph[y]) & p))
        for v in list(p - set(graph[pivot])):
            self._bron_kerbosch(r + [v], p.intersection(graph[v]), x.intersection(graph[v]), graph, cliques)
            p.remove(v)
            x.add(v)

    def _get_all_combinations(self, cliques):
        all_combinations = []
        for sublist in cliques:
            for r in range(1, len(sublist) + 1):
                combinations = itertools.combinations(sublist, r)
                for combination_tuple in combinations:
                    combination_list = list(combination_tuple)
                    all_combinations.append(combination_list)
        unique_combinations = set(tuple(sorted(cycle)) for cycle in all_combinations)
        return [list(combination) for combination in unique_combinations]

    def _dfs_graph(self, node, parent, visited, non_touching_loops, path, passed_by):
        path.append(node)
        visited[node] = 1
        passed_by.add(node)
        for child in self._graph_of_non_touching_loops[node]:
            if child != parent:
                if visited[child] == 0:
                    self._dfs_graph(child, node, visited, non_touching_loops, path, passed_by)
                elif visited[child] == 1:
                    path_copy = copy.deepcopy(path)
                    path_copy = self._handle_loops_for_non_touching_loops(path_copy, child)
                    non_touching_loops.append(path_copy)
        path.pop()
        visited[node] = 0

    def _handle_loops_for_non_touching_loops(self, path, node):
        for i in range(len(path)):
            if path[i] == node:
                return path[i:]

    def _get_loops_after_removing_forward_paths(self):
        for path in self._forward_paths:
            non_touching_loops = copy.deepcopy(self._non_touching_loops)
            for i in range(len(self._loops_without_duplicates)):
                if self._check_if_loops_touch(path, self._loops_without_duplicates[i]):
                    self._remove_all_occurrences_of_loop(non_touching_loops, i)
            unique_cycles = set(tuple(sorted(cycle)) for cycle in non_touching_loops)
            self._loops_not_touching_forward_paths.append([list(cycle) for cycle in unique_cycles])

    def _remove_all_occurrences_of_loop(self, loops, index):
        for i in range(len(loops)):
            if index in loops[i]:
                loops[i].remove(index)
        while [] in loops:
            loops.remove([])

    def _generate_forward_paths_and_loops(self):
        start_node = self._get_start_node()
        if start_node == -1:
            print("Couldn't find start node'")
            return False  # Error
        for child in self._adj_list[start_node]:
            self._get_forward_paths_and_loops([[start_node], []], child)
        return True

    def _remove_duplicates(self, loops):
        seen = set()
        unique_data = []
        for idx, sublist in enumerate(loops):
            first_list = sublist[0]
            sorted_first_list = tuple(sorted(first_list))
            if sorted_first_list not in seen:
                seen.add(sorted_first_list)
                unique_data.append(sublist)
        return unique_data
