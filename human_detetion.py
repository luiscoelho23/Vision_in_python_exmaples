import cvlib    # high level module, uses YOLO model with the find_common_objects method
import cv2      # image/video manipulation, allows us to pass frames to cvlib

# Load example the image and example resolution
img = cv2.imread("detetar_humano_centro.png")
resolution = [100,100]

cv2.imshow("img", img)
cv2.waitKey(0)

#Verify image is not empty
if resolution[0] != 0 and resolution[1] != 0:

    #Force depending on the person position
    Force = 0
    # Pos -> Go Right
    # Neg <- Go Left

    #Gain
    K = 0.05

    #Convert array from matlab
    #img = np.array(img,dtype=np.uint8)

    bbox, labels,_ = cvlib.detect_common_objects(img, model='yolov3-tiny', confidence=0.55, enable_gpu=False)
    for i in range(len(bbox)):
        if labels[i] == "person":
            x1,y1,x2,y2 = bbox[i]
            height, width, _= img.shape
            person_center = (x1 + x2)//2
            cam_center = width//2
            person_area = (x2 - x1) * (y2 - y1)

            Force = (1/(cam_center - person_center)) * person_area * K

    print(Force)