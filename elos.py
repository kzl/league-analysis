import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from adjustText import adjust_text

from utils.gather import gather_match_data
from elo.rating import Rating
from elo.teams import Team

"""
Script for generating the elos of teams and visualizing them over time.
"""

qualitative_colors = sns.color_palette('Set3', 10)

# Gather data from csv files
infos = gather_match_data()
matches, teams, patches = infos['matches'], infos['teams'], infos['patches']

# Sort patches
patches = sorted(patches)

# Create ratings and team histories
best_loss, best_k = float('inf'), 0
for k in range(20, 21):
	correct, incorrect = 0, 0
	loss = 0

	ratings = Rating(K=k)
	team_hists = {}
	for team in teams:
		team_hists[team] = Team(team)

	# Calculate elo ratings over time
	top_teams = set()
	top_scores = {}
	for i in range(len(patches)):
		# Keep track of which teams played this patch
		played = set()

		for match in matches:
			if match.patch == patches[i]:
				blue = match.blue_team
				red = match.red_team

				if blue not in played:
					played.add(blue)
				if red not in played:
					played.add(red)

				if team_hists[blue].first_patch is None:
					team_hists[blue].first_patch = i
				team_hists[blue].last_patch = i

				if team_hists[red].first_patch is None:
					team_hists[red].first_patch = i
				team_hists[red].last_patch = i

				# For WC matches, increase elodiff scale
				if 'WC' in match.tags:
					scale = 1.2
				else:
					scale = 1

				# Calculate accuracy/loss statistics
				prob_blue_win = ratings.get_prediction(blue, red, scale=scale)
				if prob_blue_win >= 0.5 and match.winner == 'blue':
					correct += 1
					loss += (1-prob_blue_win)**2
				elif prob_blue_win <= 0.5 and match.winner == 'red':
					correct += 1
					loss += (prob_blue_win)**2
				elif prob_blue_win >= 0.5 and match.winner == 'red':
					incorrect += 1
					loss += (prob_blue_win)**2
				elif prob_blue_win <= 0.5 and match.winner == 'blue':
					incorrect += 1
					loss += (1-prob_blue_win)**2

				# Updating ratings (make WC matches more important)
				if i == 0:
					ratings.K = 5*k
				elif 'WC' in match.tags:
					ratings.K = 1.5*k
				else:
					ratings.K = k
				ratings.update(blue, red, match.winner == 'blue')

		# Get statistics for the end of this patch
		scores = set()
		for team in teams:
			if team in ratings.elos:
				team_hists[team].hist[i] = ratings.elos[team]
				if team in played:
					scores.add(ratings.elos[team])
				top_scores[team] = max(ratings.elos[team], top_scores.get(team, 0))

		scores = sorted(scores, reverse=True)
		num_teams = 3 if i < len(patches)-1 else 8
		for team in teams:
			if team in ratings.elos and team in played:
				if ratings.elos[team] >= scores[min(num_teams, len(scores))-1]:
					top_teams.add(team)

	print('K=%d, accuracy: %.4f, loss: %.4f' % (k, 100 * correct / (correct + incorrect), loss))
	if loss < best_loss:
		best_k, best_loss = k, loss

print('Best K: %d' % best_k)

top_teams = sorted(top_teams, key=top_scores.get, reverse=True)
# top_teams = ['SK Telecom T1', 'G2 Esports', 'Splyce', 'Funplus Phoenix', 'Damwon Gaming', 'Invictus Gaming', 'Griffin', 'Fnatic']
# lck_teams = ['SK Telecom T1', 'Griffin', 'Damwon Gaming', 'Kingzone DragonX', 'Gen.G', 'Sandbox Gaming', 'Afreeca Freecs', 'ROX Tigers', 'KT Rolster', 'NaJin e-mFire', 'CJ Entus', 'SBENU Sonicboom', 'Jin Air Green Wings']
# top_teams.extend(lck_teams)
# top_teams = [
# 	'Funplus Phoenix', 'Royal Never Give Up', 'Splyce',
# 	'SK Telecom T1', 'Damwon Gaming', 'Invictus Gaming',
# 	'Griffin', 'Fnatic', 'Kingzone DragonX', 'G2 Esports',
# 	'Team Liquid', 'Sandbox Gaming', 'KT Rolster',
# 	'Afreeca Freecs', 'Cloud9', 'ROX Tigers', 'Flash Wolves',
# 	'Gen.G', 'J Team', 'EDward Gaming'
# ]

