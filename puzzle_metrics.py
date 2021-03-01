import json
from pprint import pprint
from helpers import pretty_date, get_board, get_solve_time, format_time
from sexy_table import sexy_table

puzzles = []

with open("data.json", 'r') as f:
    data = json.loads(f.read())

    for board in data:
        grid = get_board(board['board']['cells'])
        time = get_solve_time(grid)

        new_puz = {
            'date': pretty_date(board['print_date']),
            'time': time,
            'id': board['puzzle_id']
        }

        # we only track puzzles with solve times of less than 1 day (to remove inaccurate data)
        if time < 3600:
            puzzles.append(new_puz)

# sort data
puzzles.sort(key=lambda x: x['time'])

average_solve_time = int(sum([puz['time'] for puz in puzzles]) / len(puzzles))

# # output results somehow (for now, stdout)
print("Mini Crosswords:", len(puzzles))
print("Shortest Solve Time:", format_time(puzzles[0]['time']))
print("Longest Solve Time:", format_time(puzzles[-1]['time']))
print("Average Solve Time:", format_time(average_solve_time), "\n")

table_headers = {
    'date': 'Date',
    'time': 'Solve Time',
    'id': 'Puzzle ID'
}

order = {
    'date': 2,
    'time': 3,
    'id': 1
}

transformers = {
    'time': format_time
}

table = sexy_table(puzzles, Headers=table_headers, Transformers=transformers, Order=order)
print(table)
