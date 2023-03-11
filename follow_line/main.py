import cv2
import numpy as np
import math
import spidev

def Slope(x1, y1, x2, y2):
    if x1 != x2:
        m = (y1 - y2) / (x1 - x2)
        return m
    return float('inf')

def process(img):

    kernel = np.ones((9,9), np.uint8)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.GaussianBlur(img, (5,5), 0)
    _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)
    img = cv2.erode(img, kernel)
    img = cv2.dilate(img, kernel)
    img = cv2.Canny(img, 150, 200)

    cv2.imshow("dot", img)

    c ,l= img.shape
    car_radial = np.zeros(img.shape, np.uint8)
    x = l // 2
    y = c // 2

    r = 150

    for arg in range(1, 360, 4):
        x1 = int(x + r * np.cos(np.radians(arg)))
        y1 = int(y - r * np.sin(np.radians(arg)))
        x2 = int(x)
        y2 = int(y)
        cv2.line(car_radial, (x1, y1), (x2, y2), (255, 255, 255))

    dots = cv2.bitwise_and(car_radial, img)
    lines = cv2.HoughLines(dots, rho=1, theta=1 * np.pi / 180, threshold=10, srn=0, stn=0, min_theta=0, max_theta=np.pi)
    blank_image = np.zeros((dots.shape[0], dots.shape[1]), np.uint8)

    angle = 0
    if lines is not None:
        print (1)
        n_lines = len(lines)
        for i in range(0, len(lines)):
            for rho, theta in lines[i]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * a)

                cv2.line(blank_image, (x1, y1), (x2, y2), 255, 1)
                angle = angle + np.arctan(Slope(x1, y1, x2, y2)) * 57.29577951308232

        if n_lines > 0:
            angle = angle / len(lines)

    cv2.imshow("lines", blank_image)
    cv2.imshow("dots", dots)

    return angle - 90

capture = cv2.VideoCapture(0)
ret, frame = capture.read()

while not ret or  cv2.waitKey(1) != 27:
    cv2.imshow("Frame", frame)
    ret, frame = capture.read()
    spi.writebytes2(bytes(process(frame)))

