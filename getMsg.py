import paho.mqtt.client as mqtt
import json
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Chargement des variables d'environnement
load_dotenv()
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# Connexion MongoDB (local ou Atlas selon ton choix)
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["iot_database"]
collection = db["messages"]

# Callback de connexion
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(" Connecté au broker MQTT.")
        client.subscribe("v3/+/devices/+/up")
    else:
        print(f" Erreur de connexion : {reason_code}")

# Callback message
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        decoded_payload = data.get('uplink_message', {}).get('decoded_payload', {})

        document = {
            "topic": msg.topic,
            "received_at": data.get("received_at"),
            "payload": decoded_payload
        }
        collection.insert_one(document)
        print(" Message sauvegardé :", document)

    except Exception as e:
        print("Erreur :", e)

# Client MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("eu1.cloud.thethings.network", 1883, 60)
    print("Connexion au broker...")
    client.loop_forever()
except KeyboardInterrupt:
    print("Arrêt du client MQTT.")
    client.disconnect()