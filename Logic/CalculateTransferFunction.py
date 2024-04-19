from Logic.GraphTraversal import *
from Logic.TransferFunction import *


def subtract_one_recursive(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.append(subtract_one_recursive(item))
        elif isinstance(item, int):
            result.append(item - 1)
        else:
            result.append(item)
    return result


def calculateTransferFunction(Vertices):

    vert = []
    Edges = []
    graph = []
    
    for ver in Vertices:
        vert.append(ver.id)
        for v in ver.edges:
            Edges.append([ver.id, v[0].id, v[1]])

    graph.append(vert)
    graph.append(Edges)

    for x in graph[1]:
        x[2] = str(x[2])

    graph = subtract_one_recursive(graph)    

    gt = GraphTraversal(graph)
    
    tf = TransferFunction(gt.get_forward_paths(), gt.get_loops(), gt.get_non_touching_loops(), gt.get_loops_not_touching_forward_paths())

    result1 = [gt.get_forward_paths(), gt.get_loops()]
    result2 = [tf.get_delta(), tf.get_forward_paths_delta()]
    result3 = tf.get_transfer_function()

    return result1, result2, result3