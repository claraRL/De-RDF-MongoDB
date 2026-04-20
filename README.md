# Projet : Intégration de Données RDF vers MongoDB - Cinéma

Ce projet illustre un pipeline complet d'intégration de données : extraction via SPARQL sur Wikidata, transformation en objets JSON adaptés à MongoDB, et restructuration documentaire.

## 📋 Description
L'objectif est de constituer une base documentaire de cinéma. Pour une liste d'acteurs, nous récupérons des informations sur leurs films primés, puis nous transformons ces données "orientées films" en une collection "orientée acteurs" grâce au framework d'agrégation de MongoDB.

## 📂 Contenu du projet
- `extract.py` : Script Python pour interroger le SPARQL Endpoint de Wikidata et générer `films.json`.
- `insert_movies.py` : Script Python pour insérer les données brutes dans la collection `movies`.
- `actors_build.js` : Script MongoDB (shell) pour construire la collection `actors`.
- `films.json` : Données extraites prêtes pour l'importation.

## 🛠️ Prérequis
Avant de commencer, assurez-vous d'avoir :
- **Python 3.x** installé.
- **MongoDB** installé et en cours d'exécution (port par défaut `27017`).
- Les bibliothèques Python suivantes :
  ```bash
  pip install SPARQLWrapper pymongo
