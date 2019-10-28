# league-analysis

Analysis of data from the videogame/eSport League of Legends

## Results

### Elo Ratings Over Time

![elo ratings](https://github.com/kzl/league-analysis/raw/master/pictures/elo_102719_a.png "Elo ratings for top teams")
![elo ratings](https://github.com/kzl/league-analysis/raw/master/pictures/elo_102719_b.png "Elo ratings for top teams")

Shown are results from 2014 World Championships to end of quarterfinals of 2019 World Championships. There may be some lapses due to lack of data; some of the teams are merged by name (notably, Gen.G refers to all Samsung organizations).

### Current Highest Elo Ratings (10/27/19)

| Rank | Country | Elo Rating |
| :---: | :--- | :---: |
| 1 | Brazil | 1825.37 |
| 2 | Germany | 1772.87 |
| 3 | Argentina | 1763.83 |
| 4 | Italy | 1847.03 |
| 5 | Netherlands | 1699.77 |
| 6 | Sweden | 1687.21 |
| ... | ... | ... |
| 8 | England | 1669.83 |
| 12 | Australia | 1640.54 |
| 16 | France | 1630.51 |
| 29 | USA | 1610.60 |
| 35 | Japan | 1598.43 |
| 51 | Canada | 1583.95 |
| ... | ... | ... |
| 76 | Republic of Ireland | 1528.57 |
| 77 | Iran | 1527.75 |
| 78 | El Salvador | 1510.16 |
| 79 | Croatia | 1507.50 |
| 80 | Bulgaria | 1506.49 |
| 81 | Mexico | 1500.92 |

Prior to the events of the 2018 World Cup, the model predicted that in a game between France and Croatia, France had a 67.00% chance to win.

### Accuracy of Elo Predictions

| % Interval | Accuracy |
| :---: | :---: |
| 50% - 60% | 51.26% |
| 60% - 70% | 63.64% |
| 70% - 80% | 73.47% |
| 80% - 90% | 75.00% |
| 90% - 100% | n/a |

ex. In all games where one team had a chance to win between 50% and 60%, the model was correct 51.26% of the time.

## Project Overview

### Changelog

10/27/19: (Initial commit) Shows elo ratings over time for various teams

### Status

This is an ongoing project that I will work on occasionally. Feel free to use the scripts/results for your purposes; please cite me (Kevin Lu).

## Setup

### Datasets

If you wish to run the scripts yourself, please download data from:

[Oracle's Elixir](http://oracleselixir.com/match-data/)

[Chuck Ephron's Kaggle Dataset](https://www.kaggle.com/chuckephron/leagueoflegends/data)

### Requirements

Scripts are written in Python 3. Visualization is done with numpy, matplotlib, and seaborn. To set the text labels, I used [adjustText](https://github.com/Phlya/adjustText). All of these can be installed with pip via the command line.

### Tools Used

Python
