# Jap Anki Card Organiser

**Jap Anki Card Organiser** is a Python script that helps you create Anki cards effeciently.

---

## WWWJDIC

**WWWJDIC** is where all the heavy scrapping occures. It gets most of its data from the brilliant [Jim Breen's WWWJDIC](https://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1C).

```python
class WWWJDIC:
    # Make a beautiful soup out of the webpage
    def renderWWWJDIC(self):

    # Isolates an entire word entry from the html
    def find_word_definition(self):

    # Isolate the example sentence and its translation from webpage if any
    def get_sentence(self):

    # If there is a soundfile, get it !
    def get_sound(self):

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
In this file there are ```{.python}WordType(enum):```

```python
class HitResult:
    def clean_up_definition(definition)

    def cleanup_transitivness(transitivness):
```

## NewKanjis

## NewDef

## DeckModels
