from pprint import pprint
from tipe_scraper import *
from tipe_filter import *
from tipe_save import *
from config import atp_url
from tipe_estimation import *
import random

matches = read_json("save_matches.json")

def find_match():
    cle = random.choice(list(matches.keys()))
    return matches[cle]


nb_match = 500


def risky(benefice):
    s0 = 1000
    S = s0
    liste_sommes = [S]
    while S > 0 and len(liste_sommes) < nb_match and S <= s0:
        match = find_match()
        odds = (match["Odds Player 1"], match["Odds Player 2"])
        M = (benefice + s0 - S)/ (max(odds) - 1)
        S -= M
        if odds[0] < odds[1] and match["Score Player 2"] > match["Score Player 1"]:
            S += M*odds[1]
        elif odds[0] > odds[1] and match["Score Player 1"] > match["Score Player 2"]:
            S += M*odds[0]
        liste_sommes.append(S)
    return liste_sommes



def all_on_favor(mise):
    S = 1000
    liste_sommes = [S]
    while S > 0 and len(liste_sommes) < nb_match:
        match = find_match()
        M = mise
        S -= M
        odds = (match["Odds Player 1"],match["Odds Player 2"])
        if odds[0] < odds[1] and match["Score Player 1"] > match["Score Player 2"]:
            S += M*odds[0]
        elif odds[0] > odds[1] and match["Score Player 1"] < match["Score Player 2"]:
            S += M*odds[1]
        liste_sommes.append(S)
    return liste_sommes


def fifty_fifty(mise):
    S = 1000
    liste_sommes = [S]
    while S > 0 and len(liste_sommes) < nb_match:
        match = find_match()
        M = mise
        S -= M
        odds = (match["Odds Player 1"],match["Odds Player 2"])
        if match["Score Player 1"] > match["Score Player 2"]:
            S += (M/2) * odds[0] 
        elif match["Score Player 1"] < match["Score Player 2"]:
            S += (M/2) * odds[1]
        liste_sommes.append(S)
    return liste_sommes


def depending_proba(mise):
    S = 1000
    liste_sommes = [S]
    while S > 0 and len(liste_sommes) < nb_match:
        match = find_match()
        M = mise
        S -= M
        proba = estim_proba(match)
        odds = (match["Odds Player 1"],match["Odds Player 2"])
        if match["Score Player 1"] > match["Score Player 2"]:
            S += odds[0]* M * proba[0]
        elif match["Score Player 1"] < match["Score Player 2"]:
            S += odds[1]* M * proba[1]
        liste_sommes.append(S)
    return liste_sommes