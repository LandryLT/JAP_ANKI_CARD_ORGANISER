from urllib.error import URLError
import urllib.parse, urllib.request
from PIL import Image
import io
from time import sleep

#////////////////////////////////////////////
# Scraping from kanji.sljfaq for stroke order
#////////////////////////////////////////////

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
        i = 0
        attempts = 0
        maxAttempts = 5
        maxKanjis = len(self.kanjis)
        while i < maxKanjis:
            k = self.kanjis[i]
            try:
                attempts += 1
                # AJAX request
                url = self.url + urllib.parse.quote(k.encode('utf-8'))
                # Acquire pngs
                
                with urllib.request.urlopen(url) as response:
                    self.img[i] = Image.open(io.BytesIO(response.read()))
                    i += 1
                    attempts = 0
            except:
                if attempts < maxAttempts:
                    print("Request to KanjiSljfaq failed " + str(attempts) + "time(s)... Retrying in 5 secs...")
                    sleep(5)
                else:
                    raise KanjiSljfaqNoResponse

class KanjiSljfaqNoResponse(Exception):
    def __init__(self, kanji) -> None:
        self.message = "KanjiSljfaq is not responding for " + kanji + "..."
        super().__init__(self.message)