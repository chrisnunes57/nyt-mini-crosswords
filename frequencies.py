import json
import math
from pprint import pprint

EMPTY_SYMBOL = '*'
MONTHS = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sept",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}

# takes in date string in format 'YYYY-MM-DD' and returns prettier date
def pretty_date(date):
    tokens = date.split("-")

    year = tokens[0]
    month = MONTHS[tokens[1]]
    day = tokens[2] if tokens[2][0] != '0' else tokens[2][1:]
    
    return "{m} {d}, {y}".format(m=month, d=day, y=year)

# takes in a list of cells, returns a 2d array of the grid as tuples (guess, time)
def get_board(cells):

    length = int(math.sqrt(len(cells)))
    result = [[EMPTY_SYMBOL] * length for _ in range(length)]

    i = 0
    for r in range(length):
        for c in range(length):
            if "blank" not in cells[i]:
                result[r][c] = (cells[i]['guess'], cells[i]['timestamp'])

            i += 1
    return result

def get_longest_time_row(board, r):
    max_time = 0

    for i in range(len(board)):
        if board[r][i] != EMPTY_SYMBOL and board[r][i][1] > max_time:
            max_time = board[r][i][1]

    return max_time

def get_longest_time_col(board, c):
    max_time = 0

    for i in range(len(board)):
        if board[i][c] != EMPTY_SYMBOL and board[i][c][1] > max_time:
            max_time = board[i][c][1]

    return max_time

# takes in a list of cells, returns a dict with across and down words
# schema: {
#   'across': [...],
#   'down': [...]
# }
def get_words(cells):
    words = {
        'across': [],
        'down': []
    }
    board = get_board(cells)

    # across words
    for r in range(len(board)):
        result = []
        for c in range(len(board)):
            if board[r][c] != EMPTY_SYMBOL:
                result.append(board[r][c][0])
            elif board[r][c] == EMPTY_SYMBOL and result:
                new_tup = ("".join(result), get_longest_time_row(board, r))
                words['across'].append(new_tup)
                result = []

        if result:
            new_tup = ("".join(result), get_longest_time_row(board, r))
            words['across'].append(new_tup)

    # down words
    for r in range(len(board)):
        result = []
        for c in range(len(board)):
            if board[c][r] != EMPTY_SYMBOL:
                result.append(board[c][r][0])
            elif board[c][r] == EMPTY_SYMBOL and result:
                new_tup = ("".join(result), get_longest_time_col(board, r))
                words['down'].append(new_tup)
                result = []

        if result:
            new_tup = ("".join(result), get_longest_time_col(board, r))
            words['down'].append(new_tup)

    return words


frequencies = {}
puzzle_dates = {}

with open("data.json", 'r') as f:
    data = json.loads(f.read())

    for board in data:
        words = get_words(board['board']['cells'])

        for word_tup in words['across']:
            if not word_tup[0] in frequencies:
                frequencies[word_tup[0]] = {
                    "average_time": 0,
                    "freq": 0,
                    "puzzles": []
                }

            frequencies[word_tup[0]]['freq'] += 1
            frequencies[word_tup[0]]['average_time'] = (frequencies[word_tup[0]]['average_time'] + word_tup[1]) / frequencies[word_tup[0]]['freq']
            frequencies[word_tup[0]]['puzzles'].append(board['puzzle_id'])

        for word_tup in words['down']:
            if not word_tup[0] in frequencies:
                frequencies[word_tup[0]] = {
                    "average_time": 0,
                    "freq": 0,
                    "puzzles": []
                }

            frequencies[word_tup[0]]['freq'] += 1
            frequencies[word_tup[0]]['average_time'] = (frequencies[word_tup[0]]['average_time'] + word_tup[1]) / frequencies[word_tup[0]]['freq']
            frequencies[word_tup[0]]['puzzles'].append(board['puzzle_id'])

        puzzle_dates[board['puzzle_id']] = board['print_date']


# output results somehow (for now, stdout)
print("Mini Crosswords:", len(data))
print("Individual Words:", len(frequencies))
print('{0:.5g}'.format(sum(1 for n in frequencies if frequencies[n]['freq'] > 1) / len(frequencies) * 100) + "% of words had frequency > 1\n")

# print table of results
print('| word'.ljust(10) + '| occurances'.ljust(15) + '| average solve time'.ljust(23) + '| most recent use'.ljust(20) + '|')
print('-' * 69)

for word in sorted(frequencies, key=lambda item: frequencies[item]['freq'], reverse=True):

    avg_freq = '{0:.5g}'.format(frequencies[word]['freq'])
    avg_time = '{0:.5g}'.format(frequencies[word]['average_time']) + "s"
    date = pretty_date(puzzle_dates[frequencies[word]['puzzles'][-1]])

    print(("| " + word).ljust(10) + ('| ' + avg_freq).ljust(15) + ('| ' + avg_time).ljust(23) + ('| ' + date).ljust(20) + '|')

with open('word-data.json', 'w') as f:
    f.write(json.dumps(frequencies))


                                                            
