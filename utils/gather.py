import csv

FILES_ORACLE = [
	'2016_complete',
	'2017_complete',
	'2018_spring',
	'2018_summer',
	'2018_worlds',
	'2019_spring',
	'2019_summer',
	'2019_worlds_1027'
]

for i in range(len(FILES_ORACLE)):
	FILES_ORACLE[i] = 'data/' + FILES_ORACLE[i] + '.csv'

FILES_EPHRON = [
	'2015_2017_complete'
]

for i in range(len(FILES_EPHRON)):
	FILES_EPHRON[i] = 'data/' + FILES_EPHRON[i] + '.csv'

alias = {
	'SK Telecom T1': ['SKT', 'T1'],
	'G2 Esports': ['G2'],
	'Team SoloMid': ['TSM'],
	'EDward Gaming': ['EDG', 'Edward Gaming'],
	'Fnatic': ['FNC'],
	'Damwon Gaming': ['DWG'],
	'Griffin': ['GRF'],
	'Gen.G': ['SSG', 'SSW', 'SSB', 'Samsung Galaxy'], # not LCK 2015 SSB
	'Royal Never Give Up': ['RNG', 'SHR', 'SHRC'],
	'Funplus Phoenix': ['FPX'],
	'Splyce': ['SPY'],
	'Top Esports': ['TOP'],
	'Hong Kong Attitude': ['HKA'],
	'Hong Kong Esports': ['HKE', 'HKES'],
	'Invictus Gaming': ['IG', 'iG'],
	'Cloud9': ['C9', 'Cloud 9'],
	'Kingzone DragonX': ['Longzhu Gaming', 'Longzhu', 'LZ'],
	'Jin Air Green Wings': ['JAG'],
	'Team Liquid': ['TL'],
	'Counter Logic Gaming': ['CLG'],
	'Clutch Gaming': ['CG'],
	'Misfits': ['MSF'],
	'KT Rolster': ['KT', 'KTR', 'kT', 'kt', 'KTA', 'KTB', 'kta', 'ktb'],
	'Roccat': ['ROC'],
	'100 Thieves': ['100T'],
	'LGD Gaming': ['LGD'],
	'BBQ Olivers': ['BBQ'],
	'CJ Entus': ['CJ', 'CJE'],
	'Millenium': ['MIL'],
	'Hanwha Life Esports': ['HLE'],
	'Flash Wolves': ['FW'],
	'Gambit Esports': ['GMB'],
	'Dignitas': ['DIG'],
	'Immortals': ['IMT'],
	'Phong Vu Buffalo': ['PVB'],
	'Phoenix1': ['P1'],
	'Echo Fox': ['FOX'],
	'Giants Gaming': ['GIA'],
	'Unicorns of Love': ['UOL'],
	'KSV Esports': ['KSV'],
	'AHQ Fighter': ['AHQ', 'ahq'],
	'SK Gaming': ['SK'],
	'Roccat': ['ROC'],
	'Origen': ['OG'],
	'ROX Tigers': ['KOO', 'ROX', 'GET'],
	'NaJin e-mFire': ['NJE', 'NJF', 'NWS'],
	'Taipei Assassins': ['TPA'],
	'Dark Passage': ['DP'],
	'Ninjas in Pyjamas': ['NIP'],
	'Team Inpulse': ['TIP'],
	'KaBuM e-Sports': ['KBM'],
	'Phong Vu Buffalo': ['PVB'],
	'Machi 17': ['M17'],
	'Unicorns of Love': ['UOL'],
	'Team WE': ['WE'],
	'SBENU Sonicboom': ['SBENU']
}

alias_to_name = {}
for team in alias:
	for n in alias[team]:
		alias_to_name[n] = team

class Match:
	"""
	Class for storing match history information. winner is 'red' or 'blue'.
	"""

	def __init__(self, blue_team, red_team, winner, patch=None):
		self.blue_team = blue_team
		self.red_team = red_team
		self.winner = winner
		self.patch = patch
		self.tags = set()

def gather_match_data():
	"""
	Return set of team names, list of all matches (stored in Match class
	format), and set of all patches. Compiles from each source of data
	provided in this file.
	"""
	matches, teams, patches = [], set(), set()

	funcs = [gather_match_data_ephron, gather_match_data_oracle]

	for gather in funcs:
		infos = gather()

		matches.extend(infos['matches'])
		teams.update(infos['teams'])
		patches.update(infos['patches'])

	if '' in patches:
		patches.remove('')

	infos = {'matches': matches, 'teams': teams, 'patches': patches}

	return infos

