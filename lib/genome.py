#!/usr/bin/env python3

import sequence
import argparse
import gzip

parser = argparse.ArgumentParser(description='gather counts of a fasta file')

# add arguments that user can change
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

	# create an ordered dictionary with default 0 values to initialize variables
	bases = ['G', 'g', 'C', 'c', 'T', 't', 'A', 'a', 'N', 'n']
	bases_counts = {b: counts.get(b, 0) for b in bases}
	G, g, C, c, T, t, A, a, N, n = (counts.get(b, 0) for b in bases)
	total = G+g+C+c+T+t+A+a+N+n

	# print total counts per base
	print('G: ', G+g)
	print('C: ', C+c)
	print('T: ', T+t)
	print('A: ', A+a)
	print('N: ', N+n)
	print()
	# print various totals
	print('Total bases: ', total)
	print('Total unambiguous bases: ', total-N-n)
	print('Total unmasked bases: ', G+C+T+A)
	print('Total masked bases: ', g+c+t+a)
	print()
	# print GC content
	print('Total GC content: ', f'{(G+g+C+c)/(total-N-n)*100:.5}%')
	print('Unmasked GC content: ', f'{(G+C)/(G+C+T+A)*100:.5}%')


elif byDef == True:
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	"""
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
			print(f'{header}  GC%: {gc:.2f}%  total_bases: {total}')
	"""
