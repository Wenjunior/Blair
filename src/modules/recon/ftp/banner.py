from api.option import Option
from api.categories import Reconnaissance

class Main(Reconnaissance):
	info = {
		'title': 'FTP Banner Grabber',
		'description': 'FTP servers usually send their name and version after connecting',
		'authors': ['Wenjunior'],
		'options': [
			Option('IP', description = 'Target IP', type = str, is_required = True),
			Option('PORT', description = 'Target port', type = int, default_value = 21)
		]
	}

	def run(self, options):
		print(options)