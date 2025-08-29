import os
import requests  # dependency
from dotenv import load_dotenv

def send_msg_discord(username, content):
    load_dotenv()
    url = os.getenv('WEBHOOK_URL')  # webhook url, from here:
    # https://i.imgur.com/f9XnAew.png

    # for all params, see https://discord.com/developers/docs/resources/webhook#execute-webhook
    data = {"username": username, "content": content}

    # leave this out if you dont want an embed
    # for all params, see https://discord.com/developers/docs/resources/channel#embed-object

    result = requests.post(url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    else:
        print(f"Payload delivered successfully, code {result.status_code}.")

    # result: https://i.imgur.com/DRqXQzA.png