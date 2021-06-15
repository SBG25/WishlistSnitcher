from bs4 import BeautifulSoup
import requests
import json
from collections import OrderedDict
from operator import getitem

def get_best_price(page):
    try:
        soup = BeautifulSoup(page.content, 'html.parser')
        recommended = soup.find(class_="recommended")
        price = recommended.find(itemprop="price").text.replace("€", "")
    except Exception:
        price = 999
    return price

def is_well_formed_url(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
        req = requests.get(url, headers=headers)
        return req if req.status_code == 200 else False
    except Exception:
        return False

def write_json(games_dict, filename):
    with open(filename, 'w') as json_file:
        json.dump(games_dict, json_file)

def order_dict_by(dict_games, field):
    ordered_dict = OrderedDict(sorted(dict_games.items(), key = lambda x: (getitem(x[1], field), getitem(x[1], "well_formed"))))
    return ordered_dict

def read_json(filename):
    with open(filename) as json_file:
        return json.load(json_file)