from utils import get_best_price, is_well_formed_url, write_json, order_dict_by, read_json
from concurrent.futures import ThreadPoolExecutor


def process_game(game):
    well_formed = is_well_formed_url(game['url'])
    if(not well_formed):
        game["well_formed"] = well_formed
        game["price"] = 999
    else:
        game["well_formed"] = True
        game["price"] = float(get_best_price(well_formed))

def process_dict(games_dict, threads):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for key in games_dict.keys():
            executor.submit(process_game, games_dict[key])

def update_json(filename, threads):
    games_dict = read_json(filename)
    process_dict(games_dict, threads)
    ordered_dict = order_dict_by(games_dict, 'price')
    write_json(ordered_dict, filename)