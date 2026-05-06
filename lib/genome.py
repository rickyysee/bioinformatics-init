#!/usr/bin/env python3

import argparse
import sys
import gzip

parser = argparse.ArgumentParser()

parser.add_argument('input', help='Input file to work with.')
args = parser.parse_args()

G = 0
C = 0
T = 0
A = 0
N = 0
total = 0

with gzip.open(args.input, 'rt') as f:
	for line in f:
		if not line.startswith('>'):
			for i in line:
				if i == 'G' or i == 'g':
					G += 1
					total += 1
				if i == 'C' or i == 'c':
					C += 1
					total += 1
				if i == 'T' or i == 't':
					T += 1
					total += 1
				if i == 'A' or i == 'a':
					A += 1
					total += 1
				if i == 'N' or i == 'n':
					N += 1
					total += 1


print("G: ", G)
print("C: ", C)
print("T: ", T)
print("A: ", A)
print("N: ", N)

print("Total is: ", total)
print("Total unmasked is: ", G+C+T+A)

print("GC content: ", f"{(G+C)/(G+C+T+A)*100:.5}%")
