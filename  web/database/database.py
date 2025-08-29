import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors

# Charger les variables d'environnement
load_dotenv()


def get_connection():
    """
    Établit une connexion à MongoDB en utilisant les variables d'environnement :
    - DB_URI : URI de connexion MongoDB
    - DB_DATABASE : Nom de la base de données
    - DB_COLLECTION : Nom de la collection

    Returns:
        (client, database, collection)
    """
    try:
        uri = os.getenv("DB_URI")
        if not uri:
            raise ValueError("❌ La variable d'environnement DB_URI est manquante.")

        client = MongoClient(uri)

        db_name = os.getenv("DB_DATABASE")
        if not db_name:
            raise ValueError("❌ La variable d'environnement DB_DATABASE est manquante.")
        database = client[db_name]

        collection_name = os.getenv("DB_COLLECTION")
        if not collection_name:
            raise ValueError("❌ La variable d'environnement DB_COLLECTION est manquante.")
        collection = database[collection_name]

        print("✅ Connexion MongoDB réussie")
        return client, database, collection

    except errors.ConnectionFailure as e:
        raise RuntimeError(f"⚠️ Échec de connexion à MongoDB : {e}")
    except Exception as e:
        raise RuntimeError(f"⚠️ Une erreur est survenue : {e}")


# Exemple d’utilisation
if __name__ == "__main__":
    client, db, col = get_connection()
    print("📂 Base :", db.name)
    print("📑 Collection :", col.name)