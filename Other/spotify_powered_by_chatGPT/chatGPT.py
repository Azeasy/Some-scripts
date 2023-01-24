"""
Same script but I asked chatGPT to refactor it and write some comments
"""


import json
from run import get_cum_data_by_artist

import os

def read_json(folder_path):
    """Read and return data from all json files in a folder"""
    data = []
    for file_name in os.listdir(folder_path):
        if file_name.startswith("StreamingHistory") and file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data += json.load(file)
    return data


def group_and_sort(data, key):
    """Group data by key and sort by msPlayed"""
    group = {}
    for item in data:
        item = item.copy()
        msPlayed = item.get('msPlayed')
        if item[key] in group:
            msPlayed += group[item[key]]['msPlayed']
        item['msPlayed'] = msPlayed
        # These two lines were added by me in order to compare the results directly
        if key == 'artistName':
            del item['trackName']
        group[item[key]] = item
    return sorted(group.values(), key=lambda x: x['msPlayed'])

def print_data(data):
    """Print data in json format with indentation"""
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    folder_path = './'
    data = read_json(folder_path)
    cum_data_by_track = group_and_sort(data, 'trackName')
    cum_data_by_artist = group_and_sort(data, 'artistName')

    # print last 10 items of each list
    print_data(data[-10:])
    print_data(cum_data_by_track[-10:])
    print_data(cum_data_by_artist[-10:])

    # comparing the results of my quick-made script and the one been refactored by chatGPT
    cum_data_by_artist_test = get_cum_data_by_artist(data)
    print(cum_data_by_artist == cum_data_by_artist_test)
