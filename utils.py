from collections import OrderedDict
from operator import getitem
import json

def order_dict_by(dict_games, field):
    ordered_dict = OrderedDict(sorted(dict_games.items(), key = lambda x: (getitem(x[1], field), getitem(x[1], "well_formed"))))
    return ordered_dict
def write_json(games_dict, filename):
    with open(filename, 'w') as json_file:
        json.dump(games_dict, json_file)