# Print out top teams
TT, top_elos = ratings.get_top_teams(1000)
for i in range(len(TT)):
	print('%02d | %30s - current elo: %.4f, best elo: %.4f' % (i, TT[i], top_elos[i], top_scores[TT[i]]))

# Print out some predictions for Worlds 2019
teams = ['Griffin', 'Invictus Gaming', 'G2 Esports', 'Damwon Gaming', 'SK Telecom T1', 'Splyce', 'Funplus Phoenix', 'Fnatic']

q1 = ratings.get_prediction('Griffin', 'Invictus Gaming')
q2 = ratings.get_prediction('G2 Esports', 'Damwon Gaming')
q3 = ratings.get_prediction('SK Telecom T1', 'Splyce')
q4 = ratings.get_prediction('Funplus Phoenix', 'Fnatic')

s1 = ratings.get_prediction('Invictus Gaming', 'Funplus Phoenix')
s2 = ratings.get_prediction('SK Telecom T1', 'G2 Esports')

f1 = ratings.get_prediction('Funplus Phoenix', 'G2 Esports')

print('q1 Griffin win pct: %.4f' % q1)
print('q2 G2 Esports win pct: %.4f' % q2)
print('q3 SK Telecom T1 win pct: %.4f' % q3)
print('q4 Funplus Phoenix win pct: %.4f' % q4)

print('s1 Invictus Gaming win pct: %.4f' % s1)
print('s2 SK Telecom T1 win pct: %.4f' % s2)

print('f1 Funplus Phoenix win pct: %.4f' % f1)

# Plot ratings over time
plt.figure(figsize=(16, 12))

x = np.arange(len(patches))
texts = []
r, r_len = 0, 0
for team in top_teams:
	hist = team_hists[team].hist
	max_rating, max_patch = np.max(hist), np.argmax(hist)

	first, last = team_hists[team].first_patch, team_hists[team].last_patch
	if hist[first] == 0:
		hist[first] = 1000

	plt.plot(x[first:(last+1)], hist[first:(last+1)], label=team,
			 alpha=((4-r)/4), color=qualitative_colors[r_len], linewidth=2)

	text = plt.text(max_patch, max_rating, '%s: %4.0f' % (team, max_rating),
					# horizontalalignment='center', verticalalignment='center',
					fontsize=10,
					bbox=dict(facecolor=qualitative_colors[r_len], alpha=0.8))
	texts.append(text)

	r_len = (r_len+1) % 10
	if r_len == 0:
		r += 1

for i in range(len(patches)):
	if patches[i] in ['4.01', '5.01', '6.01', '7.01', '8.01', '9.01']:
		plt.axvline(x=i, color='gray', linestyle='dashed')
		plt.text(i, 1000, patches[i][0], fontsize=12, color='black',
				 verticalalignment='center', horizontalalignment='center',
				 bbox=dict(facecolor='white', alpha=0.9))

plt.title('Elo ratings of top historical teams over time')
plt.xlabel('Time (from Season 4 WC to Season 9 WC)')
plt.ylabel('Elo (labeled by max rating)')
# plt.legend(loc='best')

FV = 8
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='black',
								   linewidth=2, alpha=0.5),
			force_text=(FV,FV), force_points=(FV,FV), force_objects=(0,0),
			autoalign='', only_move={'points':'y', 'text':'y'})
plt.show()
