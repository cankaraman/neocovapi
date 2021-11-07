from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api


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

            response_docs = [doc.to_dict() for doc in docs_ref.stream()]

            return make_response(jsonify(response_docs), 200)
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
        raise NotImplementedError()
