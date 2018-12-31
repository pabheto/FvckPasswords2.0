from sty import fg,bg,rs

def raiseError(exception):
	print(f"{fg.red}{exception}{rs.all}")

def raiseMessage(message):
	print(f"{fg.cyan}[+]{rs.all} {message}")

def getInput(text):
	try:
		value = input(f"{fg.cyan}{text}{rs.all}")
		return value.strip()
	except KeyboardInterrupt:
		print(f"{fg.red}KeyboardInterrupt!{rs.all}")
		return

def getValues(message="Values >> "):
	try:
		value = input(f"{fg.cyan}{message}{rs.all}").strip()

		if "," in value:
			value_splitted = value.split(",")
			for v in value_splitted:
				v = v.strip()
				if v == "":
					value_splitted.remove(v)
			if len(value_splitted) > 1:
				return value_splitted
			else:
				final_value = []
				final_value.append(value_splitted.strip())
				return value
		else:
			final_value = []
			final_value.append(value)
			return final_value

	except KeyboardInterrupt:
		print(f"{fg.red}KeyboardInterrupt!{rs.all}")
		return

def createOption(question, default=True):
	# y = True, n = False
	if default:
		opc_text = f"{question} y/n (default = y) >> "
	else:
		opc_text = f"{question} y/n (default = y) >> "

	while True:
		try:
			opc = input(opc_text)
		except KeyboardInterrupt:
			break

		if opc == "y" or opc == "Y":
			return True
		elif opc == "n" or opc == "N":
			return False
		elif opc == "":
			return default
		else:
			print(f"{fg.red}Invalid option!{rs.all}")
	return 