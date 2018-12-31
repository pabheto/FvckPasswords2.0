from sty import fg,bg,rs
from core import *

class Parameter(object):
	pid = ""
	description = ""
	
	def __init__(self):
		self.values = []
		self.start_vector = None

	def auto_input(self, alias, values):
		self.alias = alias
		self.values = values
		return True

	def manual_input(self, alias):
		print(self.description)
		self.alias = alias

		vector = getValues()
		if vector == None: return

		self.set_initial_vector(vector)

		return True

	def read_input(self, alias, file=""):
		print(self.description)
		self.alias = alias

		if file == "":
			file = getInput("File to read >> ")

		if file == None:
			return
		try:
			with open(file, "r") as read_file:
				vector = read_file.readlines()
				self.start_vector = []
				self.multiple = True
				for v in vector:
					v = v.strip()
					self.start_vector.append(v)
				return True
		except Exception as e:
			raiseError(e)
			return

	def set_initial_vector(self, vector):
		if vector == None:
			return
		self.start_vector = list(vector)

	def generate_values(self):
		pass

		"""try:
			value = input(f"{fg.cyan}Value >> {rs.all}")

			if "," in value:
				value_splitted = value.split(",")
				self.start_vector = value_splitted
				self.multiple = True
			else:
				self.start_vector = value
				self.multiple = False

		except KeyboardInterrupt:
			print(f"{fg.red}KeyboardInterrupt!{rs.all}")
			return"""

	def __str__(self):
		return self.alias

class Name(Parameter):
	pid = "Name"
	description = "Parameter to enter names."

	def generate_values(self):
		clean_name_opc = createOption("Clean name format?")

		if clean_name_opc == None: return
		if clean_name_opc:
			upper_first_opc = createOption("Upper first letter?")
			if upper_first_opc == None: return
			if upper_first_opc:
				for v in self.start_vector:
					self.values.append(v.lower())
					self.values.append(v.lower().capitalize())
			else:
				for v in self.start_vector:
					self.values.append(v.lower())
		else:
			self.values.append(self.start_vector)

		return True

class Simbol(Parameter):
	pid = "Simbol"
	description = "Parameter to store simbols or words without modifications."

	def generate_values(self):
		for v in self.start_vector:
			self.values.append(v)
		return True

class Number(Parameter):
	pid = "Number"
	description = "Parameter to enter numbers and do some permutations."

	def generate_values(self):
		for v in self.start_vector:
			self.values.append(v)
		return True

class Date(Parameter):
	pid = "Date"
	description = "Parameter that can permutate dates. Enter the dates in format dd/mm/yyyy (without '/')"

	def do_permutation(self, *parameters):
		
		params = []
		for p in parameters:
			params.append(p)

		from itertools import permutations

		perms = list(permutations(params))
		final_perms = []
		for p in perms:
			a = "".join(p)
			final_perms.append(a)
		return final_perms



	def date_permutations(self, date):
		day = date[0:2]
		month = date[2:4]
		year = date[4:8]
		half_year = date[6:8]

		"""
		Returned values:
		[0] day
		[1] month
		[2] year
		[3] half_year
		[4] day + month + year
		[5] day + month
		[6] day + year
		[7] month + year
		[8] day + month + half_year
		[9] day + month
		[10] day + half_year
		[11] month + half_year 
		"""
		final_permutations = [
			[day],
			[month],
			[year],
			[half_year],
			self.do_permutation(day, month, year),
			self.do_permutation(day, month),
			self.do_permutation(day, year),
			self.do_permutation(month, year),
			self.do_permutation(day, month, half_year),
			self.do_permutation(day, month),
			self.do_permutation(day, half_year),
			self.do_permutation(month, half_year)
		]
		for v in final_permutations:
			if v == None: return

		return final_permutations

	def generate_values(self):
		for d in self.start_vector:
			if not len(d) == 8:
				raiseError(f"Date '{d}' is not valid!")
				return

		print("""
-------------------------
- [0] day
- [1] month
- [2] year
- [3] half_year
- [4] day + month + year
- [5] day + month
- [6] day + year
- [7] month + year
- [8] day + month + half_year
- [9] day + month
- [10] day + half_year
- [11] month + half_year
-------------------------
		""")
		print("Select which permutations do you want to do, you can select multiple values in format 1,2,3")
		numbers_stringlist = getValues()
		numbers_numberlist = []

		if numbers_stringlist == None: return

		for n in numbers_stringlist:
			try:
				numbers_numberlist.append(int(n))
			except:
				raiseError(f"{n} is not a valid base 10 number!")
				return

		for d in self.start_vector:
			perms = self.date_permutations(d)
			if perms == None: return
			for n in numbers_numberlist:
				if n in range(0,12):
					for p in perms[n]:
						self.values.append(p)
				else: return

		return True


class FileRead(Parameter):
	pid = "FileRead"
	description = "Parameter that just store words of a file. In values enter the name of the files."

	def generate_values(self):
		for v in self.start_vector:
			try:
				with open(v, "r") as file:
					text = file.readlines()
					text_strip = []
					for t in text:
						text_strip.append(t.strip("\n"))

					for t in text_strip:
						self.values.append(t)
			except Exception as e:
				raiseError(e)
				return
		return True

avalible_parameters = {"Name" : Name, "Simbol" : Simbol, "Number" : Number, "Date" : Date, "FileRead" : FileRead}