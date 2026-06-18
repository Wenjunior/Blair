from api.option import Option
from api.categories import Reconnaissance

class Main(Reconnaissance):
	info = {
		'title': 'TCP Port Scanner',
		'description': 'Enumerate open TCP services by performing a full TCP connect on each port',
		'authors': ['Wenjunior'],
		'options': [
			Option('IP', description = 'Target IP', type = str, is_required = True),
			Option('PORTS', description = 'Ports to scan', type = str, default_value = '21-23,25,80,443,8080,8443')
		]
	}

	def run(self, options):
		print(options)