from bs4 import BeautifulSoup
from KanjiSljfaq import KanjiSljfaq
import requests
import urllib.parse
from anki.storage import Collection
import re 

#////////////////////////////////////
# Working on yet to be learned Kanjis
#////////////////////////////////////

# Make list of kanjis already in the database
def get_existing_kanji_list(col: Collection):
    existing_kanji = []
    for cid in col.find_notes("deck:日本語::文字::漢字"):
        note = col.get_note(cid)
        existing_kanji.append( re.sub(r'[^一-龯]', '', note.fields[1]))

    return existing_kanji

# Don't add kanjis that are already in the database
def get_new_kanjis(old_kanjis: list, newWWWJDICs: list):
    
    # List kanji from new vocab
    jdic_kanjis = []
    for jdics in newWWWJDICs:
        for k in jdics.kanjis:
            jdic_kanjis.append(k)
    # Remove duplicates
    add_kanjis = list(dict.fromkeys(jdic_kanjis))
    # Make list of new unknown kanjis
    new_kanjis = [nk for nk in add_kanjis if nk not in old_kanjis]

    return new_kanjis

# Accessing WWWJDIC Kanji dictionnary and formating for Anki import
class NewKanji:
    def __init__(self, kanji) -> None:
        self.kanji = kanji
        self.soup = self.renderWWWJDIC()
        self.kunyomi = self.get_kun()
        self.onyomi = self.get_on()
        self.english = self.get_english()
        self.kanji_stroke_orders = KanjiSljfaq([kanji])

    def renderWWWJDIC(self) -> BeautifulSoup:
        # Get WWWJDIC kanji homepage
        url = 'https://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1D'
        request_body = {'ksrchkey': urllib.parse.quote(self.kanji.encode('utf-8')), 'kanjsel': 'X', 'strcnt': ''}
        
        try:
            outputsoup = BeautifulSoup(requests.post(url, request_body).content, 'html.parser').find("form", id="inp").find("label")
        except:
            raise
        
        return outputsoup

    def get_on(self):
        for s in self.soup.next_siblings:
            if s.string == '[音]':
                return s.next_sibling.next_sibling.string
        return ''

    def get_kun(self):
        for s in self.soup.next_siblings:
            if s.string == '[訓]':
                return s.next_sibling.next_sibling.string
        return ''

    def get_english(self):
        english = ''
        for soup in self.soup.next_siblings:
            if soup.string == '[英]':
                for s in soup.next_siblings:
                    if s.name == 'a':
                        break
                    elif s.name == 'b':                    
                        english += s.string + ' '
        return english
