#!/usr/bin/env python3
import sys
from typing import TextIO

# Folleto en inglés es Leaflet
Leaflet = tuple[int, int, int]          # (num_folleto, anchura, altura)
LeafletPos = tuple[int, int, int, int]  # (num_folleto, num_hoja_de_imprenta, pos_x ,pos_y)


# Lee la instancia por la entrada estándar (ver apartado 1.1)
# Devuelve el tamaño del papel de la imprenta y la lista de folletos
def read_data(f: TextIO) -> tuple[int, list[Leaflet]]:
    tamPap = int(f.readline())
    lFolletos: list[Leaflet] = []

    for linea in f.readlines():
        nF, ancho, alt = linea
        lFolletos.append((int(nF), int(ancho), int(alt)))

    return tamPap, lFolletos


# Recibe el tamaño del papel de la imprenta y la lista de folletos
# Devuelve tamaño del papel y lista de folletos
def process(paper_size: int, leaflet_list: list[Leaflet]) -> list[LeafletPos]:
    pages: list[LeafletPos] = [(-1, -1, -1, -1)] * len(leaflet_list) #Resultado con tuplas tamaño folleto, numero pagina, posición horizontal, posición vertical
    free: list[(int, int)] = [] #Las paginas son cuadradas con lados de tamaño paper_size
    indices = sorted(range(len(leaflet_list)), key=lambda i: -(leaflet_list[i][1] + leaflet_list[i][2])) #Ordenar la lista según la suma de los lados de los folletos
    ph = 0
    pv = 0

    for i in indices:
        obj = leaflet_list[i]
        np = None
        for j in range(len(free)):
            if (obj[1] + obj[2]) <= free[j]:
                np =
                break

        if np is None:
            free.append(paper_size)
            np = len(free) - 1

        pages[i] = obj[i][0], np, ph, pv
        free[np][] -= obj[1]

    return pages


# Muestra por la salida estandar las posiciones de los folletos (ver apartado 1.2)
def show_results(leafletpos_list: list[LeafletPos]):
    for elem in leafletpos_list:
        nF, nH, pH, pV = elem
        print("{0} {1} {2} {3}".format(nF, nH, pH, pV))


if __name__ == '__main__':
    paper_size0, leaflet_list0 = read_data(sys.stdin)
    leafletpos_list0 = process(paper_size0, leaflet_list0)
    show_results(leafletpos_list0)
