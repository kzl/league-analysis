
class Rating:
	"""
	A class for calculating elo ratings of competitors. Based off of chess elo
	model (see https://en.wikipedia.org/wiki/Elo_rating_system).
	"""

	def __init__(self, teams=None, start_elo=1000, K=32, rat_adv=400):
		self.start_elo = start_elo
		self.K = K
		self.rat_adv = rat_adv

		if teams is None:
			self.elos = {}
		else:
			self.elos = {team: start_elo for team in teams}

	def add_team(self, team_name):
		"""
		Add a new team to the database if they don't already exist.
		"""
		if team_name not in self.elos:
			self.elos[team_name] = self.start_elo

	def get_prediction(self, team0, team1, scale=1):
		"""
		Returns the probability that team0 will win.
		"""
		self.add_team(team0)
		self.add_team(team1)

		diff = scale*(self.elos[team0]-self.elos[team1])
		prob = 1 / (10 ** (-diff / self.rat_adv) + 1)

		return prob

	def update(self, team0, team1, winner, scale=1):
		"""
		Takes in two strings (team0, team1) and who won (either 0 or 1).
		"""
		E_0 = self.get_prediction(team0, team1, scale)

		self.elos[team0] += self.K * (winner - E_0)
		self.elos[team1] += self.K * ((1-winner) - (1-E_0))

	def get_top_teams(self, num_teams=10):
		"""
		Returns the top num_teams teams and their ratings.
		"""
		if num_teams > len(self.elos):
			num_teams = len(self.elos)

		teams = sorted(self.elos, key=self.elos.get, reverse=True)[:num_teams]
		ratings = [self.elos[team] for team in teams]

		return teams, ratings
