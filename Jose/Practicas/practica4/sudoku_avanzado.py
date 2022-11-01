import sys
from dataclasses import dataclass
from typing import TextIO, Iterable

from algoritmia.schemes.bt_scheme import bt_solve, DecisionSequence

from sudoku_lib import *

Solution = Sudoku


def read_data(f: TextIO) -> Sudoku:
    return desde_cadenas(f.readlines())


def process(sudoku: Sudoku) -> Iterator[Sudoku]:
    @dataclass
    class Extra:
        sudoku: Sudoku
        vacias: set[Position]

    class SudokuDS(DecisionSequence):
        def is_solution(self) -> bool:
            return len(self.extra.vacias) == 0

        def solution(self) -> Solution:
           return self.extra.sudoku

        def successors(self) -> Iterator["DecisionSequence"]:
            mejor = 10
            pos = None

            for v in self.extra.vacias:
                l = len(posibles_en(self.extra.sudoku, v))
                if l < mejor:
                    mejor = l
                    pos = v

            if pos is not None:                                                        #Si la posición no es None
                self.extra.vacias.remove(pos)                                          #Hacemos una copia del vacias actual
                row, col = pos
                for num in posibles_en(self.extra.sudoku, pos):                        #Recorremos todas las posibles opciones para esa posición
                    self.extra.sudoku[row][col] = num                                  #Ponemos en la posición de la copia del sudoku el primer valor posible
                    yield self.add_decision(num, self.extra)                           #Hacemos la recursividad con esa posición igual al posible en el que estemos
                self.extra.sudoku[row][col] = 0
                self.extra.vacias.add(pos)

    v = set(vacias(sudoku))
    yield from bt_solve(SudokuDS(Extra(sudoku, v)))


def show_results(solutions: Iterator[Sudoku]):
    for line in solutions:
        pretty_print(line)


if __name__ == "__main__":
    sudoku = read_data(sys.stdin)
    solutions = process(sudoku)
    show_results(solutions)