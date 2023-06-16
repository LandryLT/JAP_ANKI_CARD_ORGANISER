import ssl
from WWWJDIC import WWWJDIC, NoHits, NoMoreHits, EmptySoup
from NewKanjis import *
from KanjiSljfaq import KanjiSljfaqNoResponse
from writelogs import *
import os
from sys import stdout
from DeckModels import DeckBuilder
from anki.storage import Collection
from NewDef import *
from secured_pickle import load_secure_pickle, save_secure_pickle, check_key
from AnkiNavigation import anki_col

#///////////////////////////////////////////////////////////////////

# Where main.py is :
working_dir = os.path.dirname(os.path.realpath(__file__))
# The list of vocab to add :
vocabfile = os.path.join(working_dir, "vocab2add.txt")
# Where to write logs
logfolder = os.path.join(working_dir, "logs")
logfile = os.path.join(logfolder, "errors.log")
# Where to write the sound files :
soundfolder = os.path.join(working_dir, "sounds/")
# Where to write the new decks :
newdecksfolder = os.path.join(working_dir, "new_decks/")
# Where to store secured cache files : 
cachefolder = os.path.join(working_dir, "cache")
word_cache = os.path.join(cachefolder, "wordcache")
kanji_cache = os.path.join(cachefolder, "kanjicache")
update_word_cache = os.path.join(cachefolder, "updwordcache")
load_from_cache = False


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
