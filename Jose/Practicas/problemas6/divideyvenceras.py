import sys
from typing import TextIO

Solution = tuple[int, int, int]


def read_data(f: TextIO) -> list[int]:
    v = []
    for linea in f.readlines():
        v.append(int(linea))
    return v


def process(v: list[int]) -> Solution:
    def sm(i: int, j: int) -> Solution:
        if j - i == 1:
            return v[i], i, j
        c = (i + j) // 2
        solIzq = sm(i, c)
        solDer = sm(c, j)

        sumDer = 0
        sumAcu = 0
        posMaxDer = c + 1

        for k in range(c + 1, j):
            sumAcu += v[k]

            if sumAcu > sumDer:
                sumDer = sumAcu
                posMaxDer = k + 1

        sumIzq = 0
        sumAcu = 0
        posMaxIzq = c

        for k in range(c, i - 1, -1):
            sumAcu += v[k]

            if sumAcu > sumIzq:
                sumIzq = sumAcu
                posMaxIzq = k
        solCen = (sumIzq + sumDer, posMaxIzq, posMaxDer)

        return max(solIzq, solCen, solDer)

    return sm(0, len(v))


def show_results(s: Solution):
    print(s[0])
    print(s[1])
    print(s[2])


if __name__ == "__main__":
    v = read_data(sys.stdin)
    sol = process(v)
    show_results(sol)
