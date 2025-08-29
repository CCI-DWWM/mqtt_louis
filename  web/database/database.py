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

        # start example code here
        print("Database connected successfully")
        # end example code here
        return client, database, collection

    except Exception as e:
        raise Exception(f"The following error occurred: {e}")