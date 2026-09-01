#!/usr/bin/env python3

import gzip
import sys

# parse through fasta file to get defline and seq
# adapted from Ian Korf
def read_fasta(file):
	if file == '-':            fp = sys.stdin
	elif file.endswith('.gz'): fp = gzip.open(file, 'rt')
	else:                      fp = open(file)

	# initialize a dict
	fasta_d = {}
	defline = None

	# strip each line and assign to key or value list of dict
	for line in fp:
		line = line.rstrip()
		if line == '': continue
		if line.startswith('>'):
			defline = line[1:]
			fasta_d[defline] = []
		elif defline is not None:
			fasta_d[defline].append(line)

	# yield the id and sequence for each record
	for seq_id, seq_list in fasta_d.items():
		yield(seq_id, ''.join(seq_list))
	fp.close()

# transcribe dna to rna
def transcribe(dna):
	return dna.replace('T', 'U')

# get the reverse complement of a dna sequence
def revcomp(dna):
	rc = []
	for nt in dna[::-1]:
		if   nt == 'A': rc.append('T')
		elif nt == 'C': rc.append('G')
		elif nt == 'G': rc.append('C')
		elif nt == 'T': rc.append('A')
		else:           rc.append('N')
	return ''.join(rc) 

# get GC composition of a dna sequence
def gc_comp(seq):
	return (seq.count('C') + seq.count('G')) / len(seq)

# get the GC-skew along length of a dna sequence
def gc_skew(seq):
	c = seq.count('C')
	g = seq.count('G')
	if c + g == 0: return 0
	return (g - c) / (g + c)



AMINOKD = {
	'I' :  4.5,	'V' :  4.2,	'L' :  3.8, 'F' :  2.8, 'C' :  2.5,
	'M' :  1.9,	'A' :  1.8,	'G' : -0.4, 'T' : -0.7, 'S' : -0.8,
	'W' : -0.9, 'Y' : -1.3, 'P' : -1.6, 'H' : -3.2, 'E' : -3.5,
	'Q' : -3.5, 'D' : -3.5, 'N' : -3.5, 'K' : -3.9, 'R' : -4.5
}

# calculate total hydrophobicity using kyle-dolittle scores
def kyte_doolittle(seq):
	kd = 0
	for aa in seq:
		if aa in AMINOKD: kd += AMINOKD[aa]
	return kd

# translate a dna sequence to amino acid sequence

CODONS = {
	'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
	'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
	'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
	'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W',
	'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
	'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
	'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
	'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
	'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
	'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
	'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
	'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
	'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
	'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
	'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
	'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G'
}

# convert dna sequence to protein sequence using codon dict
def translate(dna):
	codons = ('ATG', 'TAA', 'TAG', 'TGA')
	aminos = 'M***'
	aas = []
	for i in range(0, len(dna), 3):
		codon = dna[i:i+3]
		if codon in codons:
			idx = codons.index(codon)
			aa = aminos[idx]
			aas.append(aa)
		else:
			aas.append('X')
	return ''.join(aas)