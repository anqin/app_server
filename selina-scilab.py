# coding:utf-8
#!/usr/bin/python3

import sys
import os

import time
import cv2
import paddlex as pdx
#import pyautogui as pgui


#HOME_DIR = "/Users/anqin/Documents/GitHub/app_server/"
HOME_DIR = "D:/workspace/"

class Models(object):
    def __init__(self, home_dir, model_path, topk=3):
        self.model_path = model_path
        self.home_dir = home_dir
        self.topk = topk
        #self.paddle_model = pdx.load_model(model_path)
        self.paddle_model = pdx.deploy.Predictor(model_path, use_gpu=False, use_mkl=True, mkl_thread_num=10)

    def predict(self, image_path):
        time.sleep(1)
        if not os.path.exists(image_path):
            print("Invalid path: ", image_path)
            return
        #model = pdx.load_model(self.model_path)
        result = self.paddle_model.predict(image_path, topk=self.topk)
        #print("Predict Result:", result)
        return self.parse_result(result)

    def photo_capture_and_predict(self):
        cam_url = 'http://admin:930891@192.168.1.7:8081/video'
        cap = cv2.VideoCapture(cam_url)
        num = 1
        captured_image_path = ""
        while(cap.isOpened()):
            ret_flag, Vshow = cap.read()
            cv2.imshow("CaptureImage",Vshow)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('s'):
                captured_image_path = self.home_dir + str(num) + ".jpg"
                cv2.imwrite(captured_image_path, Vshow)
                print(cap.get(3));
                print(cap.get(4));
                print("success to save: " + captured_image_path)
                num += 1
                ret_msg = self.predict(captured_image_path)
                #cv2.imshow(ret_msg,Vshow)
            elif k == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def parse_result(self, results):
        if len(results) == 0:
            print("无结果")
            return
        msg = ("新鲜度：还剩余 %s 天 (准确度： %.2f%%)" %(results[0]['category'], results[0]['score']*100))
        print(msg)
        return msg

    def video_stream_predict_and_show(self):
        print('==== YOLO =====')
        cam_url = 'http://admin:930891@192.168.43.87:8081/video'
        #cam_url = 'http://admin:930891@192.168.1.7:8081/video'
        cap = cv2.VideoCapture(cam_url)
        #cap = cv2.VideoCapture(0)
        num = 1
        captured_image_path = ""
        while(cap.isOpened()):
            ret_flag, Vshow = cap.read()
            num += 1
            #if not ret_flag or num != 2:
            #    continue
            num = 0

            result = self.paddle_model.predict(Vshow)
            output_frame = pdx.det.visualize(Vshow, result, threshold=0.02, save_dir = None)
            cv2.imshow("CaptureImage", output_frame)
            
            #captured_image_path = self.home_dir + "video_stream_temp.jpg"
            #cv2.imwrite(captured_image_path, Vshow)
            #print("success to save: " + captured_image_path)
            
            #result = self.paddle_model.predict(captured_image_path)
            #pdx.det.visualize(captured_image_path, result, threshold=0.3, save_dir='./')
            #show_image_path = "./visualize_" + captured_image_path
            #if not os.path.exists(show_image_path):
            #    print("Invalid path: ", show_image_path)
            #    continue

            #cv2.imshow("CaptureImage", cv2.imread(show_image_path))
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

def usage(prg):
    print("Usage: %s --model_path <path> --topk <number>" %prg)

def main(argv):
    model_type = 'image_classify'
    model_path = ""
    topk = 0
    if argv[0] == "--model_type":
        model_type = argv[1]

    if argv[2] == "--model_path":
        model_path = argv[3]
    if len(argv) > 4 and argv[4] == "--topk":
        topk = int(argv[5])
    else:
        topk = 3

    if model_path == "" or topk == 0:
        print("model path should be empty or topk should not be zero")
        print(model_path, topk)
        return
    print(model_path, topk)
    my_model = Models(HOME_DIR, model_path, topk)
    if model_type == "yolo":
        my_model.video_stream_predict_and_show()
    else:
        my_model.photo_capture_and_predict()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage(sys.argv[0])
    else:
        main(sys.argv[1:])
