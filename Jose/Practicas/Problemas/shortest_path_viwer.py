from algoritmia.viewers.labyrinth_viewer import LabyrinthViewer
from shortest_path import process
if __name__ == "__main__":
    rows = int(input("Filas: "))
    cols = int(input("Columnas: "))
    labyrinth, path = process(rows, cols)
    lv = LabyrinthViewer(labyrinth, canvas_width=10 * cols, canvas_height=10 * rows)
    lv.add_path(path)
    lv.run()