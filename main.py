from flask import Flask
from flask_restful import Api
from flask_cors import CORS

import os
import json

from api_resources.patients import Patients
from services import db_service

app = Flask(__name__)
api = Api(app)
CORS(app)


api.add_resource(Patients, '/api/v0/patients')

if __name__ == '__main__':
    app.run(debug=True)
