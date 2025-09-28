from pprint import pprint
from tipe_scraper import *
from tipe_filter import *
from tipe_save import *
from tipe_parser import *
from tipe_verif import *
from tipe_strategies_arbitrage import *
from config import atp_url
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import json


def curve_fifty_fifty(mise):
    values = fifty_fifty(mise)
    Y = np.array(values) # strat
    X = np.array([i for i in range(len(values))])
    Y0 = np.array([0 for i in range(len(values))])
    Yinit = np.array([1000 for i in range(len(values))])
    plt.plot(X,Y,'b')
    plt.plot(X,Y0,'r')
    plt.plot(X,Yinit,'c')
    plt.xlabel("Nombre de matchs")
    plt.ylabel("Somme totale")
    plt.title("fifty_fifty")
    plt.grid()
    plt.show()


def curve_risky(benefice):
    values = risky(benefice)
    Y = np.array(values)
    X = np.array([i for i in range(len(values))])
    Y0 = np.array([0 for i in range(len(values))])
    Yinit = np.array([1000 for i in range(len(values))])
    Ygain = np.array([(1000 + benefice) for i in range(len(values))])
    plt.plot(X,Y,'b')
    plt.plot(X,Y0,'r')
    plt.plot(X,Yinit,'c')
    plt.plot(X,Ygain,'g')
    plt.xlabel("Nombre de matchs")
    plt.ylabel("Somme totale")
    plt.grid()
    plt.show()




def curve_all_on_favor(mise):
    values = all_on_favor(mise)
    Y = np.array(values)
    Yinit = np.array([1000 for i in range(len(values))])
    Y0 = np.array([0 for i in range(len(values))])
    X = np.array([i for i in range(len(values))])
    plt.plot(X,Y,'b')
    plt.plot(X,Y0,'r')
    plt.plot(X,Yinit,'c')
    plt.xlabel("Nombre de matchs")
    plt.ylabel("Somme totale")
    plt.title("all_on_favor")
    plt.grid()
    plt.show()


def curve_depending_proba(mise):
    values = depending_proba(mise)
    Y = np.array(values)
    Yinit = np.array([1000 for i in range(len(values))])
    Y0 = np.array([0 for i in range(len(values))])
    X = np.array([i for i in range(len(values))])
    plt.plot(X,Y,'b')
    plt.plot(X,Y0,'r')
    plt.plot(X,Yinit,'c')
    plt.xlabel("Nombre de matchs")
    plt.ylabel("Somme totale")
    plt.title("depending_proba")
    plt.grid()
    plt.show()


def curve_marge():
    values = liste_marge()
    average = 0
    for i in values:
        average += i
    average /= len(values)
    Y = np.array(values)
    X = np.array([i for i in range(len(values))])
    Y0 = np.array([0 for i in range(len(values))])
    Ymoy = np.array([average for i in range(len(values))])
    plt.plot(X,Y,'')
    plt.plot(X,Y0,'r')
    plt.plot(X,Ymoy,'g', linewidth = 5)
    plt.xlabel("Nombre de matchs")
    plt.ylabel("Marges")
    plt.title("Marge moyenne pour chaque match")
    plt.grid()
    plt.show()



def curve_arbitrage():
    values = liste_arbitrage()
    average = 0
    for i in values:
        average += i
    average /= len(values)
    Y = np.array(values)
    Y0 = np.array([0 for i in range(len(values))])
    X = np.array([i for i in range(len(values))])
    Ymoy = np.array([average for i in range(len(values))])
    plt.plot(X,Y,'o')
    plt.plot(X,Y0,'r')
    plt.plot(X,Ymoy,'g', linewidth = 5)
    plt.xlabel("Nombre de matchs")
    plt.ylabel("Marges")
    plt.title("Marge minimale pour chaque match")
    plt.grid()
    plt.show()
