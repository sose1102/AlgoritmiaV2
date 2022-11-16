import sys
from dataclasses import dataclass
from typing import List, TextIO, Iterable

from algoritmia.schemes.bab_scheme import *

Solution: tuple[int, ...]


def read_data(f: TextIO) -> tuple[int, list[int]]:
    C = int(f.readline())
    w = [int(linea) for linea in f.readlines()]
    return C, w


def process(C: int, w: list[int]) -> Solution:
    @dataclass
    class Extra:
        free: list[int]

    class BinpackingDS(BoundedDecisionSequence):
        def calculate_opt_bound(self) -> int:
            minObj = w[-1]
            libre = sum(f for f in self.extra.free if f >= minObj)
            maxHueco = max(self.extra.free)

            falta = 0
            caben = 0

            for i in range(len((self), n)):
                obj = w[i]
                falta += obj

                if obj <= maxHueco:
                    caben += obj
            metemos = min(libre, caben)

            return len(self.extra.free) + (falta - metemos + C - 1) // C #numero estimado de contenedores

        def calculate_pes_bound(self) -> int:
            pass

        def is_solution(self) -> bool:
            return len(self) == n

        def solution(self) -> Solution:
            return self.decisions()

        def successors(self) -> Iterable["BinpackingDS"]:
            obj = w[len(self)]
            for i in range(len(self.extra.free)):
                if obj <= self.extra.free[i]:
                    copia_free = self.extra.free[:]
                    copia_free[i] -= obj
                    yield self.add_decision(i, Extra(copia_free))
            copia_free = self.extra.free[:]
            copia_free.append(C - obj)
            yield self.add_decision(len(copia_free) - 1, Extra(copia_free))

    n = len(w)
    return bab_min_solve(BinpackingDS())


def show_results(C: list[int]):
    for c in C:
        print(c)


if __name__ == "__main__":
    C, w = read_data(sys.stdin)
    containers = process(C, w)
    show_results(containers)
