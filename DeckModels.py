from anki.storage import Collection
from anki.notes import Note
from WWWJDIC import WWWJDIC
from NewKanjis import NewKanji
import io

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

kanji_template = col.models.get(1622109327921)
verb_template = col.models.get(1611835394471)
adj_template = col.models.get(1611940348229)

kanji_deck = col.decks.get(1648138030648)
iAdj_deck = col.decks.get(1648138176442)
naAdj_deck = col.decks.get(1648138208073)
noun_deck = col.decks.get(1648138030648)
godan_deck = col.decks.get(1648138252325)
ichidan_deck = col.decks.get(1648138267373)
dunno_deck = col.decks.get(1648149080423)

def make_ankiKanjiNote(nk: NewKanji) -> Note:    
    note = col.new_note(kanji_template)
    note.fields[0] = nk.english
    note.fields[1] = nk.kanji
    note.fields[3] = nk.kunyomi
    note.fields[4] = nk.onyomi

    img_byte_arr = io.BytesIO()
    nk.kanji_stroke_orders.img[0].save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    strk_order_f = col.media.write_data(nk.kanji + '.png', img_byte_arr)
    note.fields[2] = '<div><img src="' + strk_order_f +'"></div>'
    
    col.add_note(note, kanji_deck['id'])

    return note

# DO THIS YOU DRUNKARD
# def make_adj_note(jdic: dict) -> Note:
#     note = col.new_note(kanji_template)
#     note.fields[0] = jdic['']
#     note.fields[1] = jdic.kanji

#     note.fields[3] = nk.kunyomi
#     note.fields[4] = nk.onyomi


col.autosave()

# print(col.decks.cids(1611363338011))
# aKan = col.get_card(1634656883987)
# print(aKan.note().fields[2])