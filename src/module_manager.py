import os
import sys
from os import path
from importlib import util

from colorama import (
	Fore,
	Style
)

class Module:
	def __init__(self, module):
		main = module.Main()

		self.main = main

		info = main.info

		self.info = info

		self.options = info['options']

	def get_title(self):
		return self.info['title']

	def get_description(self):
		return self.info['description']

	def get_authors(self):
		return self.info['authors']

	def get_options(self):
		return self.options

	def run(self, options):
		return self.main.run(options)

class ExploitModule(Module):
	def get_disclosure_date(self):
		return self.info['disclosure_date']

	def get_references(self):
		return self.info['references']

class ReconnaissanceModule(Module):
	pass

class ModuleManager:
	modules = {}

	def __init__(self):
		current_path = path.realpath(__file__)

		current_dir = path.dirname(current_path)

		modules_dir = path.join(current_dir, 'modules')

		self.categories = os.listdir(modules_dir)

		for root, dirnames, filenames in os.walk(modules_dir):
			for filename in filenames:
				if not filename.endswith('.py'):
					continue

				file_path = path.join(root, filename)

				name = file_path.removeprefix(modules_dir).replace('\\', '/').removeprefix('/').removesuffix('.py')

				spec = util.spec_from_file_location(name, file_path)

				module = util.module_from_spec(spec)

				try:
					spec.loader.exec_module(module)

					if name.startswith('exploits'):
						self.modules[name] = ExploitModule(module)

						continue

					self.modules[name] = ReconnaissanceModule(module)
				except Exception as error:
					print(f'{Fore.RED}{file_path}: {error}{Style.RESET_ALL}', file = sys.stderr)

	def get_categories(self):
		return self.categories

	def get_modules(self):
		return self.modules