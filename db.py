import pyrebase

config = {
    'apiKey' : "",
    'authDomain': "",
    'databaseURL': "",
    'projectId': "",
    'storageBucket': "",
    'messagingSenderId': "",
    'appId': "",
    'measurementId': ""
  }


firebase = pyrebase.initialize_app(config)

db = firebase.database()

