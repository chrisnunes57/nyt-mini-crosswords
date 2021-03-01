import math

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

# returns the timestamp of the last letter input in the given row
def get_longest_time_row(board, r):
    max_time = 0

    for i in range(len(board)):
        if board[r][i] != EMPTY_SYMBOL and board[r][i][1] > max_time:
            max_time = board[r][i][1]

    return max_time

# returns the timestamp of the last letter input in the given col
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

# takes in a board object and returns the timestamp of the last letter input
def get_solve_time(board):
    max_time = 0

    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] != EMPTY_SYMBOL and board[r][c][1] > max_time:
                max_time = board[r][c][1]
    
    return max_time


def format_time(time):

    days = time // 86400
    hours = time % 86400 // 3600
    minutes = time % 3600 // 60
    seconds = time % 60

    return (str(days) + 'd ' if days else '') + (str(hours) + 'h ' if hours else '') + (str(minutes) + 'm ' if minutes else '') + (str(seconds) + 's ')
