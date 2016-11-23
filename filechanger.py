#coding: utf-8
import os, sys

IGNORED_FILE_ENDINGS = [".py", ".bat"]
VALID_ACTIONS = ["lower", "upper", "remove", "insert", "replace"]

def _get_file_ext(file):
	"""
	>>> _get_file_ext("C:\\Program Files\test.txt")
	'.txt'
	>>> _get_file_ext("/Users/tomas/.bash_rc")
	''
	"""
	return os.path.splitext(file)[1]

def _confirm_continue(text):
	raw_input(text)

def _input(helptext, valid_input=None):
	inputtext = raw_input(helptext + ("\n(" + ", ".join(valid_input) + ")" if valid_input else "") + "\n> ")
	if valid_input:
		while not inputtext in valid_input:
			print("Valid input is " + ", ".join(valid_input))
			inputtext = raw_input("> ").lower()
	return inputtext

def _print_usage():
	print("Usage:")
	print("python renamer ACTION POSITION (TEXT)")
	print("- ACTION: replace, insert, remove, upper, lower")
	print("- POSITION: position eller start_position:end_position")

def _get_files_to_be_converted(dir, recursive):
	if not recursive:
		return [os.path.abspath(os.path.join(dir, x)) for x in os.listdir(dir) if not (os.path.isdir(x) or _get_file_ext(x) in IGNORED_FILE_ENDINGS)]
	convert_files = []
	for root, subFolders, files in os.walk(dir):
		if ".git" in root:
			continue
		for file in files:
			if not _get_file_ext(file) in IGNORED_FILE_ENDINGS:
				convert_files.append(os.path.join(root, file))
	return convert_files

def _to_upper_case(text, start_pos_pos, end_pos):
	"""
	>>> _to_upper_case("tomas", 3, 3)
	'toMas'
	>>> _to_upper_case("tomas", 3, 50)
	'toMAS'
	"""
	if end_pos == None:
		end_pos = start_pos_pos
	first_part = text[:start_pos_pos-1]
	last_part = text[end_pos:]
	upper_case_text = text[start_pos_pos-1:end_pos].upper()
	return first_part + upper_case_text + last_part


def _to_lower_case(text, start_pos_pos, end_pos):
	"""
	>>> _to_lower_case("TOMAS", 3, 4)
	'TOmaS'
	>>> _to_lower_case("TOMS", 3, 50)
	'TOms'
	>>> _to_lower_case("tomas", 3, 50)
	'tomas'
	"""
	if end_pos == None:
		end_pos = start_pos_pos
	first_part = text[:start_pos_pos-1]
	last_part = text[end_pos:]
	lower_case_text = text[start_pos_pos-1:end_pos].lower()
	return first_part + lower_case_text + last_part


def _remove_at_pos(text, start_pos_pos, end_pos):
	"""
	>>> _remove_at_pos("tomas", 3, 4)
	'tos'
	>>> _remove_at_pos("tomas", 3, 50)
	'to'
	"""
	if end_pos == None:
		return text[:start_pos_pos-1] + text[start_pos_pos:]
	else:
		return text[:start_pos_pos-1] + text[end_pos:]

def _handle_special_input(arg):
	if arg == "help":
		_print_usage()
		return True
	if arg == "test":
		import doctest
		doctest.testmod()
		return True
	return False

def _insert_at_pos(text, insert_text, pos):
	"""
	>>> _insert_at_pos("tomas", "Fi", 3)
	'toFimas'
	>>> _insert_at_pos("tomas", "Fi", 1)
	'Fitomas'
	"""
	return text[:pos-1] + insert_text + text[pos-1:]

def upper(working_dir, start_pos, end_pos, recursive=False):
	rename(working_dir, 'upper', start_pos, end_pos, recursive)

def lower(working_dir, start_pos, end_pos, recursive=False):
	rename(working_dir, 'lower', start_pos, end_pos, recursive)

