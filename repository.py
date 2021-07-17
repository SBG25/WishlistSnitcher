import pandas as pd

class Repository:
    def __init__(self, filename):
        self.filename = filename
        self.repository = pd.read_csv(filename)

    def get_repository(self):
        return self.repository

    def get_url_from_name(self, name):
        url = self.repository[self.repository['name'] == name]['url'].values
        return url[0] if url else None

    def add_game(self, name, url):
        self.repository = self.repository.append({'name':name, 'url':url}, ignore_index=True)

    def save_file(self):
        self.repository.to_csv(self.filename, index=False)