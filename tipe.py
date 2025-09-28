"""


Sources:
# https://pythonbasics.org/selenium-get-html/
# https://www.selenium.dev/documentation/webdriver/getting_started/first_script/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://stackoverflow.com/questions/57395509/get-item-from-bs4-element-tag
# https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class

"""

from pprint import pprint
from tipe_scraper import *
from tipe_filter import *
from tipe_save import *
from config import *
from tipe_parser import *

# COMPTER JOUEURS DIFFERENTS DANS DONNEES

matches_dict = read_json('save_matches.json')
lst = []
for match in matches_dict:
    if matches_dict[match]["Player 1"] not in lst:
        lst.append(matches_dict[match]["Player 1"])
    if matches_dict[match]["Player 2"] not in lst:
        lst.append(matches_dict[match]["Player 2"])
print(len(lst))


# SCRAPE URLS MEILLEURS JOUEURS ATP

driver = webdriver.Chrome()
driver.get("https://www.atptour.com/en/rankings/singles?RankRange=201-300&Region=all&DateWeek=2022-03-21")
time.sleep(0.5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # va tout en bas du doc
time.sleep(1)
html_save = driver.page_source # prend code source 
driver.quit()

soup = BeautifulSoup(html_save, 'html.parser')
player_urls = {}

lower_rows = soup.find_all('tr', class_='lower-row')

for row in lower_rows:
    name_item = row.find('li', class_='name')
    if name_item:
        a_tag = name_item.find('a')
        if a_tag and 'href' in a_tag.attrs:
            player_name = a_tag.text.strip()
            player_url = a_tag['href']
            player_urls[player_name] = player_url

print(player_urls)
for p in player_urls.values(): print(p)


# QUANTIFIER LA SAUSAGE PARTY

dict = {}
lst = []
lst2 = []
players_dict = read_json()
matches_dict = read_json('save_matches.json')
for match in matches_dict:
    if matches_dict[match]["Player 1"] not in players_dict:
        nom_j1=matches_dict[match]["Player 1"]
        if nom_j1 not in dict:
            dict[nom_j1]=1
        else :
            dict[nom_j1] += 1
        if match not in lst : lst.append(match)
    if matches_dict[match]["Player 2"] not in players_dict:
        nom_j2=matches_dict[match]["Player 2"]
        if nom_j2 not in dict:
            dict[nom_j2]=1
        else :
            dict[nom_j2] += 1
        if match not in lst: lst.append(match)

print(sum(dict.values()))
print(len(dict))
pprint(dict)
print(lst)
print(len(lst))


# SUPPRIMER MATCHS UNITILISABLES (stats joueurs non scrappées)

print(len(matches_dict))
for key in lst:
    matches_dict.pop(key, None)
print(len(matches_dict))
save_json(matches_dict, True, 'save_matches.json')


# EXEMPLE D'UTILISATION

# Seulement le dernier match de Djoko sur terre battue
djoko = get_match("Djokovic N.", "Clay", True)
pprint(djoko)

# Ses matchs sur terre battue et dur
djoko = get_match("Djokovic N.", ("Clay", "Hard"))
pprint(djoko)

# Tous les matchs
djoko = get_match("Djokovic N.")
pprint(djoko)

# Pour avoir le dico des joueurs
players_dict = read_json()

# De même avec les matchs
matches_dict = read_json('save_matches.json')


# ODDPORTAL SCRAPE MATCHES

for year in oddsportal_url_hard:
    for URL in oddsportal_url_hard[year]:
        try:
            infos = scrape_oddsportal(URL, year, "Hard")
            # pprint(infos) # debug
            save_json(infos, False, 'save_matches.json')
        except Exception as e:
            continue


# ATPTOUR SCRAPE PLAYERS

for URL in atp_url:
    name_filtered = player_name(URL)

    log_player_status(name_filtered)

    if is_player_in_json(name_filtered):
        log_player_status(name_filtered, "ok (already scraped)")

    else:
        try:
            infos_raw = scrape_atp(URL)
            infos_filtered = {name_filtered: filter_player(infos_raw)}
            # pprint(infos_filtered) # debug
            save_json(infos_filtered)

            log_player_status(name_filtered, "ok (written)")

        except Exception as e:
            log_player_status(name_filtered, f'error ({e})')
            continue


# SCRAPE ALL ODDS

driver = webdriver.Chrome()
driver.get("https://www.oddsportal.com/tennis/france/atp-french-open/results/#/page/2/")
time.sleep(0.5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
html_odds = driver.page_source
driver.quit()

url_matches = []
soup = BeautifulSoup(html_odds, 'html.parser')

group_flex_divs = soup.find_all('div', class_='group flex')

for index, div in enumerate(group_flex_divs):
    a_tag = div.find('a', class_='next-m:flex next-m:!mt-0 ml-2 mt-2 min-h-[32px] w-full hover:cursor-pointer')
    if a_tag:
        match_url = a_tag.get('href')
        url_matches.append(match_url)

print(url_matches)

odds = read_json('save_odds.json')

for URL in url_matches:
    id = URL[-9:-1]
    if id not in odds.keys():
        odds[id] = scrape_allodds(f"https://www.oddsportal.com{URL}")
        save_json(odds, False, 'save_odds.json')
# pprint(odds)

