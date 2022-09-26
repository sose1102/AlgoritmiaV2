from algoritmia.datastructures.graphs import Digraph

g = Digraph(E=[(0, 1), (0, 2), (1, 2)])
print(g.V)
print(g.succs(0))
