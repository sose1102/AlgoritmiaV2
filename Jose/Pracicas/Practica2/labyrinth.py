import sys
from random import shuffle
from typing import TextIO

from algoritmia.datastructures.graphs import *
from algoritmia.datastructures.mergefindsets import *


def read_data(f: TextIO) -> tuple[int, int]:
    rows = int(f.readline())
    cols = int(f.readline())
    return rows, cols

def process(rows: int, cols: int) -> UndirectedGraph:
    vertex = []

    for r in range(rows - 1):
        for c in range(cols - 1):
            vertex.append((r, c))

    mfs = MergeFindSet()

    for v in vertex:
        mfs.add(v)

    edges = []


    for r, c in vertex:
        if r != 0:
            edges.append(((r - 1, c), (r, c)))
        if c != 0:
            edges.append(((r, c - 1), (r, c)))

    shuffle(edges)

    corridors = []

    for v1, v2 in edges:
        sv1 = mfs.find(v1)
        sv2 = mfs.find(v2)

        if sv1 != sv2:
            mfs.merge(v1, v2)
            corridors.append((v1, v2))

    return UndirectedGraph(E = corridors)

def show_results(labyrinth: UndirectedGraph):
    print(labyrinth)

if __name__ == "__main__":
    rows, cols = read_data(sys.stdin)
    labyrinth = process(rows, cols)
    show_results(labyrinth)