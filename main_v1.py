
# zoom
from pyzoom import ZoomClient

import tensorflow as tf
import cv2
import json
import shlex
from fer import FER

from flask import Flask, request           # import flask
app = Flask(__name__)             # create an app instance

@app.route("/")
def hello():
 return "ZMood API" 

@app.route("/createMeeting", methods=['post']) 
def createMeeting():
  apiKey = "8hb7N3pVRLS5PWVrGqmOtQ"
  apiSecret = "Y4gNfLqrJnSLMlHvOfsuFXr5Tr4uMK5GRn8d"
  client = ZoomClient(apiKey, apiSecret)
  
  topic = request.form['topic']
  start_time = request.form['start_time']
  duration_min = 60
  
  response = str(client.meetings.create_meeting(
    topic, 
    start_time=start_time,
    duration_min=duration_min
    )
  )
  responses = shlex.split(response)
  
  tempAll = ""
  i = 0
  while i < 15:
    responses[i] = responses[i].replace('=', '":"', 1)
    responses[i] = '"'+responses[i]+'"'
    tempAll += str(responses[i])+","
    i += 1
  
  print('{'+str(tempAll[:-1])+'}')
  return(json.loads('{'+str(tempAll[:-1])+'}'))

@app.route("/triggerBot" ,methods=['GET']) 
def triggerBot():
  meetId = request.args.get('meetId')
  passCode = request.args.get('passCode')
  intervals = request.args.get('intervals')
  
  startBot(meetId,passCode,intervals)
  return "success"

@app.route("/checkTensor", methods=['GET'])
def checkTensor():
  img = cv2.imread("participantFace_2.png")

  # Face detection
  detector = FER()
  detector.detect_emotions(img)

  expression, score = detector.top_emotion(img)

  return(str(expression)+"-"+str(score))

if __name__ == "_main_":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
  