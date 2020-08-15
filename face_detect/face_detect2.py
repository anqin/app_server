# -*- coding: utf-8 -*-
import face_recognition
import cv2
import datetime
import glob2 as gb
 
video_capture = cv2.VideoCapture(0)
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
 
while True:
    ret, frame = video_capture.read()
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
 
video_capture.release()
cv2.destroyAllWindows()
