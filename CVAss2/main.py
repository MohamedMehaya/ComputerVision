import math
from math import floor
import cv2
import numpy as np
import time


def CalculateIntegral(x):
    rows = len(x)
    columns = len(x[0])
    ii = np.array(np.array(x, dtype='object'), dtype='object')
    for i in range(0, rows):
        for j in range(1, columns):
            ii[i][j] += ii[i][j - 1]
            ii[i][j] = round(ii[i][j], 2)

    # print(ii)

    for i in range(1, rows):
        for j in range(0, columns):
            ii[i][j] += ii[i - 1][j]
            ii[i][j] = round(ii[i][j], 2)
    return ii


def CalculateLocalSum(ii, p0, p1):
    x0 = p0[0] - 1
    y0 = p0[1] - 1

    x1 = p1[0]
    y1 = p1[1]
    a = 0
    b = 0
    c = 0
    if not (y0 == -1 or x0 == -1):
        a = ii[y0][x0]
    if not (x0 == -1):
        b = ii[y1][x0]
    if not (y0 == -1):
        c = ii[y0][x1]
    d = ii[y1][x1]

    result = d + a - b - c
    return result


def EdgeDetect(x, n):
    hf = floor(n / 2)

    rows = len(x)
    columns = len(x[0])
    sdd = np.zeros((rows, columns))
    prewitt = np.zeros((rows, columns))
    for i in range(hf, rows - hf):
        for j in range(hf, columns - hf):
            ch1 = CalculateLocalSum(x, (j - hf, i - hf), (j + hf, i - 1))
            ch1 -= CalculateLocalSum(x, (j - hf, i + 1), (j + hf, i + hf))

            ch2 = (-1) * CalculateLocalSum(x, (j - hf, i - hf), (j - 1, i + hf))
            ch2 += CalculateLocalSum(x, (j + 1, i - hf), (j + hf, i + hf))

            # print (ch1 ** 2 , ch2 ** 2)
            prewitt[i][j] = math.sqrt(ch1 ** 2 + ch2 ** 2)

            sd = (-1) * CalculateLocalSum(x, (j - hf, i - hf), (j + hf, i + hf))
            sd += CalculateLocalSum(x, (j, i), (j, i))
            # sd -= CalculateLocalSum(x, (j - hf, i), (j - 1, i))
            # sd -= CalculateLocalSum(x, (j + 1, i), (j + hf, i))

            sd += (n ** 2 - 1) * CalculateLocalSum(x, (j, i), (j, i))

            sdd[i][j] = abs(sd)

    return prewitt, sdd  # , prewitt


def refineEdge(ii, n, r):
    hf = floor(n / 2)

    rows = len(ii)
    columns = len(ii[0])
    res = np.zeros((rows, columns))
    for i in range(hf, rows - hf):  # Looping over Rows
        for j in range(hf, columns - hf):  # Looping over Columns
            c = 0
            if CalculateLocalSum(ii, (j, i), (j, i)) > MeanAverage(ii, n, (j, i)) * r:
                c = ii[i][j]
            res[i][j] = c
    return res


def MeanAverage(ii, n, center):
    hf = floor(n / 2)
    x = center[0]
    y = center[1]

    sum = CalculateLocalSum(ii, (x - hf, y - hf), (x + hf, y + hf))
    return sum / (n ** 2)


def toImg(q):
    rows = len(q)
    columns = len(q[0])
    img = np.zeros((rows, columns, 3))
    for i in range(rows):  # Looping over Rows
        for j in range(columns):  # Looping over Columns
            img[i][j] = [q[i][j], q[i][j], q[i][j]]
    return img


one = time.time()
input = cv2.imread("L4.jpg", 0)
# testInput = [[0, 0, 0, 1], [0, 1, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 0]]
y = CalculateIntegral(input)
# print(y)
# print(CalculateLocalSum(y, (0, 0), (2, 3)))
p, s = EdgeDetect(y, 51)

PrewittEdgeDetect = toImg(p)
SDEdgeDetect = toImg(s)
two = time.time()
print("Edge Detect Execution Time (sec):",two - one)
cv2.imwrite("PrewittEdgeDetect.png", PrewittEdgeDetect)
cv2.imwrite("SDEdgeDetect.png", SDEdgeDetect)
three = time.time()
refinedPrewitt = refineEdge(p, 51, 1.25)
refinedSD = refineEdge(s, 51, 1.25)

Prewitt = toImg(refinedPrewitt)
SD = toImg(refinedSD)
four = time.time()
print("Refine Edge Execution Time (sec):",four - three)
cv2.imwrite("refinedPrewitt.png", Prewitt)
cv2.imwrite("refinedSD.png", SD)



