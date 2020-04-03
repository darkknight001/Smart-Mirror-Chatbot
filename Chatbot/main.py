from bot import Chatbot
from speech import Recognizer
import requests
import json
import os
import datetime
import snowboydecoder
from threading import Thread
from knowledge import Knowledge


#Few basic Configurations:

whether_api = '8dde38a27814bf3a025657f5632fdb40'


chatter = Chatbot()
rec = Recognizer()
kt = Knowledge(weather_api_key=whether_api)


class Assistant(object):
    
    def __init__(self):
        print("Initializing")
        os.system('aplay /home/pi/Desktop/Smart-Mirror-Chatbot/Audio-Files/Startup-Female.wav')
        
        self.detector = snowboydecoder.HotwordDetector("/home/pi/Desktop/Smart-Mirror-Chatbot/Audio-Files/smart_mirror.pmdl", 
                       sensitivity = 0.5, audio_gain = 1)
        self.basic_intent = ['Default ','College Name','CSE HOD','Dean Academics','Dean Admin','facts','fun.1','fun.2','fun.3','fun.4','HOD ECE','Introduction','IT HOD','jokes','Mission','Principal','PEO','PO','Vision','wake word','ECE']
        self.t1 = Thread(target = self.detector.start(self.__wakeword_callback))


    def __wakeword_callback(self):
        self.__start_listening()
    
    
   # def __detect_hotword(self):
        
    def start(self):
        self.t1.start()
        
    def __start_listening(self,followup = False):
        os.system(r'aplay /home/pi/Desktop/Smart-Mirror-Chatbot/Audio-Files/Fb.wav')
        print('Speak Now')
        userInput = rec.recognize()
        requests.get("http://localhost:8080/clear")
        if not followup:        
            if userInput is not None:  
                self.__decide_intent(userInput)
            else:
                self.__start_listening()
        else:
            if userInput is not None:  
                return userInput
            else:
                self.__start_listening(followup=True)
            
        
    def __decide_intent(self,userInput):       
        query_result = chatter.chat(userInput)
        print(query_result)
        #Parsing intent from response
        intent = query_result.intent.display_name
        input_text = query_result.query_text
        output = query_result.fulfillment_text
        if intent in self.basic_intent:
            
            requests.get("http://localhost:8080/statement?text=%s" % output)
            print('you said : {}\nbot said:{}'.format(input_text,output))
            rec.say(output)
        
        elif intent == 'Time':
            time_str = kt.get_time()
            requests.get("http://localhost:8080/statement?text=%s" % output)
            rec.say(time_str)
        
        elif intent == 'Date':
            res = kt.get_date()
            requests.get("http://localhost:8080/statement?text=%s" % output)
            rec.say(res)
        
        elif intent == 'Day':
            res = kt.get_day()
            requests.get("http://localhost:8080/statement?text=%s" % output)
            rec.say(res)
        
        #elif intent == 'weather':
            
         #   res = kt.find_weather()
          #  string = "It's " +
        
        elif intent == 'news':
            res = kt.get_news()
            if res:
                requests.post("http://localhost:8080/news",data = json.dumps({"articles":res}))
                rec.say("Here's some news for you!")
            else:
                rec.say("Troblue Finding news for you")                
        
        elif intent == 'faculty photograph':
            im_url = '/home/pi/Downloads/ECE_department.jpg'
            requests.get("http://localhost:8080/clear")
            body = {'url':im_url}
            #requests.get("http://localhost:8080/face")
            requests.get("http://localhost:8080/image?text=%s" % im_url)

        elif intent == 'faculty information':
            
            f_name = query_result.parameters.fields["teacher_name"]
            rec.say(output)
            
            #in case of no parameters
            if f_name != "":
                print("\n\n INFO :%s\n\n" %f_name)
            else:
                followupInput = self.__start_listening(followup=True)
                result = chatter.chat(followupInput)
                print(result.fulfillment_text)
                rec.say(result.fulfillment_text)
                
        elif intent == 'time table faculty':
            f_name = query_result.parameters.fields["teacher_name"]
            rec.say(output)
            if f_name != "":
                print("\n\n timetable :%s\n\n" %f_name)
            else:
                followupInput = self.__start_listening(followup=True)
                result = chatter.chat(followupInput)
                print(result.fulfillment_text)
                rec.say(result.fulfillment_text)
                
        elif intent == 'time table class':
            pass
        
        else:
            rec.say("I didn't get it!")
            print("fallback")
            wake_word = False
            self.__start_listening()
    







if __name__ == "__main__":
    assistant = Assistant()
    assistant.start()
