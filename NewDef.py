from HitResult import WordType
from PIL import Image
from kana_to_romaji import kana_to_romaji

class newAdj:
    def __init__(self, definition: str, wordtype: WordType, kanjis: list, kana: str, 
    en_sentence: str, ja_sentence: str, stroke_order: Image, sound_file: str) -> None:        
        self.definition = definition
        self.wordtype = wordtype
        self.kanji = ''
        for c in kanjis:
            self.kanji += c
        self.kana = kana
        self.en_sentence = en_sentence
        self.ja_sentence = ja_sentence
        self.stroke_order = stroke_order
        self.soundf = sound_file

class NewVerb(newAdj):
    def __init__(self, definition: str, wordtype: WordType, kanjis: list, kana: str,
    en_sentence: str, ja_sentence: str, stroke_order: Image, sound_file: str, transitivness: str) -> None:
        
        super().__init__(definition, wordtype, kanjis, kana, en_sentence, ja_sentence, stroke_order, sound_file)
        self.transitivness = transitivness
        self.stem = ''
        self.te_form = ''
    

    # Make nice Formating with kana to romaji
    def get_stem(self):
        return ''
    
    def get_t_form_godan(self):
        return ''