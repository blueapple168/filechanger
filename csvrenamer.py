#coding: utf-8
import os, sys, csv

IGNORED_FILE_ENDINGS = [".py", ".bat"]
CLICK_ENTER_TO_CONTINUE_TEXT = "Klikk Enter for å fortsette: "
CLICK_ENTER_TO_EXIT = "Klikk Enter for å avslutte"
CHOOSE_DIRECTORY_TEXT = "Hvilken sti vi skal endre filer i: "
CHOOSE_CSV_LOCATION = "Sti til .csv fil"
ORIGINAL_FILENAME_TEXT = "original filnavn: "
NEW_FILENAME_TEXT = "nytt filnavn: "
NO_FILES_TO_CHANGE_TEXT = "Ingen filer å endre"
INVALID_PATH = "Ikke en gyldig sti"

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
		print(path + " eksisterer ikke!")
		exit(1)

	with open(path, 'rU') as f:
		reader = csv.reader(f, delimiter=delimiter)
		l = list(reader)
		return l

def _print_usage():
	print("Bruk:")
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
			print("Linjen " + line + " er ugyldig. Ignoreres")
			continue
		old_path = line[0]
		new_path = line[1]

		if (not has_confirmed):
			print("Kommer til å kjøre (i mappen " + working_dir + ")")
			print(ORIGINAL_FILENAME_TEXT + old_path)
			print(NEW_FILENAME_TEXT + new_path)
			_confirm_continue(CLICK_ENTER_TO_CONTINUE_TEXT)
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
			print("Endret " + str(changed_files) + " filer")
			if failed_files:
				print("Kunne ikke endre " + str(failed_files) + " filer")
		elif failed_files:
			print("Kunne ikke endre " + str(failed_files) + " filer")
		else:
			print(NO_FILES_TO_CHANGE_TEXT)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		handle_special_input(sys.argv[1])
		working_dir = sys.argv[1]
	else:
		working_dir = _input(CHOOSE_DIRECTORY_TEXT)

	while not os.path.exists(working_dir):
		print(INVALID_PATH)
		working_dir = _input(CHOOSE_DIRECTORY_TEXT)

	working_dir = os.path.abspath(working_dir)

	if len(sys.argv) > 2:
		csv_file_location = sys.argv[2]
	else:
		csv_file_location = _input(CHOOSE_CSV_LOCATION)

	delimiter = ","
	if len(sys.argv) > 3:
		delimiter = sys.argv[3]

	rename(working_dir, csv_file_location, delimiter)
	_confirm_continue(CLICK_ENTER_TO_EXIT)
