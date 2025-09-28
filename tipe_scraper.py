from bs4 import BeautifulSoup
from selenium import webdriver
import time


def scrape_personal_details(datas: BeautifulSoup) -> dict:
    hands = {"Plays": datas.find('span', text='Plays').find_next_sibling('span').text}
    return hands


def scrape_atp_player_stats(datas: BeautifulSoup) -> dict:
    player_stats = {
        'YTD': {},
        'Career': {}
    }

    all_stats_details = datas.find_all('div', class_='player-stats-details')

    for stat_detail in all_stats_details:
        type_stat = stat_detail.find('div', class_='type').text.strip()

        rank = stat_detail.find('div', class_='stat').text
        w_l = stat_detail.find('div', class_='wins').text
        titles = stat_detail.find('div', class_='titles').text

        stats = {
            'Wins': int(w_l.split()[0]),
            'Loses': int(w_l.split()[2]),
            'Rank': int(rank.split()[0]),
            'Titles': int(titles.split()[0])
        }

        if type_stat == 'YTD':
            player_stats['YTD'].update(stats)
        elif type_stat == 'Career':
            player_stats['Career'].update(stats)

    return player_stats


def scrape_career_stats(datas: BeautifulSoup) -> dict:
    datas_extraites = {}

    stats = datas.find_all('li', class_='stats_items')

    for stat in stats:
        categorie = stat.find('span', class_='stats_record').text
        valeur = stat.find('span', class_='stats_percentage').text
        datas_extraites[categorie] = valeur

    return datas_extraites


def scrape_activity_stats(datas: BeautifulSoup) -> dict:
    hands = {}
    surface = {}

    table = datas.find('table')
    rows = table.find_all('tr')

    for row in rows:
        cells = row.find_all('th') + row.find_all('td')
        if cells[0].get_text(strip=True) in ['Clay', 'Grass', 'Hard']:
            career_index = cells[4].get_text(strip=True)
            surface[cells[0].get_text(strip=True)] = float(career_index)
        elif cells[0].get_text(strip=True) in ['vs. Right Handers*', 'vs. Left Handers*']:
            career_index = cells[4].get_text(strip=True)
            hands[cells[0].get_text(strip=True)] = float(career_index)

    return {"vs Hands": hands, "Surface": surface}


def scrape_atp(url: str) -> dict:
    driver = webdriver.Chrome()
    driver.get(f"https://www.atptour.com{url}overview")
    html_overview = driver.page_source
    driver.quit()

    driver = webdriver.Chrome()
    driver.get(f"https://www.atptour.com{url}player-stats?year=all&surface=all")
    html_stats = driver.page_source
    driver.quit()

    driver = webdriver.Chrome()
    driver.get(f"https://www.atptour.com{url}atp-win-loss?tourType=Tour")
    html_activity = driver.page_source
    driver.quit()

    soup1 = BeautifulSoup(html_overview, 'html.parser')
    soup2 = BeautifulSoup(html_stats, 'html.parser')
    soup3 = BeautifulSoup(html_activity, 'html.parser')

    atp_player_stats = soup1.find('div', class_='atp_player-stats')
    career_stats = soup2.find('div', class_='statistics_content')
    activity_stats = soup3.find('div', class_='atp_player-win_loss-index')
    infos = {}

    infos["Personnal Details"] = scrape_personal_details(soup1)
    infos["YTD&Career Player Stats"] = scrape_atp_player_stats(atp_player_stats) if atp_player_stats else 0
    infos["Career Stats"] = scrape_career_stats(career_stats) if career_stats else 0
    infos["Activity Stats"] = scrape_activity_stats(activity_stats) if activity_stats else 0

    return infos


def scrape_oddsportal(url: str, year: int, surface: str) -> dict:
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    html_oddsportal = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_oddsportal, 'html.parser')

    match_div = soup.find_all('div', class_='group flex')
    infos = {}

    for match in match_div:
        players = match.find_all('p', class_='participant-name')
        player1 = players[0].text.strip().split()
        player2 = players[1].text.strip().split()

        odds = match.find_all('p', class_='height-content')

        odds1 = float(odds[0].text.strip())
        odds2 = float(odds[1].text.strip())

        score_parts = match.find('div', class_='flex gap-1 font-bold font-bold')
        if score_parts:
            scores = score_parts.text.strip().split('–')
            score1 = scores[0].strip()
            score2 = scores[1].strip()
            infos[f"{year}{surface[0]}-{player1[0][:2]}{player2[0][:2]}{len(infos)}"] = {
                "Date": year,
                "Surface": surface,
                "Player 1": f"{player1[0]} {player1[-1]}",
                "Player 2": f"{player2[0]} {player2[-1]}",
                "Odds Player 1": float(odds1),
                "Odds Player 2": float(odds2),
                "Score Player 1": int(score1) if score1 != '' else '',
                "Score Player 2": int(score2) if score2 != '' else '',
            }
        else:
            continue

    return infos

def scrape_allodds(url: str) -> dict:
    driver = webdriver.Chrome()
    driver.get(url)
    html_allodds = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_allodds, 'html.parser')

    matches = soup.find_all('div', class_='border-black-borders flex h-9 border-b border-l border-r text-xs')
    infos = {}

    for match in matches:
        bookmaker_tag = match.find('p', class_='height-content')
        bookmaker = bookmaker_tag.text.strip()

        odds = match.find_all('p', class_='height-content')
        odds1 = float(odds[1].text.strip())
        odds2 = float(odds[2].text.strip())

        infos[bookmaker] = {'Odds Player 1': odds1, 'Odds Player 2': odds2}

    return infos