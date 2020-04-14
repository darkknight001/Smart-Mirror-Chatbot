import pyrebase

config = {    
    "apiKey": "AIzaSyAFQ3ezz5EzFRe1LcC7Gq5bOXN4mYIbwNQ",
    "authDomain": "imagea-8cd39.firebaseapp.com",
    "databaseURL": "https://imagea-8cd39.firebaseio.com",
    "projectId": "imagea-8cd39",
    "storageBucket": "imagea-8cd39.appspot.com",
    "messagingSenderId": "484670069784",
    "appId": "1:484670069784:web:a7eec3b4943fbdb3b2b76d",
    "measurementId": "G-T6NEF7Y1MW"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

path_on_cloud = "Technical Staff.jpg"

storage.child(path_on_cloud).download("staff_photo.jpg")
