import ssl
from KanjiSljfaq import KanjiSljfaq
from WWWJDIC import WWWJDIC, NoHits, NoMoreHits
from AnkiReader import get_existing_kanji_list
from NewKanjis import NewKanji, get_new_kanjis
import os

#///////////////////////////////////////////////////////////////////

# Where main.py is :
working_dir = os.path.dirname(os.path.realpath(__file__))
# The list of vocab to add :
vocabfile = os.path.join(working_dir, "vocab2add.txt")
# Where to write the sound files :
soundfolder = os.path.join(working_dir, ".sounds/")
# Where to write the new decks :
newdecksfolder = os.path.join(working_dir, ".new_decks/")
# Existing Kanji :
cpath = "C:\\Users\\landr\\AppData\\Roaming\\Anki2\\User 1\\collection.anki2"

# THIS KANJI 龯 IS A NICE EXAMPLE OF BUGGY KANJI

#///////////////////////////////////////////////////////////////////

# Create unprotected SSL context /!\
ssl._create_default_https_context = ssl._create_unverified_context

# Import words to add
words_to_add = []
try:
    with open(vocabfile, 'r', encoding='utf-8') as f:
        for w in f.read().splitlines():
            # Python style comment out
            if w[0] != '#':
                words_to_add.append(w)
except FileNotFoundError:
    raise

# WWWJDIC the words to add
JDIC_words = []
for w in words_to_add:
    try:
        print("WWWJDIC-ing " + w)
        JDIC_words.append(WWWJDIC(w, soundfolder))
    except NoHits:
        raise
    except NoMoreHits as e:
        print(e)
    except FileNotFoundError:
        raise

# Make new Kanji Card
NewKanjiCards = []
existing_kanjis = get_existing_kanji_list(cpath)
for k in get_new_kanjis(existing_kanjis, JDIC_words):
    (print("new Kanji: " + k + " !"))
    NewKanjiCards.append(NewKanji(k))

# Make the new deck

# # Print stuff
# print(word_def.labelID)
# for w in JDIC_words:
#     for h in w.hits:
#         if w.kana is not None:
#             print(w.word + " (" + w.kana + ") : " + str(h.type) + ": " + h.definition)
#         else:
#             print(w.word + ": " + str(h.type) + ": " + h.definition)
# # print(word_def.kanjis)
# print(word_def.word)
# print(word_def.kana)
# print(word_def.jap_sentence)
# print(word_def.eng_sentence)
# print(word_def.sound_file)

