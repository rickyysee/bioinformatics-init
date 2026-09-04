#!/usr/bin/env python3

import sequence
import argparse
import sys
import gzip

parser = argparse.ArgumentParser(description='gather counts of a fasta file')

# add arguments that user can change
parser.add_argument('input', help='input file to work with')
parser.add_argument('-d', '--defline', action='store_true', help='gather statistics by defline')
args = parser.parse_args()

file = args.input
byDef = args.defline

# initialize dict for counts
counts = {}
if byDef == False:
	with gzip.open(args.input, 'rt') as f:
		# iterate over each line
		for line in f:
			# check lines only if they are not header lines
			if line.startswith('>'): continue
			G += line.count("G")
			C += line.count("C")
			T += line.count("T")
			A += line.count("A")
			g += line.count("g")
			c += line.count("c")
			t += line.count("t")
			a += line.count("a")
			N += line.count("N")
			n += line.count("n")
			total += len(line) - 1
	# print total counts per base
	print("G: ", G+g)
	print("C: ", C+c)
	print("T: ", T+t)
	print("A: ", A+a)
	print("N: ", N+n)
	print()
	# print various totals
	print("Total bases: ", total)
	print("Total unambiguous bases: ", total-N-n)
	print("Total unmasked bases: ", G+C+T+A)
	print("Total masked bases: ", g+c+t+a)
	print()
	# print GC content
	print("Total GC content: ", f"{(G+g+C+c)/(total-N-n)*100:.5}%")
	print("Unmasked GC content: ", f"{(G+C)/(G+C+T+A)*100:.5}%")
	print()

elif byDef == True:
	# start a dictionary to store results
	results = {} # { header: {G, C, A, T, N, total}}
	current_header = None
	with gzip.open(args.input, 'rt') as f:
		for line in f:
			if line.startswith('>'):
				current_header = line
				results[current_header] = defaultdict(int)
			elif current_header is not None:
				counts = results[current_header]
				counts['G'] += line.count('G')
				counts['C'] += line.count('C')
				counts['T'] += line.count('T')
				counts['A'] += line.count('A')
				counts['g'] += line.count('g')
				counts['c'] += line.count('c')
				counts['t'] += line.count('t')
				counts['a'] += line.count('a')
				counts['N'] += line.count('N')
				counts['n'] += line.count('n')
				counts['total'] += len(line) - 1
	for header, counts in results.items():
		total = counts['total']
		if total > 0:
			gc = (counts['G'] + counts['g'] + counts['C'] + counts['c']) / total * 100
			print(f"{header}  GC%: {gc:.2f}%  total_bases: {total}")
