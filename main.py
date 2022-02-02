import ssl
from KanjiSljfaq import KanjiSljfaq
from WWWJDIC import WWWJDIC

# Create unprotected SSL context /!\
ssl._create_default_https_context = ssl._create_unverified_context

word_1 = '新婦'
word_2 = 'する'
# list_kan = []
# for c in word:
#     list_kan.append(c)
# newKan = KanjiSljfaq(list_kan)

word_def = WWWJDIC(word_2, "./.sounds/")

# Print stuff
# print(word_def.sound_file)
# print(word_def.jap_sentence)
# print(word_def.eng_sentence)