
# Elsa Voice Assistant

Elsa Voice Assistant uses VOSK as Speech Recognition for Taking voice inputs via microphone.


## Requirements
#### main:
speech_recognition  
pyttsx3  
vosk  
sounddevice

#### Sub:
 wikipedia  
 webbrowser  
 wolframalpha  
 requests
 etc.

 
 
## Features

- Offline Voice Recognition i.e No need of Internet .
- Can take basic Notes.
- easy: not that much of Complex code.
- would be fun for you and me to introduce new Commands.



## Points to Remember:

- you need to Download A model from Vosk Website, also keep it in the same Folder as that of project after extraction in a folder under name "model".

- downloading a high data model may give better accuracy but it will take time to recognize your voice so it's better to use 128/129 Mb models.

- Vosk can be easily replaced by any voice recogniton model in a minute without altering any of the code by simply changing the "TakeCommand" function.

- the code below is what takes the actual microphone input to be recognized.

while True:  
    data = q.get()     
    if rec.AcceptWaveform(data):  
        res = json.loads(rec.Result())  
        #print (res['text'])  
        if len(res['text'])==0:  
            print("Sorry I couldn't catch that!!")  
            speak("Sorry I couldn't catch that!!")  
            #print(type(comm))  
        else:  
            print("User :" + res['text'])  
            return res['text']
