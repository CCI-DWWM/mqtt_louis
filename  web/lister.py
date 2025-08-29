from database import get_connection

client, database, collection = get_connection()

docs = collection.find({"end_device_ids.device_id": "bridge-chaumont"})
for doc in docs:
    received_at = doc.get("received_at")
    device_id = doc.get("end_device_ids", {}).get("device_id")
    haut = doc.get("uplink_message", {}).get("decoded_payload", {}).get("haut")

    print(received_at, device_id, haut)