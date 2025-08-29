from flask import Flask, jsonify, render_template
from database import get_connection

app = Flask(__name__)

# Connexion à MongoDB
client, database, collection = get_connection()

@app.route("/")
def index():
    # Renvoie ton template HTML
    return render_template("index.html")

@app.route("/messages")
def messages():
    # Récupère tous les messages IoT depuis MongoDB
    docs = collection.find().sort("received_at", -1)  # tri du plus récent au plus ancien
    result = []
    for doc in docs:
        result.append({
            "received_at": doc.get("received_at"),
            "device_id": doc.get("end_device_ids", {}).get("device_id"),
            "haut": doc.get("uplink_message", {}).get("decoded_payload", {}).get("haut")
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)