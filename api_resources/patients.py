from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api


from services import db_service


class Patients(Resource):
    def get(self):
        # return {'hello': 'world'}
        try:
            # Check if ID was passed to URL query
            # patient_id = request.args.get('id')
            # if patient_id:
            #     patient = patients_ref.document(patient_id).get()
            #     return jsonify(patient.to_dict()), 200
            # else:
            all_patients = [doc.to_dict()
                            for doc in db_service.patients_ref.stream()]
            return make_response(jsonify(all_patients), 200)
        except Exception as e:
            return f"An Error Occured: {e}"
