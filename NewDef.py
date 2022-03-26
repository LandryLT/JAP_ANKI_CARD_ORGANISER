from HitResult import WordType
from PIL import Image
from kana_to_romaji import kana_to_romaji

#////////////////////////////
# Making Anki-digestable data
#////////////////////////////

class NewAdj:
    def __init__(self, definition: str, wordtype: WordType, word: str, kana: str, 
    en_sentence: str, ja_sentence: str, stroke_order: Image, sound_file: str) -> None:        
        self.definition = definition
        self.wordtype = wordtype
        self.word = word       
        self.kana = kana
        self.en_sentence = en_sentence
        self.ja_sentence = ja_sentence
        self.stroke_order = stroke_order
        self.soundf = sound_file

class NewVerb(NewAdj):
    def __init__(self, definition: str, wordtype: WordType, word: str, kana: str,
    en_sentence: str, ja_sentence: str, stroke_order: Image, sound_file: str, transitivness: str) -> None:
        
        super().__init__(definition, wordtype, word, kana, en_sentence, ja_sentence, stroke_order, sound_file)
        self.transitivness = transitivness
        self.stem = self.get_stem()
        self.te_form = self.get_te_form()
    

    # Make nice Formating with kana to romaji
    def get_stem(self):
        stem_kana = self.kana[0:-1]
        romaji = kana_to_romaji(stem_kana)
        if self.wordtype is WordType.ichidanVerb:
            stem_romaji = romaji + '-'
        elif self.wordtype is WordType.godanVerb:
            if self.kana[-1] == 'す':
                stem_romaji = romaji + 's-, ' + romaji + 'sh-'                
            else:
                stem_romaji = kana_to_romaji(self.kana)[0:-1] + '-'
        else:
            raise TypeError
        
        return stem_romaji        
    
    def get_te_form(self):
        stem_kana = self.kana[0:-1]
        romaji = kana_to_romaji(stem_kana)
        if self.wordtype is WordType.ichidanVerb:
            te_form = romaji + 'te'
        elif self.wordtype is WordType.godanVerb:
            if self.kana[-1] in ['う', 'つ', 'る']:
                te_form = romaji + 'tte'
            elif self.kana[-1] in ['ぬ', 'む', 'ぶ']:
                te_form = romaji + 'nde'
            elif self.kana[-1] == 'く':
                te_form = romaji + 'ite'
            elif self.kana[-1] == 'ぐ':
                te_form = romaji + 'ide'
            elif self.kana[-1] == 'す':
                te_form = romaji + 'shite'
        else:
            raise TypeError
        
        return te_form