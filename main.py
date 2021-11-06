from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api
from flask_cors import CORS

import os
import json

import firebase_admin
from firebase_admin import credentials, firestore
cert_json = json.loads(os.environ["firebase_json"])
cred = credentials.Certificate(cert_json)
firebase_admin.initialize_app(cred)
db = firestore.client()
patients_ref = db.collection('patients')


app = Flask(__name__)
api = Api(app)
CORS(app)


class HelloWorld(Resource):
    def get(self):
        # return {'hello': 'world'}
        try:
            # Check if ID was passed to URL query
            # patient_id = request.args.get('id')
            # if patient_id:
            #     patient = patients_ref.document(patient_id).get()
            #     return jsonify(patient.to_dict()), 200
            # else:
            all_patients = [doc.to_dict() for doc in patients_ref.stream()]
            return make_response(jsonify(all_patients), 200)
        except Exception as e:
            return f"An Error Occured: {e}"


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
