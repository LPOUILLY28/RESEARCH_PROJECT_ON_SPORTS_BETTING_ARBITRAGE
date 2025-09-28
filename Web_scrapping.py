# https://pythonbasics.org/selenium-get-html/
# https://www.selenium.dev/documentation/webdriver/getting_started/first_script/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://stackoverflow.com/questions/57395509/get-item-from-bs4-element-tag
# https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
# chatgpt

from selenium import webdriver
from bs4 import BeautifulSoup
"""
Crawling & scraping des pages joueurs ATPTour pour le TIPE du plus grand bg de Versailles.

Sources:
# https://pythonbasics.org/selenium-get-html/
# https://www.selenium.dev/documentation/webdriver/getting_started/first_script/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://stackoverflow.com/questions/57395509/get-item-from-bs4-element-tag
# https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
# chatgpt

"""


# init du driver selenium avec browser chrome
driver = webdriver.Chrome()
driver.get("https://www.atptour.com/en/players/Jakub-Mensik/M0NI/overview")
html = driver.page_source # extraction du code source html (à défaut de parser sur page ouverte avec xpaths)
driver.quit()

# vu que le code html est une "nested data structure", on itinialise un obj bs pour l'analyser
soup = BeautifulSoup(html, 'html.parser')

# de ce bordel on extrait la section du conteneur de classe personaldetaild
personal_details = soup.find('div', class_='personal_details')
infos = {}

if personal_details:
    # on cherche les éléments de listes (li de ul) dans le padding left et right (les deux colonnes)
    details_left = personal_details.find('ul', class_='pd_left').find_all('li')
    details_right = personal_details.find('ul', class_='pd_right').find_all('li')

    # pour mieux itérer dessus
    details = details_left + details_right

    print(details) # debug
    print(type(details))

    # on parcourt chaque élément (type <li><span>Age</span><span>18 (2005.09.01)</span></li>)
    # nb : details est une LISTE d'objets bs4 (detail), donc on hérite des méthodes de la classe
    for detail in details:
        categorie = detail.find('span').text  # sélectionne le PREMIER conteneur span, et associe la attribut text de l'objet à categorie
        valeur = detail.find_all('span')[1].text  # de même mais find_all nous sort une liste de conteneurs, on veux le second avec la valeur
        infos[categorie] = valeur

    print(infos)
else:
    print("Aucune info trouvée.")
    
    
###############################################################################
from selenium import webdriver
from pprint import pprint
from tipe_scraper import *

URL : str = "https://www.atptour.com/en/players/Jakub-Mensik/M0NI/"


driver = webdriver.Chrome() # init du driver selenium avec browser chrome
driver.get(f"{URL}overview")
html_overview = driver.page_source # extraction du code source html (à défaut de parser sur page ouverte avec xpaths)
driver.quit()

# on prend un nouveau driver pour éviter la sécurité de cloudflare (moins rapide mais bon)
driver = webdriver.Chrome()
driver.get(f"{URL}player-stats?year=all&surface=all")
html_stats = driver.page_source # extraction du code source html (à défaut de parser sur page ouverte avec xpaths)
driver.quit()

sauvegarde(html_overview, "html_extrait1") # debug
sauvegarde(html_stats, "html_extrait2") # debug

# SI JAMAIS TU VEUX EVITER DE FAIRE 10000 REQUETES ET TRAITER EN LOCAL, METS CE QUI A AU DESSUS
# EN COMMENTAIRES (à partir de driver)
# html_overview = lire_html("html_extrait1")
# html_stats = lire_html("html_extrait2")


# vu que le code html est une "nested data structure", on itinialise un obj bs pour l'analyser
soup1 = BeautifulSoup(html_overview, 'html.parser')
soup2 = BeautifulSoup(html_stats, 'html.parser')

# de ce bordel on extrait la section du conteneur de classe personaldetaild
personal_details = soup1.find('div', class_='personal_details')
atp_player_stats = soup1.find('div', class_='atp_player-stats')
career_stats = soup2.find('div', class_='statistics_content')
infos = {}

infos["Personnal Details"] = scrape_personal_details(personal_details) if personal_details else 0
infos["YTD Player Stats"] = scrape_atp_player_stats(atp_player_stats) if atp_player_stats else 0
infos["Career Stats"] = scrape_career_stats(career_stats) if career_stats else 0

pprint(infos)



