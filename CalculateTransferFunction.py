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

    print(graph)

    
    # Fill me in

    print("this is the transfer function")
    pass