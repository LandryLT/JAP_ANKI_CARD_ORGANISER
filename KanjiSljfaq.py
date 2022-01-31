from urllib.error import URLError
import urllib.parse, urllib.request
from PIL import Image
import io

# 
class KanjiSljfaq:
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
