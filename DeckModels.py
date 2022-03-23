from anki.storage import Collection
import json
import genanki

# USE GENANKI OR JUST ANKI ????



# id: 1611940348229
# name: "Jap. Adjectives Template"

# id: 1611835394471
# name: "Jap. Verbs Template"

# id: 1622109327921
# name: "Kanji Card"

cpath = "C:\\Users\\landr\\AppData\\Roaming\\Anki2\\User 1\\collection.anki2"
col = Collection(cpath)
print(json.dumps(col.models.get(1611940348229), sort_keys=True, indent=4))