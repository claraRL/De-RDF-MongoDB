// actors_build.js
// Lancer avec : mongosh cinema actors_build.js

db.actors.drop();

db.movies.aggregate([

  // Étape 1 : décompose le tableau cast
  // Un film avec 5 acteurs devient 5 documents séparés
  { $unwind: "$cast" },

  // Étape 2 : regroupe par acteur
  // Accumule tous les films de chaque acteur dans un tableau
  {
    $group: {
      _id:         "$cast.wikidata_id",
      name:        { $first: "$cast.name" },
      birthDate:   { $first: "$cast.birthDate" },
      wikidata_id: { $first: "$cast.wikidata_id" },
      films: {
        $push: {
          wikidata_id: "$wikidata_id",
          title:       "$title",
          year:        "$year",
          director:    "$director",
          genres:      "$genres"
        }
      }
    }
  },

  // Étape 3 : formate le document final
  {
    $project: {
      _id:         0,
      wikidata_id: 1,
      name:        1,
      birthDate:   1,
      films:       1
    }
  },

  // Étape 4 : écrit le résultat dans la collection actors
  { $out: "actors" }

]);

print("Collection actors créée.");
print("Nombre d'acteurs : " + db.actors.countDocuments());
print("\nExemple d'acteur :");
printjson(db.actors.findOne());