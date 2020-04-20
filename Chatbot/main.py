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
import pyrebase
from threading import Thread
from knowledge import Knowledge


#Few basic Configurations:
dir_path = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(dir_path)
whether_api = '8dde38a27814bf3a025657f5632fdb40'


firebase_config = {    
    "apiKey": "AIzaSyAFQ3ezz5EzFRe1LcC7Gq5bOXN4mYIbwNQ",
    "authDomain": "imagea-8cd39.firebaseapp.com",
    "databaseURL": "https://imagea-8cd39.firebaseio.com",
        "projectId": "imagea-8cd39",
    "storageBucket": "imagea-8cd39.appspot.com",
    "messagingSenderId": "484670069784",
    "appId": "1:484670069784:web:a7eec3b4943fbdb3b2b76d",
    "measurementId": "G-T6NEF7Y1MW"
}

firebase = pyrebase.initialize_app(firebase_config)


storage = firebase.storage()
db = firebase.database()

fb_token = None
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
                rec.say("unable get it!, come again")
                self.__start_listening()
        else:
            if userInput is not None:  
                return userInput
            else:
                rec.say("unable get it!, come again")
                self.__start_listening(followup=True)
           
        
    def __decide_intent(self,userInput):       
        query_result = chatter.chat(userInput)
        requests.get("http://localhost:8080/clear")
        #Parsing intent from response
        intent = query_result.intent.display_name
        
        action = query_result.action
        input_text = query_result.query_text
        print(input_text)
        output = query_result.fulfillment_text
        if "smalltalk" in action:
            
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
        
        elif intent == 'Faculty Photograph':
            path_on_cloud = "ece.jpg"
            path = storage.child(path_on_cloud).get_url(token=None)
            rec.say(output)
            body = {'url': path}
            requests.post("http://localhost:8080/image", data=json.dumps(body))
        
        elif intent == 'Contact Information':
            path_on_cloud = "staff.jpg"
            path = storage.child(path_on_cloud).get_url(token=None)
            rec.say(output)
            body = {'url': path}
            requests.post("http://localhost:8080/image", data=json.dumps(body))
        
        elif intent == 'faculty information':
            
            f_name = query_result.parameters.fields["teacher_name"].string_value
            rec.say(output)
            #in case of no parameters
            if f_name != "":
                print("\n\n INFO :%s\n\n" %f_name)
                path_on_cloud = "faculty/"+ f_name +".jpg"
                path = storage.child(path_on_cloud).get_url(token=None)
                body = {'url': path}
                requests.post("http://localhost:8080/image", data=json.dumps(body))
            else:
                followupInput = self.__start_listening(followup=True)
                result = chatter.chat(followupInput)
                print(result.fulfillment_text)
                rec.say(result.fulfillment_text)
                f_name = query_result.parameters.fields["teacher_name"].string_value
                path_on_cloud = "faculty/"+ f_name +".jpg"
                path = storage.child(path_on_cloud).get_url(token=None)
                body = {'url': path}
                requests.post("http://localhost:8080/image", data=json.dumps(body))

                
        elif intent == 'time table faculty':
            f_name = query_result.parameters.fields["teacher_name"].string_value
            rec.say(output)
            #in case of no parameters
            if f_name != "":
                print("\n\n Time_table :%s\n\n" %f_name)
                path_on_cloud = "Time_table/Faculty_time_table/"+ f_name +".png"
                path = storage.child(path_on_cloud).get_url(token=None)
                body = {'url': path}
                requests.post("http://localhost:8080/image", data=json.dumps(body))
            else:
                followupInput = self.__start_listening(followup=True)
                result = chatter.chat(followupInput)
                print(result.fulfillment_text)
                rec.say(result.fulfillment_text)
                f_name = query_result.parameters.fields["teacher_name"].string_value
                path_on_cloud = "Time_table/Faculty_time_table/"+ f_name +".png"
                path = storage.child(path_on_cloud).get_url(token=None)
                body = {'url': path}
                requests.post("http://localhost:8080/image", data=json.dumps(body))
                
        elif intent == 'time table class':
            section = query_result.parameters.fields["section"].string_value
            college_year = query_result.parameters.fields["college_year"].string_value
            print(section)
            print(college_year)
            rec.say(output)
            path_on_cloud = "Time_table/students_time_table/"+ section+"_"+college_year +".png"
            path = storage.child(path_on_cloud).get_url(token=None)
            body = {'url': path}
            requests.post("http://localhost:8080/image", data=json.dumps(body))
        
        elif intent == "notice faculty":
            announement = db.child("Announcement Teacher").child().get()
            l = []
            for date,val in announement.val().items():
                d,m,y,s_no = date.split("_")
                date = d+"/"+m+"/"+y
                data = {}
                data["serial"] = s_no
                data["date"] = date
                data["description"] = val
                l.append(data)
            print(json.dumps(l))
            rec.say(output)
            requests.post("http://localhost:8080/notice",data=json.dumps(l))

        elif intent == "notice student":
            announement = db.child("Announcement Student").child().get()
            l = []
            for date,val in announement.val().items():
                d,m,y,s_no = date.split("_")
                date = d+"/"+m+"/"+y
                data = {}
                data["serial"] = s_no
                data["date"] = date
                data["description"] = val
                l.append(data)
            print(json.dumps(l))
            rec.say(output)
            requests.post("http://localhost:8080/notice",data=json.dumps(l))

        elif intent == "notice general":
            announement = db.child("Notice_IPU").child().get()

            l = []
            for date,val in announement.val().items():
                d,m,y,s_no = date.split("_")
                date = d+"/"+m+"/"+y
                data = {}
                data["serial"] = s_no
                data["date"] = date
                data["description"] = val
                l.append(data)
            print(json.dumps(l))
            rec.say(output)
            requests.post("http://localhost:8080/notice",data=json.dumps(l))
            
        elif intent == "Default Fallback Intent":
            requests.get("http://localhost:8080/statement?text=%s" % output)
            print('fallback : '.format(output))
            rec.say(output)
            
        else:
            requests.get("http://localhost:8080/statement?text=%s" % output)
            print('you said : {}\nbot said:{}'.format(input_text,output))
            rec.say(output)
    







if __name__ == "__main__":
    assistant = Assistant()
    assistant.start()
