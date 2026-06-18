from abc import ABCMeta, abstractmethod

class Exploit(metaclass = ABCMeta):
	@abstractmethod
	def run(self, options):
		pass

class Reconnaissance(metaclass = ABCMeta):
	@abstractmethod
	def run(self, options):
		pass