from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connexion MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["iot_database"]
collection = db["messages"]

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/messages", methods=["GET"])
def get_messages():
    messages = list(collection.find({}, {"_id": 0}))
    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True, port=5000)