# coding:utf-8
#!/usr/bin/python3

import sys
import os

import time
import cv2
import paddlex as pdx



HOME_DIR = "/Users/anqin/Documents/GitHub/app_server/"#"D:/workspace/"

class Models(object):
    def __init__(self, home_dir, model_path, topk=3):
        self.model_path = model_path
        self.home_dir = home_dir
        self.topk = topk
        self.paddle_model = pdx.load_model(model_path)

    def predict(self, image_path):
        time.sleep(1)
        if not os.path.exists(image_path):
            print("Invalid path: ", image_path)
            return
        #model = pdx.load_model(self.model_path)
        result = self.paddle_model.predict(image_path, topk=self.topk)
        #print("Predict Result:", result)
        self.parse_result(result)

    def photo_capture_and_predict(self):
        cap = cv2.VideoCapture(0)
        num = 1
        captured_image_path = ""
        while(cap.isOpened()):
            ret_flag, Vshow = cap.read()
            cv2.imshow("Capture Image",Vshow)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('s'):
                captured_image_path = self.home_dir + str(num) + ".jpg"
                cv2.imwrite(captured_image_path, Vshow)
                print(cap.get(3));
                print(cap.get(4));
                print("success to save: " + captured_image_path)
                num += 1
                self.predict(captured_image_path)
            elif k == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def parse_result(self, results):
        if len(results) == 0:
            print("无结果")
            return
        print("新鲜度：还剩余 %s 天 (准确度： %d)" %(results[0]['category'], results[0]['score']))


def usage(prg):
    print("Usage: %s --model_path <path> --topk <number>" %prg)

def main(argv):
    model_path = ""
    topk = 0
    if argv[0] == "--model_path":
        model_path = argv[1]
    if argv[2] == "--topk":
        topk = int(argv[3])

    if model_path == "" or topk == 0:
        print("model path should be empty or topk should not be zero")
        print(model_path, topk)
        return
    print(model_path, topk)
    my_model = Models(HOME_DIR, model_path, topk)
    my_model.photo_capture_and_predict()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        usage(sys.argv[0])
    else:
        main(sys.argv[1:])
