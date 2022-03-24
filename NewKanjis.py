import imp
from bs4 import BeautifulSoup
from KanjiSljfaq import KanjiSljfaq
import requests
import urllib.parse



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
        return BeautifulSoup(requests.post(url, request_body).content, 'html.parser').find("form", id="inp").find("label")

    def get_on(self):
        for s in self.soup.next_siblings:
            if s.string == '[音]':
                return s.next_sibling.next_sibling.string

    def get_kun(self):
        for s in self.soup.next_siblings:
            if s.string == '[訓]':
                return s.next_sibling.next_sibling.string

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
