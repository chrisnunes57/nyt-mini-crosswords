import requests
from pprint import pprint
import json
from multiprocessing.dummy import Pool as ThreadPool
import time

def read_config(filename):
    data = None
    with open(filename, 'r') as f:
        data = json.loads(f.read())
    return data

config = read_config('config.json')
puzzle_ids = []
game_url_template = "https://nyt-games-prd.appspot.com/svc/crosswords/v6/game/"
security_header = config['s-header']
user_id = config['user-id']
game_data = []
# for multithreading

urls = [
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2019-01-01&date_end=2019-02-28',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2019-03-01&date_end=2019-04-30',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2019-05-01&date_end=2019-06-30',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2019-07-01&date_end=2019-07-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2019-08-01&date_end=2019-10-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2019-11-01&date_end=2020-01-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-02-01&date_end=2020-03-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-04-01&date_end=2020-06-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-07-01&date_end=2020-08-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-09-01&date_end=2020-11-31',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2020-12-01&date_end=2021-02-28',
    'https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user_id + '/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start=2021-03-01&date_end=2021-03-08'
]

def get_cword_data(cword):
    data_url = game_url_template + str(cword['puzzle_id']) + ".json"

    cword_response = requests.get(data_url, headers=security_header)
    cword_response_data = json.loads(cword_response.content)

    cword["board"] = cword_response_data["board"]

    return cword

def main():
    start = time.time()
    # scrape crossword lists for publish dates and game ids
    for url in urls:
        response = requests.get(url, headers=security_header)

        data = json.loads(response.content)['results']

        solved_cwords = [cword for cword in data if cword['solved']]

        with ThreadPool(20) as pool:
            results = pool.map(get_cword_data, solved_cwords)
            game_data.extend(results)

    # output the list of boards somehow (for now, writing to a json file)
    with open("data.json", "w") as f:
        f.write(json.dumps(game_data))

    end = time.time()
    print("script finished in", end - start, "s")


if __name__ == "__main__":
    main()

