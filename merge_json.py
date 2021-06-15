from utils import read_json, order_dict_by, write_json

def merge_json(filename1, filename2, output):
    dict1 = read_json(filename1)
    dict2 = read_json(filename2)

    dict2.update(dict1)
    new_entries = len(dict2) - len(dict1)
    print(str(new_entries) + " new entries.")

    ordered_dict = order_dict_by(dict2, 'price')
    write_json(ordered_dict, output)