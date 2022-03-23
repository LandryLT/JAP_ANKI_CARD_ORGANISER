import ssl
from KanjiSljfaq import KanjiSljfaq
from WWWJDIC import WWWJDIC, NoHits, NoMoreHits

# Create unprotected SSL context /!\
ssl._create_default_https_context = ssl._create_unverified_context

word_1 = '新婦'
word_2 = 'する'
word_3 = '滑る'
word_4 = '勉強'
word_5 = 'なら'
word_6 = '無事'
# list_kan = []
# for c in word:
#     list_kan.append(c)
# newKan = KanjiSljfaq(list_kan)
try:
    word_def = WWWJDIC(word_6, "./.sounds/")
except NoHits:
    raise
except NoMoreHits as e:
    print(e)

# Print stuff
# print(word_def.labelID)
# for h in word_def.hits:
#     print(str(h.type) + ": " + h.definition)
# print(word_def.kanjis)
# print(word_def.word)
# print(word_def.kana)
# print(word_def.jap_sentence)
# print(word_def.eng_sentence)
# print(word_def.sound_file)

