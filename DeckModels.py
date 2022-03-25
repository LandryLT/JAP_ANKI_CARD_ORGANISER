import random
from anki.storage import Collection
from anki.notes import Note
from HitResult import WordType
from NewDef import newAdj
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
class DeckBuilder:
    def __init__(self, col: Collection) -> None:        

        self.col = col

        self.kanji_template = col.models.get(1622109327921)
        self.verb_template = col.models.get(1611835394471)
        self.adj_template = col.models.get(1611940348229)
        self.kanji_deck = col.decks.get(1648138030648)
        self.iAdj_deck = col.decks.get(1648138176442)
        self.naAdj_deck = col.decks.get(1648138208073)
        self.noun_deck = col.decks.get(1648138030648)
        self.godan_deck = col.decks.get(1648138252325)
        self.ichidan_deck = col.decks.get(1648138267373)
        self.dunno_deck = col.decks.get(1648149080423)

    def make_ankiKanjiNote(self, nk: NewKanji) -> Note:    
        note = self.col.new_note(self.kanji_template)
        note.fields[0] = nk.english
        note.fields[1] = nk.kanji
        note.fields[3] = nk.kunyomi
        note.fields[4] = nk.onyomi

        img_byte_arr = io.BytesIO()
        nk.kanji_stroke_orders.img[0].save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        strk_order_f = self.col.media.write_data(nk.kanji + '.png', img_byte_arr)
        note.fields[2] = '<div><img src="' + strk_order_f +'"></div>'
        
        self.col.add_note(note, self.kanji_deck['id'])

        return note

    def make_ankiAdjNote(self, jdic: newAdj) -> Note:
        note = self.col.new_note(self.adj_template)
        note.fields[0] = jdic.definition
        note.fields[1] = jdic.kanji
        note.fields[2] = jdic.kana    
        note.fields[3] = jdic.ja_sentence
        note.fields[4] = jdic.en_sentence
        note.fields[5] = ''
        if len(jdic.stroke_order.img) > 0:
            note.fields[5] += '<div>'
            for i in jdic.stroke_order.img:
                img_byte_arr = io.BytesIO()
                i.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                strk_order_f = self.col.media.write_data(str(random.randint(0, 9999999999999)) + '.png', img_byte_arr)
                note.fields[5] += '<img src="' + strk_order_f +'">'
            note.fields[5] += '</div>'
        
        if jdic.soundf is not None:
            snd_byte_arr = io.BytesIO()
            with open(jdic.soundf, 'rb') as s:
                data = s.read()
                snd_byte_arr = io.BytesIO(data)
                snd_byte_arr = snd_byte_arr.getvalue()
                soundf = self.col.media.write_data(jdic.kanji + '.mp3', snd_byte_arr)
                note.fields[6] = '[sound:'+ soundf + ']'

        if jdic.wordtype is WordType.noun:
            self.col.add_note(note, self.noun_deck['id'])
        elif jdic.wordtype is WordType.naAdj:
            self.col.add_note(note, self.naAdj_deck['id'])
        elif jdic.wordtype is WordType.iAdj:
            self.col.add_note(note, self.iAdj_deck['id'])
        elif jdic.wordtype is WordType.dunno:
            self.col.add_note(note, self.dunno_deck['id'])

        return note

    def saveall(self):
        self.col.autosave()



    # print(col.decks.id_for_name("日本語::語彙::名詞と他"))
    # print(col.decks.cids(1612191424176))
    # aKan = col.get_card(1637179150351)
    # print(aKan.note().fields[6])