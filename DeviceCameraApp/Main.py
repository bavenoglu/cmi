import http
import numpy as np
import requests
import cv2 as cv
import SicDataMessage_pb2
import csv
import time
import httplib2
conn = httplib2.Http()
URL = "http://10.98.98.233:8000/BilginPhone1Camera1Snd"
headers2 = {
    "Content-Type": 'application/octet-stream'
}

for x in range(1000):
    img_neutral = cv.imread("angry.jpg")
    resultVid = SicDataMessage_pb2.SicDataMessage(UID='BilginPhone1Camera1',bData=img_neutral.tobytes())
    serialString = resultVid.SerializeToString()
    time_1 = time.time_ns() #int(round(time.time() * 1000))
    response = conn.request(URL, 'POST', body=serialString, headers=headers2)
    #time.sleep(2)
    #requests.post(URL, data=img_neutral.tobytes(), headers=headers2)
    #time_fin = int(round(time.time() * 1000))
    with open('1.csv', 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel', delimiter=';')
        writer.writerow([time_1])
    print(x)
print("finished!")
