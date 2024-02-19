from JAP_ANKI_CARD_ORGANISER_const import *

deck_names = ["日本語::語彙::名詞と他", "日本語::語彙::形容詞::ナ形容詞", "日本語::語彙::形容詞::イ形容詞", 
              "日本語::語彙::動詞::一段動詞", "日本語::語彙::動詞::五段動詞", "日本語::文字::漢字"]

def reorder_due_by_newest(deck_name):
    new_cards_date_sorted = list(map(anki_col.getCard, anki_col.find_cards('deck:"'+deck_name+'" is:new', anki_col.get_browser_column("noteCrt"))))
    new_cards_rev_due_sorted = list(map(anki_col.getCard, anki_col.find_cards('deck:"'+deck_name+'" is:new', "c.due desc")))

    for i in  range(len(new_cards_date_sorted)):
        print(i, new_cards_date_sorted[i].due, new_cards_rev_due_sorted[i].due)
        setattr(new_cards_date_sorted[i], "due", new_cards_rev_due_sorted[i].due)
        new_cards_date_sorted[i].flush()

for deck in deck_names:
    reorder_due_by_newest(deck)

if saveall:
    anki_col.autosave()