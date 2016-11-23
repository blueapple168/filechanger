#coding: utf-8
import os, sys, csv


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

def _write_csv(path, content):
	thefile = open(path, 'w')

	for item in content:
		thefile.write("%s\n" % item)

def export(working_dir, csv_file_location=None, include_directories=False):
	files = []
	for path in os.listdir(working_dir):
		if os.path.isfile(os.path.join(working_dir, path)):
			files.append(path)
		elif os.path.isdir(os.path.join(working_dir, path)):
			if include_directories:
				files.append(path)
	if csv_file_location:
		_write_csv(csv_file_location, files)
	return files

def _print_usage():
	print("Usage:")
	print("python csvrenamer.py CSV_FILE DIRECTORY (INCLUDE_DIRECTORIES)")
	print("- CSV_FILE: Where to create csv file")
	print("- DIRECTORY: directory to index")
	print("- INCLUDE_DIRECTORIES: whether or not to include directories (y/n)")


if __name__ == '__main__':
	if len(sys.argv) > 1:
		handle_special_input(sys.argv[1])
		working_dir = sys.argv[1]
	else:
		working_dir = _input("Path to directory: ")

	while not os.path.exists(working_dir):
		print("Invalid path!")
		working_dir = _input("Path to directory: ")

	working_dir = os.path.abspath(working_dir)

	if len(sys.argv) > 2:
		csv_file_location = sys.argv[2]
	else:
		csv_file_location = _input("Where to save csv file? ")

	if len(sys.argv) > 3:
		include_directories = sys.argv[2]
	else:
		include_directories = _input("Include subfolders?", ["y", "n"])

	include_directories = True if include_directories == "y" else False

	files = export(working_dir, csv_file_location, include_directories)
	_confirm_continue(csv_file_location + " has been created with " + str(len(files)) + " file names\n" + "Click Enter to exit...")

