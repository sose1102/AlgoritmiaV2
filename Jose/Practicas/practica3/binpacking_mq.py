import sys
from typing import List, TextIO


def read_data(f: TextIO) -> tuple[int, list[int]]:
    C = int(f.readline())
    w = [int(linea) for linea in f.readlines()]
    return C, w


def process(C: int, w: list[int]) -> list[int]:
    containers: list[int] = []
    free = C
    nC = 0

    for i in w:
        if i > free:
            nC += 1
            free = C
        containers.append(nC)
        free -= i
    return containers


def show_results(C: list[int]):
    for c in C:
        print(c)


if __name__ == "__main__":
    C, w = read_data(sys.stdin)
    containers = process(C, w)
    show_results(containers)
