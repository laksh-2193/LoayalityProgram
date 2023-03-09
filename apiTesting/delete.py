from flask import Flask, jsonify
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

@app.route("/delete/<id>", methods=["DELETE"])
def delete_item(id):
    # Delete the document with the specified ID
    result = collection.delete_one({"_id": id})
    # Return a response with the number of documents deleted
    return jsonify({"deleted_count": result.deleted_count})

if __name__ == "__main__":
    app.run()
