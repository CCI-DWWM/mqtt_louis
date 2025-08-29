import json
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

from webhook import send_msg_discord
from database import get_connection

# Charger les variables d'environnement
load_dotenv()


# Callback quand le client se connecte au broker MQTT
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("✅ Connexion MQTT réussie")
        # S'abonner au topic défini dans .env
        topic = os.getenv("MQTT_SUBSCRIBE")
        if topic:
            client.subscribe(topic)
            print(f"📡 Abonné au topic : {topic}")
        else:
            print("⚠️ Aucun topic MQTT défini dans .env (clé MQTT_SUBSCRIBE).")
    else:
        print(f"⚠️ Échec connexion MQTT, code {reason_code}")


# Callback quand un message est reçu depuis le broker
def on_message(client, userdata, msg):
    try:
        db_client, database, collection = get_connection()

        print(f"📩 Message reçu sur {msg.topic} : {msg.payload}")

        # Décodage JSON
        data = json.loads(msg.payload.decode("utf-8"))

        # Enregistrement dans la collection MongoDB
        result = collection.insert_one(data)
        print(f"✅ Insertion MongoDB OK : {result.inserted_id}")

        # Envoi sur Discord (si souhaité)
        # send_msg_discord(msg.topic, json.dumps(data, indent=2))

    except Exception as e:
        print(f"⚠️ Erreur lors du traitement du message : {e}")


def main():
    # Création d'un client MQTT
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Authentification MQTT
    mqtt_user = os.getenv("MQTT_USER")
    mqtt_password = os.getenv("MQTT_PASSWORD")
    if mqtt_user and mqtt_password:
        mqttc.username_pw_set(mqtt_user, mqtt_password)

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    # Connexion au broker
    mqtt_host = os.getenv("MQTT_HOST", "localhost")
    mqtt_port = int(os.getenv("MQTT_PORT", 1883))

    print(f"🚀 Connexion au broker MQTT {mqtt_host}:{mqtt_port} ...")
    mqttc.connect(mqtt_host, mqtt_port, 60)

    # Boucle infinie pour écouter les messages
    mqttc.loop_forever()


if __name__ == "__main__":
    main()