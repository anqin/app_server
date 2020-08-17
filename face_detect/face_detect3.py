# -*- coding: utf-8 -*-
import sys
import face_recognition
import cv2
import datetime
import glob2 as gb
import ffmpeg
#from ffmpy import FFmpeg

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string('input_video', None, 'the path of candidate video for parsing')
flags.DEFINE_string('output_file', './person_relationship_list.txt', 'the parth of file for result output')


def read_frame_by_time(in_file, time):
    """
    指定时间节点读取任意帧
    """
    out, err = (
        ffmpeg.input(in_file, ss=time)
              .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
              .run(capture_stdout=True)
    )
    return out



def get_video_info(in_file):
    """
    获取视频基本信息
    """
    try:
        probe = ffmpeg.probe(in_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print('No video stream found', file=sys.stderr)
            sys.exit(1)
        return video_stream
    except ffmpeg.Error as err:
        print(str(err.stderr, encoding='utf8'))
        sys.exit(1)


# video_capture = cv2.VideoCapture(0)
img_path=gb.glob(r'D:\workspace\github\app_server\face_detect\photo\\*.png')
known_face_names=[]
known_face_encodings=[]
 
for i in img_path:
    picture_name=i.replace('D:\\workspace\\github\\app_server\\face_detect\photo\\','')
    picture_newname=picture_name.replace('.png','')
    print("new name: " + picture_newname)
    someone_img = face_recognition.load_image_file(i)
    someone_face_encoding = face_recognition.face_encodings(someone_img)[0]
    known_face_names.append(picture_newname)
    known_face_encodings.append(someone_face_encoding)
    someone_img=[]
    someone_face_encoding=[]
	
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

print('known_face_num: ' + known_face_names[0])

'''
while True:
   # ret, frame = video_capture.read()

    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame=small_frame[:,:,::-1]
    
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for i in face_encodings:
                match = face_recognition.compare_faces(known_face_encodings,i,tolerance=0.5)
                face_distances = face_recognition.face_distance(known_face_encodings, i)
                #print(face_distances)
                if True in match:
                    match_index=match.index(True)
                    name = "match"
                #To print name and time
                    cute_clock = datetime.datetime.now()
                    print (known_face_names[match_index]+':'+str(cute_clock))
                    name = known_face_names[match_index]
                else:
                    name = "unknown"
                face_names.append(name)
 
    process_this_frame = not process_this_frame
 
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
 
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255),  2)
 
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)
 
    cv2.imshow('Video', frame)
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''


#video_capture.release()


def main(argv):
    del argv
    input_video_path = FLAGS.input_video
    output_file = FLAGS.output_file

    print("Open: " + input_video_path)

    video_info = get_video_info(input_video_path)
    total_duration = video_info['duration']
    print('总时间：' + total_duration + 's')

    span = 0
    while span < total_duration:

        frame = read_frame_by_time(input_video_path, span)
        span += 3

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame=small_frame[:,:,::-1]
    
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for i in face_encodings:
                match = face_recognition.compare_faces(known_face_encodings,i,tolerance=0.5)
                face_distances = face_recognition.face_distance(known_face_encodings, i)
                #print(face_distances)
                if True in match:
                    match_index=match.index(True)
                    name = "match"
                #To print name and time
                    cute_clock = datetime.datetime.now()
                    print (known_face_names[match_index]+':'+str(cute_clock))
                    name = known_face_names[match_index]
                else:
                    name = "unknown"
                face_names.append(name)
 

cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(main)
