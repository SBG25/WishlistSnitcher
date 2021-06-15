import re
import requests
from utils import get_best_price, is_well_formed_url, write_json, order_dict_by
from concurrent.futures import ThreadPoolExecutor

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

def update_row(games_dict, key, result_dict):
    name, row = generate_dict_row(games_dict, key)
    result_dict[name] = row

def process_dict(games_dict, threads):
    result_dict = dict()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for key in games_dict.keys():
            executor.submit(update_row, games_dict, key, result_dict)
    return result_dict

def process_pages(url_json):
    page = 0
    data = requests.get(url_json.replace("{page}", str(page))).json()
    if(data == {'success':2}):
        raise Exception("Invalid Steam user id.")
    games_dict = dict(data)
    
    page += 1
    while data:
        data = requests.get(url_json.replace("{page}", str(page))).json()
        games_dict.update(dict(data))
        page += 1
    return games_dict


def generate_json(id_user, filename, threads):
    url_json = URL.replace("{user_id}", id_user)

    games_dict = process_pages(url_json)
    result_dict = process_dict(games_dict, threads)

    ordered_dict = order_dict_by(result_dict, 'price')
    write_json(ordered_dict, filename)