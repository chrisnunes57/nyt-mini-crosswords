import json
import math
from pprint import pprint
from helpers import pretty_date, get_board, get_words

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


                                                            
