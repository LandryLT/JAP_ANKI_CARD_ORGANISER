from anki.storage import Collection
import re 

def get_existing_kanji_list(cpath: str):
    col = Collection(cpath)
    existing_kanji = []
    for cid in col.find_notes("deck:日本語::文字::漢字"):
        note = col.get_note(cid)
        existing_kanji.append( re.sub(r'[^一-龯]', '', note.fields[1]))

    return existing_kanji