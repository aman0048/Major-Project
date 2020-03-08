from flask import Flask, request, redirect, url_for, send_from_directory, render_template, Response
import time
import os
import pyrebase
 
config = {
  'apiKey': "AIzaSyArDmVdmj8maZuih3SYCYosI4pCVq_my6g",
  'authDomain': "altrix-fc7d2.firebaseapp.com",
  'databaseURL': "https://altrix-fc7d2.firebaseio.com",
  'projectId': "altrix-fc7d2",
  'storageBucket': "altrix-fc7d2.appspot.com",
  'messagingSenderId': "698495361145"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# # In[16]:


# from nltk.tokenize import word_tokenize

# Setup Flask app.
app = Flask(__name__)
app.debug = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def downloadComplete(): 
 
  # coding: utf-8

  # In[8]:


  #!/usr/bin/env python
  # coding: utf-8

  # In[15]:

  import sys
  import nltk
  import numpy as np
  import speech_recognition as sr


  # In[16]:


  from nltk.tokenize import word_tokenize


  # In[17]:

  r = sr.Recognizer()
  mic = sr.Microphone()
  file = sr.AudioFile('sound.wav')
  # CHECK ADDRESS
  with file as source:
      r.adjust_for_ambient_noise(source)
      audio = r.record(source)
  text = r.recognize_google(audio)


  # In[101]:


  words = word_tokenize(text)
  words = np.array(words)
  words = words.reshape(1,-1)


  # In[124]:
  name = ''
  gender = ''
  address = ''
  age = ''
  phone = ''
  aadhar = ''
  g_name = ''
  g_relationship = ''
  g_number = ''

  for w in range(words[0].shape[0]):
    if words[0][w]=='patient' and words[0][w+1]=='name':
      name= words[0][w+2]+" "+words[0][w+3]
    if words[0][w]=='gender':
      gender=words[0][w+1]
    if words[0][w]=='age':
      age=words[0][w+1]
    if words[0][w]=='patient' and words[0][w+1]=='number':
      for a in range(10):
        phone += words[0][w+2+a]
    if (words[0][w]=='Attendee' or words[0][w]=='attendee') and words[0][w+1]=='name':
      g_name=words[0][w+2]+" "+words[0][w+3]
    if (words[0][w]=='Attendee' or words[0][w]=='attendee') and words[0][w+1]=='relationship':
      g_relationship=words[0][w+4]
    if (words[0][w]=='Attendee' or words[0][w]=='attendee') and words[0][w+1]=='number':
      g_number=words[0][w+2]
  output = {'patient_name':name, 'patient_gender':gender,'patient_age':age, 'patient_phone_number':phone, 'Attendee_name':g_name,'Attendee_relationship_with_patient':g_relationship, 'Attendee_phone_number':g_number}

  import json
  with open('result.json', 'w') as fp:
      json.dump(output, fp)


def predict(data):
  import pandas as pd
  import numpy as np
  from sklearn import preprocessing
  from sklearn.linear_model import LogisticRegression
  from sklearn.model_selection import train_test_split
  data1 = pd.read_csv('./Training.csv')
  data = data[1:-1]
  a = np.array([])
  for ix in range(len(data)):
    a = np.append(a,ord(data[ix])-48)
  x = data1.values
  X = x[:,:-1]
  X = X[:,20:40]
  Y = x[:,-1]
  le = preprocessing.LabelEncoder()
  le.fit(Y)
  Y = le.transform(Y)
  Y.shape

  X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
  lr = LogisticRegression(solver='lbfgs', multi_class='multinomial')
  lr.fit(X_train,Y_train)
  y_pred = lr.predict(a.reshape(1,-1))
  Y_pred = le.inverse_transform(y_pred)
  user = db.child("Prediction").child('data',Y_pred[0])
  return Y_pred[0]


# def ocr1():
#   import re
#   import sys
#   import pytesseract
#   from PIL import Image, ImageEnhance, ImageFilter
#   import cv2
#   import os
#   from io import StringIO
#   from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
#   from sklearn.decomposition import LatentDirichletAllocation
#   import pandas as pd
#   import numpy as np
#   image = cv2.imread('Screenshot.png')
#   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#   gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#   filename = "{}.png".format(os.getpid())
#   cv2.imwrite(filename, gray)
#   text = pytesseract.image_to_string(Image.open(filename))
#   os.remove(filename)
#   clean_cont = text.splitlines()
#   sent_str = ""
#   for i in clean_cont:
#       sent_str += str(i) + " "
#   sent_str = sent_str[:-1]
#   from nltk.tokenize import sent_tokenize
#   clean_cont = sent_tokenize(sent_str)
#   dubby=[re.sub("[^a-zA-Z]+", " ", s) for s in clean_cont[1:]]
#   from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
#   vect=TfidfVectorizer(ngram_range=(1,1),stop_words='english')
#   dtm=vect.fit_transform(dubby)
#   result = dtm.toarray()
#   a = np.array([])
#   for ix in range(result.shape[0]):
#       a=np.append(a,np.sum(result[ix]))
#   ind = np.argsort(a)
#   summary = np.array([])
#   array1 = ind[-2:]
#   sorted(array1)
#   for ix in array1:
#       summary = np.append(summary,dubby[ix])
#   summary_str = str(clean_cont[0])+ " "
#   for ix in summary:
#       summary_str+= str(ix)+" "
#   device.close()
#   retstr.close()
#   return summary_str


# Routes
@app.route('/')
def root():
  return render_template('home.html')

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/details')
def detail():
  return render_template('details.html')

# AJAX Request Handler
@app.route('/done', methods=['GET', 'POST'])
def recordedSample():
  time.sleep(3)
  downloadComplete()
  time.sleep(3)
  os.remove('./sound.wav')
  
  user = db.child("Recordings").child('data',result.json)
  return send_from_directory('./', 'result.json')

@app.route('/predicted')
def Predicted():
  return render_template('predicted.html')  
  
@app.route('/prediction/<string:key>')
def Prediction(key):
  return(predict(key))

@app.route('/ocr')
def OCR():
  return(ocr1())  

if __name__ == '__main__':
  app.run()

