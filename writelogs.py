from datetime import datetime

def noHitsWriteLog(logfile: str, word: str) -> None:
    print("/!\\ " + word + " could not be found AT ALL... /!\\")
    prefix = datetime.now().strftime("[%d/%m/%Y-%H:%M:%S] - noHitsAtAll - ")
    with open(logfile, 'a', encoding="utf-8") as lf:
        lf.write(prefix + word + "\n")

def kanjiSljfaqNotRespondingWriteLog(logfile: str, word: str) -> None:
    print("/!\\ KanjiSljfaq is not responding for" + word + " /!\\")
    prefix = datetime.now().strftime("[%d/%m/%Y-%H:%M:%S] - KanjiSljfaqNoResponse - ")
    with open(logfile, 'a', encoding="utf-8") as lf:
        lf.write(prefix + word + "\n")