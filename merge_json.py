from utils import read_json, order_dict_by, write_json
from create_json import URL, process_dict, process_pages

def merge_json(id_user, filename, threads):
    dict1 = read_json(filename)
    
    url_json = URL.replace("{user_id}", id_user)
    games_dict = process_pages(url_json)
    result_dict = process_dict(games_dict, threads)

    result_dict.update(dict1)
    new_entries = len(result_dict) - len(dict1)
    print(str(new_entries) + " new entries.")

    ordered_dict = order_dict_by(result_dict, 'price')
    write_json(ordered_dict, filename)