def scrape_personal_details(datas: BeautifulSoup) -> set :
    datas_extraites = {}

    # on cherche les éléments de listes (li de ul) dans le padding left et right (les deux colonnes)
    details_left = datas.find('ul', class_='pd_left').find_all('li')
    details_right = datas.find('ul', class_='pd_right').find_all('li')

    # pour mieux itérer dessus
    details = details_left + details_right

    # on parcourt chaque élément (type <li><span>Age</span><span>18 (2005.09.01)</span></li>)
    # nb : details est une LISTE d'objets bs4 (detail), donc on hérite des méthodes de la classe
    for detail in details:
        categorie = detail.find('span').text  # sélectionne le PREMIER conteneur span, et associe la attribut text de l'objet à categorie
        valeur = detail.find_all('span')[1].text  # de même mais find_all nous sort une liste de conteneurs, on veux le second avec la valeur
        datas_extraites[categorie] = valeur

    return datas_extraites

def scrape_atp_player_stats(datas: BeautifulSoup) -> set :
    ytd_stats = {}

    rank = datas.find('div', class_='stat').text
    w_l = datas.find('div', class_='wins').text
    titles = datas.find('div', class_='titles').text

    # mise en forme
    # ytd_stats['W-L'] = w_l[:-4]
    ytd_stats['Wins'] = int(w_l.split()[0])
    ytd_stats['Loses'] = int(w_l.split()[2])
    ytd_stats['Rank'] = int(rank.split()[0])
    ytd_stats['Titles'] = int(titles.split()[0])

    return ytd_stats

def scrape_career_stats(datas: BeautifulSoup) -> set :
    datas_extraites = {}

    stats = datas.find_all('li', class_='stats_items')

    for stat in stats:
        categorie = stat.find('span', class_='stats_record').text
        valeur = stat.find('span', class_='stats_percentage').text
        datas_extraites[categorie] = valeur

    return datas_extraites


# POUR MOI : --------

def sauvegarde(html : str, nom_fichier : str) -> None :
    """
        car prudence est mêre de sûreté (et pour potentiellement faire des logs)
    """
    with open(nom_fichier, "w") as fichier :
        for ligne in html :
            fichier.write(ligne)

def lire_html(nom_fichier : str) -> str:
    html = ""
    with open(nom_fichier, "r") as fichier:
        html = fichier.read()
    return html


# matrice de joueurs 

M =[]

def ajout_joueur(M):
#programme ajoutant un 0 sur chaque ligne de M + une ligne de 0 pour garder le, format carré de la matrice
    n =len(M)
    for ligne in M:
        ligne.append(0)
    nouvelle_ligne = [0]*(n+1)
    M.append(nouvelle_ligne)
    return M

M_modif = ajout_joueur(M)

print(ajout_joueur(M_modif))

def afficher_resultat_match(joueur1, joueur2, scores):
    for i in range(len(scores)):
        set_score = scores[i]
        print(f"Set {i+1}: {joueur1} {set_score[0]} - {joueur2} {set_score[1]}") # permet d'inserer des variables à l'intérieur d'une chaine de caractère
        

# Exemple d'utilisation
joueur1 = "Joueur 1"
joueur2 = "Joueur 2"

# Scores connus pour un match en 3 sets
scores = [
    [6, 4],  # Set 1: Joueur 1 6 - Joueur 2 4
    [3, 6],  # Set 2: Joueur 1 3 - Joueur 2 6
    [7, 5]   # Set 3: Joueur 1 7 - Joueur 2 5
]

afficher_resultat_match(joueur1, joueur2, scores)

# Fonction pour trouver l'indice d'un joueur dans la liste des joueurs
def trouver_indice(liste, element):
     for i in range(len(liste)):
         if liste[i] == element:
             return i
     return -1  # Retourne -1 si l'élément n'est pas trouvé

def resultat_match_tennis(joueurs, scores):
    n = len(joueurs)
    M = [[0] * n for _ in range(n)]
    for match in scores:
        joueur1, joueur2, sets = match
        # Calculer les scores totaux pour chaque joueur sans utiliser sum
        score_joueur1 = 0
        score_joueur2 = 0
        for set_score in sets:
            score_joueur1 += set_score[0]
            score_joueur2 += set_score[1]
        resultat = score_joueur1 - score_joueur2
        i = trouver_indice(joueurs, joueur1)
        j = trouver_indice(joueurs, joueur2)
        if i != -1 and j != -1: #les joueurs sont bien dans la liste 
            M[i][j] = resultat
            M[j][i] = -resultat
    return M

# Exemple d'utilisation
joueurs = ["Joueur 1", "Joueur 2", "Joueur 3"]

# Scores connus: chaque entrée est (joueur1, joueur2, [(set1_score_joueur1, set1_score_joueur2), ...])
scores = [
    ("Joueur 1", "Joueur 2", [(6, 1), (6, 2), (6, 3)]),
    ("Joueur 1", "Joueur 3", [(6, 4), (7, 5), (6,2)]),
    ("Joueur 2", "Joueur 3", [(4, 6), (2, 6),(1,6)])
]

resultat_match_tennis(joueurs, scores)

# Afficher la matrice de résultats
#for ligne in matrice_resultats:
#    print(ligne)
