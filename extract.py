from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import json, time

ACTORS = {
    "Tom Hanks":      "Q2263",
    "Meryl Streep":   "Q873",
    "Cate Blanchett": "Q44077",
}

ENDPOINT = "https://query.wikidata.org/sparql"

QUERY = """
SELECT DISTINCT ?film ?filmLabel ?year ?genreLabel ?director ?directorLabel ?directorBirth ?actor ?actorLabel ?actorBirth ?roleLabel WHERE {{
  BIND(wd:{qid} AS ?targetActor)
  ?film wdt:P161 ?targetActor .
  ?film wdt:P166 ?award .
  ?film wdt:P577 ?releaseDate .
  ?film wdt:P57  ?director .
  ?film wdt:P136 ?genre .

  # Récupération du casting avec le rôle
  ?film p:P161 ?statement .
  ?statement ps:P161 ?actor .
  OPTIONAL {{ ?statement pq:P453 ?role . }} 

  OPTIONAL {{ ?director wdt:P569 ?directorBirth }}
  OPTIONAL {{ ?actor wdt:P569 ?actorBirth }}

  BIND(YEAR(?releaseDate) AS ?year)

  SERVICE wikibase:label {{ 
    bd:serviceParam wikibase:language "fr,en".
    ?role rdfs:label ?roleLabel.
    ?film rdfs:label ?filmLabel.
    ?genre rdfs:label ?genreLabel.
    ?director rdfs:label ?directorLabel.
    ?actor rdfs:label ?actorLabel.
  }}
}}
"""

def val(row, key, default=""):
    return row.get(key, {}).get("value", default)

def extract_qid(uri):
    return uri.split("/")[-1] if uri else ""

def normalize_date(raw):
    if not raw:
        return ""
    raw = raw.lstrip("+")
    return raw[:4] if len(raw) >= 4 else raw


import re  # Ajoute cet import en haut du fichier

import re
import json


def fetch_rows(qid):
    sparql = SPARQLWrapper(ENDPOINT)
    # Rappel : Utilise bien les doubles accolades {{ }} dans ta QUERY pour .format()
    sparql.setQuery(QUERY.format(qid=qid))
    sparql.setReturnFormat(JSON)

    try:
        # CORRECTION : .query() suffit, puis .convert() ou .response.read()
        # Pour pouvoir nettoyer le texte avant le JSON, on fait ceci :
        result = sparql.query()
        response = result.response.read().decode('utf-8')

        # NETTOYAGE : Supprime les caractères de contrôle ASCII
        clean_response = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', response)

        data = json.loads(clean_response)
        return data["results"]["bindings"]

    except Exception as e:
        print(f"Erreur lors de la requête pour {qid}: {e}")
        return []

def group_rows_into_films(rows):
    films = {}
    for row in rows:
        film_qid = extract_qid(val(row, "film"))
        if not film_qid:
            continue
        if film_qid not in films:
            dir_uri = val(row, "director")
            films[film_qid] = {
                "wikidata_id": film_qid,
                "title":       val(row, "filmLabel") or val(row, "film"),
                "year":        int(val(row, "year")) if val(row, "year") else None,
                "director": {
                    "wikidata_id": extract_qid(dir_uri),
                    "name":        val(row, "directorLabel"),
                    "birthDate":   normalize_date(val(row, "directorBirth")),
                },
                "genres": set(),
                "cast":   {},
            }
        doc = films[film_qid]
        genre = val(row, "genreLabel")
        if genre:
            doc["genres"].add(genre)
        actor_qid = extract_qid(val(row, "actor"))
        if actor_qid and actor_qid not in doc["cast"]:
            doc["cast"][actor_qid] = {
                "wikidata_id": actor_qid,
                "name":        val(row, "actorLabel"),
                "birthDate":   normalize_date(val(row, "actorBirth")),
                "role":        "",
            }
    result = []
    for doc in films.values():
        doc["genres"] = sorted(doc["genres"])
        doc["cast"]   = list(doc["cast"].values())
        result.append(doc)
    return result

def build_movie_database():
    all_films = {}
    for actor_name, actor_qid in ACTORS.items():
        print(f"\nRecherche pour {actor_name}...")
        rows = fetch_rows(actor_qid)
        print(f"  {len(rows)} lignes reçues")
        films = group_rows_into_films(rows)
        added = 0
        for film in films:
            fid = film["wikidata_id"]
            if fid not in all_films:
                all_films[fid] = film
                added += 1
                if added == 3:
                    break
        print(f"  {added} films ajoutés")
        time.sleep(1)
    return list(all_films.values())

if __name__ == "__main__":
    movies = build_movie_database()
    with open("films.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    print(f"\nTerminé : {len(movies)} films dans films.json")
    if movies:
        print(json.dumps(movies[0], ensure_ascii=False, indent=2))