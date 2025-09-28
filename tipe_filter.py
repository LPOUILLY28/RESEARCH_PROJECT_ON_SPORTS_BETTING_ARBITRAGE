import re


def filter_player(infos: dict) -> dict:
    hands_infos = infos["Personnal Details"]["Plays"].split(", ")
    hand = "Right-Handed" if "Right-Handed" in hands_infos else "Left-Handed"
    surface_dict = infos["Activity Stats"]["Surface"]

    infos_f = {"Rank (YTD)": int(infos["YTD&Career Player Stats"]["YTD"]["Rank"]),
               "Titles (Career)": int(infos["YTD&Career Player Stats"]["Career"]["Titles"]),
               "Wins (YTD)": int(infos["YTD&Career Player Stats"]["YTD"]["Wins"]),
               "Loses (YTD)": int(infos["YTD&Career Player Stats"]["YTD"]["Loses"]),
               "Wins (Career)": int(infos["YTD&Career Player Stats"]["Career"]["Wins"]),
               "Loses (Career)": int(infos["YTD&Career Player Stats"]["Career"]["Loses"]),
               "Preferred Surface": max(surface_dict, key=surface_dict.get),
               "Dominant Hand": hand,
               "1st Serve Points Won": int(infos["Career Stats"]["1st Serve Points Won"][:-1]),
               "1st Serve Return Points Won": int(infos["Career Stats"]["1st Serve Return Points Won"][:-1]),
               "2nd Serve Points Won": int(infos["Career Stats"]["2nd Serve Points Won"][:-1]),
               "2nd Serve Return Points Won": int(infos["Career Stats"]["2nd Serve Return Points Won"][:-1]),
               "Break Points Converted": int(infos["Career Stats"]["Break Points Converted"][:-1]),
               "Break Points Saved": int(infos["Career Stats"]["Break Points Saved"][:-1]),
               "Clay Index (Career)": float(infos["Activity Stats"]["Surface"]["Clay"]),
               "Grass Index (Career)": float(infos["Activity Stats"]["Surface"]["Grass"]),
               "Hard Index (Career)": float(infos["Activity Stats"]["Surface"]["Hard"]),
               "VS Right-Handers Index (Career)": float(infos["Activity Stats"]["vs Hands"]["vs. Right Handers*"]),
               "VS Left-Handers Index (Career)": float(infos["Activity Stats"]["vs Hands"]["vs. Left Handers*"]),
               }
    return infos_f


def player_name(url: str) -> str:
    extract_name = re.search(r"/players/([a-zA-Z-]+-[a-zA-Z-]+)/", url)
    names = extract_name.group(1).split('-')
    return f"{names[-1][0].upper()}{names[-1][1:].lower()} {names[0][0].upper()}."