def gather_match_data_ephron():
	"""
	Match data collection. Reads from Chuck Ephron's Kaggle dataset. Only
	process until 2016, i.e. when we have Oracle's Elixir dataset.
	"""
	matches, teams, patches = [], set(), set()

	for file in FILES_EPHRON:
		print('Reading ' + file)
		with open(file, 'r', encoding='utf-8') as f:
			reader = csv.reader(f, delimiter=',')

			idxs, first_row = {}, True

			for row in reader:
				# Set up header indices for accessing, is on a per-file basis
				if first_row:
					first_row = False
					for i in range(len(row)):
						if row[i] == 'Year':
							idxs['year'] = i
						elif row[i] == 'Season':
							idxs['season'] = i
						elif 'League' in row[i]:
							idxs['league'] = i
						elif row[i] == 'blueTeamTag':
							idxs['blue'] = i
						elif row[i] == 'redTeamTag':
							idxs['red'] = i
						elif row[i] == 'bResult':
							idxs['bluewin'] = i
						elif row[i] == 'rResult':
							idxs['redwin'] = i
					continue

				# Only care if before 2016
				if row[idxs['year']] not in ['2014', '2015']:
					continue

				# Get team tags
				blue, red = row[idxs['blue']], row[idxs['red']]

				# Edge case handling
				if blue == 'SSB' and row[idxs['league']] == 'LCK' \
								 and row[idxs['year']] == '2015':
					blue = 'SBENU Sonicboom'
				elif red == 'SSB' and row[idxs['league']] == 'LCK' \
								  and row[idxs['year']] == '2015':
					red = 'SBENU Sonicboom'

				# Convert the tags into name format
				blue = alias_to_name[blue] if blue in alias_to_name else blue
				red = alias_to_name[red] if red in alias_to_name else red

				# Add to our set of teams
				if blue not in teams:
					teams.add(blue)
				if red not in teams:
					teams.add(red)

				# Create a pseudo patch id (for sorting purposes)
				if row[idxs['year']] == '2014':
					patch = '4.01'
				elif row[idxs['year']] == '2015' and row[idxs['league']] == 'WC':
					patch = '5.04'
				elif row[idxs['year']] == '2015' and row[idxs['league']] == 'MSI':
					patch = '5.02'
				elif row[idxs['year']] == '2015' and row[idxs['season']] == 'Spring':
					patch = '5.01'
				elif row[idxs['year']] == '2015' and row[idxs['season']] == 'Summer':
					patch = '5.03'

				# Store match
				winner = 'blue' if row[idxs['bluewin']] == '1' else 'red'
				patches.add(patch)
				match = Match(blue, red, winner, patch)
				if row[idxs['league']] == 'WC':
					match.tags.add('WC')
				matches.append(match)

	infos = {'matches': matches, 'teams': teams, 'patches': patches}
	return infos

def gather_match_data_oracle():
	"""
	Match data collection. Reads from Oracle's Elixir dataset.
	"""
	matches, teams, patches = [], set(), set()

	for file in FILES_ORACLE:
		print('Reading ' + file)
		with open(file, 'r', encoding='utf-8') as f:
			reader = csv.reader(f, delimiter=',')

			idxs, first_row = {}, True
			blue, red, winner = None, None, None

			for row in reader:
				# Set up header indices for accessing, is on a per-file basis
				if first_row:
					first_row = False
					for i in range(len(row)):
						if row[i] == 'side':
							idxs['side'] = i
						elif row[i] == 'league':
							idxs['league'] = i
						elif row[i] == 'position':
							idxs['pos'] = i
						elif row[i] == 'team':
							idxs['team'] = i
						elif row[i] == 'result':
							idxs['res'] = i
						elif row[i] == 'patchno':
							idxs['patch'] = i
					continue

				# Only care if it is the team result, and add to dict if new
				if row[idxs['pos']] != 'Team':
					continue
				team = row[idxs['team']]
				if team in alias_to_name:
					team = alias_to_name[team]
				if team not in teams:
					teams.add(team)

				# Store who won, which team played on which side
				side = row[idxs['side']]
				if side == 'Blue':
					blue = team
					if row[idxs['res']] == '1':
						winner = 'blue'
				elif side == 'Red':
					red = team
					if row[idxs['res']] == '1':
						winner = 'red'

				# Add to match history if we have both teams that played
				if blue is not None and red is not None:
					patches.add(row[idxs['patch']])
					match = Match(blue, red, winner, row[idxs['patch']])
					if row[idxs['league']] == 'WC':
						match.tags.add('WC')
					matches.append(match)
					blue, red, winner = None, None, None

	infos = {'matches': matches, 'teams': teams, 'patches': patches}
	return infos
