"""
Some script made for fan that sorts the data generated by spotify
It could be made online, obviously, this is more nerdy way and it gives
an exact number of milliseconds
"""

import json

path = 'StreamingHistory0.json'

def get_json(path):
    with open(path, 'r') as file:
        data = json.load(file)

    data = sorted(data, key=lambda x: x.get('msPlayed'))
    return data


def get_cum_data(data):
    cum_data_dict = {}
    for track_true in data:
        track = track_true.copy()
        track['msPlayed'] = track.get('msPlayed') +\
                                cum_data_dict.get(track.get('trackName'),
                                                  {'msPlayed': 0}).get('msPlayed')
        cum_data_dict[track.get('trackName')] = track

    cum_data = []
    for uniq_track in cum_data_dict:
        cum_data += cum_data_dict[uniq_track],

    cum_data = sorted(cum_data, key=lambda x: x.get('msPlayed'))
    return cum_data


def get_cum_data_by_artist(data):
    cum_data_dict = {}
    for track_true in data:
        track = track_true.copy()
        track['msPlayed'] = track.get('msPlayed') +\
                                cum_data_dict.get(track.get('artistName'),
                                                  {'msPlayed': 0}).get('msPlayed')
        del track['trackName']
        cum_data_dict[track.get('artistName')] = track

    cum_data = []
    for uniq_track in cum_data_dict:
        cum_data += cum_data_dict[uniq_track],

    cum_data = sorted(cum_data, key=lambda x: x.get('msPlayed'))
    return cum_data


def pprint(data):
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    data = get_json(path)

    cum_data = get_cum_data(data)

    cum_data_by_artist = get_cum_data_by_artist(data)

    # pprint(data[-10:])
    pprint(cum_data[-10:])
    # pprint(cum_data_by_artist[-10:])

    # pprint(data[140:160])
    # pprint(cum_data[55:75])
    # pprint(cum_data_by_artist[:30])
