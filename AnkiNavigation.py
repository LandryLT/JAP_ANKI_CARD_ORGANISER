from anki.storage import Collection
from enum import Enum
import re
# Existing Kanji :
cpath = "C:\\Users\\landr\\AppData\\Roaming\\Anki2\\MAIN\\collection.anki2"
anki_col = Collection(cpath)

class SearchModelType(Enum):
    adj_temp = "Jap. Adjectives Template"
    verb_temp = "Jap. Verbs Template"
    verb_conj_temp = "Japanese Verb Conjugation"
    kanji_temp = "Kanji Card"
    JLPT_temp = "MonoField"
    duolinguo_temp = "Duolinguo tips"

def findCardByDeckModel(deck_model):
    try:
        if type(deck_model) not in (tuple, list):
            if type(deck_model) is not SearchModelType:
                raise TypeError
            return list(anki_col.find_notes('"note:'+ deck_model.value +'"'))
    except TypeError:
        raise
