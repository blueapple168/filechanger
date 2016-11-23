#coding: utf-8
import os, sys, csv

IGNORED_FILE_ENDINGS = [".py", ".bat"]

VALID_ACTIONS = ["lower", "upper", "remove", "insert", "replace"]

def _get_file_ext(file):
	return os.path.splitext(file)[1]

def _confirm_continue(txt):
	raw_input(txt)

def _input(helptext, valid_input=None):
	inputtext = raw_input(helptext + ("\n(" + ", ".join(valid_input) + ")" if valid_input else "") + "\n> ")
	if valid_input:
		while not inputtext in valid_input:
			print(VALID_INPUT_IS_TEXT + ", ".join(valid_input))
			inputtext = raw_input("> ").lower()
	return inputtext

def _readcsv(path, delimiter):
	if not os.path.isfile(path):
		print(path + " does not exist!")
		exit(1)

	with open(path, 'rU') as f:
		reader = csv.reader(f, delimiter=delimiter)
		l = list(reader)
		return l

def _print_usage():
	print("Usage:")
	print("python csvrenamer.py CSV_FILE DIRECTORY (DELIMITER)")
	print("- CSV_FILE: Path to csv file")
	print("- DIRECTORY: directory to run in")
	print("- DELIMITER: delimiter in csv-file (default ',')")

def rename(working_dir, csv_file_location, delimiter=',', silent=True):
	file_mappings = _readcsv(csv_file_location, delimiter)

	has_confirmed = silent
	current_filename = ""
	changed_files = 0
	failed_files = 0

	for line in file_mappings:
		if (len(line) != 2):
			print("The line " + line + " is invalid. Ignoring...")
			continue
		old_path = line[0]
		new_path = line[1]

		if (not has_confirmed):
			print("Will run (in folder " + working_dir + ")")
			print("Original file name: " + old_path)
			print("New filename" + new_path)
			_confirm_continue("Click Enter to continue...")
			has_confirmed = True

		old_filename = os.path.join(working_dir, old_path)
		new_filename = os.path.join(working_dir, new_path)

		if os.path.exists(old_filename):
			print(old_filename + " > " + new_filename)
			os.rename(old_filename, new_filename)
			changed_files += 1
		else:
			print(old_filename + " did not exist!")
			failed_files += 1

	if not silent:
		if changed_files:
			print(str(changed_files) + " files were changed")
			if failed_files:
				print(str(failed_files) + " files could not be changed")
		elif failed_files:
			print(str(failed_files) + " files could not be changed")
		else:
			print("No files to change")


if __name__ == '__main__':
	if len(sys.argv) > 1:
		handle_special_input(sys.argv[1])
		working_dir = sys.argv[1]
	else:
		working_dir = _input("Path to directory: ")

	while not os.path.exists(working_dir):
		print("Invalid path")
		working_dir = _input("Path to directory: ")

	working_dir = os.path.abspath(working_dir)

	if len(sys.argv) > 2:
		csv_file_location = sys.argv[2]
	else:
		csv_file_location = _input("Path for csv file")

	delimiter = ","
	if len(sys.argv) > 3:
		delimiter = sys.argv[3]

	rename(working_dir, csv_file_location, delimiter)
	_confirm_continue("Click Enter to exit...")
