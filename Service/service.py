import numpy as np
import cv2
from PIL import Image
from keras.models import load_model
from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
import SicDataMessage_pb2
import csv
import time
import httplib2
conn = httplib2.Http()
# parameters for loading data and images
detection_model_path = 'haarcascade_frontalface_default.xml'
emotion_model_path = 'fer2013_mini_XCEPTION.102-0.66.hdf5'
emotion_labels = get_labels('fer2013')

# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)

# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]

# starting lists for calculating modes
emotion_window = []

camera = "EmotionRecognitionRcvTopic"
boxes = "camera:0:yolo"
field = "image".encode('utf-8')
emotion_text = "null"
emotion_text_temp = "null"



#@app.route('/Result', methods=['POST'])
#def hello():
import redis
r = redis.Redis(host="10.98.98.61", port="6379")
q = r.pubsub()
q.subscribe('EmotionRecognitionRcv')

for item in q.listen():
    time_2 = time.time_ns() #int(round(time.time() * 1000))
    if (item['type'] != "message"):
        continue
    data = item['data']
    #data = request.data
    vid = SicDataMessage_pb2.SicDataMessage()
    vid.ParseFromString(data)

    im = Image.frombytes('RGB', (640, 480), vid.bData)
    bgr_image = np.asarray(im, dtype=np.uint8)
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    faces = detect_faces(face_detection, gray_image)

    for face_coordinates in faces:
        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]

    time_3 = time.time_ns() #int(round(time.time() * 1000))

    resultVid = SicDataMessage_pb2.SicDataMessage(UID=vid.UID,bData=str.encode(emotion_text))
    URL = "http://10.98.98.233:8000/EmotionRecognitionSnd"
    headers2 = {
        "Content-Type": 'application/octet-stream'
        #"Content-Type": 'application/json'
    }
    #time_4 = int(round(time.time() * 1000))
    serialString = resultVid.SerializeToString()
    response = conn.request(URL, 'POST', body=serialString, headers=headers2)

    #response = requests.request('POST', URL, data=resultVid.SerializeToString(), headers=headers2)
    #time_5 = int(round(time.time() * 1000))
    with open('2.csv', 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel', delimiter=';')
        writer.writerow([time_2])
    with open('3.csv', 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel', delimiter=';')
        writer.writerow([time_3])

