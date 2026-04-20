from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["cinema"]
movies = db["movies"]

with open("films.json", encoding="utf-8") as f:
    docs = json.load(f)

movies.drop()          # repart de zéro à chaque exécution
result = movies.insert_many(docs)

print(f"{len(result.inserted_ids)} films insérés dans la collection movies.")

# Vérification rapide : afficher les titres insérés
for doc in movies.find({}, {"title": 1, "year": 1, "_id": 0}):
    print(f"  - {doc['title']} ({doc.get('year', '?')})")

client.close()