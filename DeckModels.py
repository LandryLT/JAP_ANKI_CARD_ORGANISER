from base64 import decode, encode
from anki.storage import Collection
from anki.models import NotetypeDict
import json
from WWWJDIC import WWWJDIC

#//////////////////////////////////////////////
# MODELS

# id: 1611940348229
# name: "Jap. Adjectives Template"

# id: 1611835394471
# name: "Jap. Verbs Template"

# id: 1622109327921
# name: "Kanji Card"

#//////////////////////////////////////////////
# DECKS

# id: 1648138176442
# name: Staging::イ形容詞

# id: 1648138208073
# name: Staging::ナ形容詞

# id: 1648138267373
# name: Staging::一段動詞

# id: 1648138252325
# name: Staging::五段動詞

# id: 1648138030648
# name: Staging::漢字

# id: 1648149080423
# name: "Staging::dunno"

#//////////////////////////////////////////////

cpath = "C:\\Users\\landr\\AppData\\Roaming\\Anki2\\User 1\\collection.anki2"

col = Collection(cpath)
print(col.decks.all_names_and_ids())

kanji_template = col.models.get(1622109327921)
verb_template = col.models.get(1611835394471)
adj_template = col.models.get(1611940348229)

# print(col.new_note(kanji_template))

