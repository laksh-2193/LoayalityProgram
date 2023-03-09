from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

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

@app.route("/update/<id>", methods=["PUT"])
def update_item(id):
    # Get the data from the request
    data = request.get_json()
    # Update the document with the specified ID
    result = collection.update_one({"_id": id}, {"$set": data})
    # Return a response with the number of documents updated
    return jsonify({"updated_count": result.modified_count})

if __name__ == "__main__":
    app.run()
