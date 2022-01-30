from bs4 import BeautifulSoup
import urllib.parse, urllib.request
import ssl
from PIL import Image
import io

# Create SSL certificate
ssl._create_default_https_context = ssl._create_unverified_context

# Kanji image
kanji_url = 'https://kanji.sljfaq.org/kanjivg/memory.cgi?k='
kanji = '端'
url = kanji_url + urllib.parse.quote(kanji.encode('utf-8'))

with urllib.request.urlopen(url) as response:
    img = Image.open(io.BytesIO(response.read()))
    img.show()

# class KanjiSoup:
#     def __init__(self, url: str, kanji: str) -> None:
#         self.url = url
#         self.kanji = kanji

#     def get_kanji_img(self):


