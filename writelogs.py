from datetime import datetime

def noHitsWriteLog(logfile: str, word: str) -> None:
    print("/!\\ " + word + " could not be found AT ALL... /!\\")
    prefix = datetime.now().strftime("[%d/%m/%Y-%H:%M:%S] - ")
    with open(logfile, 'a') as lf:
        lf.write(prefix + word + "\n")