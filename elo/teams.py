import numpy as np

class Team:
	"""
	Class for storing elo history information for a team (useful for plotting).
	"""

	def __init__(self, name, names=None, max_patches=100):
		self.name = name
		self.hist = np.zeros(max_patches)
		self.first_patch = None
		self.last_patch = None

		self.names = set()
		self.names.add(self.name)
		if names is not None:
			for n in names:
				self.names.add(n)
