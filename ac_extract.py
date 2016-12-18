#!/bin/py

# get accession numbers of every sequence in a fasta file

from Bio import SeqIO
import re
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

fout=open(outfile, 'w')
for each in SeqIO.parse(infile, 'fasta'):
    ac = re.split('\|', each.id)[3]
    fout.write(ac+'\n')
fout.close()


