import snowboydecoder 
def detected_callback(): 
    print ("hotword detected") 
  
    # do your task here or call other program. 
detector = snowboydecoder.HotwordDetector("/home/pi/Desktop/Smart-Mirror-Chatbot/Audio-Files/smart_mirror.pmdl", 
                       sensitivity = 0.5, audio_gain = 1) 
  
detector.start(detected_callback) 
