from core import *
from parameters import Parameter

class Format(object):
	alias = ""

	def __init__(self):
		self.parameters = []

	def auto_input(self, parameters_storage, alias, parameters_list):
		self.alias = alias
		for p in parameters_list:
			if not p in parameters_storage:
				raiseError(f"Parameter {p} don't exist in the program!")
				return

			if isinstance(parameters_storage[p], Parameter): self.parameters.append(parameters_storage[p])
			else:
				raiseError(f"{p} is not a Parameter instance!")
				return
		return True

	def manual_input(self, parameters_storage):
		self.alias = getInput("Alias for the format >> ")
		if self.alias == None: return

		temp_parameters = getValues()
		if temp_parameters == None: return
		if type(temp_parameters) == str:
			# Adding a imaginary parameter
			if p.startswith('"') and p.endswith('"'):
				paramlist = list(p)
				paramlist.pop(0)
				paramlist.pop()
				value = "".join(paramlist)
				print(f"Value: {value}")
				a = Parameter()
				a.alias = f'"{value}"'
				a.values = [value]
				self.parameters.append(a)

			if not temp_parameters in parameters_storage:
				raiseError(f"Parameter {temp_parameters} don't exist in the program!")
				return
			
			if isinstance(parameters_storage[temp_parameters], Parameter): self.parameters.append(parameters_storage[temp_parameters])
			else: 
				raiseError(f"{temp_parameters} is not a Parameter instance!")
				return
		else:
			for p in temp_parameters:
				# Adding a imaginary parameter
				if p.startswith('"') and p.endswith('"'):
					paramlist = list(p)
					paramlist.pop(0)
					paramlist.pop()
					value = "".join(paramlist)
					print(f"Value: {value}")
					a = Parameter()
					a.alias = f'"{value}"'
					a.values = [value]
					self.parameters.append(a)
					continue

				if not p in parameters_storage:
					raiseError(f"Parameter {p} don't exist in the program!")
					return

				if isinstance(parameters_storage[p], Parameter): self.parameters.append(parameters_storage[p])
				else:
					raiseError(f"{p} is not a Parameter instance!")
					return

		final_parameters_out = [x.alias for x in self.parameters]
		raiseMessage(f"Creating format {self.alias} with the parameters {final_parameters_out}")
		return True
	def __str__(self):
		return self.alias