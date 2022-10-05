from algoritmia.datastructures.graphs import UndirectedGraph

Vertex = tuple[int, int]
Edges = tuple[Vertex, Vertex]

def knigth_graph(orws: int, cols: int) -> UndirectedGraph[Vertex]