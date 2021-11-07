from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
from utils import fake_patient_generator

from services import db_service
from datetime import datetime


class Patients(Resource):
    def get(self):
        try:
            status = request.args.get('status')
            fromDate = request.args.get('fromDate')
            toDate = request.args.get('toDate')
            print(status)

            docs_ref = db_service.patients_ref

            if not (status or fromDate or toDate):
                docs_ref = self.__get_all_patients(docs_ref)

            if status:
                docs_ref = self. __get_patients_with_status(docs_ref, status)

            if toDate:
                docs_ref = self. __get_patients_to(docs_ref, toDate)

            if fromDate:
                docs_ref = self. __get_patients_from(docs_ref, fromDate)

            patients = list()
            for doc in docs_ref.stream():
                doct_dict = doc.to_dict()
                doct_dict['id'] = doc.id
                patients.append(doct_dict)

            return make_response(jsonify(patients), 200)
        except Exception as e:
            if type(e) is ValueError:
                return make_response(jsonify('invalid argument'), 400)
            else:
                return make_response(jsonify('server error'), 500)

    def __get_all_patients(self, ref):
        return ref

    def __get_patients_to(self, ref, toDate):
        toDate = datetime.strptime(toDate, '%Y-%m-%d')
        return ref.where(u'updated', u'<=', toDate)

    def __get_patients_from(self, ref, fromDate):
        fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
        return ref.where(u'updated', u'>=', fromDate)

    def __get_patients_with_status(self, ref, status):
        return ref.where(u'status', u'==', status)

    def put(self):
        if not self.__isPostBodyValid() and request.json.get('id'):
            return make_response(jsonify('invalid patient json'), 400)

        updated_patient = {
            'status': request.json['status'],
            'updated': datetime.now()
        }

        try:
            doc_ref = db_service.patients_ref.document(
                request.json.get('id'))
            if not doc_ref.get().exists:
                return make_response(jsonify('patient not found'), 400)

            doc_ref.set(updated_patient, merge=True)
            return make_response(jsonify('patient status updated'), 201)
        except Exception as e:
            return make_response(jsonify('server error'), 500)

    def post(self):
        generate = request.args.get('generate')
        if self.__shouldGeneratePatients(generate):
            generate = int(generate)
            return self.__add_generated_patients(generate)
        else:
            if not self.__isPostBodyValid():
                return make_response(jsonify('invalid patient json'), 400)

            new_patient = {
                'entryDate': datetime.now(),
                'firstName': request.json['firstName'],
                'lastName': request.json['lastName'],
                'status': request.json['status'],
                'updated': datetime.now()
            }

            try:
                db_service.patients_ref.add(new_patient)
                return make_response(jsonify('patient added'), 201)
            except Exception as e:
                return make_response(jsonify('server error'), 500)

    def __shouldGeneratePatients(self, generate):

        if not generate:
            return False

        try:
            if int(generate) > 0:
                return True
        except ValueError as e:
            return False

        return False

    def __add_generated_patients(self, generate):
        fake_patients = fake_patient_generator.generate_fake_patients(
            generate)
        try:
            batch = db_service.db.batch()
            for patient in fake_patients:
                batch.set(db_service.patients_ref.document(), patient)

            batch.commit()

            return make_response(jsonify(f'random {generate} patient(s) added'), 201)

        except Exception as e:
            return make_response(jsonify(f'server error, adding random {generate} patient(s) failed'), 500)

    def __isPostBodyValid(self):
        if (not request.json or not 'firstName' in request.json or
                not 'lastName' in request.json or not 'status' in request.json):
            return False

        return True
