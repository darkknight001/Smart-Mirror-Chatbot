from bot import Chatbot
from speech import Recognizer
import requests
import json
import os
import datetime
import snowboydecoder
from threading import Thread


#Few basic Configurations:

whether_api = ''


chatter = Chatbot()
rec = Recognizer()


class Assistant(object):
    
    def __init__(self):
        print("Initializing")
        os.system('aplay /home/pi/Desktop/Smart-Mirror-Chatbot/Audio-Files/Startup-Female.wav')
        
        self.wake_word = False
        
        self.detector = snowboydecoder.HotwordDetector("/home/pi/Desktop/Smart-Mirror-Chatbot/Audio-Files/smart_mirror.pmdl", 
                       sensitivity = 0.5, audio_gain = 1)
       
        
    def __wakeword_callback(self):
        self.__start_listening()
    
    
    def __detect_hotword(self):
        self.detector.start(self.__wakeword_callback)
    
    def start(self):
        self.__detect_hotword()
        
    def __start_listening(self):
        os.system(r'aplay /home/pi/Desktop/Smart-Mirror-Chatbot/Audio-Files/Fb.wav')
        print('Speak Now')
        userInput = rec.recognize()
        requests.get("http://localhost:8080/clear")
        if userInput is not None:  
            query_result = chatter.chat(userInput)
            #Parsing information from response
            input_text = query_result.query_text
            output = query_result.fulfillment_text
            intent = query_result.intent.display_name
            requests.get("http://localhost:8080/statement?text=%s" % output)
            print('you said : {}\nbot said:{}'.format(input_text,output))
            rec.say(output)
            
            
            #if intent == 'Time':
                
            #if intent == 'faculty information':
                
            if intent == 'faculty photograph':
                im_url = '/home/pi/Downloads/ECE_department.jpg'
                requests.get("http://localhost:8080/clear")
                body = {'url':im_url}
                #requests.get("http://localhost:8080/face")
                requests.get("http://localhost:8080/image?text=%s" % im_url)

                
            #if intent = 'time table faculty':
            
            #if intent = 'time table class':
            
            #if intent = 'weather':
                
            
            
            
            if not intent == 'Default Fallback Intent':
                wake_word = False







if __name__ == "__main__":
    assistant = Assistant()
    assistant.start()
