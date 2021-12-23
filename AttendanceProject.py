import cv2
import numpy as np
import os
from datetime import datetime
import mysql.connector as conn
from tkinter import *
import face_recognition


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        b1 = Button(self, text="Face-Attendance", command=self.my_function, fg='white', bg='red')
        b2 = Button(self, text="Connect to Database", command=self.connect_to_database, fg='white', bg='red')
        b3 = Button(self, text="Find Encodings", command=self.find_all_the_encodings, fg='white', bg='red')
        b1.pack(side=LEFT)
        b2.pack(side=RIGHT)
        b3.pack(side=BOTTOM)

    def connect_to_database(self):
        self.mydb = conn.connect(
            host="localhost",
            user="root",
            password="mysql@123",
            database="mydatabase"
        )
        print("Connected to Database")
        # ********************************************************

    def find_all_the_encodings(self):
        self.path = 'ImagesAttendance'
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path)
        # print(self.myList)
        for cl in self.myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImg)
            # print(self.images)
            self.classNames.append(os.path.splitext(cl)[0])
            # print(self.classNames)

        def findEncodings(images):
            self.encodeList = []
            for img in self.images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                self.encodeList.append(encode)
            return self.encodeList

        self.encodeListKnown = findEncodings(self.images)
        # print(self.encodeListKnown)
        print('Encoding Complete')

    def my_function(self):
        def markAttendance(name):
            with open('Attendance.csv', 'r+')as f:
                self.myDataList = f.readlines()
                self.nameList = []
                for line in self.myDataList:
                    entry = line.split(',')
                    # print(entry)
                    self.nameList.append(entry[0])

                if name not in self.nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name},{dtString}')
                    mycursor = self.mydb.cursor()
                    sql = "INSERT INTO attendance (name, time) VALUES (%s, %s)"
                    val = (name, dtString)

                    mycursor.execute(sql, val)

                    self.mydb.commit()

        self.cap = cv2.VideoCapture(0)
        self.cap.set(10, 150)

        while True:
            success, img = self.cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)
                # print(matches)
                if matches[matchIndex]:
                    name = self.classNames[matchIndex].upper()
                    # print(name)
                    y, w, h, x = faceLoc

                    cv2.rectangle(img, (x, y), (w, h), (255, 0, 255), 1)
                    cv2.line(img, (x, y), (x + 30, y), (255, 0, 255), 5)
                    cv2.line(img, (x, y), (x, y + 30), (255, 0, 255), 5)

                    cv2.line(img, (w, y), (w - 20, y), (255, 0, 255), 5)
                    cv2.line(img, (w, y), (w, y + 20), (255, 0, 255), 5)

                    cv2.line(img, (x, h), (x + 20, h), (255, 0, 255), 5)
                    cv2.line(img, (x, h), (x, h - 20), (255, 0, 255), 5)

                    cv2.line(img, (w, h), (w - 20, h), (255, 0, 255), 5)
                    cv2.line(img, (w, h), (w, h - 20), (255, 0, 255), 5)
                    # cv2.rectangle(img,(x,h),(w,h+50),(0,255,0),cv2.FILLED)
                    cv2.putText(img, name, (x - 6, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                    markAttendance(name)
            cv2.imshow('Webcam', img)
            cv2.waitKey(1)


root = Tk()

root.geometry("400x300")
#creation of an instance
app = Window(root)
#mainloop
root.mainloop()