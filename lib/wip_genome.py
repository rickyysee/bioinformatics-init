#!/usr/bin/env python3

import argparse
import sys
import gzip
from collections import Counter

parser = argparse.ArgumentParser()

parser.add_argument('input', help='Input file to work with.')
args = parser.parse_args()

G = C = T = A = g = c = t = a = N = n = 0

with gzip.open(args.input, 'rt', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith('>'):
            continue  # skip header lines
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

total = G + C + T + A + g + c + t + a + N + n


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

"""
bases = Counter(
G = 0,
C = 0,
T = 0,
A = 0,
g = 0,
c = 0,
t = 0,
a = 0,
N = 0,
n = 0
)

# Open the gz file
with gzip.open(args.input, 'rt') as f:
	for line in f:
		if not line.startswith('>'):
			bases.update(line.rstrip('\n'))

# Print total counts per base
for base in bases:
	print(f"{base}: {bases[base]}")

print("G: ", bases['G']+bases['g'])
print("C: ", bases['C']+bases['c'])
print("T: ", bases['T']+bases['t'])
print("A: ", bases['A']+bases['a'])
print("N: ", bases['N']+bases['n'])

print()

# Print various totals
print("Total bases: ", sum(bases.values()))
print("Total unambiguous bases: ", sum(bases.values())-bases['N']-bases['n'])
print("Total unmasked bases: ", bases['G']+bases['C']+bases['T']+bases['A'])
print("Total masked bases: ", bases['g']+bases['c']+bases['t']+bases['a'])

print()

# Print GC content
print("Total GC content: ", f"{(bases['G']+bases['C']+bases['g']+bases['c'])/(sum(bases.values())-bases['N']-bases['n'])*100:.5}%")
print("Unmasked GC content: ", f"{(bases['G']+bases['C'])/(bases['G']+bases['C']+bases['T']+bases['A'])*100:.5}%")

print()
"""