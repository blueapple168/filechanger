#coding: utf-8
import os, sys, csv

CLICK_ENTER_TO_CONTINUE_TEXT = "Klikk Enter for å fortsette: "
CLICK_ENTER_TO_EXIT = "Klikk Enter for å avslutte"
CHOOSE_DIRECTORY_TEXT = "Hvilken sti skal vi lagre filnavn fra: "
CHOOSE_CSV_LOCATION = "Hvor skal .csv filen lagres?"
INVALID_PATH = "Ikke en gyldig sti"
INCLUDE_DIRECTORIES_TEXT = "Skal mapper inkluderes?"

def get_file_ext(file):
	return os.path.splitext(file)[1]

def confirm_continue(txt):
	raw_input(txt)

def input(helptext, valid_input=None):
	inputtext = raw_input(helptext + ("\n(" + ", ".join(valid_input) + ")" if valid_input else "") + "\n> ")
	if valid_input:
		while not inputtext in valid_input:
			print(VALID_INPUT_IS_TEXT + ", ".join(valid_input))
			inputtext = raw_input("> ").lower()
	return inputtext

def write_csv(path, content):
	thefile = open(path, 'w')

	for item in content:
		thefile.write("%s\n" % item)

def print_usage():
	print("Bruk:")
	print("python csvrenamer.py CSV_FILE DIRECTORY (INCLUDE_DIRECTORIES)")
	print("- CSV_FILE: Where to create csv file")
	print("- DIRECTORY: directory to index")
	print("- INCLUDE_DIRECTORIES: whether or not to include directories (y/n)")


if len(sys.argv) > 1:
	handle_special_input(sys.argv[1])
	working_dir = sys.argv[1]
else:
	working_dir = input(CHOOSE_DIRECTORY_TEXT)

while not os.path.exists(working_dir):
	print(INVALID_PATH)
	working_dir = input(CHOOSE_DIRECTORY_TEXT)

working_dir = os.path.abspath(working_dir)

if len(sys.argv) > 2:
	csv_file_location = sys.argv[2]
else:
	csv_file_location = input(CHOOSE_CSV_LOCATION)

if len(sys.argv) > 3:
	include_directories = sys.argv[2]
else:
	include_directories = input(INCLUDE_DIRECTORIES_TEXT, ["y", "n"])

include_directories = True if include_directories == "y" else False

files = []
for path in os.listdir(working_dir):
	if os.path.isfile(os.path.join(working_dir, path)):
		files.append(path)
	elif os.path.isdir(os.path.join(working_dir, path)):
		if include_directories:
			files.append(path)

write_csv(csv_file_location, files)
confirm_continue(csv_file_location + " har blitt opprettet med " + str(len(files)) + " filnavn\n" + CLICK_ENTER_TO_EXIT)


