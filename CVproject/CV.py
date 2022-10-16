import cv2
import numpy as np


def imOpen(name):
    img = cv2.imread(name)
    q = np.zeros((img.shape[0], img.shape[1]))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            q[i][j] = (int(img[i][j][0])+int(img[i][j][1])+int(img[i][j][2]))//3
    return q


# print(trial)
def toFile(name, run):
    f = open(name + ".txt", "w+")
    f.write(run)


def toStrV(img):
    trial = ""
    trial += "V " + str(img.shape[1]) + " " + str(img.shape[0]) + "\n"
    for j in range(img.shape[1]):  # traverses through height of the image
        last = ''
        for i in range(img.shape[0]):  # traverses through width of the image
            if last != str(img[i][j]):
                if i == 1:
                    last = str(img[i][j])
                    trial += str(img[i][j]) + " "
                    trial += str(i - 1) + " "

                elif i >= 1:
                    last = str(img[i][j])
                    trial += str(i - 1) + " "
                    trial += str(img[i][j]) + " "
                    trial += str(i) + " "

        trial += str(img.shape[0] - 1)
        if not (j == img.shape[1] - 1):
            trial += "\n"
    # print(trial)
    return trial


def toStrH(img):
    trial = ""
    trial += "H " + str(img.shape[1]) + " " + str(img.shape[0]) + "\n"
    for i in range(img.shape[0]):  # traverses through height of the image
        last = ''
        for j in range(img.shape[1]):  # traverses through width of the image
            if last != str(img[i][j]):
                if j == 1:
                    last = str(img[i][j])
                    trial += str(img[i][j]) + " "
                    trial += str(j - 1) + " "

                elif j >= 1:
                    last = str(img[i][j])
                    trial += str(j - 1) + " "
                    trial += str(img[i][j]) + " "
                    trial += str(j) + " "

        trial += str(img.shape[1] - 1)
        if not (i == img.shape[0] - 1):
            trial += "\n"
    # print(trial)
    return trial


def toImg(f):
    t = open(f + ".txt", "r")
    img = t.readlines()
    height = int(img[0].split()[2])
    width = int(img[0].split()[1])

    q = np.zeros((height, width))
    if img[0].split()[0] == 'H':
        for i in range(1, height + 1):
            row = img[i].split()
            for j in range(len(row) // 3):
                value = int(row[3 * j])
                start = int(row[3 * j + 1])
                end = int(row[3 * j + 2])
                for k in range(start, end + 1):
                    q[i - 1][k] = [value, value, value]
    elif img[0].split()[0] == 'V':
        for i in range(1, width + 1):
            col = img[i].split()
            for j in range(len(col) // 3):
                value = int(col[3 * j])
                start = int(col[3 * j + 1])
                end = int(col[3 * j + 2])
                for k in range(start, end + 1):
                    q[k][i - 1] = [value, value, value]

    cv2.imwrite("output.bmp", q)


gray1 = imOpen("photo.png")  # .bmp
gray2 = imOpen("bars2.jpeg")  # .bmp

toFile("V", toStrV(gray1))
toFile("H", toStrH(gray1))

toFile("V2", toStrV(gray2))
toFile("H2", toStrH(gray2))

# toImg("Mystery1")
toImg("Mystery2")
