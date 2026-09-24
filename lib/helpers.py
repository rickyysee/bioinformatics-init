#!/usr/bin/env python3

# collection of python functions that are not necessarily exclusive to bioinformatics

import os
import argparse

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
				# if path not in current: print(current, dirs, files)
				if path in current: exclusion_flag = True
		# else: print(current, dirs, files)

		# if current directory is marked for exclusion, go to next cycle
		if exclusion_flag == True: continue
		
		# add any found files to the overall list
		for file in files:
			if search and search not in file: continue
			found_file = os.path.join(current, file)
			found_files.append(found_file)

	return found_files

if __name__ == '__main__':
	# use CLI to search for files
	if directory_path: print(find_files(directory_path, search_string, exclude_paths))