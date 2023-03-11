import cv2
import numpy as np

# Load example the image and example resolution
img = cv2.imread("detetar_vermelho_2.png")
resolution = [100,100]

#Verify image is not empty
if resolution[0] != 0 and resolution[1] != 0:

    #Convert array from matlab
    #img = np.array(img,dtype=np.uint8)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range of colors for the red in HSV
    lower_color = np.array([0, 50, 50])
    upper_color = np.array([10, 255, 255])

    lower_color_1 = np.array([240, 50, 50])
    upper_color_1 = np.array([255, 255, 255])

    # Threshold the image to get only the red color
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask_1 = cv2.inRange(hsv, lower_color_1, upper_color_1)

    mask = cv2.bitwise_or(mask, mask_1)

    # Find the center of the image
    height, width = img.shape[:2]
    center = (width//2, height//2)

    rho = 1
    theta = np.pi/180
    threshold = 20
    min_line_length = 50
    max_line_gap = 10

    # Perform Hough Transform to find lines in the image
    lines = cv2.HoughLinesP(mask, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    detect = 0
    # Check if there is any line detected
    if lines is not None:
        # Iterate over the lines
        for line in lines:
            for x1,y1,x2,y2 in line:
                # Check if the line is close to the center of the image and it's vertical
                if abs(x1 - x2) < 5 and abs(x1 - center[0]) < width//20:
                    detect = 1

    print(detect)