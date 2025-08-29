from flask import Flask, jsonify, render_template
from database import get_connection
import json

app = Flask(__name__)

# Connexion à MongoDB
try:
    client, database, collection = get_connection()
except Exception as e:
    print(f"Erreur de connexion à MongoDB : {e}")
    client, database, collection = None, None, None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/messages")
def messages():
    if collection is None:
        return jsonify({"error": "Connexion à la base de données échouée"}), 500
    docs = collection.find().sort("received_at", -1)
    result = [doc for doc in docs]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)