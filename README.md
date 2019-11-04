# league-analysis

Analysis of data from the videogame/eSport League of Legends

## Results

### Elo Ratings Over Time

![elo ratings](https://github.com/kzl/league-analysis/raw/master/pictures/elo_102719_a.png "Elo ratings for top teams")
![elo ratings](https://github.com/kzl/league-analysis/raw/master/pictures/elo_102719_b.png "Elo ratings for top teams")

Shown are results from 2014 World Championships to end of quarterfinals of 2019 World Championships. There may be some lapses due to lack of data; some of the teams are merged by name (notably, Gen.G refers to all Samsung organizations; ROX and KOO are equivalent).

Until halfway through Season 8, a Korean team was always the highest rated team (except for a tiny blip of TSM during Season 7): one of SKT, ROX, or Gen.G. In particular, SKT was the strongest team for almost three straight seasons. In Season 8, FW overtook Gen.G before being overtaken by IG, the eventual Season 8 World Champions. In Season 9, GRF, SKT, and IG all briefly held the top spot, until G2 held it for the latter half of the season. Now, nearing the end of the Season 9 World Championships (matches up to 10/27/19), G2, SKT, and FPX are all near the top.

### 2019 World Championships Predictions

These were the predictions given by the model for each of the playoffs matches:

Quarterfinals
* Griffin has 69.07% probability of beating Invictus Gaming
* G2 Esports has 56.68% probability of beating Damwon Gaming
* SK Telecom T1 has 74.42% probability of beating Splyce
* Funplus Phoenix has 50.54% probability of beating Fnatic

Semifinals
* Funplus Phoenix has a 64.36% probability of beating Invictus Gaming
* G2 Esports has a 50.01% probability of beating SK Telecom T1

Finals
* G2 Esports has a 54.14% probability of beating Funplus Phoenix

### Current Highest Elo Ratings (10/27/19)

| Rank | Country | Current Elo | Max Elo |
| :---: | :--- | :---: | :---: |
| 1 | G2 Esports | 1333.7326 | 1333.7326 |
| 2 | SK Telecom T1 | 1333.6348 | 1372.4373 |
| 3 | Funplus Phoenix | 1319.9833 | 1319.9833 |
| 4 | Fnatic | 1266.7824 | 1293.9204 |
| 5 | Griffin | 1264.8608 | 1313.3327 |
| 6 | Damwon Gaming | 1245.7890 | 1245.7890 |
| 7 | Invictus Gaming | 1217.2790 | 1390.6369 |
| 8 | Team Liquid | 1202.6217 | 1241.0897 |
| 9 | Royal Never Give Up | 1188.3210 | 1330.2810 |
| 10 | J Team | 1186.9854 | 1203.7513 |
| ... | ... | ... | ... |
| 13 | Cloud9 | 1173.4663 | 1222.2835 |
| 14 | Kingzone DragonX | 1161.4264 | 1312.0595 |
| 15 | Splyce | 1148.4633 | 1163.8148 |
| 16 | Gen.G | 1137.2856 | 1359.2501 |
| 19 | Afreeca Freecs | 1135.6467 | 1236.3068 |
| 20 | Sandbox Gaming | 1135.6378 | 1207.7971 |
| 23 | EDward Gaming | 1120.1916 | 1179.9334 |
| 33 | Team SoloMid | 1082.8518 | 1262.7547 |

## Project Overview

### Changelog

10/27/19: (Initial commit) Shows elo ratings over time for various teams

### Status

This is an ongoing project that I will work on occasionally. Feel free to use the scripts/results for your purposes; please cite me (Kevin Lu).

## Methodology

### Elo Ratings

See [538](https://fivethirtyeight.com/methodology/how-our-nfl-predictions-work/) for a more detailed description of Elo ratings.

I set K=20 for updates. To initialize teams faster, I use K=100 for the Season 4 World Championships. To emphasize importance of the world championships and to help blend ratings of different regions, I set K=40 for updates during a world championship. Some of the teams are merged by name (this may not be fully complete).

## Setup

### Datasets

If you wish to run the scripts yourself, please download data from:

[Oracle's Elixir](http://oracleselixir.com/match-data/)

[Chuck Ephron's Kaggle Dataset](https://www.kaggle.com/chuckephron/leagueoflegends/data)

### Requirements

Scripts are written in Python 3. Visualization is done with numpy, matplotlib, and seaborn. To set the text labels, I used [adjustText](https://github.com/Phlya/adjustText). All of these can be installed with pip via the command line.

### Tools Used

Python
