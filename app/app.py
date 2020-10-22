from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["users"]

# Utility functions
def verfifyPw(username, password):
     hashed = users.find({
            "Username":username
     })[0]["Password"]

     if bcrypt.hashpw(password.encode('utf8'), hashed) == hashed:
         return True
     else:
         return False

def countTokens(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]
    return tokens

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        # Get the username and password
        username = postedData["username"]
        password = postedData["password"]
        # Hash the password, username
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        # Store username, password in SentencesDatabase
        users.insert({
            "Username": username,
            "Password":hashed_pw,
            "Sentence": "",
            "Tokens": 6
        })
        retJson = {
            "Status Code": 200,
            "Message" : "User Registered Successfully"
        }

        return jsonify(retJson)

class Store(Resource):
    def post(self):
        postedData = request.get_json()

        # Read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData['sentence']

        # Verify the credentials
        correct_pw = verfifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)
        # Verify the user has tokens or not
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)
        # Store the sentence and return 200 ok message
        users.update({
            "Username":username,
        }, {
            "$set": {
                    "Sentence":sentence,
                    "Tokens": num_tokens - 1
                }
        })
        retJson = {
            "Status":200,
            "Message": "Sentence saved Successfully"
        }
        return jsonify(retJson)

class Retrieve(Resource):
    def get(self):
        postedData = request.get_json()
        # Get the username and password
        username = postedData["username"]
        password = postedData["password"]
        # Verify the credentials
        correct_pw = verfifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)

        # Verify the user has tokens or not
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)

        # Decrement the tokens when user utlizes existing tokens
        users.update({
            "Username":username,
        }, {
            "$set": {
                    "Tokens": num_tokens - 1
                }
        })

        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "sentence": sentence
        }
        return jsonify(retJson)

api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Retrieve, '/get')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
