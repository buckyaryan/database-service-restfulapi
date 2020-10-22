from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import os

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_users"]
        new_num  = prev_num + 1
        UserNum.update({}, {"$set":{"num_of_users":new_num}})
        return str("Hello User "+str(new_num))

def checkPostedData(postedData, functionName):
    if functionName in ['add', 'substract','multiply']:
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif functionName in ["division"]:
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"])==0:
            return 302
        else:
            return 200

class Addition(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "add")

        if status_code != 200:
            retjson = {
                "Message": "An error occured",
                "Status Code": status_code

            }
            return jsonify(retjson)

        x = int(postedData["x"])
        y = int(postedData["y"])
        ret = x + y
        retmap = {
            'Sum': ret,
            "Status Code": 200
        }
        return jsonify(retmap)

class Substraction(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "substract")

        if status_code != 200:
            retjson = {
                "Message": "An error occured",
                "Status Code": status_code

            }
            return jsonify(retjson)

        x = int(postedData["x"])
        y = int(postedData["y"])
        ret = x - y
        retmap = {
            'Sum': ret,
            "Status Code": 200
        }
        return jsonify(retmap)

class Mutliplication(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "multiply")

        if status_code != 200:
            retjson = {
                "Message": "An error occured",
                "Status Code": status_code

            }
            return jsonify(retjson)

        x = int(postedData["x"])
        y = int(postedData["y"])
        ret = x * y
        retmap = {
            'Sum': ret,
            "Status Code": 200
        }
        return jsonify(retmap)

class Division(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "division")

        if status_code != 200:
            retjson = {
                "Message1": "An error occured",
                "Status Code": status_code

            }
            return jsonify(retjson)

        x = int(postedData["x"])
        y = int(postedData["y"])
        ret = (x*1.0) / y
        retmap = {
            'Sum': ret,
            "Status Code": 200
        }
        return jsonify(retmap)

api.add_resource(Addition, '/add')
api.add_resource(Substraction, '/sub')
api.add_resource(Mutliplication, '/mul')
api.add_resource(Division, '/div')
api.add_resource(Visit, '/hello')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
