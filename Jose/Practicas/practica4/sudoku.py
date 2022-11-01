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
        sudoku : Sudoku

    class SudokuDS(DecisionSequence):
        def is_solution(self) -> bool:
            return primera_vacia(self.extra.sudoku) is None

        def solution(self) -> Solution:
           return self.extra.sudoku

        def successors(self) -> Iterator["DecisionSequence"]:
            pos = primera_vacia(self.extra.sudoku)                       #Obtenemos la primera posición vacía
            if pos is not None:                                          #Si la posición no es None
                copia: Sudoku = [fila[:] for fila in self.extra.sudoku]  #Hacemos una copia del sudoku actual
                for num in posibles_en(copia, pos):                      #Recorremos todas las posibles opciones para esa posición
                    row, col = pos
                    copia[row][col] = num                                #Ponemos en la posición de la copia del sudoku el primer valor posible
                    yield self.add_decision(num, Extra(copia))           #Hacemos la recursividad con esa posición igual al posible en el que estemos

    yield from bt_solve(SudokuDS(Extra(sudoku)))


def show_results(solutions: Iterator[Sudoku]):
    for line in solutions:
        pretty_print(line)


if __name__ == "__main__":
    sudoku = read_data(sys.stdin)
    solutions = process(sudoku)
    show_results(solutions)