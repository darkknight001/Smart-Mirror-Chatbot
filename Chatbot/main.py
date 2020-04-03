from bot import Chatbot
from speech import Recognizer
import requests
import json
import os
import datetime


#Few basic Configurations:

wake_word = False
whether_api = ''


chatter = Chatbot()
rec = Recognizer()


class Assistant(object):
    
    def __init__(self):
        print("initializing")
        os.system('aplay /home/pi/Desktop/Smart-Mirror-Chatbot/Audio-Files/Startup-Female.wav')
    
    def start(self):
        wake_word = False
        while True:
            #print('Listening')
            userInput = rec.recognize()
            if userInput is not None:  
                query_result = chatter.chat(userInput)

            #Parsing information from response
                input_text = query_result.query_text
                # output = query_result.fulfillment_text
                intent = query_result.intent.display_name
                print(input_text, intent)
                # check is ok mirror is said or not
                if  intent == 'wake word':
                    wake_word = True
            if wake_word:
                os.system(r'aplay /home/pi/Desktop/Smart-Mirror-Chatbot/Audio-Files/Fb.wav')
                requests.get("http://localhost:8080/clear")
                print('Speak Now')
                userInput = rec.recognize()
                #print(userInput)
            
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
