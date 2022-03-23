from HitResult import *
from bs4 import BeautifulSoup
import requests
import urllib.parse
import os.path

class WWWJDIC:
    def __init__(self, word: str, sound_download_dir: str, rendered_soup= None, excludedIDs=[]) -> None:
        self.word = word
        
        # Allready rendered page
        self.allsoup = rendered_soup
        if self.allsoup is None:
            self.allsoup = self.renderWWWJDIC()
        
        self.bestsoup = self.find_word_definition(excludedIDs)
        self.labelID = self.get_ID()
        self.kana = self.get_kana()
        self.kanjis = self.get_kanjis()
        self.jap_sentence, self.eng_sentence = self.get_sentence()
        self.sound_file = self.get_sound(sound_download_dir)
        self.rough_def = self.get_rough_def()
        self.hits = self.get_hits()
    

    # Render web page
    def renderWWWJDIC(self) -> BeautifulSoup:
        # Get WWWJDIC homepage
        url = 'https://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1E'
        request_body = {'dsrchkey': urllib.parse.quote(self.word.encode('utf-8')), 'dicsel': '1'}
        return BeautifulSoup(requests.post(url, request_body).content, 'html.parser')

    # Get best guess of dict entry
    def find_word_definition(self, excludedIDs) -> BeautifulSoup:
        # Get dic entries
        allheadwords_soup = self.allsoup.find("form", id="inp").find_all("div", style="clear: both;")

        # Strip headwords
        for e in allheadwords_soup:
            
            # Allready done in previous WWWJDIC search
# MUST TEST !!!!!!!!!!!!!
            labelID = e.find('input')['id']
            if labelID in excludedIDs:
                continue
# MUST TEST !!!!!!!!!

            headword = e.find('label').find('font', size='+1').stripped_strings
            headword_str = ''
            for s in headword:
                headword_str = headword_str + s           
            
            # Regex just the kanji part
            reg_pattern = r'(?P<hdwrd>^.*)(【.*】|《(?P<kanjiopt>.*)》||\(P\))'
            hdwrd = re.match(reg_pattern, headword_str).group('hdwrd')
            extra_kanji = re.match(reg_pattern, headword_str).group('kanjiopt')
            if extra_kanji is not None:
                hdwrd += '; ' + extra_kanji
            hits = re.findall(r'[^;\s\(P\)]+', hdwrd)          
            
            # If matches exactly self.word
            for h in hits:
                if re.match(re.compile(h), self.word):
                    return e
            
        # Else raise exception
        if len(excludedIDs) == 0:
            raise NoHits(self.word)
        else:
            raise NoMoreHits(self.word)


    # Get example sentence and translation
    def get_sentence(self) -> tuple:  
        
        br = self.bestsoup.find('br')
        # No sentences ...
        if br is None:
            return(None,None)

        # Possible sentences !
        both_l = ''
        for s in br.next_sibling.contents[2:-2]:
            both_l = both_l + str(s)
        
        # Seperate Japanese and English
        both_l_re = re.match(r'(?P<jap>^.*)(\t)(?P<eng>.*$)', both_l)
        if both_l_re is None:
            return (None, None)
        
        return (both_l_re.group('jap'), both_l_re.group('eng'))


    # Download sound if any
    def get_sound(self, dir: str) -> str:

        # Find query string 
        query_string = re.match(r'm\(\'(?P<qstring>.+)\'\)',self.bestsoup.find('script').text).group('qstring')
        
        # No sound
        if query_string is None:
            return None
        
        # Sound file !
        audiofile_request = 'http://assets.languagepod101.com/dictionary/japanese/audiomp3.php?' + query_string

        # Make file path
        soundfile = requests.get(audiofile_request)
        soundfile_path = dir + self.word + '.mp3'
        inc = 1
        while os.path.isfile(soundfile_path):
            soundfile_path = dir + self.word + '_' + str(inc) + '.mp3'
            inc+=1

        # Write sound file
        with open(soundfile_path, 'wb') as f:
            f.write(soundfile.content)
        
        return soundfile_path


    # Get kana
    def get_kana(self) -> str:
        kana_url = re.search(r'm\(\'kana=(?P<kana>[^&]+)(\&kanji=.*)?\'\)', self.bestsoup.find('script').text).group('kana')
        kana = urllib.parse.unquote(kana_url)
        if kana == self.word:
            kana = None
        return kana


    # Get a list of the Kanjis
    def get_kanjis(self):
        output = []
        for r in re.findall(r'[一-龯]', self.word):
            output.append(r)
        return output

    # Get unique LabelID
    def get_ID(self) -> str:
        return self.bestsoup.find('input')['id']

    def get_rough_def(self) -> str:
        # Sometimes <a> muck it up (stops to first sibling)
        bestsoup_def = self.bestsoup.find('label').find('font').next_sibling
        bestsou_def_str = ''
        while bestsoup_def is not None:
            bestsou_def_str += str(bestsoup_def.string)
            bestsoup_def = bestsoup_def.next_sibling
        
        return bestsou_def_str


    # Gets definitions and corresponding wordtypes (Hits)
    def get_hits(self) -> list:
        # Get all rough definitions with "(wordtype) definition" format 
        found_defs = []        
        for r in re.finditer(final_regex, self.rough_def):
            for t in r.groupdict():
                if r[t] is not None:
                    found_defs.append(r[t])

        # Seperate into different wordtypes
        wordtype_def = {'noun': '', 'godan': '', 'ichidan': '', 'naAdj': '', 'iAdj': ''}
        for d in found_defs:
            for k in wordtypes_regex:
                wordtype = re.match(wordtypes_regex[k], d)
                if wordtype is not None:
                    wordtype_def[k] += re.sub(wordtypes_regex[k], "", d)
        
        # Transform into hits
        hits = []
        for wt in wordtype_def:
            d = wordtype_def[wt] 
            if len(d) > 0:
                if wt == 'noun':
                    hits.append(HitResult(WordType.noun, d))
                elif wt == 'naAdj':
                    hits.append(HitResult(WordType.naAdj, d))
                elif wt == 'iAdj':
                    hits.append(HitResult(WordType.iAdj, d))
                elif wt == 'godan':
                    hits.append(HitResult(WordType.godanVerb, d))
                elif wt == 'ichidan':
                    hits.append(HitResult(WordType.ichidanVerb, d))
        
        return hits
