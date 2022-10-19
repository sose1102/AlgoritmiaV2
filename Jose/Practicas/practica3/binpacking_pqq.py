import sys
from typing import List, TextIO


def read_data(f: TextIO) -> tuple[int, list[int]]:
    C = int(f.readline())
    w = [int(linea) for linea in f.readlines()]
    return C, w


def process(C: int, w: list[int]) -> list[int]:
    containers: list[int] = []
    free: List[int] = []

    for i in w:
        nc = None
        for j in range(len(free)):
            if i <= free[j]:
                nc = j
                break
        if nc is None:
            free.append(C)
            nc = len(free) - 1
        containers.append(nc)
        free[nc] -= i

    return containers


def show_results(C: list[int]):
    for c in C:
        print(c)


if __name__ == "__main__":
    C, w = read_data(sys.stdin)
    containers = process(C, w)
    show_results(containers)
