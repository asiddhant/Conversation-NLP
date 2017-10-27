import os  
import speech_recognition as sr
r = sr.Recognizer()
import pandas as pd

results={'s_id':[],
         'u_id':[],
         'sentence':[]}
results=pd.DataFrame(results)

for fn in os.listdir('.'):
     if os.path.isfile(fn):

        with sr.WavFile(fn) as source:
            audio = r.record(source)  

        try:
            sphtempaudio = r.recognize_sphinx(audio)
            print("Sphinx thinks you said " + sphtempaudio)
        except sr.UnknownValueError:
            sphtempaudio = ''
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            sphtempaudio = ''
            print("Sphinx error; {0}".format(e))

        try:
            ggltempaudio = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + ggltempaudio)
        except sr.UnknownValueError:
            ggltempaudio = ''
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            ggltempaudio = ''
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
        s_id=int(fn[7:9])
        u_id=fn[0:7]
        sentence=ggltempaudio
        
        temp={'s_id':[s_id],
         'u_id':[u_id],
         'sentence':[sentence]}
        temp=pd.DataFrame(temp)
        results=results.append(temp)

results=results.sort('s_id')
results.to_csv("results.csv",sep=",")
        
        
        