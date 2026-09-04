# minimize a genome by capturing the first n% of each defline

import sequence
import argparse
import sys

parser = argparse.ArgumentParser(description='minimize a genome by capturing specified percent of each sequence')
parser.add_argument('input', help='input FASTA file')
parser.add_argument('-p', '--percent', type=float, default=0.01, help='percent of file to capture [0.01]')
parser.add_argument('-w', '--width', type=int, default=80, help='width of each sequence line [80]')
args = parser.parse_args()

file = args.input
perc = args.percent
width = args.width

for defline, seq in sequence.read_fasta(file):
	print(f'>{defline}')

	# subset sequence by selected percentage
	end = int((len(seq) * perc) // 1)
	seq = seq[:end]

	# print lines in chunks of selected width
	for i in range(0, end, width):
		window = seq[i:i+width]
		print(window)

	print()