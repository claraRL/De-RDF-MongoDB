// actors_build.js
// Lancer avec : mongosh cinema actors_build.js

db.actors.drop();

db.movies.aggregate([
  { $unwind: "$cast" },
  { $sort: { "year": -1 } }, // Tri par année avant le groupement
  {
    $group: {
      _id: "$cast.wikidata_id",
      name: { $first: "$cast.name" },
      birthDate: { $first: "$cast.birthDate" },
      wikidata_id: { $first: "$cast.wikidata_id" },
      films: {
        $push: {
          title: "$title",
          year: "$year",
          role: "$cast.role",
          director_name: "$director.name"
        }
      }
    }
  },
  { $out: "actors" }
]);

print("Collection actors créée.");
print("Nombre d'acteurs : " + db.actors.countDocuments());
print("\nExemple d'acteur :");
printjson(db.actors.findOne());