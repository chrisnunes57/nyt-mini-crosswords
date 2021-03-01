# NYT Mini Crossword Data

Puzzle data for over 750 NYT Daily Mini Crossword puzzles from January 2019 - February 2021. This repository contains the downloaded data for these games, as well as the python scripts I used to download, clean, and analyze the data.

# About

There are only a few files in this repository. `scraper.py` is the script I used to download all of my mini crossword data from the NYT games API and write it to a json file. The `frequencies.py` script parses the json data and outputs some significant stats in a table format. Currently, it just finds the most frequent words and the my average solve time for each word. Ex:

```
Mini Crosswords: 752
Individual Words: 5152
33.036% of words had frequency > 1

| word    | occurances   | average solve time   | most recent use   |
---------------------------------------------------------------------
| YES     | 16           | 1.1374s              | Sept 30, 2020     |
| EYES    | 11           | 3.3347s              | Jan 7, 2021       |
| OREO    | 10           | 1.9425s              | Dec 17, 2020      |
| RED     | 10           | 1.7924s              | Nov 23, 2020      |
| ABC     | 9            | 1.7772s              | Dec 22, 2020      |
| SHY     | 9            | 10.565s              | Dec 15, 2020      |
| EMAIL   | 9            | 2.4516s              | Dec 8, 2020       |
| ...     | ...          | ...                  | ...               |
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

You can find both of these values by using `Inspect Element` and poking around the **session storage** until you find the `pz-user` and `pz-user-check` values. 

Then, in the above `config.json`, substitute the value of `pz-user` for `<user_id>` and the value of `pz-user-check` for `<security_token>`.

# Usage

Once you have a valid `config.json`, you can scrape the data yourself by following these steps. 

1. Run `scraper.py` to populate `data.json` with data. 
    - This might take a minute, as it will make a request for each day in the desired date range
3. Once `data.json` is populated, run `frequencies.py` to print word-related analysis to stdout
    - It's a lot of output, so it can be useful to pipe to a file, like `python frequencies.py > text.out`

# Important Notes

The crosswords fetched by the program will reflect the amount of crosswords that you have solved. So, if you have only solved 30 crosswords, `scraper.py` will only return data about 30 crosswords. 

Additionally, I haven't tested for the exact number, but it looks like the NYT API will only return **two months** worth of data per API call. It might beneficial to find the exact number at somepoint so that I can optimize my API calls (i.e., not make 11 API calls to get the data).
