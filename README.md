# Projet : Intégration de Données RDF vers MongoDB (Cinéma)

Ce projet réalise un pipeline complet d'intégration de données, allant de l'extraction de connaissances sur le Web Sémantique (Wikidata) à la structuration d'une base de données documentaire NoSQL (MongoDB).

## 📋 Description du Projet
L'objectif est de constituer une base documentaire de films primés en utilisant deux approches complémentaires :
1. **Extraction de données** via SPARQL sur le point d'accès de Wikidata.
2. **Gestion et transformation** des données dans MongoDB pour créer des vues orientées "films" et "acteurs".

## 📂 Structure des Scripts
Le projet se compose des fichiers suivants :
- `extract.py` : Script Python qui interroge Wikidata et produit le fichier `films.json`.
- `insert_movies.py` : Script Python qui importe les données dans la collection `movies` de MongoDB.
- `actors_build.js` : Script shell MongoDB (Aggregation Framework) qui génère la collection `actors`.
- `films.json` : Fichier de données intermédiaire généré par l'extracteur.

## 🛠️ Prérequis
Avant l'exécution, assurez-vous d'avoir installé les éléments suivants :

### 1. Environnement
- **Python 3.x**
- **MongoDB** (doit être lancé localement sur le port 27017)

### 2. Bibliothèques Python
Installez les dépendances nécessaires via `pip` :

```bash
pip install SPARQLWrapper pymongo
```

🚀 Instructions d'exécution

Veuillez suivre les étapes dans cet ordre précis pour construire la base de données :

**Étape 1** : Extraction depuis Wikidata

Lancez le script d'extraction pour récupérer les informations sur les acteurs et leurs films primés :

```bash
python extract.py
```

Cette étape crée le fichier films.json avec les titres, dates, genres, réalisateurs et castings.

**Étape 2** : Insertion dans MongoDB

Importez les données extraites dans la collection initiale :

```bash
python insert_movies.py
```

Le script crée (ou réinitialise) la collection movies dans la base de données cinema.

**Étape 3** : Transformation (Modèle Acteurs)

Exécutez le script d'agrégation pour restructurer la base de données par acteur :

```bash
mongosh cinema actors_build.js
```

Ce script utilise le framework d'agrégation pour regrouper tous les films pour chaque acteur présent dans la base.

🔍 Vérification des données

Vous pouvez vérifier le succès de l'opération directement dans le shell MongoDB (mongosh) :


```JavaScript
use cinema
// Pour voir un film
db.movies.findOne()
// Pour voir un acteur et la liste de ses films
db.actors.findOne()
```

📝 Auteur

Ralu--Leroy Clara - Avril 2026
