from abc import ABCMeta, abstractmethod

class Exploit(metaclass = ABCMeta):
	@abstractmethod
	def run(self, values):
		pass

class Reconnaissance(metaclass = ABCMeta):
	@abstractmethod
	def run(self, values):
		pass