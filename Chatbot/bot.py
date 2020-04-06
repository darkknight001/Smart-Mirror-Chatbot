import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(dir_path)
class Chatbot:
    
    def __init__(self):
       
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = dir_path+'/mm.json'

        DIALOGFLOW_PROJECT_ID = 'magicmirror-chatbot-dkqbju'
        SESSION_ID = 'me'

        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    
    def chat(self,userInput):
        DIALOGFLOW_LANGUAGE_CODE = 'en'
        text_input = dialogflow.types.TextInput(text=userInput, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = self.session_client.detect_intent(session=self.session, query_input=query_input)
        except InvalidArgument:
            raise
        # print(response.query_result.parameters.fields['geo-city'].string_value)
        
       # print("You said:", response.query_result.query_text)
        
        # print("intent:", response.query_result.intent.display_name)
        #print("Bot said:", response.query_result.fulfillment_text)
        return response.query_result