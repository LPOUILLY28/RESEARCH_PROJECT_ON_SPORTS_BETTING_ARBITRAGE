import json
import logging


def save_json(infos: dict, force=False, file='save.json') -> None:
    if force:
        with open(file, 'w') as f: # ouvre le fichier +  écriture write 
            json.dump(infos, f, indent=4) 
            # on importe la librairie , et dump ça réécrit dans le fichier f , indentation pour gérer l'espace
        return None

    try:
        with open(file, 'r') as f: # lecture 
            data = json.load(f)  # pour le charger 
    except (FileNotFoundError, json.JSONDecodeError): #s'il y a une erreur 
        data = {} # d'ou le dico vide 

    data.update(infos)

    with open(file, 'w') as f:
        json.dump(data, f, indent=4) # on réécrit comme en haut 


def read_json(file='save.json') -> dict:
    with open(file, 'r') as f:
        data = json.load(f)
        return data


def is_player_in_json(player_name: str, file='save.json') -> bool:
    try:
        with open(file, 'r') as f:
            return player_name in json.load(f) 
        # vérifie dans si ton joueur est dans ton fichier , toujours sous forme de dico !
    except:
        return False # cas où il y a un problème de lecture 


logging.basicConfig(filename='log_player.txt', level=logging.INFO, format='%(asctime)s - %(message)s') 
#pour avoir un journal de tout ce qui s'est passé 


def log_player_status(name: str, status: str = 'waiting'):
    logging.info(f'{name} - Status: {status}') # vérification dans le fichier log 

