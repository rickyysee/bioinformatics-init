#!/usr/bin/env python3

import sequence
import argparse
import sys
import gzip

# handle args
parser = argparse.ArgumentParser(description='minimize a genome by capturing specified percent of each sequence')
parser.add_argument('input', help='input FASTA')
parser.add_argument('-p', '--percent', type=float, default=0.01, help='percent of file to capture [0.01]')
parser.add_argument('-w', '--width', type=int, default=80, help='width of each sequence line [80]')
parser.add_argument('-g', '--gtf', help='will instead minimize GTF file based on FASTA if deflines match')
args = parser.parse_args()

fasta = args.input
perc = args.percent
width = args.width
gtf = args.gtf

def mini_genome(fasta, perc, width):
	
	for defline, seq in sequence.read_fasta(fasta):
		print(f'>{defline}')

		# subset sequence by selected percentage
		end = int((len(seq) * perc) // 1)
		seq = seq[:end]

		# print lines in chunks of selected width
		for i in range(0, end, width):
			window = seq[i:i+width]
			print(window)

		print()

def mini_gtf(gtf, fasta):
	
	# make a dict with the length of each sequence in the fasta
	lengths = {}
	for defline, seq in sequence.read_fasta(fasta):
		id = defline.split()[0]
		length = len(seq)
		if id not in lengths: lengths[id] = length
		else:                 lengths[id] = 'Duplicate'
	
	# handle opening the gtf file
	if gtf.endswith('gz'):    fp = gzip.open(gtf, 'rt')
	elif gtf.endswith('gtf'): fp = open(gtf, 'rt')
	for line in fp:
		
		# clean the line, print comments, avoid lines not found in fasta
		line = line.strip()
		if line.startswith('#'): 
			print(line)
			continue
		if id not in lengths: continue

		# obtain the id, start, and end coordinate of each feature
		fields = line.split()
		id = fields[0]
		start = int(fields[3])
		end = int(fields[4])
		
		# set the limit of the features from the fasta length
		limit = lengths[id]

		# avoid any features that surpass the limit
		if start >= limit or end > limit: continue

		print(line)

	fp.close()

if not gtf: mini_genome(fasta, perc, width)
else:       mini_gtf(gtf, fasta)
