import os
import requests
from dotenv import load_dotenv

def send_msg_discord(username, content):
    load_dotenv()
    url = os.getenv('WEBHOOK_URL')
    data = {"username": username, "content": content}
    try:
        result = requests.post(url, json=data)
        result.raise_for_status()
        print("Message envoyé avec succès")
    except requests.exceptions.HTTPError as err:
        print(f"Erreur lors de l'envoi du message : {err}")