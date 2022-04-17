import ssl
from WWWJDIC import WWWJDIC, NoHits, NoMoreHits
from NewKanjis import *
import os
from DeckModels import DeckBuilder
from anki.storage import Collection
from NewDef import *
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
anki_col = Collection(cpath)

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
    print("WWWJDIC-ing " + w)
    excludedIDs = []
    prerenderedSoup = None
    # Multipass until NoMoreHits
    while True:
        try:
            newJDIC = WWWJDIC(w, soundfolder, prerenderedSoup, excludedIDs)
            JDIC_words.append(newJDIC)
            excludedIDs.append(newJDIC.labelID)
            prerenderedSoup = newJDIC.allsoup
        except NoMoreHits:
            break
        except NoHits:
            raise
        except FileNotFoundError:
            raise

# Make new Kanji Card
NewKanjiCards = []
existing_kanjis = get_existing_kanji_list(anki_col)
for k in get_new_kanjis(existing_kanjis, JDIC_words):
    print("new Kanji: " + k + " !")
    NewKanjiCards.append(NewKanji(k))


mkdeck = DeckBuilder(anki_col)
# Import Kanjis in Anki
for kjc in NewKanjiCards:
    if type(kjc) is not NewKanji:
        raise TypeError

    print("Importing " + kjc.kanji + " in Anki")
    mkdeck.make_ankiKanjiNote(kjc)

# Import Vocab in Anki
for jwrd in JDIC_words:
    if type(jwrd) is not WWWJDIC:
        raise TypeError

    for nc in jwrd.clean_definitions:
        print("Importing " + nc.word + " (" + str(nc.wordtype).replace("WordType.", "") + ") in Anki")
        mkdeck.make_ankiNote(nc)

# Save all and finish !
print("All done :)")
# mkdeck.saveall()