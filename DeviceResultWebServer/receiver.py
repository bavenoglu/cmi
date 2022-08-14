from flask import Flask, request
from datetime import datetime
import cv2
import SicDataMessage_pb2
from PIL import Image
import numpy as np
import csv
import time
"""
import redis
import time
r = redis.Redis(host="localhost", port="6379")
q = r.pubsub()
q.subscribe('EmotionRecognitionSnd')

for item in q.listen():
    print(item)
"""
app = Flask(__name__)

@app.route('/Result', methods = ['POST'])
def hello():
    data = request.data
    vid = SicDataMessage_pb2.SicDataMessage()
    vid.ParseFromString(data)

    time_4 = time.time_ns()
    with open('4.csv', 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel', delimiter=';')
        writer.writerow([time_4])
    print(vid.bData)
    return "Hello World!"
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')

"""
    im = Image.frombytes('RGB', (640, 480), vid.bData)
    img = np.asarray(im, dtype=np.uint8)
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S") + ".jpg"
    cv2.imwrite(date_time, img)
"""