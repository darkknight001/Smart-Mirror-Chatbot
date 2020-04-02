from bot import Chatbot
from speech import Recognizer
import requests
import json


#Few basic Configurations:

wake_word = False
whether_api = ''


chatter = Chatbot()
rec = Recognizer()


class Assistant(object):
    
    def __init__(self):
        while not wake_word:
            print('Listening')
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
    
    def start(self):
        while True:
            print('Speak Now, Listening')
            userInput = rec.recognize()
            #print(userInput)
        
            if userInput is not None:  
                query_result = chatter.chat(userInput)
    
                #Parsing information from response
                input_text = query_result.query_text
                output = query_result.fulfillment_text
                intent = query_result.intent.display_name
                rec.say(output)
                print('you said : {}\nbot said:{}'.format(input_text,output))







if __name__ == "__main__":
    
    assistant = Assistant()
    assistant.start()
