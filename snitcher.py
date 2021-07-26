import requests
import re
from repository import Repository
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from utils import order_dict_by, write_json

class Snitcher():

    URL = "https://store.steampowered.com/wishlist/profiles/{user_id}/wishlistdata/?p={page}"
    URL_GAME = "https://gocdkeys.com/en/buy-{game_name}-pc-cd-key"

    def __init__(self, id_user, filename, threads, repository):
        self.id_user = id_user
        self.filename = filename
        self.threads = threads
        self.repository = Repository(repository)
        self.url_user = self.URL.replace("{user_id}", id_user)

    def generate_json(self):
        games_raw = self.process_pages()
        games_processed = self.process_games(games_raw)

        ordered_dict = order_dict_by(games_processed, 'price')
        write_json(ordered_dict, self.filename)
        self.repository.save_file()

    def process_pages(self):
        page = 0
        data = requests.get(self.url_user.replace("{page}", str(page))).json()
        if(data == {'success':2}):
            raise Exception("Invalid Steam user id.")
        games_raw = dict(data)

        page += 1
        while data:
            data = requests.get(self.url_user.replace("{page}", str(page))).json()
            games_raw.update(dict(data))
            page += 1
        return games_raw

    def process_games(self, games_raw):
        games_processed = dict()

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for key in games_raw.keys():
                executor.submit(self.update_row, games_raw, key, games_processed).add_done_callback(self.worker_callbacks)
        return games_processed

    def update_row(self, games_raw, key, result_dict):
        name, row = self.generate_dict_row(games_raw, key)
        result_dict[name] = row

    def generate_dict_row(self, data, key):
        name = data[key]["name"]
        url_game = self.repository.get_url_from_name(name)
        new_url = True

        row = dict()
        if(url_game):
            row["url"] = url_game
            new_url = False
        else:
            row["url"] = self.URL_GAME.replace("{game_name}", self.normalize_name(name))

        row["tags"] = data[key]["tags"]

        well_formed = self.is_well_formed_url(row["url"])
        if(not well_formed):
            row["well_formed"] = well_formed
            row["price"] = 999
        else:
            if(new_url):
                self.repository.add_game(name, row["url"])
            row["well_formed"] = True

            store, price = self.get_best_price(well_formed)
            row["price"] = float(price)
            row["store"] = store

        return name, row

    def is_well_formed_url(self, url):
        try:
            headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
            req = requests.get(url, headers=headers)
            return req if req.status_code == 200 else False
        except Exception:
            return False

    def get_best_price(self, page):
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            recommended = soup.find(class_="recommended")
            store = recommended.find('img').get('title')
            price = recommended.find(itemprop="price").text.replace("€", "")
        except Exception:
            store = None
            price = 999
        return store, price

    def normalize_name(self, name):
        name = name.replace("'", "")

        name = re.sub(r'\W+', ' ',name)
        name = name.lower().replace(" ", "-")
        return name

    def worker_callbacks(self, f):
        e = f.exception()

        if e is None:
            return

        trace = []
        tb = e.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        print(str({
            'type': type(e).__name__,
            'message': str(e),
            'trace': trace
        }))