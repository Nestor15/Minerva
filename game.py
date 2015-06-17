"""
This module contains classes required to simulate the board game Risk.
"""

class Territory():
	"""
	Simulates a territory on a Risk board
	"""
	
	def __init__(self, name, continent=None, borders=None,
                     sea_lines=None, owner=None, armies=0):
		"""
		Creates a new territory with the following attributes
		"""
		
		self.name = name
		self.continent = continent
		self.borders = borders
		self.sea_lines = sea_lines
		self.owner = owner
		self.armies = armies

class Continent():
	"""
	Simulates a continent, or group of territories, on a Risk board
	"""
	
	def __init__(self, name, value, territories):
		"""
		Creates a new continent
		"""
		
		self.name = name
		self.value = value
		self.territories = territories

class Board():
	"""
	Simulates a Risk board's territories and continents
	"""
	
	def __init__(self, territories=None, continents=None):
		self.territories = territories
		self.continents = continents
	
	def __getitem__(self, key):
		#Return whatever territory/continent we find, if any
		return self.territories.get(key) or self.continents.get(key)
	
	def __setitem__(self, key, value):
		#Assign the item to the correct dictionary
		if isinstance(value, Territory):
			self.territories[key] = value
		elif isinstance(value, Continent):
			self.continents[key] = value

class StandardBoard(Board):
	"""
	A standard Risk board
	"""
	
	def __init__(self):
		#Set up all of the standard territories and continents
		self.territories = {}
		self.continents = {}
		
		#Make a list of territory names for setup
		names = [
		'Alaska',
		'Alberta',
		'Central America',
		'Eastern United States',
		'Greenland',
		'Northwest Territory',
		'Ontario',
		'Quebec',
		'Western United States',
		'Argentina',
		'Brazil',
		'Peru',
		'Venezuela',
		'Great Britain',
		'Iceland',
		'Northern Europe',
		'Scandinavia',
		'Southern Europe',
		'Ukraine',
		'Western Europe',
		'Congo',
		'East Africa',
		'Egypt',
		'Madagascar',
		'North Africa',
		'South Africa',
		'Afghanistan',
		'China',
		'India',
		'Irkutsk',
		'Japan',
		'Kamchatka',
		'Middle East',
		'Mongolia',
		'Siam',
		'Siberia',
		'Ural',
		'Yakutsk',
		'Eastern Australia',
		'Indonesia',
		'New Guinea',
		'Western Australia']
		
		#Create a territory for every name in the list
		for name in names:
			self[name] = Territory(name)
		
		#Now, we set up the continents
		#First, North America
		continent = (
		self['Alaska'],
		self['Alberta'],
		self['Central America'],
		self['Eastern United States'],
		self['Greenland'],
		self['Northwest Territory'],
		self['Ontario'],
		self['Quebec'],
		self['Western United States'])
		
		self['North America'] = Continent('North America', 5, continent)
		
		#Next, South America
		continent = (
		self['Argentina'],
		self['Brazil'],
		self['Peru'],
		self['Venezuela'])
		
		self['South America'] = Continent('South America', 2, continent)
		
		#Europe
		continent = (
		self['Great Britain'],
		self['Iceland'],
		self['Northern Europe'],
		self['Scandinavia'],
		self['Southern Europe'],
		self['Ukraine'],
		self['Western Europe'])
		
		self['Europe'] = Continent('Europe', 5, continent)
		
		#Africa
		continent = (
		self['Congo'],
		self['East Africa'],
		self['Egypt'],
		self['Madagascar'],
		self['North Africa'],
		self['South Africa'])
		
		self['Africa'] = Continent('Africa', 3, continent)
		
		#Asia
		continent = (
		self['Afghanistan'],
		self['China'],
		self['India'],
		self['Irkutsk'],
		self['Japan'],
		self['Kamchatka'],
		self['Middle East'],
		self['Mongolia'],
		self['Siam'],
		self['Siberia'],
		self['Ural'],
		self['Yakutsk'])
		
		self['Asia'] = Continent('Asia', 7, continent)
		
		#Australia/Oceania
		continent = (
		self['Eastern Australia'],
		self['Indonesia'],
		self['New Guinea'],
		self['Western Australia'])
		
		self['Australia'] = Continent('Australia', 2, continent)
		
		#TODO: Add borders and sea lines between territories
