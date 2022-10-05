import sys

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.queues import *
#import Jose.Practicas.Practica2.labyrinth
import labyrinth

Vertex = tuple[int,int]
Edge = tuple[Vertex, Vertex]

def bf_search(g: UndirectedGraph[Vertex], source: Vertex, target: Vertex)  -> list[Edge]:
    q = Fifo()
    seen = set()
    act = source
    res = [(source, source)]

    q.push(source)
    seen.add(source)

    while len(q) > 0:
        v = q.pop()

        for suc in g.succs(v):
            if suc not in seen:
                q.push(suc)
                seen.add(suc)
                res.append((v, suc))

                if suc == target:
                    return res

    raise Exception("Target no encontrado")

def path_recover(edges: list[Edge], target: Vertex) -> List[Vertex]:
    bp = {}

    for o, d in edges: #Coger unicamente los vertices de "Llegada"
        bp[d] = o

    v = target
    path = [v]

    while bp[v] != v:
        v = bp[v]
        path.append(v)

    path.reverse()

    return path

def read_data(f: TextIO) -> tuple[int, int]:
    rows = int(f.readline())
    cols = int(f.readline())
    return rows,cols

def process(rows: int, cols:int) -> tuple[UndirectedGraph[Vertex], list[Vertex]]:
    #g = Jose.Practicas.Practica2.labyrinth.process(rows, cols)
    g = labyrinth.create_labyrinth(rows, cols)
    target = (rows - 1, cols - 1)
    edges = bf_search(g, (0, 0), target)
    path = path_recover(edges, target)
    return g, path

def show_results(path: list[Vertex]):
    print(path)

if __name__ == "__main__":
    rows, cols = read_data(sys.stdin)
    _, path = process(rows, cols)
    show_results(path)