from bot import Chatbot
from speech import Recognizer
import requests
import json
import os
import datetime
import snowboydecoder
from threading import Thread
from knowledge import Knowledge


#Few basic Configuration:

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
     #Parsing intent from response
        intent = query_result.intent.display_name
        
        action = query_result.action
        print("name:",action)
        input_text = query_result.query_text
        print(input_text)
        output = query_result.fulfillment_text
        if intent in self.basic_intent or "smalltalk" in action:
            
            requests.get("http://localhost:8080/statement?text=%s" % output)
            print('you said : {}\nbot said:{}'.format(input_text,output))
            rec.say(output)
        
        elif intent == 'Time':
            time_str = kt.get_time()
            requests.get("http://localhost:8080/statement?text=%s" % time_str)
            rec.say(time_str.replace("'","\'"))
        
        elif intent == 'Date':
            res = kt.get_date()
            requests.get("http://localhost:8080/statement?text=%s" % res)
            rec.say(res.replace("'","\'"))
        
        elif intent == 'weather': 
            res = kt.find_weather()
            string = "Right now in " + res['city'] + ", it is " +res['temperature'] + "° Celcius and " + res['forcast']
            print(string)
            rec.say(string.replace("'","\'"))
            requests.get("http://localhost:8080/statement?text=%s" % string)
            
        
        elif intent == 'news':
            res = kt.get_news()
            if res:
                requests.post("http://localhost:8080/news",data = json.dumps({"articles":res}))
                rec.say("here is some news for you!".replace("'","\'"))
            else:
                rec.say("Troblue Finding news for you")                
        
        elif intent == 'faculty photograph':
            im_url = 'ece'
            requests.get("http://localhost:8080/clear")
            requests.get("http://localhost:8080/data?text=%s" % im_url)

        elif intent == 'faculty information':
            
            f_name = query_result.parameters.fields["teacher_name"].string_value
            rec.say(output)
            im_url = f_name
            requests.get("http://localhost:8080/clear")
            requests.get("http://localhost:8080/data?text=%s" % im_url)
            #in case of no parameters
            if f_name != "":
                print("\n\n INFO :%s\n\n" %f_name)
            else:
                followupInput = self.__start_listening(followup=True)
                result = chatter.chat(followupInput)
                print(result.fulfillment_text)
                rec.say(result.fulfillment_text)
                
        elif intent == 'time table faculty':
            f_name = query_result.parameters.fields["teacher_name"].string_value
            rec.say(output)
            im_url = f_name
            requests.get("http://localhost:8080/clear")
            requests.get("http://localhost:8080/data?text=%s" % im_url)
            if f_name != "":
                print("\n\n timetable :%s\n\n" %f_name)
            else:
                followupInput = self.__start_listening(followup=True)
                result = chatter.chat(followupInput)
                print(result.fulfillment_text)
                rec.say(result.fulfillment_text)
                
        elif intent == 'time table class':
            section = query_result.parameters.fields["section"].string_value
            college_year = query_result.parameters.fields["college_year"].string_value
            print(section)
            print(college_year)
            im_url = section+" "+college_year
            requests.get("http://localhost:8080/clear")
            requests.get("http://localhost:8080/data?text=%s" % im_url)
            print("\n\n timetable :%s\n\n" %im_url)
        
        elif intent == "Default Fallback Intent":
            requests.get("http://localhost:8080/statement?text=%s" % output)
            print('fallback : '.format(output))
            rec.say(output)
            
        else:
            rec.say("unable get it!, come again".replace("'","\'"))
            print("fallback")
            wake_word = False
            self.__start_listening()
    







if __name__ == "__main__":
    assistant = Assistant()
    assistant.start()
