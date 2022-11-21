from __future__ import annotations

import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional, TextIO, Iterable, Tuple

from algoritmia.schemes.bt_scheme import *

from board import Board, RowCol
from brick import Brick
from direction import Direction, directions2string

# Variable global con la salida de show_results() si no hay solución
INSTANCE_WITHOUT_SOLUTION = "INSTANCE WITHOUT SOLUTION"

# Tipos que utilizarás en el process() al aplicar el esquema de backtracking
Decision = Direction  # Cuatro valores posibles: Directions.Right, Direction.Left, Direction.Up, Direction.Down
Solution = tuple[Decision, ...]  # Utilizad la función auxiliar 'directions2string' de direction.py para convertir


# una solución en una cadena del tipo 'RRUUULLDR...'


# ---------------------------------------------------------------------------------------------------------------------

def read_data(f: TextIO) -> Board:
    lines = [f for f in f.readlines()]
    return Board(lines)


def process(board: Board) -> Optional[Solution]:
    @dataclass
    class Extra:
        brick: Brick
        # control de visitados

    class BoardDS(DecisionSequence):
        def is_solution(self) -> bool:
            return len(
                self.extra.posicion) == 'T'  # Cuando se alcance la posición T y los bloques esten en la misma posición

        def successors(self) -> Iterable["DecisionSequence"]:
            # Para todas las posiciones posibles hacer el movimiento para cada una de ellas

            yield  # Añadir las decisiones que se puedan tomar en cada caso

            # Volver el tablero a la posición anterior

        def state(self) -> State:  # Poda
            return self.extra.piezas

    brik = Brick(board.start_pos(), board.start_pos())
    initial_ds = BoardDS(Extra(brik))
    try:
        return next(bt_vc_solve(initial_ds))
    except:
        return None


def show_results(solution: Optional[Solution]):
    if solution is None:
        print("INSTANCE WITHOUT SOLUTION")
    else:
        print(directions2string(solution))


# Programa principal --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    board0 = read_data(sys.stdin)
    solution0 = process(board0)
    show_results(solution0)
