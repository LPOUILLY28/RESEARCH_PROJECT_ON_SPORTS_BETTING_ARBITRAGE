from pprint import pprint
from tipe_scraper import *
from tipe_filter import *
from tipe_save import *
from tipe_parser import *
from tipe_estimation import *
from config import atp_url
import json
import random


joueurs = read_json("save.json")

matches = read_json('save_matches.json')

odds = read_json('save_odds.json')


def find_match():
    cle = random.choice(list(matches.keys()))
    return matches[cle]


def surface(dico):
    hard = 0
    grass = 0
    clay = 0
    for x in dico.values() :
        if x["Preferred Surface"] == "Hard" :
            hard += 1
        if x["Preferred Surface"] == "Grass" :
            grass += 1
        if x["Preferred Surface"] == "Clay" :
            clay += 1
    return hard,grass,clay


def test_coherence_estim_proba():
    i = 0
    total = 0
    for match in matches.values():
        total += 1
        if estim_proba(match)[0] < estim_proba(match)[1] and match["Odds Player 1"] > match["Odds Player 2"]:
            i += 1
        elif estim_proba(match)[0] > estim_proba(match)[1] and match["Odds Player 1"] < match["Odds Player 2"]:
            i += 1
    return (100*i/total,total,i)


def nb_joueurs():
    L = []
    for match in matches.values():
        if (match["Player 1"] in joueurs) and not (match["Player 1"] in L):
            L.append(match["Player 1"])
        if (match["Player 2"]) in joueurs and not (match["Player 2"] in L):
            L.append(match["Player 2"])
    return L, len(L)
print(nb_joueurs())

def liste_arbitrage():
    arbitrage = []
    for match in odds.values():
        cote_joueur1 = []
        cote_joueur2 = []
        for site in match.values():
            cote_joueur1.append(site["Odds Player 1"])
            cote_joueur2.append(site["Odds Player 2"])
        cote_max = (max(cote_joueur1),max(cote_joueur2))
        arbitrage.append(1/cote_max[0] + 1/cote_max[1] - 1)
    return arbitrage