import requests
from pprint import pprint
import json

def read_config(filename):
    data = None
    with open(filename, 'r') as f:
        data = json.loads(f.read())
    return data

urls = [
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/103098841/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2019-07-01&date_end=2019-07-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/103098841/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2019-08-01&date_end=2019-10-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/103098841/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2019-11-01&date_end=2020-01-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/103098841/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-02-01&date_end=2020-03-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/103098841/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-04-01&date_end=2020-06-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/103098841/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-07-01&date_end=2020-08-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/103098841/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-09-01&date_end=2020-11-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/103098841/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-12-01&date_end=2021-01-31'
]

puzzle_ids = []
game_url_template = "https://nyt-games-prd.appspot.com/svc/crosswords/v6/game/"
security_header = read_config("config.json")

# scrape crossword lists for publish dates and game ids
for url in urls:
    response = requests.get(url, headers=security_header)

    data = json.loads(response.content)['results']

    for cword in data:
        puzzle_ids.append(cword['puzzle_id'])

game_data = []
# get board data for each game
for id in puzzle_ids:
    data_url = game_url_template + str(id) + ".json"
    response = requests.get(data_url, headers=security_header)
    game_data.append(json.loads(response.content)["board"])

# output the list of boards somehow (for now, writing to a json file)
with open("data.json", "w") as f:
    f.write(json.dumps(game_data))
