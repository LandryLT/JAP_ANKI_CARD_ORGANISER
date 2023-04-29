import random
from anki.storage import Collection
from anki.notes import Note
from HitResult import WordType
from NewDef import NewVerb, NewAdj
from NewKanjis import NewKanji
import io

#//////////////////////////////
# Getting everything into Anki
#//////////////////////////////

class DeckBuilder:
    def __init__(self, col: Collection) -> None:        
        # Collection
        self.col = col
        # Templates
        self.kanji_template = col.models.get(1622109327921)
        self.verb_template = col.models.get(1611835394471)
        self.adj_template = col.models.get(1611940348229)
        # Decks
        self.kanji_deck = col.decks.get(1648138030648)
        self.iAdj_deck = col.decks.get(1648138176442)
        self.naAdj_deck = col.decks.get(1648138208073)
        self.noun_deck = col.decks.get(1648324489749)
        self.godan_deck = col.decks.get(1648138252325)
        self.ichidan_deck = col.decks.get(1648138267373)
        self.dunno_deck = col.decks.get(1648149080423)


    def make_ankiKanjiNote(self, nk: NewKanji) -> Note:    
        note = self.col.new_note(self.kanji_template)
        note.fields[0] = nk.english
        note.fields[1] = nk.kanji
        note.fields[3] = nk.kunyomi
        note.fields[4] = nk.onyomi

        # Writing image in the collection.media default location
        img_byte_arr = io.BytesIO()
        nk.kanji_stroke_orders.img[0].save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        strk_order_f = self.col.media.write_data(nk.kanji + '.png', img_byte_arr)
        # Filling in the field
        note.fields[2] = '<div><img src="' + strk_order_f +'"></div>'
        
        self.col.add_note(note, self.kanji_deck.get('id'))

        return note


    def make_ankiNote(self, jdic: NewAdj) -> Note:
        # Depending if it's a verb or not
        note = self.col.new_note(self.adj_template)
        stroke_order_field = 5
        sound_field = 6
        if type(jdic) is NewVerb:
            note = self.col.new_note(self.verb_template)
            stroke_order_field = 8
            sound_field = 9

        # Filling basic fields
        note.fields[0] = jdic.definition
        note.fields[1] = jdic.word
        note.fields[2] = jdic.kana    
        note.fields[3] = jdic.ja_sentence
        note.fields[4] = jdic.en_sentence

        # Filling the verb specific fields
        if type(jdic) is NewVerb:
            note.fields[5] = jdic.transitivness
            note.fields[6] = jdic.stem
            note.fields[7] = jdic.te_form

        # Adding stroke order mediafile
        note.fields[stroke_order_field] = ''
        if len(jdic.stroke_order.img) > 0:
            note.fields[stroke_order_field] += '<div>'
            for i in jdic.stroke_order.img:
                if i is None:
                    continue
                # Writing images in the collection.media default location
                img_byte_arr = io.BytesIO()
                i.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                strk_order_f = self.col.media.write_data(str(random.randint(0, 9999999999999)) + '.png', img_byte_arr)
                note.fields[stroke_order_field] += '<img src="' + strk_order_f +'">'
            note.fields[stroke_order_field] += '</div>'
        
        # Adding the sound mediafile
        if jdic.soundf is not None:
            snd_byte_arr = io.BytesIO()
            with open(jdic.soundf, 'rb') as s:
                # Writing sound in the collection.media default location
                data = s.read()
                snd_byte_arr = io.BytesIO(data)
                snd_byte_arr = snd_byte_arr.getvalue()
                soundf = self.col.media.write_data(jdic.word + '.mp3', snd_byte_arr)
                note.fields[sound_field] = '[sound:'+ soundf + ']'

        # Adding note to correct deck
        if jdic.wordtype is WordType.noun:
            self.col.add_note(note, self.noun_deck.get('id'))
        elif jdic.wordtype is WordType.naAdj:
            self.col.add_note(note, self.naAdj_deck.get('id'))
        elif jdic.wordtype is WordType.iAdj:
            self.col.add_note(note, self.iAdj_deck.get('id'))
        elif jdic.wordtype is WordType.dunno:
            self.col.add_note(note, self.dunno_deck.get('id'))
        elif jdic.wordtype is WordType.ichidanVerb:
            self.col.add_note(note, self.ichidan_deck.get('id'))
        elif jdic.wordtype is WordType.godanVerb:
            self.col.add_note(note, self.godan_deck.get('id'))

        return note

    def saveall(self):
        self.col.autosave()