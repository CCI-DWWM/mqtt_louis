import os
import requests
from dotenv import load_dotenv


def send_msg_discord(username: str, content: str) -> None:
    """Envoie un message simple à un webhook Discord."""
    load_dotenv()

    url = os.getenv("WEBHOOK_URL")
    if not url:
        print("❌ Erreur : aucune URL de webhook trouvée dans .env (clé WEBHOOK_URL manquante).")
        return

    payload = {
        "username": username,
        "content": content
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"⚠️ Erreur HTTP : {err} - code {response.status_code}")
    except requests.exceptions.RequestException as err:
        print(f"⚠️ Erreur de requête : {err}")
    else:
        print(f" Message envoyé avec succès (code {response.status_code}).")
