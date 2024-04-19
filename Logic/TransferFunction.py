import sympy as sp


class TransferFunction:
    def __init__(self, forward_paths, loops, non_touching_loops, loops_not_touching_forward_paths):
        self._forward_paths = forward_paths
        self._loops = loops
        self._non_touching_loops = non_touching_loops
        self._loops_not_touching_forward_paths = loops_not_touching_forward_paths
        self._loops_gains = []
        self._forward_paths_gains = []
        self._delta_of_forward_paths = []
        self._non_touching_loops_gains = []
        self._transfer_function = '( '

        self._assign_data()
        self._calculate_transfer_function()

    def get_transfer_function(self):
        return self._transfer_function

    def get_delta(self):
        simplified = sp.sympify(self._non_touching_loops_gains)
        return sp.simplify(simplified)

    def get_forward_paths_delta(self):
        container = []
        for delta in self._delta_of_forward_paths:
            container.append(sp.simplify(sp.sympify(delta)))
        return container

    def _assign_data(self):
        self._non_touching_loops = self._group_lists_by_length(self._non_touching_loops)

        temp = []
        for loops in self._loops_not_touching_forward_paths:
            temp.append(self._group_lists_by_length(loops))
        self._loops_not_touching_forward_paths = temp

        for path in self._forward_paths:
            self._forward_paths_gains.append(self._calculate_forward_path_gain(path[1]))

        for loop in self._loops:
            self._loops_gains.append(self._calculate_loop_gain(loop[1]))

        for loop in self._loops_not_touching_forward_paths:
            self._delta_of_forward_paths.append(self._calculate_forward_path_delta(loop))

        self._non_touching_loops_gains = self._calculate_delta(self._non_touching_loops)

    def _calculate_forward_path_gain(self, forward_path: list[str]):
        return self._calculate_loop_gain(forward_path)

    def _calculate_loop_gain(self, loop: list[str]):
        gain = f" ( {loop[0]} )"
        for edge in loop[1:]:
            gain += f" * ( {edge} )"
        return gain

    def _calculate_delta(self, loops: list[list[list[int]]]):
        return self._calculate_forward_path_delta(loops)

    def _calculate_forward_path_delta(self, forward_path_loops: list[list[list[int]]]):
        delta = '1'
        if len(forward_path_loops) == 0:
            return delta
        for lists_of_same_size in forward_path_loops:
            summation = '( '
            flag_summation = False
            for list_of_non_touching_loops in lists_of_same_size:
                product = ''
                flag_product = False
                for loop_index in list_of_non_touching_loops:
                    if not flag_product:
                        product += f"( {self._loops_gains[loop_index]} )"
                        flag_product = True
                    else:
                        product += f" * ( {self._loops_gains[loop_index]} )"
                if not flag_summation:
                    summation += f"( {product} )"
                    flag_summation = True
                else:
                    summation += f" + ( {product} )"
            summation += ' )'
            sign = '-' if (-1) ** len(lists_of_same_size[0]) == -1 else '+'
            delta += f" {sign} ( {summation} )"
        return delta

    def _calculate_transfer_function(self):
        s = sp.symbols('s')
        flag = False
        for i in range(len(self._forward_paths)):
            if not flag:
                self._transfer_function += f"( ( {self._forward_paths_gains[i]} ) * ( {self._delta_of_forward_paths[i]} ) )"
                flag = True
            else:
                self._transfer_function += f" + ( ( {self._forward_paths_gains[i]} ) * ( {self._delta_of_forward_paths[i]} ) )"

        self._transfer_function += f" ) * ( 1 / ( {self._non_touching_loops_gains} ) )"
        expression_string = sp.sympify(self._transfer_function)
        self._transfer_function = sp.simplify(expression_string)

    def _group_lists_by_length(self, input_lists: list[list]):
        length_groups = {}
        for lst in input_lists:
            length = len(lst)
            if length not in length_groups:
                length_groups[length] = []
            length_groups[length].append(lst)
        output = [group for group in length_groups.values()]
        return output
