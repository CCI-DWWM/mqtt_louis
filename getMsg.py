import paho.mqtt.client as mqtt
import json, random

# Callback appelé lorsque le client se connecte au broker
def on_connect(client, userdata, flags, reason_code, properties): #(client, userdata, flags, rc):
    print("Connected with result code "+str(reason_code))
    # Abonnement à un topic
    client.subscribe("v3/+/devices/+/up")

# Callback appelé quand un message est reçu du broker
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    print(msg.topic, data.get('received_at'))
    #print(json.dumps(data, indent=2))
    print(json.dumps(data.get('uplink_message').get('decoded_payload'), indent=2))

APPID  = "cci-blois@ttn"
PSW    = 'NNSXS.45H7G7TM4TNK72DVRBFD7JIUF334XPHARQN2CQA.IYIBJDTD4WEV3MAAOCJP7BSKMIZQ7IDDIPTZBUYGWRNJJY4T3WZA'

# Création d'un client MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Configuration du nom d'utilisateur et du mot de passe
client.username_pw_set(APPID, PSW)

# Attribution des fonctions de callback
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker MQTT
client.connect("eu1.cloud.thethings.network", 1883, 60)

# Boucle pour maintenir le client en écoute des messages
client.loop_forever()
#while True:
#    client.loop()