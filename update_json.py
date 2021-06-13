import json
from utils import get_best_price, is_well_formed_url, write_json
import sys

def read_json(filename):
    with open(filename) as json_file:
        return json.load(json_file)

def process_game(game):
    well_formed = is_well_formed_url(game['url'])
    if(not well_formed):
        game["well_formed"] = well_formed
        game["price"] = 999
    else:
        game["well_formed"] = True
        game["price"] = float(get_best_price(well_formed))

def process_dict(games_dict):
    total_games = len(games_dict.keys())
    updated_games = 1

    for key in games_dict.keys():
        process_game(games_dict[key])

        sys.stdout.write("\r{current}/{total}".replace("{current}", str(updated_games)).replace("{total}", str(total_games)))
        sys.stdout.flush()
        updated_games += 1

def update_json(filename):
    games_dict = read_json(filename)
    process_dict(games_dict)
    write_json(games_dict, filename)