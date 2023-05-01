import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/Users/carlosburbano/Documents/2023/Projects/SmartGrow/smartgrow1000-firebase-adminsdk-oihbi-237773b2e0.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartgrow1000-default-rtdb.firebaseio.com/'
})

database = db.reference()

