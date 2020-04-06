from bot import Chatbot
from speech import Recognizer
import requests
import json
import os
import datetime
import time
import snowboydecoder
import subprocess
import signal
from threading import Thread
from knowledge import Knowledge


#Few basic Configurations:
dir_path = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(dir_path)
whether_api = '8dde38a27814bf3a025657f5632fdb40'


chatter = Chatbot()
rec = Recognizer()
kt = Knowledge(weather_api_key=whether_api)


class Assistant(object):
    
    def __init__(self):
        print("Initializing")
        self.interrupted = False
        subprocess.Popen(["aplay", "{}/Audio-Files/Startup-Female.wav".format(ROOT_PATH)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.detector = snowboydecoder.HotwordDetector(os.path.dirname(dir_path)+"/Audio-Files/smart_mirror.pmdl", 
                       sensitivity = 0.75, audio_gain = 1)
        self.basic_intent = ['Default ','College Name','CSE HOD','Dean Academics','Dean Admin','facts','fun.1','fun.2','fun.3','fun.4','HOD ECE','Introduction','IT HOD','jokes','Mission','Principal','PEO','PO','Vision','wake word','ECE']
        self.t1 = Thread(target = self.start_detector)

    def signal_handler(self,signal, frame):
        self.interrupted = True

    def interrupt_callback(self,):
        return self.interrupted
    
    def start_detector(self):
        self.detector.start(detected_callback=self.wakeword_callback,
            interrupt_check=self.interrupt_callback,
            sleep_time=0.03)
        
    def wakeword_callback(self):
        self.__start_listening()

    def start(self):
        self.t1.start()

    def __start_listening(self,followup = False):
        
        subprocess.Popen(["aplay", "{}/Audio-Files/Fb.wav".format(ROOT_PATH)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        requests.get("http://localhost:8080/clear")
        requests.get("http://localhost:8080/listening")
        print('Speak Now')
        userInput = rec.recognize()
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
        requests.get("http://localhost:8080/clear")
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
            string = "Right now in " + res['city'] + ', it\'s ' +res['temperature'] + "° Celcius and " + res['forcast']
            print(string)
            rec.say(string.replace("'","\'"))
            requests.get("http://localhost:8080/statement?text=%s" % string)
            
        
        elif intent == 'news':
            res = kt.get_news()
            if res:
                requests.post("http://localhost:8080/news",data = json.dumps({"articles":res}))
                rec.say('here\'s some news for you!'.replace("'","\'"))
            else:
                rec.say("Troblue Finding news for you")                
        
        elif intent == 'faculty photograph':
            im_url = 'ece'
            rec.say(output)
            requests.get("http://localhost:8080/clear")
            requests.get("http://localhost:8080/data?text=%s" % im_url)
        
        elif intent == 'Contact Information':
            im_url = 'contacts'
            rec.say(output)
            requests.get("http://localhost:8080/data?text=%s" % im_url)

        elif intent == 'faculty information':
            
            f_name = query_result.parameters.fields["teacher_name"].string_value
            rec.say(output)
            #in case of no parameters
            if f_name != "":
                print("\n\n INFO :%s\n\n" %f_name)
                requests.get("http://localhost:8080/data?text=%s" % f_name)
            else:
                followupInput = self.__start_listening(followup=True)
                result = chatter.chat(followupInput)
                print(result.fulfillment_text)
                rec.say(result.fulfillment_text)
                f_name = query_result.parameters.fields["teacher_name"].string_value
                requests.get("http://localhost:8080/data?text=%s" % f_name)

                
        elif intent == 'time table faculty':
            f_name = query_result.parameters.fields["teacher_name"].string_value
            rec.say(output)
            #in case of no parameters
            if f_name != "":
                print("\n\n Time_table :%s\n\n" %f_name)
                requests.get("http://localhost:8080/data?text=%s" % f_name)
            else:
                followupInput = self.__start_listening(followup=True)
                result = chatter.chat(followupInput)
                print(result.fulfillment_text)
                rec.say(result.fulfillment_text)
                f_name = query_result.parameters.fields["teacher_name"].string_value
                requests.get("http://localhost:8080/data?text=%s" % f_name)
                
        elif intent == 'time table class':
            section = query_result.parameters.fields["section"].string_value
            college_year = query_result.parameters.fields["college_year"].string_value
            print(section)
            print(college_year)
            rec.say(output)
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
