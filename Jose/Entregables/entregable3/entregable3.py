from __future__ import annotations

import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional, TextIO, Iterable

from algoritmia.schemes.bt_scheme import bt_min_solve, ScoredDecisionSequence, State

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

    class BoardDS(ScoredDecisionSequence):
        def is_solution(self) -> bool:
            return self.extra.brick.b1 == self.extra.brick.b2 == board.target_pos()  # Cuando se alcance la posición T y los bloques esten en la misma posición

        def solution(self) -> Solution:
            return self.decisions()

        def successors(self) -> Iterable["ScoredDecisionSequence"]:
            if not self.is_solution():
                posiblesMovimientos = [Direction.Down, Direction.Up, Direction.Right, Direction.Left]

                for pM in posiblesMovimientos:
                    copia = self.extra.brick.move(pM)

                    if board.has_tile(copia.b1) and board.has_tile(copia.b2):  # En caso de que la copia salga del tablero no la coge
                        yield self.add_decision(pM,Extra(copia))  # Añadir las decisiones que se puedan tomar en cada caso

        def state(self) -> State:  # Poda
            return self.extra.brick

        def score(self) -> int:
            return len(self)

    brik = Brick(board.start_pos(), board.start_pos())
    initial_ds = BoardDS(Extra(brik))
    moves = tuple(bt_min_solve(initial_ds))  # Soluciones ordenadas de mayor a menor

    try:
        return moves[-1]
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
