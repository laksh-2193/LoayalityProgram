from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Replace the placeholders with your own MongoDB connection details
client = MongoClient("mongodb+srv://lakshayhex:lakshayhex@testing.nhy1m2r.mongodb.net/?retryWrites=true&w=majority")
db = client["Student"]
collection = db["info"]

@app.route("/items", methods=["GET"])
def get_items():
    # Retrieve all documents from the collection
    items = list(collection.find())
    # Convert the documents to JSON and return them
    return jsonify(items)

@app.route("/create", methods=["POST"])
def create_item():
    # Get the data from the request
    data = request.get_json()
    # Insert the data into the collection
    result = collection.insert_one(data)
    # Return a response with the inserted ID
    return jsonify({"inserted_id": str(result.inserted_id)})

if __name__ == "__main__":
    app.run()
