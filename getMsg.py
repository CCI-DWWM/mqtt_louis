import json
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
from webhook import send_msg_discord
from database import get_connection

load_dotenv()

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connecté au broker MQTT")
        client.subscribe(os.getenv("MQTT_TOPIC"))
    else:
        print(f"Échec de la connexion : {reason_code}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        client, database, collection = get_connection()
        collection.insert_one(payload)
        send_msg_discord("IoT Bot", f"Nouveau message : {payload}")
    except Exception as e:
        print(f"Erreur lors du traitement du message : {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASSWORD"))
    client.connect(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT")), 60)
    client.loop_forever()
except Exception as e:
    print(f"Erreur MQTT : {e}")