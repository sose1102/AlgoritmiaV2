#!/usr/bin/env python3
import sys
from random import shuffle, seed
from typing import TextIO, Optional, List

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.queues import Fifo
from pandocfilters import Math

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]

NO_VALID_WALL = 'NO VALID WALL'

# Función ya implementada
# Esta función utiliza un MFSet para crear un laberinto, pero le añade n aristas
# adicionales que provocan que el laberinto tenga ciclos.
def create_labyrinth(rows: int, cols: int, n: int, s: int) -> UndirectedGraph[Vertex]:
    vertices: list[Vertex] = [(r, c) for r in range(rows) for c in range(cols)]
    mfs: MergeFindSet[Vertex] = MergeFindSet((v,) for v in vertices)
    edges: list[Edge] = [((r, c), (r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    edges.extend([((r, c), (r, c + 1)) for r in range(rows) for c in range(cols - 1)])
    seed(s)
    shuffle(edges)
    corridors: list[Edge] = []
    for (u, v) in edges:
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u, v)
            corridors.append((u, v))
        elif n > 0:
            n -= 1
            corridors.append((u, v))
    return UndirectedGraph(E=corridors)

'''
    def crearmatriz(filas:int,cols:int):
    m = []
    for i in range(filas):
        m.append([])
        for j in range(cols):
            m[i].append(-1)
    return m
'''
def bf_search(g: UndirectedGraph[Vertex], source: Vertex) -> List[Edge]:
    edges = []
    q = Fifo()
    seen = set()

    q.push((source, source))
    seen.add(source)

    while len(q) > 0:
        ori, des = q.pop()
        edges.append((ori, des))

        for suc in g.succs(des):
            if suc not in seen:
                seen.add(suc)
                q.push((des, suc))
    return edges


def backpointers(edges: List[Edge]):
    bp = {}
    indexPath = 0
    for orig, dest in edges:
        if orig != dest:
            indexPath = bp[orig][1] + 1
        bp[dest] = (orig, indexPath)
    return bp


def read_data(f: TextIO) -> tuple[UndirectedGraph[Vertex], int, int]:
    rows = int(f.readline())
    cols = int(f.readline())
    arisAd = int(f.readline())
    gener = int(f.readline())
    g = create_labyrinth(rows, cols, arisAd, gener)
    return g, rows, cols


def process(lab: UndirectedGraph[Vertex], rows: int, cols: int) -> tuple[Optional[Edge], int, int]:
    source = (0, 0)
    target = ((rows - 1), (cols - 1))

    wall = None

    start = backpointers(bf_search(lab, source))
    end = backpointers(bf_search(lab, target))

    norm = start[(rows - 1, cols - 1)][1]
    short = norm

    for r in range(rows - 1):
        for c in range(cols - 1):

            jStart = start[(r, c)][1]
            jEnd = end[(r, c + 1)][1]

            if (jStart + jEnd + 1) < short:
                short = jStart + jEnd + 1
                wall = ((r, c), (r, c + 1))

            jEnd = end[(r + 1, c)][1]

            if (jStart + jEnd + 1) < short:
                short = jStart + jEnd + 1
                wall = ((r, c), (r + 1, c))

    return wall, norm, short


def show_results(edge_to_add: Optional[Edge], length_before: int, length_after: int):
    if edge_to_add is None:
        print(NO_VALID_WALL)
    else:
        e1, e2 = edge_to_add
        r1, c1 = e1
        r2, c2 = e2
        print("{0} {1} {2} {3}".format(r1, c1, r2, c2))
    print(length_before)
    print(length_after)


if __name__ == '__main__':
    graph0, rows0, cols0 = read_data(sys.stdin)
    edge_to_add0, length_before0, length_after0 = process(graph0, rows0, cols0)
    show_results(edge_to_add0, length_before0, length_after0)
