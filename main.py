import ssl
from KanjiSljfaq import KanjiSljfaq
from WWWJDIC import WWWJDIC, NoHits, NoMoreHits
from AnkiReader import get_existing_kanji_list
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
existing_kanjis = get_existing_kanji_list(cpath)
# THIS KANJI 龯 IS A NICE EXAMPLE OF BUGGY KANJI

#///////////////////////////////////////////////////////////////////

# Create unprotected SSL context /!\
ssl._create_default_https_context = ssl._create_unverified_context

# Import words to add
words_to_add = []
try:
    with open(vocabfile, 'r', encoding='utf-8') as f:
        words_to_add = f.read().splitlines()
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

# Make the new deck


# word_1 = '新婦'
# word_2 = 'する'
# word_3 = '滑る'
# word_4 = '勉強'
# word_5 = 'なら'
# word_6 = '無事'
# list_kan = []
# for c in word:
#     list_kan.append(c)
# newKan = KanjiSljfaq(list_kan)

# # Print stuff
# print(word_def.labelID)
# for h in word_def.hits:
#     print(str(h.type) + ": " + h.definition)
# print(word_def.kanjis)
# print(word_def.word)
# print(word_def.kana)
# print(word_def.jap_sentence)
# print(word_def.eng_sentence)
# print(word_def.sound_file)

