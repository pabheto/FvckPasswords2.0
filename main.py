from cmd import Cmd
from core import *
from sty import fg, bg, rs, ef
from parameters import *
from format import Format
import os

class Program(Cmd):

	program_parameters = {}
	program_formats = {}

	prompt = f"{fg.magenta}{ef.i}{ef.bold}(FvckPasswords) {rs.all}"

	def emptyline(self):
		return
	def do_shell(self, s):
		while True:
			command = getInput("Command >> ")
			if command == None:
				break
			os.system(command)
	def do_exit(self, s):
		quit()

	def do_parameters(self, s):
		print("+------------------+")
		print("|Created Parameters|")
		print("+------------------+")
		if len(self.program_parameters) == 0:
			raiseError("There aren't any parameters!")
		for parameter in self.program_parameters:
			print(f"{fg.green}{parameter}{rs.all} ~ {self.program_parameters[parameter].values}")

	def do_add_parameter(self, s):
		args = s.split()
		if len(args) == 0:
			print("+-------------------+")
			print("|Avalible Parameters|")
			print("+-------------------+")
			for parameter in avalible_parameters:
				print(f"{fg.green}{avalible_parameters[parameter].pid}{rs.all}: {avalible_parameters[parameter].description}")
			param = getInput("Parameter ID --> ")
			if param == None: return

			if param in avalible_parameters:
				a = avalible_parameters[param]()

				alias = getInput("Alias for the parameter >> ") # Check if exists in the program parameters
				if alias == None: return
				if alias in self.program_parameters: 
						raiseError(f"{alias} already exists!")
						return

				if a.manual_input(alias):
					if not a.generate_values(): return

					self.program_parameters[a.alias] = a
					raiseMessage(f"Parameter {a.alias} created correctly!")

				else: raiseError("An error ocurred adding the parameter!")

		elif len(args) == 1:
			if args[0] in avalible_parameters:
				a = avalible_parameters[args[0]]()

				alias = getInput("Alias for the parameter >> ") # Check if exists in the program parameters
				if alias == None: return
				if alias in self.program_parameters: 
						raiseError(f"{alias} already exists!")
						return

				if a.manual_input(alias):
					if not a.generate_values(): return

					self.program_parameters[a.alias] = a
					raiseMessage(f"Parameter {a.alias} created correctly!")

				else: raiseError("An error ocurred adding the parameter!")

		elif len(args) == 2:
			if args[0] in avalible_parameters:
				a = avalible_parameters[args[0]]()

				alias = getInput("Alias for the parameter >> ") # Check if exists in the program parameters
				if alias == None: return
				if alias in self.program_parameters:
						raiseError(f"{alias} already exists!")
						return

				if a.read_input(alias, args[1]):
					a.generate_values()
					print(a.values)
					self.program_parameters[a.alias] = a
					raiseMessage(f"Parameter {a.alias} created correctly!")
				else: raiseError("An error ocurred adding the parameter!")
		else:
			raiseError("Too many parameters!")
	
	def do_formats(self, s):
		print("+----------------+")
		print("|Avalible Formats|")
		print("+----------------+")
		if len(self.program_formats) == 0:
			raiseError("There aren't any formats!")
		for f in self.program_formats:
			print(f"{fg.green}{f}{rs.all} ~ {[x.alias for x in self.program_formats[f].parameters]}")

	def do_add_format(self, s):
		args = s.split()

		self.do_parameters(None)
		a = Format()

		if len(args) == 0:
			if a.manual_input(self.program_parameters):
				self.program_formats[a.alias] = a
				raiseMessage(f"Format {a} added correctly!")
			else:
				return

		elif len(args) > 1:

			temp_alias = args[0].strip()
			temp_parameters = args[1:].strip()
			temp_clean_parameters = []
			for p in temp_parameters:
				if p.endswith(","): # Remove last , of a string
					temp_string_list = list(p)
					temp_string_list.pop()
					p = "".join(temp_string_list)
				t = p.split(",")
				if not t == "":
					if type(t) == list:
						for x in t:
							temp_clean_parameters.append(x)
					else:
						temp_clean_parameters.append(t)
			print(temp_clean_parameters)
			if a.auto_input(self.program_parameters, temp_alias, temp_clean_parameters):
				self.program_formats[a.alias] = a
				raiseMessage(f"Format {a} added correctly!")
			else:
				return
		else:
			raiseError("Uncorrect usage!")
			return

	def do_generate_wordlist(self, s):
		try:
			if "," in s:
				args = s.split(",")
			else:
				args = s.split()
			formats = []
			if len(args) > 0:
				for a in args:
					if a in self.program_formats:
						formats.append(a)
					else:
						raiseError(f"Format {a} don't exist!")
						return

			else:
				self.do_formats(None)
				formats = getValues(message="Formats >> ")
				if formats == None: return

				for f in formats:
					if not f in self.program_formats:
						raiseError(f"Format {f} don't exist!")
						return

				if formats == None: return

			if len(formats) == 0: 
				raiseError("There aren't enought formats to create the wordlist!")
				return

			wordlist = []
			output = getInput("Output file >> ")
			if output == None: return

			raiseMessage("Creating wordlist...")
			total_number = 0
			for f in formats:
				values = []
				for p in self.program_formats[f].parameters:
					values.append(p.values)

				from itertools import product
				
				# Getting wordlist length
				numbers = []

				for values_group in values:
					a = len(values_group)
					numbers.append(a)
				result = numbers[0]

				for number in numbers[1:]:
					result *= number
				total_number += result

				raiseMessage(f"Generating wordlist with format {f} ({result} words)")

				checkpoint = result // 10
				count = 0
				percentage = 0
				for c in product(*values):
					if count == checkpoint:
						if not percentage == 100:
							percentage += 10
						raiseMessage(f"Generated {percentage}%...")
						count = 0
					word = "".join(c)
					# if not word in wordlist: wordlist.append(word)
					wordlist.append(word)
					count += 1


			raiseMessage(f"Wordlist created with {total_number} words!")
			raiseMessage(f"Writting wordlist into {output}...")

			with open(output, "w")as file:
				file.writelines("".join([x + "\n" for x in wordlist]))

			raiseMessage("Done!")
		except KeyboardInterrupt:
			raiseError("Wordlist generation process interrupted!")

	def do_rename_parameter(self, s):
		args = s.split()
		if len(args) == 0:
			value = getInput("Parameter >> ")
			if value == None: return

		elif len(args) == 1:
			value = args[0].strip()
		else:
			value = args[0].strip()

		if value in self.program_parameters:
			name = args[1].strip()
			self.program_parameters[value].alias = name
			raiseMessage(f"Parameter {value} renamed succesfully!")
		else:
			raiseError(f"Parameter {value} don't exists!")

	def do_append_parameter(self, s):
		args = s.split()
		if len(args) == 0:
			parameter_name = getInput("Parameter >> ")
		else:
			parameter_name = args[1].strip()

		
		if parameter_name == None: return

		if parameter_name in self.program_parameters:
			parameter = self.program_parameters[parameter_name]
			parameter.manual_input(parameter_name)
			parameter.generate_values()
		else:
			raiseError(f"Parameter {parameter_name} don't exists!")

	def do_remove_parameter(self, s):
		args = s.split()
		if len(args) == 0:
			parameter = getInput("Parameter >> ")

		elif len(args) == 1:
			parameter = args[0].strip()

		if parameter in self.program_parameters:
			self.program_parameters.pop(parameter)
			raiseMessage(f"Parameter {parameter} deleted!")
		else:
			raiseError(f"Parameter {parameter} don't exists!")

	def do_remove_format(self,s):
		args = s.split()
		if len(args) == 0:
			f = getInput("Format >> ")
			if f == None: return

		elif len(args) == 1:
			f = args[0].strip()

		if f in self.program_formats:
			program_formats.pop(f)
			raiseMessage(f"Format {f} deleted!")
		else:
			raiseError(f"Format {parameter} don't exists!")
	
	# HELPS

	def help_shell(self):
		print("Open a simple shell to execute system commands.")

	def help_exit(self):
		print("Exit from the program")

	def help_parameters(self):
		print("Show created parameters by the user.")

	def help_add_parameters(self):
		print("Add parameters. 3 usages:")
		print("add_parameter: It shows you avalible parameters ids.")
		print("add_parameter paramId: Create the parameter with paramId.")
		print("add_parameter paramId file: You can load words of a file to process them with the parameter function.")

	def help_formats(self):
		print("Show created formats by the user.")

	def help_add_format(self):
		print("Create a format. 2 usages:")
		print("add_format: It show you avalible created formats to add.")
		print("add_format alias params: It creates automatically a format with the alias and the parameters chosed. You can split them with spaces or commas.")
	
	def help_generate_wordlist(self):
		print("Generate a wordlist. 2 usages:")
		print("generate_wordlist: It shows you the avalible created formats.")
		print("generate_wordlist formats: It generates the wordlist with the entered formats.")

	def help_rename_parameter(self):
		print("Rename a parameter. 3 usages: ")
		print("rename_parameter: It asks you for the parameter and the alias.")
		print("rename_parameter parameter: It asks you for the new alias.")
		print("rename_parameter parameter newalias: Rename automatically parameter.")

	def help_remove_parameter(self):
		print("Remove a parameter. 2 usages: ")
		print("remove_parameter: It asks you for the name of the parameter to delete.")
		print("remove_parameter parameter: Delete automatically parameter.")

	def help_append_parameter(self):
		print("Append values to a parameter. 2 usages:")
		print("append_parameter: It will ask you for the parameter to choose.")
		print("append_parameter parameter: It will start the append.")

	def help_remove_format(self):
		print("Remove a format. 2 usages:")
		print("remove_format: It asks you for the name of the format to delete.")
		print("remove_format parameter: Delete automatically format.")

if __name__ == "__main__":
	__author__ = "Pabheto"
	main = Program()
	main.cmdloop()