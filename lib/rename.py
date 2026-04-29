#!/usr/bin/env python3

import argparse
import os

# Call the argument parser and set it to a simple variable
parser = argparse.ArgumentParser()

# Create arguments
parser.add_argument('input', help='The input file to rename. Only first column will be renamed.')
parser.add_argument('-r', '--rename', dest='rename', help='The file to use for renaming. Should have first and second columns as old and new.')
parser.add_argument('-o', '--output', help='The desired output directory. Defaults to current directory.')

# This will parse through arguments that the user has given at the CLI
args = parser.parse_args()

### Code
# Set default output directory and name
if args.output is None:
	output_path = f"{os.path.basename(args.input)}_renamed" # The default output will be ./${input}_renamed
else:
	output_path = os.path.join(args.output, os.path.basename(args.input)) # The output path will be ./${output}/${input}
	os.makedirs(args.output, exist_ok=True) # Make the directory if it doesn't exist

# Make a dictionary for the renaming
print(args)
rename = {}
with open(args.rename, 'r') as r:
	for line in r:
		line = line.strip()
		if not line:
			continue
		old, new, *_ = line.split()
		rename[old] = new

# Read input, rename input, and write to an output file
with open(args.input, 'r') as t, open(output_path, 'w') as o:
	for line in t:
		columns = line.strip().split()
		if columns[0] in rename:
			columns[0] = rename[columns[0]]
		o.write('\t'.join(columns) + '\n')

print("Content updated successfully.")