
import cv2
cv2.namedWindow("webcam test")
cam_url='http://admin:930891@192.168.1.7:8081/video'
cap=cv2.VideoCapture(cam_url)
if cap.isOpened(): 
    rval, frame = cap.read()
else:
    cap.open(cam_url)
    rval = False

while rval:
    cv2.imshow("webcam test", frame)
    rval, frame = cap.read()
    key = cv2.waitKey(1)
    if key == 27: # exit on ESC
        break
cap.release()
cv2.destroyAllWindows()
