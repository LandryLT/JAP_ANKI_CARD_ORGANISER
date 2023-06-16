from difflib import SequenceMatcher
from JAP_ANKI_CARD_ORGANISER_const import *
from HitResult import *
from time import time, sleep

class SearchModelType(Enum):
    adj_temp = "Jap. Adjectives Template"
    verb_temp = "Jap. Verbs Template"
    verb_conj_temp = "Japanese Verb Conjugation"
    kanji_temp = "Kanji Card"
    JLPT_temp = "MonoField"
    duolinguo_temp = "Duolinguo tips"

def findCardByDeckModel(deck_model, word=""):
    try:
        if type(deck_model) not in (tuple, list):
            if type(deck_model) is not SearchModelType:
                raise TypeError
            if word != "":
                word = " JapDicFormKanji:_*"+ word + "*"
            return list(anki_col.find_notes('"note:'+ deck_model.value +'"' + word))
    except TypeError:
        raise


def getDeckType(deck_name):
    if re.search("名詞と他", deck_name) or re.search("オノマトピア", deck_name):
        return WordType.noun
    if re.search("イ形容詞", deck_name):
        return WordType.iAdj
    if re.search("ナ形容詞", deck_name):
        return WordType.naAdj
    if re.search("五段動詞", deck_name):
        return WordType.godanVerb
    if re.search("一段動詞", deck_name):
        return WordType.ichidanVerb

# Import words to add
words_to_update = []
try:
    with open(updatevocabfile, 'r', encoding='utf-8') as f:
        for w in f.read().splitlines():
            # Python style comment out
            if w[0] != '#':
                words_to_update.append(w)
except FileNotFoundError:
    raise

all_words = []
if len(words_to_update) == 0:
    print("No words in words2update.txt: Update wholde database ? (y|n)")
    response = input()
    if (not re.match(r'^y(es)?$', response, re.IGNORECASE)):
        print("aborting...goodbye !")
        quit()
    all_adj_temp = findCardByDeckModel(SearchModelType.adj_temp)
    all_verb_temp = findCardByDeckModel(SearchModelType.verb_temp)
    all_words = all_adj_temp + all_verb_temp
else :
    for w in words_to_update:
        all_adj_temp = findCardByDeckModel(SearchModelType.adj_temp, w)
        all_verb_temp = findCardByDeckModel(SearchModelType.verb_temp, w)
        all_words += all_adj_temp + all_verb_temp

update_JDIC_words =[]
totalWords = len(all_words)
lastTime = time()
twentyLastTimes = []
estimatedRemainingTime = 0
if load_from_cache:
    cachedBestHit = load_secure_pickle(update_word_cache)
else:
    cachedBestHit = {}

ind = 0
for note_id in all_words:
    ind += 1
    cache_len = len(cachedBestHit) 
    note = anki_col.get_note(note_id) 
    deck_name = anki_col.decks.get(note.cards()[0].current_deck_id())["name"]
    note_type = getDeckType(deck_name)
    if note_type == None:
        continue
    w = re.sub(r"(\(.*\)|\[.*\])|\&nbsp|\<[^\<]+\>|;", "", note.fields[1])
    old_def = note.fields[0]
    estHours = int(estimatedRemainingTime/3600)
    estMinutes = int(estimatedRemainingTime/60)%60
    estSeconds = int(estimatedRemainingTime%60)
    estString = str(estHours).zfill(2) + ":" + str(estMinutes).zfill(2) + ":" + str(estSeconds).zfill(2)
    if old_def in cachedBestHit.keys():
        print("(cache) upd. WWWJDIC  " + w.ljust(10) + "\t("+ str(ind) + "/" + str(totalWords) +" - " + "{:.2f}".format((ind/totalWords)*100.) + "% - ERA: "+ estString + ")")
        note.fields[0] = cachedBestHit[old_def]
        note.flush()
        continue
    
    emptySoupAttempts = 0

    # Multipass until NoMoreHits
    prerenderedSoup = None
    updatesWWWJDICs = []
    excludedIDs = []
    print("update WWWJDIC  " + w.ljust(10) + "\t("+ str(ind) + "/" + str(totalWords) +" - " + "{:.2f}".format((ind/totalWords)*100.) + "% - ERA: "+ estString + ")")
    while True:
        try:
            aNewUpdatedWWWJDIC = WWWJDIC(w, soundfolder, prerenderedSoup, excludedIDs)
            updatesWWWJDICs.append(aNewUpdatedWWWJDIC)
            excludedIDs.append(aNewUpdatedWWWJDIC.labelID)
            prerenderedSoup = aNewUpdatedWWWJDIC.allsoup
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
        except EmptySoup:
            emptySoupAttempts += 1
            if emptySoupAttempts > 15:
                raise
            print("Reloading " + w + "... waiting " + str(emptySoupAttempts) + "s...")
            sleep(emptySoupAttempts)
    bestHit = [None, 0.]
    for revJDIC in updatesWWWJDICs:
        for hit in revJDIC.clean_definitions:
            if hit.wordtype != WordType.dunno and hit.wordtype != note_type:
                continue
            score = SequenceMatcher(None, hit.definition, old_def).ratio()
            if score > bestHit[1]:
                bestHit = [hit.definition, score]
    if bestHit[0] != None:
        note.fields[0] = bestHit[0]
        note.flush()
        cachedBestHit[old_def] = bestHit[0]
    save_secure_pickle(cachedBestHit, update_word_cache)
    #Progress bar
    timeDiff = time() - lastTime
    lastTime = time()
    twentyLastTimes.append(timeDiff)
    if len(twentyLastTimes) > 20:
        twentyLastTimes = twentyLastTimes[:-20]
    twentyLastTimes.sort()
    estimatedRemainingTime = (twentyLastTimes[int((len(twentyLastTimes)-1)/2)])*(totalWords - ind)
if saveall:
    anki_col.autosave()
    

    
    

