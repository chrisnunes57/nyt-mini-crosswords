# NYT Mini Crossword Data

Board data for over 600 NYT Daily Mini Crossword puzzles from late 2019 to today. This repository contains the downloaded data for these games, as well as the python scripts I used to download, clean, and analyze the data.

# About

There are only a few files in this repository. `scraper.py` is the script I used to download all of my mini crossword data from the NYT games API and write it to a json file. The `main.py` script parses the json data and outputs some significant stats in a table format. Ex:

  - Mini Crosswords: 581
  - Individual Words: 4279
  - 29.283% of words had frequency > 1

  - | word    | occurances   | average solve time   |
  - ------------------------------------------------
  - | YES     | 13           | 1.4057s              |
  - | RED     | 10           | 1.7924s              |
  - | EYES    | 9            | 4.1658s              |
  - | EMAIL   | 8            | 2.8304s              |
  - | OREO    | 8            | 2.4502s              |
  - | SHY     | 7            | 2.4929s              |
  - | ACHOO   | 7            | 2.6192s              |

Finally, the `data.json` file contains the actual data output from running `scraper.py`. The data is formatted as a list of objects, where each object is an individual mini crossword. 

# Usage

1. Run `scraper.py` to populate `data.json` with data. 
2. Once `data.json` is populated, run `main.py` to print analysis to stdout
    - It could be useful to pipe this output to a file, like `python main.py > text.out`