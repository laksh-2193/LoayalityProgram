from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import random, json, datetime
import secrets

app = Flask(__name__)
client = MongoClient("mongodb+srv://cardandeducate:cardandeducate@cardandeducate.ydrpzsc.mongodb.net/?retryWrites=true&w=majority")
db = client["Information"]
db["user"].create_index("email", unique=True)
db["user"].create_index("contact", unique=True)
db["card"].create_index("userid", unique=True)

@app.route("/get/<info>", methods=["GET"])
def getData(info):
    items = list(db[info].find())
    return jsonify(items)


@app.route("/insert/<info>", methods=["POST"])
def insertData(info):
    data = request.get_json()
    result = db[info].insert_one(data)
    return jsonify({"Response": str(result.inserted_id)})


@app.route("/purchase/<userid>/<clientid>", methods=["GET"])
def purchase(userid, clientid):
    data = request.get_json()
    result = db["purchase"].insert_one(data)
    return jsonify({"Response": str(result.inserted_id)})