import json
import math
from pprint import pprint

EMPTY_SYMBOL = '*'

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


with open("data.json", 'r') as f:
    data = json.loads(f.read())
    frequencies = {}

    for board in data:
        words = get_words(board['cells'])

        for word_tup in words['across']:
            if not word_tup[0] in frequencies:
                frequencies[word_tup[0]] = {
                    "average_time": 0,
                    "freq": 0
                }

            frequencies[word_tup[0]]['freq'] += 1
            frequencies[word_tup[0]]['average_time'] = (frequencies[word_tup[0]]['average_time'] + word_tup[1]) / frequencies[word_tup[0]]['freq']

        for word_tup in words['down']:
            if not word_tup[0] in frequencies:
                frequencies[word_tup[0]] = {
                    "average_time": 0,
                    "freq": 0
                }

            frequencies[word_tup[0]]['freq'] += 1
            frequencies[word_tup[0]]['average_time'] = (frequencies[word_tup[0]]['average_time'] + word_tup[1]) / frequencies[word_tup[0]]['freq']

    # output results somehow (for now, stdout)
    print("Mini Crosswords:", len(data))
    print("Individual Words:", len(frequencies))
    print('{0:.5g}'.format(sum(1 for n in frequencies if frequencies[n]['freq'] > 1) / len(frequencies) * 100) + "% of words had frequency > 1\n")

    # print table of results
    print('| word'.ljust(10) + '| occurances'.ljust(15) + '| average solve time'.ljust(23) + "|")
    print('-' * 48)

    for w in sorted(frequencies, key=lambda item: frequencies[item]['freq'], reverse=True):
        print(("| " + w).ljust(10) + ('| ' + '{0:.5g}'.format(frequencies[w]['freq'])).ljust(15) + ('| ' + '{0:.5g}'.format(frequencies[w]['average_time']) + "s").ljust(23) + "|")
                                                            
