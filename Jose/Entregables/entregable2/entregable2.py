#!/usr/bin/env python3
import sys
from typing import TextIO

# Folleto en inglés es Leaflet
Leaflet = tuple[int, int, int]          # (num_folleto, anchura, altura)
LeafletPos = tuple[int, int, int, int]  # (num_folleto, num_hoja_de_imprenta, pos_x ,pos_y)


# Lee la instancia por la entrada estándar (ver apartado 1.1)
# Devuelve el tamaño del papel de la imprenta y la lista de folletos
def read_data(f: TextIO) -> tuple[int, list[Leaflet]]:
    paper_size : int = int(f.readline())
    leaflet_list : list[Leaflet] = []
    for folleto in f.readlines():
        num_folleto, anchura, altura = folleto.rstrip().split()
        leaflet_list.append((int(num_folleto), int(anchura), int(altura)))
    return paper_size, leaflet_list


# Recibe el tamaño del papel de la imprenta y la lista de folletos
# Devuelve tamaño del papel y lista de folletos
def process(paper_size: int, leaflet_list: list[Leaflet]) -> list[LeafletPos]:
    leafletpos_list: list[LeafletPos] = []
    hojas: list[tuple[int,int]] = []
    indices = range(len(leaflet_list))
    sorted_indices = sorted(leaflet_list, key=lambda i: (-i[2], -i[1]))

    for i in sorted_indices:
        num, anch, alt = sorted_indices[i]
        metido = False
        for nc in range(len(hojas)):
            posh = hojas[nc][0]
            posv=hojas[nc][1]
            if posh + anch <= paper_size and alt<=paper_size:
                #si cabe en una posicion
                leafletpos_list.append((i+1,nc+1,posh,0))
                hojas[nc] = (posh+anch,max(alt,posv))
                #hojas[nc][0]+=anch
                #hojas[nc][1]+=alt
                metido =True
                break;
            elif posv + alt <= paper_size and anch <=paper_size:
                leafletpos_list.append((i + 1, nc + 1, 0, posv))
                hojas[nc] = (max(posh,anch), posv + alt)
                # hojas[nc][0] += alt
                # hojas[nc][1] += anch
                metido = True
                break;
        if metido is False:
            if anch <= paper_size and alt <= paper_size:
                # si cabe en una posicion
                hojas.append((anch,alt))
                leafletpos_list.append((i+1, len(hojas), 0, 0))
                #hojas[nc][0] += anch
                #hojas[nc][1] += alt
    return leafletpos_list


# Muestra por la salida estandar las posiciones de los folletos (ver apartado 1.2)
def show_results(leafletpos_list: list[LeafletPos]):
    for leafletpos in leafletpos_list:
        folleto, hoja, h, v = leafletpos
        print(folleto, hoja, h, v)

if __name__ == '__main__':
    paper_size0, leaflet_list0 = read_data(sys.stdin)
    leafletpos_list0 = process(paper_size0, leaflet_list0)
    show_results(leafletpos_list0)




#si lo que mide en horizontal y en vertica cabe partiendo del punto de la hoja x
#si lo que mide el folleto cabe partiendo del punto de la hija y
#lo mismo en vertical

#si no existe la hoja
#directamente desde el 0,0.
