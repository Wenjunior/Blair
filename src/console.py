import os
import sys
import shlex
import platform

from colorama import (
	Fore,
	Style
)
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style as ptStyle

from exceptions import (
	CloseConsole,
	ModuleNotFound,
	OptionNotFound,
	UnknownCommand,
	TooFewArguments,
	CategoryNotFound,
	TooManyArguments
)
from module_manager import ModuleManager

BOLD = '\033[1m'

session = PromptSession(style = ptStyle.from_dict({'prompt': '#A347BA bold'}))

class BaseConsole:
	def loop(self, prompt):
		while True:
			try:
				command_line = session.prompt(prompt)

				if not command_line:
					continue

				tokens = shlex.split(command_line)

				command, args = tokens[0], tokens[1:]

				function_name = f'do_{command}'

				if not hasattr(self, function_name):
					raise UnknownCommand()

				function = getattr(self, function_name)

				function(args)
			except EOFError:
				break
			except CloseConsole:
				break
			except KeyboardInterrupt:
				break
			except Exception as error:
				print(f'{Fore.YELLOW}{error}{Style.RESET_ALL}', file = sys.stderr)

	def do_help(self, args):
		if args:
			raise TooManyArguments()

		function_names = dir(self)

		for function_name in function_names:
			if not function_name.startswith('do_'):
				continue

			function = getattr(self, function_name)

			doc_string = function.__doc__

			if not doc_string:
				continue

			command = function_name.removeprefix('do_')

			print(f'{command}\t\t{doc_string}')

	def do_clear(self, args):
		"""Clear terminal screen"""

		if args:
			raise TooManyArguments()

		os_name = platform.system()

		command = 'clear'

		if os_name == 'Windows':
			command = 'cls'

		os.system(command)

	def do_exit(self, args):
		"""Close console"""

		if args:
			raise TooManyArguments()

		sys.exit()

class BaseModuleConsole(BaseConsole):
	def __init__(self, module):
		self.module = module

	def show_basic_info(self):
		title = self.module.get_title()

		print(f'{BOLD}Title:{Style.RESET_ALL} {title}')

		description = self.module.get_description()

		print(f'{BOLD}Description:{Style.RESET_ALL} {description}')

		authors = self.module.get_authors()

		print(f'{BOLD}Authors:{Style.RESET_ALL} ' + ', '.join(authors))

	def do_show(self, args):
		"""Show all options or option value"""

		args_len = len(args)

		if args_len < 1:
			raise TooFewArguments('show (options|<name>)')

		if args_len > 1:
			raise TooManyArguments()

		option_chosen = args[0]

		options = self.module.get_options()

		if option_chosen == 'options':
			print('{}{: <10} {: <30} {: <25} Is required{}'.format(BOLD, 'Name', 'Description', 'Value', Style.RESET_ALL))

			print('{: <10} {: <30} {: <25} ==========='.format('====', '=' * 11, '====='))

			for option in options:
				name = option.get_name()

				description = option.get_description()

				value = option.get_value()

				if value is None:
					value = ''

				is_required = option.is_required()

				if is_required:
					is_required = 'yes'
				else:
					is_required = 'no'

				print('{: <10} {: <30} {: <25} {}'.format(name, description, value, is_required))

			return

		for option in options:
			name = option.get_name()

			if name != option_chosen:
				continue

			value = option.get_value()

			if value is None:
				value = ''

			print(value)

			return

		raise OptionNotFound()

	def do_set(self, args):
		"""Set option value"""

		args_len = len(args)

		if args_len < 2:
			raise TooFewArguments('set <name> <value>')

		if args_len > 2:
			raise TooManyArguments()

		options = self.module.get_options()

		name = args[0]

		value = args[1]

		for option in options:
			if option.get_name() != name:
				continue

			option.set_value(value)

			return

		raise OptionNotFound()

	def do_run(self, args):
		"""Run module"""

		if args:
			raise TooManyArguments()

		options = self.module.get_options()

		values = {}

		for option in options:
			name = option.get_name()

			value = option.get_value()

			values[name] = value

		self.module.run(values)

	def do_back(self, args):
		"""Go back"""

		if args:
			raise TooManyArguments()

		raise CloseConsole()

class ExploitModuleConsole(BaseModuleConsole):
	def do_info(self, args):
		"""Show more details"""

		if args:
			raise TooManyArguments()

		self.show_basic_info()

		disclosure_date = self.module.get_disclosure_date()

		print(f'{BOLD}Disclosure date:{Style.RESET_ALL} {disclosure_date}')

		references = self.module.get_references()

		print(f'{BOLD}References:{Style.RESET_ALL}')

		for index, reference in enumerate(references):
			index += 1

			print(f'   {BOLD}{index}.{Style.RESET_ALL} {reference}')

class ReconnaissanceModuleConsole(BaseModuleConsole):
	def do_info(self, args):
		"""Show more details"""

		if args:
			raise TooManyArguments()

		self.show_basic_info()

class Console(BaseConsole):
	manager = ModuleManager()

	def do_show(self, args):
		"""Show modules by category"""

		args_len = len(args)

		categories = self.manager.get_categories()

		if args_len < 1:
			raise TooFewArguments('show (all|' + '|'.join(categories) + ')')

		if args_len > 1:
			raise TooManyArguments()

		category = args[0]

		if category != 'all' and category not in categories:
			raise CategoryNotFound(categories)

		print('{}Index {: <40} Title{}'.format(BOLD, 'Name', Style.RESET_ALL))

		print('===== {: <40} ====='.format('===='))

		modules = self.manager.get_modules()

		for index, name in enumerate(modules):
			if category != 'all' and not name.startswith(category):
				continue

			module = modules[name]

			title = module.get_title()

			print('{: <5} {: <40} {}'.format(index, name, title))

	def do_use(self, args):
		"""Select a module by index or name"""

		args_len = len(args)

		if args_len < 1:
			raise TooFewArguments('use (<index>|<name>)')

		if args_len > 1:
			raise TooManyArguments()

		option = args[0]

		name = option

		modules = self.manager.get_modules()

		if option.isdigit():
			index = int(option)

			keys = list(modules.keys())

			if index >= len(keys):
				raise ModuleNotFound()

			name = keys[index]

		if name not in modules:
			raise ModuleNotFound()

		module = modules[name]

		module_console = ExploitModuleConsole(module)

		if name.startswith('recon'):
			module_console = ReconnaissanceModuleConsole(module)

		module_console.loop(f'({name}) > ')