import urllib.parse
import requests
from bs4 import BeautifulSoup
from KanjiSljfaq import KanjiSljfaq
import ssl
import re

# Create unprotected SSL context /!\
ssl._create_default_https_context = ssl._create_unverified_context

class WWWJDIC:
    def __init__(self, word: str) -> None:
        self.url = 'https://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1E'
        self.word = word
        request_body = {'dsrchkey': urllib.parse.quote(self.word.encode('utf-8')), 'dicsel': '1'}
        self.allsoup = BeautifulSoup(requests.post(self.url, request_body).content, 'html.parser')
        self.bestsoup = self.find_word_definition()
        self.get_sentence()
    
    # Get best guess of dict entry
    def find_word_definition(self) -> BeautifulSoup:
        # Get dic entries
        allheadwords_soup = self.allsoup.find("form", id="inp").find_all("div", style="clear: both;")

        # Strip headwords
        for e in allheadwords_soup:
            headword = e.find('label').find('font', size='+1').stripped_strings
            headword_str = ''
            for s in headword:
                headword_str = headword_str + s
            
            # Regex just the kanji part
            headword_str = re.match(r'(?P<hdwrd>^.*)(【.*】|《.*》)', headword_str).group('hdwrd')
            hits = re.findall(r'[^;\s]+', headword_str)
            
            # If matches exactly self.word
            for h in hits:
                if re.match(re.compile(h), self.word):
                    return e
    
    def get_sentence(self):
        both_l = self.bestsoup.find('br').next_sibling.contents[2:-2]
        # Go to bed !
        



word = 'する'
word_def = WWWJDIC(word)


# test_kan = '一生懸命'
# list_kan = []
# for c in test_kan:
#     list_kan.append(c)
# newKan = KanjiSljfaq(list_kan)