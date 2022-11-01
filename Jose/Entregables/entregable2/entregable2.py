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
        nF, ancho, alt = linea.strip().split()
        lFolletos.append((int(nF), int(ancho), int(alt)))

    return tamPap, lFolletos


# Recibe el tamaño del papel de la imprenta y la lista de folletos
# Devuelve tamaño del papel y lista de folletos
def process(paper_size: int, leaflet_list: list[Leaflet]) -> list[LeafletPos]:
    pages: list[LeafletPos] = []
    free: list[tuple[tuple[int, int], tuple[int, int]]] = []
    indices = sorted(leaflet_list, key=lambda tup: (-tup[2], -tup[1]))

    for obj in indices:
        nF, anc, alt = obj
        nH = None
        for i in range(len(free)):
            lado, arriba = free[i]

            if lado[0] + anc <= paper_size and (alt < arriba[0] != 0 or anc + lado[0] < lado[1] != 0):
                pages.append((nF, (i + 1), lado[0], 0))
                free[i] = ((lado[0] + anc, lado[0]), arriba)
                nH = i
                break

            elif arriba[0] + alt <= paper_size and (anc < lado[0] != 0 or arriba[0] > arriba[1] != 0):
                pages.append((nF, (i + 1), 0, arriba[0]))
                free[i] = (lado, (arriba[0] + alt, arriba[0]))
                nH = i
                break

        if nH is None:
            free.append(((anc, 0), (alt, 0)))
            pages.append((nF, len(free), 0, 0))

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
