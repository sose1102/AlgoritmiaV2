import sys
from typing import List, TextIO


def read_data(f: TextIO) -> tuple[int, list[int]]:
    C = int(f.readline())
    w = [int(linea) for linea in f.readlines()]
    return C, w


def process(C: int, w: list[int]) -> list[int]:
    containers: list[int] = [-1] * len(w) #Crear una lista de tamaño len(w) con todos los campos a -1
    free: List[int] = []
    indices = sorted(range(len(w)), key=lambda i: -w[i]) #Ordenar de mayor a menor guardando los indices

    for i in indices:
        obj = w[i]
        nc = None #Numero de contenedor
        for j in range(len(free)): #Recorre la lista de libres
            if obj <= free[j]: #Si el objeto cabe lo inserta
                nc = j
                break

        if nc is None: #Si no se inserta el dato y se acaban los contenedores
            free.append(C) #Se añade otro contenedor
            nc = len(free) - 1

        containers[i] = nc #Se indica la posición del elemento
        free[nc] -= obj #Se le resta a la capacidad del contenedor el tamaño del objeto

    return containers


def show_results(C: list[int]):
    for c in C:
        print(c)


if __name__ == "__main__":
    C, w = read_data(sys.stdin)
    containers = process(C, w)
    show_results(containers)
