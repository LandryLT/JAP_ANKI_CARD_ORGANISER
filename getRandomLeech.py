from JAP_ANKI_CARD_ORGANISER_const import *
from random import randint
import re
from PIL import Image

iterations = 3
def recursive_img_open(img_list = []):
    if len(img_list) > 0:
        img_file_name = img_list.pop()
        with Image.open(img_file_name) as rand_img:
            rand_img.show()
            recursive_img_open(img_list)


JLPT_deck_name = "日本語::文法::JLPT"
all_JLPT_leeches = list(anki_col.find_notes('"deck:'+ JLPT_deck_name +'" "tag:leech" "card:Card 1"'))

rand_ints = []
rand_imgs = []
for i in range(0, iterations):
    rand_i = randint(0, len(all_JLPT_leeches) - 1)
    while rand_i in rand_ints:
        rand_i = randint(0, len(all_JLPT_leeches) - 1)

    rand_card = anki_col.get_card(all_JLPT_leeches[rand_i])
    img_file_name = anki_col.media.dir() + "\\" + re.findall(r'img src\=\"(\d+\.png)\"', rand_card.answer())[0]
    rand_imgs.append(img_file_name)

recursive_img_open(rand_imgs)