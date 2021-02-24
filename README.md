# NYT Mini Crossword Data

Board data for over 600 NYT Daily Mini Crossword puzzles from late 2019 to today. This repository contains the downloaded data for these games, as well as the python scripts I used to download, clean, and analyze the data.

# About

There are only a few files in this repository. `scraper.py` is the script I used to download all of my mini crossword data from the NYT games API and write it to a json file. The `frequencies.py` script parses the json data and outputs some significant stats in a table format. Currently, it just finds the most frequent words and the my average solve time for each word. Ex:

```
Mini Crosswords: 581
Individual Words: 4279
29.283% of words had frequency > 1

| word    | occurances   | average solve time   |
------------------------------------------------
| YES     | 13           | 1.4057s              |
| RED     | 10           | 1.7924s              |
| EYES    | 9            | 4.1658s              |
| EMAIL   | 8            | 2.8304s              |
| OREO    | 8            | 2.4502s              |
| SHY     | 7            | 2.4929s              |
| ACHOO   | 7            | 2.6192s              |
| ...     | ...          | ...                  |
```


Finally, the `data.json` file contains the actual data output from running `scraper.py`. The data is formatted as a list of objects, where each object is an individual mini crossword. The format of each crossword puzzle object is as follows: 

```json
{
    "author": "Joel Fagliano",
    "editor": "",
    "format_type": "Normal",
    "print_date": "2019-07-01",
    "publish_type": "Mini",
    "puzzle_id": 16905,
    "title": "",
    "version": 4,
    "percent_filled": 100,
    "solved": true,
    "star": null,
    "cells": [
        {
            "guess": "F",
            "timestamp": 27
        },
        {
            "guess": "A",
            "timestamp": 9
        },
        {
            "guess": "U",
            "timestamp": 29
        },
        {
            "guess": "S",
            "timestamp": 34
        },
        {
            "guess": "T",
            "timestamp": 15
        },
        
        ...
        
    ]
}
```

Each entry in the `"cells"` array represents one letter in the grid, and the timestamp when the letter was submitted (ex: above, I submitted 'F' after 27 seconds). 

So in the above example, we can see that the first word in the grid was "Faust" (the guy who traded his soul to the devil), and I entered the first letter after 9 seconds and the last letter after 34 seconds. 

By using cells array, we can figure out the layout of the grid and the across/down words of the grid.

# Setup

This `frequencies.py` file will work as-is, but the requests to the NYT servers in `scraper.py` won't work without adding some of your own security credentials. To make `scraper.py` work, you need to create a `config.json` file in the same directory. The file will be structured as follows:

```json
{
    "s-header": {
        "nyt-s": "<security_token>"
    },
    "user-id": "<user_id" 
}
```

The `nyt-s` token is a security cookie that the NYT game server uses to validate each request, and the `user-id` token is a numeric ID that is used to identify each user. 

You can find both of these values by using `Inspect Element` and poking around the session storage until you find the `pz-user` and `pz-user-check` values. 

Then, in the above `config.json`, substitute the value of `pz-user` for `<user_id>` and the value of `pz-user-check` for `<security_token>`.

# Usage

Once you have a valid `config.json`, you can scrape the data yourself by following these steps. 

1. Run `scraper.py` to populate `data.json` with data. 
    - This might take a minute, depending on how many crosswords you request
3. Once `data.json` is populated, run `frequencies.py` to print analysis to stdout
    - It's a lot of output, so it can be useful to pipe to a file, like `python frequencies.py > text.out`

# Important Notes

The board data fetched by `scraper.py` will only contain correct data if you have correctly solved the mini crosswords that you request. If your mini crosswords are unsolved/incorrect, the data will match what you have. So, the more crosswords you have solved, the better your data will be. 
