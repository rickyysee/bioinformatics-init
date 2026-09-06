#!/usr/bin/env python3

import sequence
import argparse

parser = argparse.ArgumentParser(description='gather counts of a fasta file')

# handle arguments and assign to variables
parser.add_argument('input', help='input file to work with')
parser.add_argument('-d', '--defline', action='store_true', help='gather statistics by defline')
parser.add_argument('-t', '--tsv', action='store_true', help='output as TSV format')
parser.add_argument('-a', '--all', action='store_true', help='distinguish masked bases if outputting in TSV format')
args = parser.parse_args()

fasta = args.input
byDef = args.defline
outTSV = args.tsv
outAll = args.all

# print a header line for TSV
if byDef:
	if outTSV and outAll:
		print(f'def\tG\tg\tC\tc\tT\tt\tA\ta\tN\tn\ttotal')
	if outTSV and not outAll:
		print(f'def\tG\tC\tT\tA\tN\ttotal')

# create a dictionary to store all results
results = {} # {defline: {G, g, ... N, n, total}}
this_defline = None

# read in the fasta
for defline, seq in sequence.read_fasta(fasta):

	# create a dictionary for the current defline
	this_defline = defline
	if this_defline not in results: results[this_defline] = {}
	counts = results[this_defline]

	# count the bases in this defline's sequence
	for nt in seq:
		if nt not in counts: counts[nt] = 0
		counts[nt] += 1
	
	### dictates whether to print out by defline ###
	if byDef == False: continue

	# store dictionary counts in variables for easier calling
	bases = ['G', 'g', 'C', 'c', 'T', 't', 'A', 'a', 'N', 'n']
	G, g, C, c, T, t, A, a, N, n = (counts.get(b, 0) for b in bases)
	total = G + g + C + c + T + t + A + a + N + n

	# do not print deflines with no sequence
	if total == 0: continue
	gc = (G + C + g + c) / total

	# print out counts depending on args
	if not outTSV:
		print(f'>{defline}')
		print(f'G:{G+g}\tC:{C+c}\tT:{T+t}\tA:{A+a}\tN:{N+n}')
		print(f'GC:{gc*100:.2f}%\ttotal:{total}')
		
	elif outAll:
		print(f'\'{defline}\'\t{G}\t{g}\t{C}\t{c}\t{T}\t{t}\t{A}\t{a}\t{N}\t{n}\t{total}')

	elif not outAll:
		print(f'\'{defline}\'\t{G+g}\t{C+c}\t{T+t}\t{A+a}\t{N+n}\t{total}')

if not byDef:

	# create a new dict with each base summed up
	totals = {}
	for defline, counts in results.items():
		for nt, count in counts.items():
			totals[nt] = totals.get(nt, 0) + count

	# store dictionary counts in variables for easier calling
	bases = ['G', 'g', 'C', 'c', 'T', 't', 'A', 'a', 'N', 'n']
	G, g, C, c, T, t, A, a, N, n = (totals.get(b, 0) for b in bases)
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
