import ssl
from warnings import catch_warnings
from KanjiSljfaq import KanjiSljfaq
from WWWJDIC import WWWJDIC, NoHits, NoMoreHits

# Create unprotected SSL context /!\
ssl._create_default_https_context = ssl._create_unverified_context

word_1 = '新婦'
word_2 = 'する'
word_3 = '滑る'
# list_kan = []
# for c in word:
#     list_kan.append(c)
# newKan = KanjiSljfaq(list_kan)
try:
    word_def = WWWJDIC(word_3, "./.sounds/")
except NoHits:
    raise
except NoMoreHits as e:
    print(e)

# Print stuff
# print(word_def.sound_file)
# print(word_def.jap_sentence)
# print(word_def.eng_sentence)