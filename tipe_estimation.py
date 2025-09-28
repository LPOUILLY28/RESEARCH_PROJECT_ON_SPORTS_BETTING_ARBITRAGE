from pprint import pprint
from tipe_scraper import *
from tipe_filter import *
from tipe_save import *
from tipe_parser import *
from tipe_strategies_arbitrage import *
from config import atp_url
import json
import random

joueurs = read_json("save.json")

matches = read_json("save_matches.json")


def calc_pts_score_joueur1(infoJ1,infoJ2,surface):
    pts_rank = infoJ2["Rank (YTD)"]-infoJ1["Rank (YTD)"]
    pts_titles = infoJ1["Titles (Career)"]
    if infoJ2["Dominant Hand"] == "Left-Handed":
        pts_dom_hand = infoJ1["VS Left-Handers Index (Career)"]
    else:
        pts_dom_hand = infoJ1["VS Right-Handers Index (Career)"]
    if surface == "Clay":
        pts_surface = infoJ1["Clay Index (Career)"]
    elif surface == "Grass":
        pts_surface = infoJ1["Grass Index (Career)"]
    else:
        pts_surface = infoJ1["Hard Index (Career)"]
    
    pts_winlose = infoJ1["Wins (YTD)"]-infoJ1["Loses (YTD)"]
    pts_serve = (infoJ1["1st Serve Points Won"] + infoJ1["1st Serve Return Points Won"] + infoJ1["2nd Serve Points Won"] + infoJ1["2nd Serve Return Points Won"]) / 100
    pts_break = (infoJ1["Break Points Converted"] + infoJ1["Break Points Saved"]) / 100
    pts_score = 0.015*pts_rank + 0.07*pts_titles + 2*pts_dom_hand + 3*pts_surface + 0.1*pts_winlose + 2*pts_serve + 6*pts_break
    if pts_score <= 0:
        return 0.01
    else:
        return pts_score


def estim_proba(match):
    player1,player2 = match["Player 1"],match["Player 2"]
    surface = match["Surface"]
    score1,score2 = match["Score Player 1"],match["Score Player 2"]
    infoJ1,infoJ2 = joueurs[player1],joueurs[player2]
    pts_score1 = calc_pts_score_joueur1(infoJ1,infoJ2,surface)
    pts_score2 = calc_pts_score_joueur1(infoJ2,infoJ1,surface)
    total_pts = pts_score1 + pts_score2
    return (pts_score1/total_pts,pts_score2/total_pts)


def estim_marge():
    L = liste_marge()
    n = len(L)
    odds_average = 0
    for odds  in L:
        odds_average += odds
    odds_average -= n
    odds_average /= n
    return odds_average


def liste_marge():
    L = []
    for match in matches.values():
        L.append((1/match["Odds Player 1"]) + (1/match["Odds Player 2"]) - 1)
    return L