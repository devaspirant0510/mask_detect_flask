#-*- coding: utf-8 -*-

# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
import pandas as pd
import google
import multiprocessing.pool
import pandas as pd
import datetime


df=pd.read_csv("static/dataset/dataset.csv")
print("처음불러온 df:",df)



def detect_and_predict_mask(frame, faceNet, maskNet):

	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	faceNet.setInput(blob)
	detections = faceNet.forward()
	print(detections.shape)


	faces = []
	locs = []
	preds = []


	for i in range(0, detections.shape[2]):

		confidence = detections[0, 0, i, 2]


		if confidence > 0.5:

			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")


			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))


			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)


			faces.append(face)
			locs.append((startX, startY, endX, endY))


	if len(faces) > 0:

		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)


	return (locs, preds)


prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)


maskNet = load_model("mask_detector.model")


print("[INFO] starting video stream...")
def start(num):
	global mask,nomask
	try:

		frame = cv2.imread(f'static/aa{num}.jpg',cv2.IMREAD_COLOR)
		frame = imutils.resize(frame, width=300)

		# detect faces in the frame and determine if they are wearing a
		# face mask or not
		(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

		peopleli=[]
		for (box, pred) in zip(locs, preds):
			(startX, startY, endX, endY) = box
			(mask, withoutMask) = pred

			label = "Mask" if mask > withoutMask else "No Mask"
			name=label
			#print(name)

			color = (0, 255, 0) if label == "Mask" else (0, 0, 255)


			label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

			cv2.putText(frame, label, (startX, startY - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)


			peopleli.append(name)
		#print(peopleli)
		mask=0
		nomask=0
		for i in peopleli:

			if i=="Mask":
				mask+=1
			else:
				nomask+=1
		cv2.imwrite(f"static/number{num}.jpg",frame)
		return mask,nomask
	except:
		start(num)

def makephoto(num):
	start(num)
n=1
num=len(df)

while True:
	mask=0
	nomask=0
	path_dir = 'D:/승호/프로그래밍/웹/flask8/venv/Include/static'
	file_list = os.listdir(path_dir)
	name = f'aa{n}.jpg'

	if name in file_list:
		#print(name)
		makephoto(n)
		date = datetime.datetime.now()
		dateli = f'{date.year}-{date.month}-{date.day}|{date.hour}:{date.minute}'
		usrdf = pd.read_csv("static/dataset/userdataset.csv")
		dateset = pd.DataFrame({'date': [dateli],
								'user': [usrdf['user'][n-1]],
								'id': [usrdf['id'][n-1]],
								'mask': [mask],
								'nomask': [nomask]})
		print(dateset)
		df=pd.concat([df,dateset], ignore_index=True)
		#df = df.append(dateset,ignore_index=True)
		df.drop(df.filter(regex="Unname"), axis=1, inplace=True)
		print(df)
		df.to_csv("static/dataset/dataset.csv")
		df=pd.read_csv("static/dataset/dataset.csv")

		n+=1
