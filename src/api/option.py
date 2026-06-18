class Option:
	def __init__(self, name, description, type, default_value = None, is_required = False):
		self.name = name

		self.description = description

		self.type = type

		self.value = default_value

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