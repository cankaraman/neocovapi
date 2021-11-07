import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

__cred = None
__cert_file_path = "neo-covid-firebase-key.json"


if 'firebase_json' in os.environ:
    __cred = credentials.Certificate(json.loads(os.environ["firebase_json"]))
elif os.path.exists(__cert_file_path):
    __cred = credentials.Certificate(__cert_file_path)

firebase_admin.initialize_app(__cred)
db = firestore.client()
patients_ref = db.collection('patients')