def remove(working_dir, start_pos, end_pos, recursive=False):
	rename(working_dir, 'remove', start_pos, end_pos, recursive)

def insert(working_dir, start_pos, insert_text, recursive=False):
	rename(working_dir, 'insert', start_pos, start_pos, recursive, insert_text)

def replace(working_dir, start_pos, end_pos, insert_text, recursive=False):
	rename(working_dir, 'replace', start_pos, end_pos, recursive, insert_text)

def rename(working_dir, action, start_pos, end_pos, recursive, insert_text=None, quiet=True):
	has_confirmed = False
	current_filename = ""
	changed_files = 0

	files_to_be_converted = _get_files_to_be_converted(working_dir, recursive)
	for file in files_to_be_converted:
		path, filename = os.path.split(file)
		if (action.lower() == "lower"):
			new_filename = _to_lower_case(filename, start_pos, end_pos)
		elif (action.lower() == "upper"):
			new_filename = _to_upper_case(filename, start_pos, end_pos)
		elif (action.lower() == "remove"):
			new_filename = _remove_at_pos(filename, start_pos, end_pos)
		elif (action.lower() == "insert"):
			new_filename = _insert_at_pos(filename, insert_text, start_pos)
		elif (action.lower() == "replace"):
			new_filename = _remove_at_pos(filename, start_pos, end_pos)
			new_filename = _insert_at_pos(new_filename, insert_text, start_pos)
		else:
			_print_usage()
			return

		if new_filename == filename:
			continue

		if (not has_confirmed and not quiet):
			print("Will run (in folder " + working_dir + ") "
				+ action + " on position " + str(start_pos) + (" to " + str(end_pos) if end_pos else "") +
				(" with the word " + insert_text if insert_text else ""))
			print("Original filename: " + filename)
			print("New filename: " + new_filename)
			_confirm_continue("Click Enter to continue...")
			has_confirmed = True

		changed_files += 1

		new_filepath = os.path.join(path, new_filename)
		print(file + " > " + new_filename)

		os.rename(file, new_filepath)

	if changed_files:
		print("Changed " + str(changed_files) + " files")
	else:
		print("No files to be changed.")


if __name__ == '__main__':
	if len(sys.argv) > 1:
		if _handle_special_input(sys.argv[1]):
			exit()
		working_dir = sys.argv[1]
	else:
		working_dir = _input("Path to directory: ")

	while not os.path.exists(working_dir):
		print("Not a valid directory")
		working_dir = _input("Path to directory: ")

	working_dir = os.path.abspath(working_dir)

	if len(sys.argv) > 2:
		action = sys.argv[2]

	if not action or action not in VALID_ACTIONS:
		action = _input("Choose action", VALID_ACTIONS)

	if len(sys.argv) > 3:
		position = sys.argv[3]
		if ":" in position:
			start_pos = int(position.split(":")[0])
			end_pos = int(position.split(":")[1])
		else:
			start_pos = int(position)
			end_pos = None
	else:
		start_pos = int(_input("Start position: "))
		if action != "insert":
			end_pos = int(_input("End position: "))
		else:
			end_pos = None

	insert_text = False
	recursive = True
	if action in ["insert", "replace"]:
		if (len(sys.argv) > 4):
			insert_text = sys.argv[4]
		else:
			insert_text = _input("Text to be inserted: ")
		if (len(sys.argv) > 5):
			recursive = sys.argv[5] != "nonrecursive"
		else:
			if (len(sys.argv) < 4):
				recursive = _input("Should subfolders be included?", ["y", "n"]) == "y"
	else:
		if (len(sys.argv) > 4):
			recursive = sys.argv[4] != "nonrecursive"
		else:
			recursive = _input("Should subfolders be included?", ["y", "n"]) == "y"

	rename(working_dir, action, start_pos, end_pos, recursive, insert_text, False)
	_confirm_continue("Click Enter to exit...")
