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


def importance_rank():
    i = 0
    total = 0
    for match in matches.values():
        total += 1
        if joueurs[match["Player 1"]]["Rank (YTD)"] < joueurs[match["Player 2"]]["Rank (YTD)"] and match["Score Player 1"] > match["Score Player 2"]:
            i += 1
        elif joueurs[match["Player 1"]]["Rank (YTD)"] > joueurs[match["Player 2"]]["Rank (YTD)"] and match["Score Player 1"] < match["Score Player 2"]:
            i += 1
    return (100*i/total,total)


def importance_titles():
    i = 0
    total = 0
    for match in matches.values():
        total += 1
        if joueurs[match["Player 1"]]["Titles (Career)"] > joueurs[match["Player 2"]]["Titles (Career)"] and match["Score Player 1"] > match["Score Player 2"]:
            i += 1
        elif joueurs[match["Player 1"]]["Titles (Career)"] < joueurs[match["Player 2"]]["Titles (Career)"] and match["Score Player 1"] < match["Score Player 2"]:
            i += 1
    return (100*i/total,total)


def importance_win_lose():
    i = 0
    total = 0
    for match in matches.values():
        total += 1
        win_lose1 = joueurs[match["Player 1"]]["Wins (YTD)"] - joueurs[match["Player 1"]]["Loses (YTD)"]
        win_lose2 = joueurs[match["Player 2"]]["Wins (YTD)"] - joueurs[match["Player 2"]]["Loses (YTD)"]
        if win_lose1 > win_lose2 and match["Score Player 1"] > match["Score Player 2"]:
            i += 1
        elif win_lose1 < win_lose2 and match["Score Player 1"] < match["Score Player 2"]:
            i += 1
    return (100*i/total,total)