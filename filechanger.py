#coding: utf-8
import os, sys

IGNORED_FILE_ENDINGS = [".py", ".bat"]
CLICK_ENTER_TO_CONTINUE_TEXT = "Klikk Enter for å fortsette: "
VALID_INPUT_IS_TEXT = "Gyldig input er "
CHOOSE_DIRECTORY_TEXT = "Hvilken sti vi skal endre filer i: "
CHOOSE_ACTION_TEXT = "Hva skal vi gjøre? "
ORIGINAL_FILENAME_TEXT = "original filnavn: "
NEW_FILENAME_TEXT = "nytt filnavn: "
START_POS_TEXT = "startposisjon: "
END_POS_TEXT = "sluttposisjon: "
INSERT_TEXT = "Tekst som skal settes inn: "
NO_FILES_TO_CHANGE_TEXT = "Ingen filer å endre"
RECURSIVE_TEXT = "Skal alle undermapper endres? "

def get_file_ext(file):
	return os.path.splitext(file)[1]

def confirm_continue():
	raw_input(CLICK_ENTER_TO_CONTINUE_TEXT)

def input(helptext, valid_input=None):
	inputtext = raw_input(helptext + ("\n(" + ", ".join(valid_input) + ")" if valid_input else "") + "\n> ")
	if valid_input:
		while not inputtext in valid_input:
			print(VALID_INPUT_IS_TEXT + ", ".join(valid_input))
			inputtext = raw_input("> ").lower()
	return inputtext

def print_usage():
	print("Bruk:")
	print("python renamer ACTION POSITION (TEXT)")
	print("- ACTION: replace, insert, remove, upper, lower")
	print("- POSITION: posisjon eller startposisjon:sluttposisjon")
	print("            Negative tall vil være posisjon fra enden")


def get_files_to_be_converted(dir, recursive):
	if not recursive:
		return [x for x in os.listdir(dir) if not (os.path.isdir(x) or get_file_ext(x) in IGNORED_FILE_ENDINGS)]
	convert_files = []
	for root, subFolders, files in os.walk(dir):
		if ".git" in root:
			continue
		for file in files:
			if not get_file_ext(file) in IGNORED_FILE_ENDINGS:
				convert_files.append(os.path.join(root, file))
	return convert_files

def to_upper_case(text, start_pos, end_pos):
	"""
	>>> to_upper_case("tomas", 3, 3)
	'toMas'
	>>> to_upper_case("tomas", 3, 50)
	'toMAS'
	"""
	if end_pos == None:
		end_pos = start_pos
	first_part = text[:start_pos-1]
	last_part = text[end_pos:]
	upper_case_text = text[start_pos-1:end_pos].upper()
	return first_part + upper_case_text + last_part


def to_lower_case(text, start_pos, end_pos):
	"""
	>>> to_lower_case("TOMAS", 3, 4)
	'TOmaS'
	>>> to_lower_case("TOMS", 3, 50)
	'TOms'
	>>> to_lower_case("tomas", 3, 50)
	'tomas'
	"""
	if end_pos == None:
		end_pos = start_pos
	first_part = text[:start_pos-1]
	last_part = text[end_pos:]
	lower_case_text = text[start_pos-1:end_pos].lower()
	return first_part + lower_case_text + last_part


def remove_at_pos(text, start_pos, end_pos):
	"""
	>>> remove_at_pos("tomas", 3, 4)
	'tos'
	>>> remove_at_pos("tomas", 3, 50)
	'to'
	"""
	if end_pos == None:
		return text[:start_pos-1] + text[start_pos:]
	else:
		return text[:start_pos-1] + text[end_pos:]

def handle_special_input(arg):
	if arg == "help":
		print_usage()
		exit()
	if arg == "test":
		import doctest
		doctest.testmod()
		exit()

def insert_at_pos(text, insert_text, pos):
	"""
	>>> insert_at_pos("tomas", "Fi", 3)
	'toFimas'
	>>> insert_at_pos("tomas", "Fi", 1)
	'Fitomas'
	"""
	return text[:pos-1] + insert_text + text[pos-1:]

if len(sys.argv) > 1:
	handle_special_input(sys.argv[1])
	working_dir = sys.argv[1]
else:
	working_dir = input(CHOOSE_DIRECTORY_TEXT)

while not os.path.exists(working_dir):
	print("Not a valid directory")
	working_dir = input(CHOOSE_DIRECTORY_TEXT)

working_dir = os.path.abspath(working_dir)

if len(sys.argv) > 2:
	action = sys.argv[2]
else:
	action = input(CHOOSE_ACTION_TEXT, ["lower", "upper", "remove", "insert", "replace"])

if len(sys.argv) > 3:
	position = sys.argv[3]
	if ":" in position:
		start = int(position.split(":")[0])
		slutt = int(position.split(":")[1])
	else:
		start = int(position)
		slutt = None
else:
	start = int(input(START_POS_TEXT))
	if action != "insert":
		slutt = int(input(END_POS_TEXT))
	else:
		slutt = None

insert_text = False
recursive = True
if action in ["insert", "replace"]:
	if (len(sys.argv) > 4):
		insert_text = sys.argv[4]
	else:
		insert_text = input(INSERT_TEXT)
	if (len(sys.argv) > 5):
		recursive = sys.argv[5] != "nonrecursive"
	else:
		if (len(sys.argv) < 4):
			recursive = input(RECURSIVE_TEXT, ["ja", "nei"]) == "ja"
else:
	if (len(sys.argv) > 4):
		recursive = sys.argv[4] != "nonrecursive"
	else:
		recursive = input(RECURSIVE_TEXT, ["ja", "nei"]) == "ja"

has_confirmed = False
current_filename = ""
changed_files = 0

files_to_be_converted = get_files_to_be_converted(working_dir, recursive)

for file in files_to_be_converted:
	path, filename = os.path.split(file)
	if (action.lower() == "lower"):
		new_filename = to_lower_case(filename, start, slutt)
	elif (action.lower() == "upper"):
		new_filename = to_upper_case(filename, start, slutt)
	elif (action.lower() == "remove"):
		new_filename = remove_at_pos(filename, start, slutt)
	elif (action.lower() == "insert"):
		new_filename = insert_at_pos(filename, insert_text, start)
	elif (action.lower() == "replace"):
		new_filename = remove_at_pos(filename, start, slutt)
		new_filename = insert_at_pos(new_filename, insert_text, start)
	else:
		print_usage()
		exit()

	if new_filename == filename:
		continue

	if (not has_confirmed):
		print("Kommer til å kjøre (i mappen " + working_dir + ") "
			+ action + " på posisjon " + str(start) + (" til " + str(slutt) if slutt else "") +
			(" med ordet " + insert_text if insert_text else ""))
		print(ORIGINAL_FILENAME_TEXT + filename)
		print(NEW_FILENAME_TEXT + new_filename)
		confirm_continue()
		has_confirmed = True
	changed_files += 1

	new_filepath = os.path.join(path, new_filename)
	print(file + " > " + new_filename)

	os.rename(file, new_filepath)

if changed_files:
	print("Endret " + str(changed_files) + " filer")
else:
	print(NO_FILES_TO_CHANGE_TEXT)

