#!/usr/bin/env python3

import sequence
import argparse
import gzip

parser = argparse.ArgumentParser(description='gather counts of a fasta file')

# handle arguments and assign to variables
parser.add_argument('input', help='input file to work with')
parser.add_argument('-d', '--defline', action='store_true', help='gather statistics by defline')
args = parser.parse_args()

file = args.input
byDef = args.defline

if byDef == False:
	# count bases with dict
	counts = {}
	for defline, seq in sequence.read_fasta(file):
		for nt in seq:
			if nt not in counts: counts[nt] = 0
			counts[nt] += 1

	# initialize variables based on a set alphabet
	bases = ['G', 'g', 'C', 'c', 'T', 't', 'A', 'a', 'N', 'n']
	G, g, C, c, T, t, A, a, N, n = (counts.get(b, 0) for b in bases)
	total = G + g + C + c + T + t + A + a + N + n

	# print total counts per base
	print(f'G: {G+g}')
	print(f'C: {C+c}')
	print(f'T: {T+t}')
	print(f'A: {A+a}')
	print(f'N: {N+n}')
	print()
	# print various totals
	print(f'Total bases: {total}')
	print(f'Total unambiguous bases: {total-N-n}')
	print(f'Total unmasked bases: {G+C+T+A}')
	print(f'Total masked bases: {g+c+t+a}')
	print()
	# print GC content
	print(f'Total GC content: {(G+g+C+c)/(total-N-n)*100:.5}%')
	print(f'Unmasked GC content: {(G+C)/(G+C+T+A)*100:.5}%')


elif byDef == True:
	# create a dictionary to store all results
	results = {} # {defline: {G, g, ... N, n, total}}
	this_defline = None

	# read in the fasta
	for defline, seq in sequence.read_fasta(file):

		# create a dictionary for the current defline
		this_defline = defline
		if this_defline not in results: results[this_defline] = {}
		counts = results[this_defline]

		# count the bases in this defline's sequence
		for nt in seq:
			if nt not in counts: counts[nt] = 0
			counts[nt] += 1

		# store dictionary counts in variables for easier calling
		bases = ['G', 'g', 'C', 'c', 'T', 't', 'A', 'a', 'N', 'n']
		G, g, C, c, T, t, A, a, N, n = (counts.get(b, 0) for b in bases)
		total = G + g + C + c + T + t + A + a + N + n

		# do not print deflines with no sequence
		if total == 0: continue

		gc = (G + C + g + c) / total

		print(f'>{defline}')
		print(f'G:{G+g}\tC:{C+c}\tT:{T+t}\tA:{A+a}\tN:{N+n}')
		print(f'GC:{gc*100:.2f}%\ttotal:{total}')
		