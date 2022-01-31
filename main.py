from urllib.error import URLError
from bs4 import BeautifulSoup
import urllib.parse, urllib.request
import ssl
from PIL import Image
import io

# Create SSL certificate
ssl._create_default_https_context = ssl._create_unverified_context

# # Kanji image
# kanji_url = 'https://kanji.sljfaq.org/kanjivg/memory.cgi?k='
# kanji = '端'
# url = kanji_url + urllib.parse.quote(kanji.encode('utf-8'))

# with urllib.request.urlopen(url) as response:
#     img = Image.open(io.BytesIO(response.read()))
#     img.show()

class KanjiSoup:
    def __init__(self, kanji_l: list) -> None:
        self.url = 'https://kanji.sljfaq.org/kanjivg/memory.cgi?k='
        self.kanjis = kanji_l
        self.img = [None] * len(kanji_l)
        try:
            self.get_kanji_img()
        except URLError:
            raise
        except:
            raise

    def get_kanji_img(self):
        for k in self.kanjis:
            # AJAX request
            url = self.url + urllib.parse.quote(k.encode('utf-8'))
            # Acquire pngs
            with urllib.request.urlopen(url) as response:
                self.img[self.kanjis.index(k)] = Image.open(io.BytesIO(response.read()))

test_kan = '一生懸命'
list_kan = []
for c in test_kan:
    list_kan.append(c)
newKan = KanjiSoup(list_kan)
newKan.img[2].show()