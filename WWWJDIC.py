import re
from bs4 import BeautifulSoup
<<<<<<< HEAD
import requests
import urllib.parse
import os.path

class WWWJDIC:
    def __init__(self, word: str, sound_download_dir: str) -> None:
        self.word = word
        self.allsoup = self.renderWWWJDIC()
        self.bestsoup = self.find_word_definition()
        self.jap_sentence, self.eng_sentence = self.get_sentence()
        self.sound_file = self.get_sound(sound_download_dir)
    

    # Render web page
    def renderWWWJDIC(self) -> BeautifulSoup:
        # Get WWWJDIC homepage
        url = 'https://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1E'
        request_body = {'dsrchkey': urllib.parse.quote(self.word.encode('utf-8')), 'dicsel': '1'}
        return BeautifulSoup(requests.post(url, request_body).content, 'html.parser')

=======
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import requests

class WWWJDIC:
    def __init__(self, brwsr: Firefox, word: str, sound_download_dir: str) -> None:
        self.word = word
        self.allsoup = self.renderWWWJDIC(brwsr)
        self.bestsoup = self.find_word_definition()
        self.jap_sentence, self.eng_sentence = self.get_sentence()
        self.sound_file = sound_download_dir + word + '.mp3'
        self.get_sound()
    
    # Render web page
    def renderWWWJDIC(self, b: Firefox) -> BeautifulSoup:
        # Get WWWJDIC homepage
        url = 'https://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1C'
        b.get(url)
        # Find form elements
        search_bar = b.find_element(By.NAME, 'dsrchkey')
        submit_button = b.find_element(By.XPATH, "//input[@type='submit']")
        # Fill and submit form
        search_bar.send_keys(self.word)
        submit_button.click()

        return BeautifulSoup(b.page_source, 'html.parser')
>>>>>>> 769a1c9e41757b517dcd5cfe82581806b25386ef

    # Get best guess of dict entry
    def find_word_definition(self) -> BeautifulSoup:
        # Get dic entries
        allheadwords_soup = self.allsoup.find("form", id="inp").find_all("div", style="clear: both;")
       
        # Strip headwords
        for e in allheadwords_soup:
            headword = e.find('label').find('font', size='+1').stripped_strings
            headword_str = ''
            for s in headword:
                headword_str = headword_str + s           
            
            # Regex just the kanji part
            headword_str = re.match(r'(?P<hdwrd>^.*)(【.*】|《.*》)', headword_str).group('hdwrd')
            hits = re.findall(r'[^;\s]+', headword_str)          
            
            # If matches exactly self.word
            for h in hits:
                if re.match(re.compile(h), self.word):
                    return e
            
<<<<<<< HEAD
        # Else raise error
        print(self.word + " could not be found in Jim Breen's WWWJDIC")
        raise


=======
            # Else raise error
            print(self.word + " could not be found in Jim Breen's WWWJDIC")
            raise
    
>>>>>>> 769a1c9e41757b517dcd5cfe82581806b25386ef
    # Get example sentence and translation
    def get_sentence(self) -> tuple:  
        
        br = self.bestsoup.find('br')
        
        # No sentences...
<<<<<<< HEAD
        if br is None:
=======
        if br is None or br.next_sibling.name == 'a':
>>>>>>> 769a1c9e41757b517dcd5cfe82581806b25386ef
            return (None, None)

        # Possible sentences !
        both_l = ''
        for s in br.next_sibling.contents[2:-2]:
            both_l = both_l + str(s)
        
        # Seperate Japanes and English
        both_l_re = re.match(r'(?P<jap>^.*)(\t)(?P<eng>.*$)', both_l)
        
        return (both_l_re.group('jap'), both_l_re.group('eng'))

<<<<<<< HEAD

    # Download sound if any
    def get_sound(self, dir: str):

        # Find query string 
        query_string = re.match(r'm\(\'(?P<tophp>.+)\'\)',self.bestsoup.find('script').text).group('tophp')
        
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
=======
    # Download sound if any
    def get_sound(self):
        
        # print(self.bestsoup.prettify())
        audio_player = self.bestsoup.find('audio')
        
        # No sound
        if audio_player is None:
            return None
        
        # Sound file !
        soundfile = requests.get(audio_player.find('source')['src'])
        with open(self.sound_file, 'wb') as f:
            f.write(soundfile.content)
>>>>>>> 769a1c9e41757b517dcd5cfe82581806b25386ef
