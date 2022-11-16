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
    dondeMirar = 0

    for obj in indices:
        numFolleto, ancho, alto = obj
        nH = None
        for i in range(dondeMirar, len(free)):
            añadirLado, añadirArriba = free[i]

            if añadirLado[0] + ancho <= paper_size and (alto < añadirArriba[0] != 0 or ancho + añadirLado[0] < añadirLado[1] != 0):
                pages.append((numFolleto, (i + 1), añadirLado[0], 0))
                free[i] = ((añadirLado[0] + ancho, añadirLado[0]), añadirArriba)
                nH = i
                #if (añadirLado[0] * añadirArriba[1]) / (paper_size * paper_size) > 0.7:
                #    dondeMirar = i
                break

            elif añadirArriba[0] + alto <= paper_size and (ancho < añadirLado[0] != 0 or añadirArriba[0] > añadirArriba[1] != 0):
                pages.append((numFolleto, (i + 1), 0, añadirArriba[0]))
                free[i] = (añadirLado, (añadirArriba[0] + alto, añadirArriba[0]))
                nH = i
                #if (añadirLado[0] * añadirArriba[1]) / (paper_size * paper_size) > 0.7:
                #    dondeMirar = i
                break

        if nH is None:
            free.append(((ancho, 0), (alto, 0)))
            pages.append((numFolleto, len(free), 0, 0))

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