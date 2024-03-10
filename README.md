# Jap Anki Card Organiser

**Jap Anki Card Organiser** is a Python script that helps you create Anki cards effeciently.
These scripts are tested and used on my personnal Anki deck and templates. As noted in the **DeckModels** section of this README, you might need to adapt some of the code if you want the scripts to work on your own deck. For reference here are the relevant templates and deck tree that I use :

### Templates :

**Kanji Card** *[Meaning, Kanji, Stroke Order, KunYomi, OnYomi]*
**Jap. Ajectives Templates** *[English Translation, JapDicFormKanji, JapDicFormHiragana, EampleSentence, ExampleEnglishTranslation, StrokeOrder, Audio]*
**Jap. Verbs Templates** *[English Translation, JapDicFormKanji, JapDicFormHiragana, ExampleSentence, ExampleSentenceTranslation, Transitivness, Stem, TeForm, StrokeOrder, Audio]*

### Deck Tree : 
├── Staging
   ├── dunno
   ├── イ形容詞
   ├── ナ形容詞
   ├── 一段動詞
   ├── 五段動詞
   ├── 名詞と他
   ├── 漢字

Note also that this repo has other scripts to update my deck and reorganise, which will certainly not work if the deck isn't exactly structured as my personnal one. You can reverse engineer if you feel like it, but I ain't doing to much documentation for something so personnal (cf: *updateWWWJDIC.py*)
---

## WWWJDIC

**WWWJDIC** is where all the heavy scrapping occures. It gets most of its data from the brilliant [Jim Breen's WWWJDIC](https://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1C).

- `EmptySoup(Exception)` is raised if the website serves empty html. This happens because I think they think this script is DDOSing them. If the problem is persistent, change IP one way or another (switching to mobile data for example)

```python
class WWWJDIC:
    # Make a beautiful soup out of the webpage
    def renderWWWJDIC(self):

    # Isolates an entire word entry from the html
    def find_word_definition(self, excludedIDs):

    # Isolate the example sentence and its translation from webpage if any
    def get_sentence(self):

    # If there is a soundfile, get it !
    def get_sound(self, dir):

    #　Gets all the kana (not as easy)
    def get_kana(self):
          
    # Makes a list of all the kanjis in the word
    def get_kanjis(self):

    #　Get label ID if we need to search recursively through the webpage (needs more testing)
    def get_ID(self):

    # Isolates the definition part in the isolated word entry html
    def get_rough_def(self):

    # Gets clean definitions and corresponding wordtypes (Hits)
    def get_hits(self):

    # Create Anki-digestable data
    def make_clean_defs(self):
```

## KanjiSljfaq

**KanjiSljfaq** scraps a stroke order PNG image from [Ben Bullock's kanji.sljfaq](https://kanji.sljfaq.org/kanjivg.html)

```python
class KanjiSljfaq:
    # Scraps the kanji stroke order and stores it in the self.img list
    def get_kanji_img(self):
```

## HitResult

All the nasty regex for guessing the wordtypes, transitivenss of verbs and cleaning up the messy definitions are in **HitResult**.
In this file there is :

- `WordType(enum)` for clean wordtype distinction
- `NoMoreHits(Exception)` and `NoHits(Exception)` for throwing "*not found on WWWJDIC*" exceptions.
- a bunch of regular expression to get the corresponding wordtypes
- an `class HitResult` to tie everything together

```python
class HitResult:
    # Get rid of unnecessary stuff in definitions
    def clean_up_definition(definition):
    
    # Replace dirty transitivness by 自動詞また他動詞それとも両方
    def cleanup_transitivness(transitivness):
```

## NewKanjis

**NewKanjis** gives methods to make a list of kanjis already in the database (`get_existing_kanji_list`) and to compare it to the list of kanji in the list of new words(`get_new_kanjis`).

```python
class NewKanji:
    # Make a beautiful soup out of the Kanji search webpage
    def renderWWWJDIC(self):
    
    # Isolates the onyomi
    def get_on(self):

    # Isolates the kunyomi
    def get_kun(self):

    # Isolates the english translation
    def get_english(self):
```

## NewDef

**NewDef** is a file containing two Classes (`NewDef` and `NewVerb(NewDef)`) which are just Anki-digestable form of data.

```python
class NewDef:
    # No methods except for init :)


class NewVerb(NewDef):
    # Get a romaji version of the verb stem
    def get_stem(self):

    # Get a romaji version of the verb te-form
    def get_te_form(self):
```

## DeckModels

**DeckModels** is the module the imports everything into Anki. All deck and template IDs are hardcoded in the main classe's attributes. You might need to find your own with the method :

```python
from anki.storage import Collection

col = Collection('[...user home path]/AppData/Roaming/Anki2/User 1/collection.anki2')
col.decks.id_for_name('[deck name]')
```

```python
class DeckBuilder:
    # Adds a kanji note to corresponding deck
    def make_ankiKanjiNote(self, newKanji):

    # Adds a verb or adjective note to corresponding deck
    def make_ankiNote(self, newWord):
    
    # Import all modifications in Anki
    def saveall(self):
```

## Secured Pickles

**Secured Pickles** is more for debugging. You can save Python objects in a signed file. It contains exception such as `InvalidSignature(Exception)` if cache files have an invalid signatures and `UserKeyNotFound(Exception)` if .secret_key file is missing. To create a secret_key file use the `check_key` method.

```python
# Save a pickled file with hmac signature
def save_secure_pickle (obj, filepath):

# Load a pickled file with hmac signature
def load_secure_pickle (filepath):

# Check for key in folder, create one if missing
def check_key(working_dir):
```

## update WWWJDIC

**update WWWJDIC** is a script to run in case of reformatting Anki cards, it is long and tedious and still needs a manual check once it's finished.



## get random leech

**get random leech** is a script to pick a given number of random leech in the JLPT grammar deck, and output the answer (for studying purposes).