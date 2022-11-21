from __future__ import annotations

from dataclasses import dataclass

from board import *
from direction import Direction


# dataclass: Brick
# Esta dataclass se encarga de gestionar los movimientos del bloque (prisma rectangular, ladrillo o brick)
#
# - Contine dos atributos del tipo RowCol, b1 y b2, con las posiciones de los dos cubos que forman
#   el bloque.
# - Para simplificar la implementación añadimos dos restriciones obligatorias:
#     - Cuando el bloque esté tumbado sobre una fila, b1 deberá ser el bloque de menor columna.
#     - Cuando el bloque esté tumbado sobre una columna, b1 deberá ser el bloque de menor fila.
# - Con estas dos restricciones un bloque debe cumplir una de estas tres condiciones:
#     b1.row == b2.row and b1.col == b2.col       # El boque está de pie
#     b1.row == b2.row and b1.col == b2.col - 1   # El boque está tumbado en una fila
#     b1.row == b2.row - 1 and b1.col == b2.col   # El boque está tumbado en una columna
# - Los objetos de esta clase son inmutables, por lo tanto, el método move() devuelve un nuevo bloque.
#
@dataclass(frozen=True)
class Brick:
    b1: RowCol
    b2: RowCol

    # El método __post_init__() es una ayuda para detectar bugs, se llama automáticamnte despues del constructor.
    # Comprueba que cada bloque que se construya cumpla una de las tres condiciones válidas
    def __post_init__(self):
        is_valid = self.b1.row == self.b2.row and self.b1.col == self.b2.col or \
                   self.b1.row == self.b2.row and self.b1.col == self.b2.col - 1 or \
                   self.b1.row == self.b2.row - 1 and self.b1.col == self.b2.col
        if not is_valid:
            raise RuntimeError(f"Built an invalid Brick (see restrictions): {self}")

    # Funcion para mover el bloque, como el bloque es inmutable el 'move' devuelve otro bloque
    def move(self, d: Direction) -> Brick:
        # TODO: IMPLEMENTAR
        b1 = self.b1
        b2 = self.b2
        if b1 == b2: #Si esta de pie
            row = b1.row
            col = b1.col
            if d.value == "L":
                nB1 = RowCol(row, col - 2)
                nB2 = RowCol(row, col - 1)
            elif d.value == "R":
                nB1 = RowCol(row, col + 1)
                nB2 = RowCol(row, col + 2)
            elif d.value == "U":
                nB1 = RowCol(row - 2, col)
                nB2 = RowCol(row - 1, col)
            else:
                nB1 = RowCol(row + 1, col)
                nB2 = RowCol(row + 2, col)
        else: #Si esta acostado
            col1 = b1.col
            row1 = b1.row
            col2 = b2.col
            row2 = b2.row
            if col1 == col2: #Si esta acostado sobre el eje y
                if d.value == "L":
                    nB1 = RowCol(row1, col1-1)
                    nB2 = RowCol(row2, col2-1)
                elif d.value == "R":
                    nB1 = RowCol(row1, col1+1)
                    nB2 = RowCol(row2, col2+1)
                elif d.value == "U":
                    nB1 = nB2 = RowCol(row1 - 1, col1)
                else:
                    nB1 = nB2 = RowCol(row2 + 1, col2)
            else: #Si esta acostado sobre el eje x
                if d.value == "L":
                    nB1 = nB2 = RowCol(row1, col1 - 1)
                elif d.value == "R":
                    nB1 = nB2 = RowCol(row2, col2 + 1)
                elif d.value == "U":
                    nB1 = RowCol(row1 - 1, col1)
                    nB2 = RowCol(row2 - 1, col2)
                else:
                    nB1 = RowCol(row1 + 1, col1)
                    nB2 = RowCol(row2 + 1, col2)

        return Brick(nB1, nB2)

    # IMPORTANTE: Puedes añadir métodos adicionales a la clase Brick
    def posibles_move(self, board: Board):
        posibles = []
        b1 = self.b1
        b2 = self.b2
        if b1 == b2:  # Si esta de pie
            if board.has_tile(RowCol(b1.row, b1.col - 2)): #Es posible el movimiento a la Izquierda
                posibles.append('L')
            if board.has_tile(RowCol(b2.row, b2.col + 2)): #Es posible el movimiento a la Derecha
                posibles.append('R')
            if board.has_tile(RowCol(b2.row - 1, b2.col)):  # Es posible el movimiento a la Arriba
                posibles.append('U')
            if board.has_tile(RowCol(b2.row + 2, b2.col)):  # Es posible el movimiento a la Abajo
                posibles.append('D')
        else:  # Si esta acostado
            col1 = b1.col
            row1 = b1.row
            col2 = b2.col
            row2 = b2.row
            if col1 == col2:  # Si esta acostado sobre el eje y
                if board.has_tile(RowCol(row1, col1 - 1)) and board.has_tile(RowCol(row2, col2 - 1)):  # Es posible el movimiento a la Izquierda
                    posibles.append('L')
                if board.has_tile(RowCol(row1, col1 + 1)) and board.has_tile(RowCol(row2, col2 + 1)):  # Es posible el movimiento a la Derecha
                    posibles.append('R')
                if board.has_tile(RowCol(row1 - 1, col1)):  # Es posible el movimiento a la Arriba
                    posibles.append('U')
                if board.has_tile(RowCol(row2 + 1, col2)):  # Es posible el movimiento a la Abajo
                    posibles.append('D')
            else:  # Si esta acostado sobre el eje x
                if board.has_tile(RowCol(row1, col1 - 1)):  # Es posible el movimiento a la Izquierda
                    posibles.append('L')
                if board.has_tile(RowCol(row2, col2 + 1)):  # Es posible el movimiento a la Derecha
                    posibles.append('R')
                if board.has_tile(RowCol(row1 - 1, col1)) and board.has_tile(RowCol(row2 - 1, col2)):  # Es posible el movimiento a la Arriba
                    posibles.append('U')
                if board.has_tile(RowCol(row1 + 1, col1)) and board.has_tile(RowCol(row2 + 1, col2)):  # Es posible el movimiento a la Abajo
                    posibles.append('D')

        return posibles
