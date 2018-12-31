# FvckPasswords2.0
Simple framework to generate wordlists.

# Usage
The program work using "objects". Parameters and formats.
You can create password formats using parameters.
A format is a group of parameters. For example a password could be compossed of VICTIM_NAME + SIMBOL + VICTIM_BIRTHDAY. Right, that is a format. Each value (VICTIM_NAME, SIMBOL, VICTIM_BIRTHDAY) is a parameter.
First of all, you have to create some parameters, for example, you can create a Name parameter for the VICTIM_NAME.
You enter to it some start values, and the parameter will use their own function to generate a list of values.
After all of this, you have to create a format, using parameters.
When you have created your format, you can generate a wordlist permutating each parameter values.

# Development
You can create new modules creating a new class that expands the Parameter class and then adding then to the avalible_parameters var in the parameters file.
By default, all classes that expand the Parameter class will ask for values ussing the function manual_input. There are other options that you can modify in the new parameters.
The special option of each parameter is generate_values.
