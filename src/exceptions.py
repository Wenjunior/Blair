from colorama import (
	Fore,
	Style
)

class UnknownCommand(Exception):
	def __str__(self):
		return f'Unknown command{Style.RESET_ALL}\nRun the {Fore.GREEN}help{Style.RESET_ALL} command to see built-in commands'

class TooFewArguments(Exception):
	def __init__(self, usage):
		self.usage = usage

	def __str__(self):
		return f'Usage: {self.usage}'

class TooManyArguments(Exception):
	def __str__(self):
		return 'Too many arguments'

class CategoryNotFound(Exception):
	def __init__(self, categories):
		self.categories = categories

	def __str__(self):
		return f'Category not found{Style.RESET_ALL}\nAvailable categories: ' + ', '.join(self.categories)

class ModuleNotFound(Exception):
	def __str__(self):
		return 'Module not found'

class OptionNotFound(Exception):
	def __str__(self):
		return 'Option not found'

class CloseConsole(Exception):
	pass