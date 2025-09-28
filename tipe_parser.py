from tipe_save import read_json


def get_match(player: str, surface=("Grass", "Clay", "Hard"), only_last=False) -> dict:
    matches = read_json('save_matches.json')
    played_matches = {}

    for id, match in matches.items(): #lit le id associé à la valeur du match en question
        if player in (match["Player 1"], match["Player 2"]) and match["Surface"] in surface:
            played_matches[id] = match

    if played_matches:
        if only_last:
            last_id = sorted(played_matches.keys())[-1] 
            # sortir  dans l'ordre  croissant, dernier année (prendra un match forcément en terre battu car 'Clay')
            return {last_id: played_matches[last_id]}
        return played_matches

    return None

