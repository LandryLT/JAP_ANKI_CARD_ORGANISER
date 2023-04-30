import ssl
from WWWJDIC import WWWJDIC, NoHits, NoMoreHits
from NewKanjis import *
from writelogs import noHitsWriteLog
import os
from sys import stdout
from DeckModels import DeckBuilder
from anki.storage import Collection
from NewDef import *
from secured_pickle import load_secure_pickle, save_secure_pickle, check_key

#///////////////////////////////////////////////////////////////////

# Where main.py is :
working_dir = os.path.dirname(os.path.realpath(__file__))
# The list of vocab to add :
vocabfile = os.path.join(working_dir, "vocab2add.txt")
# Where to write logs
logfolder = os.path.join(working_dir, "logs")
nohit_logfile = os.path.join(logfolder, "WWWJDIC_notfound.log")
# Where to write the sound files :
soundfolder = os.path.join(working_dir, "sounds/")
# Where to write the new decks :
newdecksfolder = os.path.join(working_dir, "new_decks/")
# Where to store secured cache files : 
cachefolder = os.path.join(working_dir, "cache")
word_cache = os.path.join(cachefolder, "wordcache")
kanji_cache = os.path.join(cachefolder, "kanjicache")
load_from_cache = True
# Existing Kanji :
cpath = "C:\\Users\\landr\\AppData\\Roaming\\Anki2\\User 1\\collection.anki2"
anki_col = Collection(cpath)

# THIS KANJI 龯 IS A NICE EXAMPLE OF BUGGY KANJI

#///////////////////////////////////////////////////////////////////

# Create unprotected SSL context /!\
ssl._create_default_https_context = ssl._create_unverified_context

# Check if secret key exists for secure cache
check_key(working_dir)

# Load from cache prompt (because cache loading is more of a debugging tool)
if load_from_cache:
    print("Are you sure you want to load from cache, you might create duplicate cards unintentionally ? (y|n)")
    response = input()
    if (not re.match(r'^y(es)?$', response, re.IGNORECASE)):
        load_from_cache = False


JDIC_words = []
if load_from_cache:
    #Load from cache
    JDIC_words = load_secure_pickle(word_cache)
    #Print loaded
    print("Loading " + str(len(JDIC_words)) + " WWWJDIC from cache:")
    for word in JDIC_words[:-1]:
        for c in word.clean_definitions:        
            stdout.write(c.word)
        stdout.write(", ")
    for c in JDIC_words[-1:][0].kanjis:
        stdout.write(c)
    stdout.write("\n\n")
else:
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
                noHitsWriteLog(nohit_logfile, w)
                break
            except FileNotFoundError:
                raise
    save_secure_pickle(JDIC_words, word_cache)

NewKanjiCards = []
if load_from_cache:
    #Load from cache
    NewKanjiCards = load_secure_pickle(kanji_cache)
    #Print loaded
    print("Loading " + str(len(NewKanjiCards)) + " Kanjis from cache:")
    for kanji in NewKanjiCards[:-1]:
        for c in kanji.kanji:        
            stdout.write(c)
        stdout.write(", ")
    for c in NewKanjiCards[-1:][0].kanji:
        stdout.write(c)
    stdout.write("\n\n")
else:
    # Make new Kanji Card   
    existing_kanjis = get_existing_kanji_list(anki_col)
    for k in get_new_kanjis(existing_kanjis, JDIC_words):
        print("new Kanji: " + k + " !")
        NewKanjiCards.append(NewKanji(k))
    save_secure_pickle(NewKanjiCards, kanji_cache)


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
mkdeck.saveall()