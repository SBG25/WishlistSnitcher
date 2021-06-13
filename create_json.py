import json
import re
import requests
from collections import OrderedDict
from operator import getitem
from utils import get_best_price, is_well_formed_url, write_json

URL = "https://store.steampowered.com/wishlist/profiles/{user_id}/wishlistdata/?p={page}"
URL_GAME = "https://gocdkeys.com/en/buy-{game_name}-pc-cd-key"

def normalize_name(name):
    name = re.sub(r'\W+', ' ',name)
    name = name.lower().replace(" ", "-")
    return name

def generate_dict_row(data, key):
    name = data[key]["name"]
    normalized_name = normalize_name(name)
    url_game = URL_GAME.replace("{game_name}", normalized_name)

    row = dict()
    row["url"] = url_game
    row["tags"] = data[key]["tags"]

    well_formed = is_well_formed_url(url_game)
    if(not well_formed):
        row["well_formed"] = well_formed
        row["price"] = 999
    else:
        row["well_formed"] = True
        row["price"] = float(get_best_price(well_formed))

    return name, row

def process_page(url_json, games_dict):
    data = requests.get(url_json).json()
    if(data == {'success':2}):
        raise Exception("Invalid Steam user id.")

    if(not data):
        return None
    else:
        for key in data.keys():
            name, row = generate_dict_row(data, key)
            games_dict[name] = row
        return True

def order_dict_by(dict_games, field):
    ordered_dict = OrderedDict(sorted(dict_games.items(), key = lambda x: getitem(x[1], field)))
    return ordered_dict

def generate_json(id_user, filename):
    games_dict = dict()
    url_json = URL.replace("{user_id}", id_user)

    page = 0
    while process_page(url_json.replace("{page}", str(page)), games_dict) is not None:
        page += 1

    ordered_dict = order_dict_by(games_dict, 'price')
    write_json(ordered_dict, filename)