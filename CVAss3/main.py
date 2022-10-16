import cv2
import numpy as np


def A3(x, y):
    # 1,4
    c1 = 0
    # print(len(x) - (len(y) // 2) + 1)
    # print(len(y) // 2)

    # '''
    # for i in range(len(y) // 2, len(x) - len(y) // 2 ): #rows
    rows = len(x)
    columns = len(x[0])
    z = np.array(np.array(x))
    for i in range(1, rows - 1):  # rows
        for j in range(1, columns - 1):  # cols
            # need to change x.length to x.size[0]
            # c1 += 1

            list1 = []
            for k in range(i - 1, i + 2):
                for l in range(j - 1, j + 2):
                    num = x[k][l]
                    list1.append(num)
            result = Medianize(list1, y)
            z[i][j] = result

    # print(x)
    # print("c1")
    # print(c1)
    return z
    # '''


def Medianize(x, y):
    list2 = []
    for i in range(3):
        for j in range(3):
            list2.append(y[i][j])

    list = []
    # print("41")
    # print(x)
    for i in range(9):
        num = int(x[i])
        num2 = int(list2[i])

        for j in range(0, num2):
            list.append(int(num))
    list.sort()
    result = list[len(list) // 2]
    return result


input = cv2.imread("BarCode2.jpg", 0)
x = [[4, 0, 3, 2, 1], [0, 1, 3, 2, 3], [2, 1, 4, 5, 4], [3, 3, 7, 8, 9]]

w = [[1, 3, 1], [3, 5, 3], [1, 3, 1]]
u = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

weightedMedian = A3(input, w)
median = A3(input, u)

cv2.imwrite("BarCodeWeightedMedian.jpg", weightedMedian)
cv2.imwrite("BarCodeMedian.jpg", median)