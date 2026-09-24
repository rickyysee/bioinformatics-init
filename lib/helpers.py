#!/usr/bin/env python3

# collection of python functions that are not necessarily exclusive to bioinformatics

import os
import argparse
from pathlib import Path

# handle arguments and assign variables for CLI usage
parser = argparse.ArgumentParser(description='non-bioinformatic helper functions')

parser.add_argument('directory', help='directory to search (can contain subdirectories)')
parser.add_argument('--search', help='string used to search for files (if none specified all files will be listed)')
parser.add_argument('--exclude', nargs='+', action='extend', help='directories not to parse')
args = parser.parse_args()

directory_path = args.directory
search_string = args.search
exclude_paths = args.exclude

# search a directory for files matching search string, optionally exclude some subdirectories
def find_files(directory, search, exclude):

	# keep a list of the files that meet search criteria
	found_files = []

	# recursively walk through each subdirectory
	for current, dirs, files in os.walk(directory):
		exclusion_flag = False
		
		# if the current directory has an excluded directory, mark it for exclusion
		if exclude:
			for path in exclude:
				if path in current: exclusion_flag = True

		# if current directory is marked for exclusion, go to next cycle
		if exclusion_flag == True: continue
		
		for file in files:
			# if search is specified and the string is not in the filename, go to next cycle
			if search and search not in file: continue
			found_file = os.path.join(current, file)

			# convert file to a path object and append it to overall list
			found_file = Path(found_file)
			found_files.append(found_file)

	return found_files

if __name__ == '__main__':
	# use CLI to search for files
	if directory_path: print(find_files(directory_path, search_string, exclude_paths))