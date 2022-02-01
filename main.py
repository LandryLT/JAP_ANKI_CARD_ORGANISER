from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
import ssl
from KanjiSljfaq import KanjiSljfaq
from WWWJDIC import WWWJDIC

# Create unprotected SSL context /!\
ssl._create_default_https_context = ssl._create_unverified_context

# Initiate Selenium browser
webservice = Service(GeckoDriverManager().install())
browser_options = FirefoxOptions()
browser_options.headless = True
browser = Firefox(service=webservice, options=browser_options )

word = '新婦'
# list_kan = []
# for c in word:
#     list_kan.append(c)
# newKan = KanjiSljfaq(list_kan)

word_def = WWWJDIC(browser, word, "./.sounds/")

# Print stuff
# print(word_def.sound_file)
# print(word_def.jap_sentence)
# print(word_def.eng_sentence)
browser.quit()

