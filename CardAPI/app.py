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

def generate_card_number():
    iin = random.choice(["4", "5", "37", "6"]) + "".join([str(random.randint(0, 9)) for _ in range(5)])
    account_number = "".join([str(random.randint(0, 9)) for _ in range(9)])
    digits = [int(d) for d in iin + account_number]
    checksum = sum(digits[::-2] + [sum(divmod(d * 2, 10)) for d in digits[-2::-2]])
    if checksum % 10 == 0:
        check_digit = "0"
    else:
        check_digit = str(10 - checksum % 10)
    return iin + account_number + check_digit

@app.route("/insert/<info>", methods=["POST"])
def insertData(info):
    data = request.form.to_dict()
    result = db[info].insert_one(data)
    return jsonify({"Response": str(result.inserted_id)})

@app.route("/purchase/<userid>/<clientid>", methods=["GET"])
def purchase(userid, clientid):
    data = request.get_json()
    result = db["purchase"].insert_one(data)
    return jsonify({"Response": str(result.inserted_id)})

@app.route("/", methods=["GET","POST"])
def index():
    randomNo = str(random.randint(10000,99999))+str(secrets.randbelow(10000000)+10000)
    users = list(db["user"].find())
    cardsData = list(db["card"].find())
    print(cardsData,"\n",users)
    validityFrom = datetime.datetime.now().strftime('%Y-%m-%d')
    availableUsers = [user for user in users if user['_id'] not in [card['userid'] for card in cardsData]]
    return render_template('index.html', randomnumber=randomNo, cardNo=generate_card_number(),users=availableUsers,validityFrom=validityFrom)



@app.route("/transaction")
def transaction():
    items = list(db["purchase"].find())
    sorted_items = sorted(items, key=lambda x: x['timestamp'], reverse=True)
    for item in sorted_items:
        item['timestamp'] = datetime.datetime.fromtimestamp(item['timestamp']/1000.0).strftime('%B %d, %Y %H:%M:%S')
    return render_template('purchase.html',data=sorted_items)



@app.route("/userinfo")
def userinfo():
    card = list(db["card"].find())
    user = list(db["user"].find())
    return render_template("cardsInfo.html", cards=card, users=user)



if __name__ == "__main__":
    app.run()