from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TextIO, Iterable, Any
from algoritmia.schemes.bt_scheme import *

Value = int
Weight = int
Solution = tuple[Value, Weight, tuple[int, ...]]
Score = Value

def read_data(f: TextIO) -> tuple[Weight, list[Value], list[Weight]]:
    W = int(f.readline())
    v: list[Value] = []
    w: list[Weight] = []

    for line in f.readlines():
        parts = line.strip().split()
        v.append(int(parts[0]))
        w.append(int(parts[1]))

    return W,v,w

def process(W: Weight, v: list[Value], w: list[Weight]) -> Solution:
    @dataclass
    class Extra:
        peso: Weight
        valor: Value

    class KnapsackDS(ScoredDecisionSequence):
        def calculate_opt_bound(self) -> Value:
            libre = W - self.extra.peso
            valor = self.extra.valor

            for i in range(len(self), n):
                if w[i] <= libre:
                    libre -= w[i]
                    valor += v[i]
                else:
                    r = libre / w[i]
                    valor += v[i] * r
                    break

            return valor

        def calculate_pes_bound(self) -> Value:
            libre = W - self.extra.peso
            valor = self.extra.valor

            for i in range(len(self), n):
                if w[i] <= libre:
                    libre -= w[i]
                    valor += v[i]

            return valor

        def is_solution(self) -> bool:
            return len(self) == n

        def solution(self) -> Solution:
            return self.extra.valor, self.extra.peso, self.decisions()

        def successors(self) -> Iterable[KnapsackDS]:
            if not self.is_solution():
                yield self.add_decision(0, self.extra)
                i = len(self)
                peso_nuevo = self.extra.peso + w[i]
                if peso_nuevo <= W:
                    valor_nuevo = self.extra.valor + v[i]
                    nuevo_extra = Extra(peso_nuevo, valor_nuevo)
                    yield self.add_decision(1, nuevo_extra)

        def score(self) -> Score:
            return self.extra.valor

        def state(self) -> Any:
            return len(self), self.extra.peso

    n = len(v)
    return list(bt_max_solve(KnapsackDS(Extra(0,0))))[-1]


def show_results(sol: Solution):
    print(sol[0])
    print(sol[1])
    for d in sol[2]:
        print(d)

if __name__ == "__main__":
    W, v, w = read_data(sys.stdin)
    solution = process(W, v, w)
    show_results(solution)