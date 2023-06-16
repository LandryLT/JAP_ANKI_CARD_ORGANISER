from JAP_ANKI_CARD_ORGANISER_const import *

JDIC_words = []
if load_from_cache:
    #Load from cache
    JDIC_words = load_secure_pickle(word_cache)
    #Print loaded
    print("Loading " + str(len(JDIC_words)) + " WWWJDIC from cache:")
    for word in JDIC_words[:-1]:
        for c in word.clean_definitions:        
            stdout.write(c.word)
        stdout.write(", ")
    for c in JDIC_words[-1:][0].kanjis:
        stdout.write(c)
    stdout.write("\n\n")
else:
    # Import words to add
    words_to_add = []
    try:
        with open(vocabfile, 'r', encoding='utf-8') as f:
            for w in f.read().splitlines():
                # Python style comment out
                if w[0] != '#':
                    words_to_add.append(w)
    except FileNotFoundError:
        raise

    # WWWJDIC the words to add
    for w in words_to_add:
        print("WWWJDIC-ing " + w)
        excludedIDs = []
        prerenderedSoup = None
        # Multipass until NoMoreHits
        while True:
            try:
                newJDIC = WWWJDIC(w, soundfolder, prerenderedSoup, excludedIDs)
                JDIC_words.append(newJDIC)
                excludedIDs.append(newJDIC.labelID)
                prerenderedSoup = newJDIC.allsoup
            except NoMoreHits:
                break
            except NoHits:
                noHitsWriteLog(logfile, w)
                break
            except FileNotFoundError:
                raise
    save_secure_pickle(JDIC_words, word_cache)

NewKanjiCards = []
if load_from_cache:
    #Load from cache
    NewKanjiCards = load_secure_pickle(kanji_cache)
    #Print loaded
    print("Loading " + str(len(NewKanjiCards)) + " Kanjis from cache:")
    for kanji in NewKanjiCards[:-1]:
        for c in kanji.kanji:        
            stdout.write(c)
        stdout.write(", ")
    for c in NewKanjiCards[-1:][0].kanji:
        stdout.write(c)
    stdout.write("\n\n")
else:
    # Make new Kanji Card   
    existing_kanjis = get_existing_kanji_list(anki_col)
    for k in get_new_kanjis(existing_kanjis, JDIC_words):
        print("new Kanji: " + k + " !")
        NewKanjiCards.append(NewKanji(k))
    save_secure_pickle(NewKanjiCards, kanji_cache)


mkdeck = DeckBuilder(anki_col)
# Import Kanjis in Anki
for kjc in NewKanjiCards:
    if type(kjc) is not NewKanji:
        raise TypeError

    print("Importing " + kjc.kanji + " in Anki")
    mkdeck.make_ankiKanjiNote(kjc)

# Import Vocab in Anki
for jwrd in JDIC_words:
    if type(jwrd) is not WWWJDIC:
        raise TypeError

    for nc in jwrd.clean_definitions:
        print("Importing " + nc.word + " (" + str(nc.wordtype).replace("WordType.", "") + ") in Anki")
        mkdeck.make_ankiNote(nc)

# Save all and finish !
print("All done :)")
if saveall:
    mkdeck.saveall()