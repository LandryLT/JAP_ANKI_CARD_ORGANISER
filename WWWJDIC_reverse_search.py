from difflib import SequenceMatcher
from AnkiNavigation import *
from JAP_ANKI_CARD_ORGANISER_const import *
from HitResult import *
from time import time

def getDeckType(deck_name):
    if re.search("名詞と他", deck_name):
        return WordType.noun
    if re.search("イ形容詞", deck_name):
        return WordType.iAdj
    if re.search("ナ形容詞", deck_name):
        return WordType.naAdj
    if re.search("五段動詞", deck_name):
        return WordType.godanVerb
    if re.search("一段動詞", deck_name):
        return WordType.ichidanVerb

all_adj_temp = findCardByDeckModel(SearchModelType.adj_temp)
all_verb_temp = findCardByDeckModel(SearchModelType.verb_temp)
all_kanji_temp = findCardByDeckModel(SearchModelType.kanji_temp)
all_words = all_adj_temp + all_verb_temp

reverse_JDIC_words =[]
i = 0
totalWords = len(all_words)
startTime = time()
estimatedRemainingTime = 0
if load_from_cache:
    cachedBestHit = load_secure_pickle(rev_word_cache)
else:
    cachedBestHit = {}
for note_id in all_words:
    i += 1
    note = anki_col.get_note(note_id) 
    deck_name = anki_col.decks.get(note.cards()[0].current_deck_id())["name"]
    note_type = getDeckType(deck_name)
    w = re.sub(r"(\(.*\)|\[.*\])|\&nbsp|\<[^\<]+\>|;", "", note.fields[1])
    old_def = note.fields[0]
    estHours = int(estimatedRemainingTime/3600)
    estMinutes = int(estimatedRemainingTime/60)%60
    estSeconds = int(estimatedRemainingTime%60)
    estString = str(estHours).zfill(2) + ":" + str(estMinutes).zfill(2) + ":" + str(estSeconds).zfill(2)
    if old_def in cachedBestHit.keys():
        print("(cache) rev. WWWJDIC  " + w.ljust(10) + "\t("+ str(i) + "/" + str(totalWords) +" - " + "{:.2f}".format((i/totalWords)*100.) + "% - ERA: "+ estString + ")")
        note.fields[0] = cachedBestHit[old_def]
        continue
    
    # Multipass until NoMoreHits
    prerenderedSoup = None
    revJDICs = []
    excludedIDs = []
    print("reverse WWWJDIC-ing  " + w.ljust(10) + "\t("+ str(i) + "/" + str(totalWords) +" - " + "{:.2f}".format((i/totalWords)*100.) + "% - ERA: "+ estString + ")")
    while True:
        try:
            newRevJDIC = WWWJDIC(w, soundfolder, prerenderedSoup, excludedIDs)
            revJDICs.append(newRevJDIC)
            excludedIDs.append(newRevJDIC.labelID)
            prerenderedSoup = newRevJDIC.allsoup
        except NoMoreHits:
            break
        except NoHits:
            noHitsWriteLog(logfile, w)
            break
        except KanjiSljfaqNoResponse:
            kanjiSljfaqNotRespondingWriteLog(logfile, w)
            break
        except FileNotFoundError:
            raise
    bestHit = [None, 0.]
    for revJDIC in revJDICs:
        for hit in revJDIC.clean_definitions:
            if hit.wordtype != WordType.dunno and hit.wordtype != note_type:
                continue
            score = SequenceMatcher(None, hit.definition, old_def).ratio()
            if score > bestHit[1]:
                bestHit = [hit.definition, score]
    if bestHit[0] != None:
        note.fields[0] = bestHit[0]
        cachedBestHit[old_def] = bestHit[0]
    save_secure_pickle(cachedBestHit, rev_word_cache)
    totalRuntime = time() - startTime
    cached_items = int(load_from_cache) * len(cachedBestHit)
    estimatedRemainingTime = (totalRuntime/i)*(totalWords - i - cached_items)

#anki_col.autosave()
    
    

