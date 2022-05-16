import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
#from ecapture import ecapture as ec
import wolframalpha
import json
import requests
import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
from vosk import SetLogLevel
SetLogLevel(-1)



clear = lambda: os.system('cls')

#text to speech conversion
#voices[0] means male voice 
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[1].id')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    t = time.localtime()
    hour = int(time.strftime("%H", t))
    
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")

def takeCommand(text):
    statement = text.lower()

    if "stop" in statement or "exit" in statement:
        print('Elsa is shutting down')
        speak('Elsa is shutting down')
        exit()


    elif 'wikipedia' in statement:
        speak('Searching Wikipedia...')
        statement =statement.replace("wikipedia", "")
        results = wikipedia.summary(statement, sentences=3)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open videos' in statement or 'open youtube' in statement or 'youtube' in statement:
        webbrowser.open_new_tab("https://www.youtube.com")
        speak("youtube is open now")
        time.sleep(5)

    elif 'open google' in statement or 'google' in statement:
        webbrowser.open_new_tab("https://www.google.com")
        speak("Google chrome is open now")
        time.sleep(5)

    elif 'open gmail' in statement or 'open mail' in statement or 'mail' in statement:
        webbrowser.open_new_tab("https://www.gmail.com")
        speak("Google Mail is open now")
        time.sleep(5)
 
    elif "good morning" in statement or "good afternoon" in statement or "good evening" in statement:
        speak("A warm" + statement)
        speak("How are you Mister")
        #speak(assname)
    
    elif 'open stackoverflow' in statement or "stack" in statement or "overflow" in statement:
            speak("Here you go to Stack Over flow.Happy coding")
            webbrowser.open("https://www.stackoverflow.com")  

    

    elif "will you be my gf" in statement or "will you be my bf" in statement:  
        speak("I'm not sure about, may be you should give me some time")
 
    elif "how are you" in statement:
        speak("I'm fine, thanks for asking!")
 
    elif "i love you" in statement:
        speak("Get yourself a girlfriend it's not good to flirt with an assistant")

    elif "restart" in statement:
            subprocess.call(["shutdown", "/r"])
             
    elif "hibernate" in statement or "sleep" in statement:
        speak("Hibernating")
        subprocess.call("shutdown / h")
    
    elif "log off" in statement or "sign out" in statement:
        speak("Make sure all the application are closed before sign-out")
        time.sleep(5)
        subprocess.call(["shutdown", "/l"])














if __name__=='__main__':

    clear()
    print("Loading your personal voice assistant Elsa")
    speak("Loading your personal voice assistant Elsa")
    wishMe()
    print("Listening..")
    speak("Listening!!")



    q = queue.Queue()

    def int_or_str(text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        '-f', '--filename', type=str, metavar='FILENAME',
        help='audio file to store recording to')
    parser.add_argument(
        '-m', '--model', type=str, metavar='MODEL_PATH',
        help='Path to the model')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-r', '--samplerate', type=int, help='sampling rate')
    args = parser.parse_args(remaining)
    
    try:
        if args.model is None:
            args.model = "model"
        if not os.path.exists(args.model):
            print ("Please download a model for your language from https://alphacephei.com/vosk/models")
            print ("and unpack as 'model' in the current folder.")
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])

        model = vosk.Model(args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                                channels=1, callback=callback):
                #print('#' * 80)
                #print('Press Ctrl+C to stop the recording')
                #print('#' * 80)
                rec = vosk.KaldiRecognizer(model, args.samplerate)
                
                while True:
                    #clear()
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
                            takeCommand(res['text'])
                            
                        #time.sleep(3)
                        
                    #else:
                    #  print(rec.PartialResult())
                # if dump_fn is not None:
                    #   dump_fn.write(data)

    except KeyboardInterrupt:
        print('\nDone')
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))





        

time.sleep(3)

