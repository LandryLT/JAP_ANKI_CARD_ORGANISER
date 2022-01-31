from bs4 import BeautifulSoup
from KanjiSljfaq import KanjiSljfaq
import ssl

# Create SSL certificate
ssl._create_default_https_context = ssl._create_unverified_context

test_kan = '一生懸命'
list_kan = []
for c in test_kan:
    list_kan.append(c)
newKan = KanjiSljfaq(list_kan)