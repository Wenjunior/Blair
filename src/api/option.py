class Option:
	def __init__(self, name, description, type, default_value = None, is_required = False):
		if not isinstance(name, str):
			raise ValueError('option name is not a str')

		self.name = name

		if not isinstance(description, str):
			raise ValueError('option description is not a str')

		self.description = description

		if type is not int and type is not str and type is not bool:
			raise ValueError('option type is not int, str or bool')

		self.type = type

		if default_value is not None:
			if isinstance(type, int) and not isinstance(default_value, int):
				raise ValueError('option default value is not a int')

			if isinstance(type, str) and not isinstance(default_value, str):
				raise ValueError('option default value is not a str')

			if isinstance(type, bool) and not isinstance(default_value, bool):
				raise ValueError('option default value is not a bool')

		self.value = default_value

		if not isinstance(is_required, bool):
			raise ValueError('is_required is not a bool')

		self.is_required_ = is_required

	def get_name(self):
		return self.name

	def get_description(self):
		return self.description

	def get_type(self):
		return self.type

	def get_value(self):
		return self.value

	def set_value(self, value):
		self.value = value

	def is_required(self):
		return self.is_required_