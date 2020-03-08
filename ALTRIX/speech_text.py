
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
file = sr.AudioFile('./sound.wav')
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
    if words[0][w]=='name':
        name= words[0][w+1]+" "+words[0][w+2]
    if words[0][w]=='gender':
        gender=words[0][w+1]
    if words[0][w]=='address':
        address=''
        a=w+1
        while words[0][a]!='patient':
            address+=words[0][a]+' '
            a+=1
    if words[0][w]=='age':
        age=words[0][w+1]
    if words[0][w]=='patient' and words[0][w+2]=='number':
        a = w+3
        while words[0][a]!='patient':
            phone+=words[0][a]
            a+=1
    if words[0][w]=='patient' and (words[0][w+2]=='aadhar' or words[0][w+2]=='Aadhar'):
        aadhar=words[0][w+3]
    if (words[0][w]=='Attendee' or words[0][w]=='attendee') and words[0][w+1]=='name':
        g_name=words[0][w+2]+" "+words[0][w+3]
    if (words[0][w]=='Attendee' or words[0][w]=='attendee') and words[0][w+1]=='relationship':
        g_relationship=words[0][w+4]
    if (words[0][w]=='Attendee' or words[0][w]=='attendee') and words[0][w+2]=='number':
        g_number=words[0][w+3]
output = {'patient_name':name, 'patient_gender':gender,'patient_age':age,'patient_address':address, 'patient_phone_number':phone, 'Attendee_name':g_name,'Attendee_relationship_with_patient':g_relationship, 'Attendee_phone_number':g_number}

# import json
# with open('result.json', 'w') as fp:
#     json.dump(output, fp)
print(name)
# , gender, age, address, phone, g_name, g_relationship, g_number

# In[47]:





# In[ ]:



