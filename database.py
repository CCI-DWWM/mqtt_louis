import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        uri = os.getenv('DB_URI')
        client = MongoClient(uri)
        database = client[os.getenv('DB_DATABASE')]
        collection = database[os.getenv('DB_COLLECTION')]
        print("Connexion à la base de données réussie")
        return client, database, collection
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise