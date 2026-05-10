#!/usr/bin/env python3

import argparse
import sys
import gzip

parser = argparse.ArgumentParser()

parser.add_argument('input', help='Input file to work with.')
args = parser.parse_args()

# initialize all variables as zero
G = C = T = A = 0
g = c = t = a = 0
N = n = 0
total = 0

# open the gz file
with gzip.open(args.input, 'rt') as f:
	# iterate over each line
	for line in f:
		# check lines only if they are not header lines
		if line.startswith('>'):
			continue
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
