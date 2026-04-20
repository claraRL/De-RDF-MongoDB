# Rapport de Projet : Pipeline d’Intégration de Données (Wikidata vers MongoDB)

**Auteur :** Clara Ralu--leroy  
**Date :** Avril 2026  
**Cours :** NoSQL & Web Sémantique

---

## 1. Approche Adoptée
Ce projet implémente un pipeline complet d'intégration de données, de l'extraction de connaissances sur le Web Sémantique à la modélisation documentaire. 
L'objectif est de constituer une base documentaire de cinéma en s'appuyant sur des données ouvertes récupérées automatiquement depuis Wikidata.

L'approche se divise en trois phases :
1. **Extraction (Python/SPARQL)** : Interrogation du SPARQL Endpoint de Wikidata pour récupérer des films primés pour une liste d'acteurs.
2. **Ingestion (JSON/MongoDB)** : Transformation des données en objets JSON et insertion dans une collection `movies`.
3. **Transformation (MongoDB Aggregation)** : Construction d'une collection orientée "acteurs" via un script shell MongoDB.

## 2. Choix de Conception

### Structure JSON (Collection `movies`)
Le modèle suit une structure centrée sur le film pour respecter les principes de localité des données de MongoDB:
- **Imbrication** : Le réalisateur et le casting sont directement inclus dans le document film.
- **Identifiants** : Conservation des identifiants Wikidata (`Qxxxx`) pour faciliter les liens futurs.
- **Normalisation** : Les labels sont extraits en français (priorité) ou anglais, et les dates sont uniformisées pour ne garder que l'année.

### Organisation de la collection `actors`
Conformément aux consignes, nous avons créé une vue "acteur-centrique". 

Chaque document regroupe :
- Les informations d'identité de l'acteur (Nom, date de naissance).
- Un tableau de tous les films présents dans la base dans lesquels il a joué, incluant le titre et le réalisateur.

## 3. Justification des décisions
- **Framework d'Agrégation** : Pour transformer la donnée, nous avons utilisé `$unwind` et `$group`.
C'est le choix le plus efficace car le traitement est réalisé côté serveur MongoDB sans transfert de données inutile vers un script externe.
- **Filtrage des données** : Nous avons restreint l'extraction aux films ayant reçu au moins un prix pour garantir la pertinence du jeu de données.

## 4. Difficultés rencontrées
- **Format SPARQL vs JSON** : Les requêtes SPARQL renvoient des résultats "plats" (une ligne par relation).
Il a fallu développer une logique de regroupement en Python pour fusionner ces lignes en documents JSON complexes (gestion des multiples genres et acteurs par film).
- **Hétérogénéité des données** : Certaines propriétés (comme les dates de naissance des réalisateurs) sont optionnelles sur Wikidata, nécessitant l'usage de clauses `OPTIONAL` pour éviter de perdre des documents complets.
- **Identifiants de dates** : La récupération des dates complètes de Wikidata exigeait un nettoyage post-extraction pour ne stocker que l'entier de l'année dans MongoDB.

---
*Ce projet a été réalisé dans le cadre du TP "De RDF à MongoDB" dirigé par Nicoleta Preda.*
