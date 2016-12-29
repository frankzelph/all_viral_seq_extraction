#!/bin/py
# Convert read1 and read2 fastq.gz file into fasta file, and merged them into one.
# Usage:
#       python merge_r1_r2.py file_list.txt
#

import sys
import os
import re
from Bio import SeqIO




# function: merge two read files into one
def merge(read1_file, read2_file, merged_file):
    bashCommand = "cat "+read1_file+' '+read2_file +' > '+merged_file
    os.system(bashCommand)
    os.system("rm -rf "+read1_file)
    os.system("rm -rf "+read2_file)

# function: change the read_ids in the NGS data
def change_rid(fasta_file, read_direct, outfile):
    fh = open(fasta_file, 'r')
    fout = open(outfile, 'w')
    for record in SeqIO.parse(fh, 'fasta'):
        record.id += read_direct
        record.description = ''
        SeqIO.write(record, fout, 'fasta')
    fh.close()
    fout.close()
    os.system("rm -rf "+fasta_file)
    os.system("mv "+outfile+" "+fasta_file)
        

# function: parse file_list and combine two read file into one
def main(file_list):
    fin = open(file_list, 'r')
    for line in fin:
        tmp = re.split('\t', line.rstrip())
        if len(tmp) != 3:
            print "Error: some line in list file \""+file_list+"\" has not 3 columns."
            os.system("exit 1")
            return 1
        read1_file = tmp[0]
        read1_fasta = re.split('\.', read1_file)[0]+'.fasta'
        read2_file = tmp[1]
        read2_fasta = re.split('\.', read2_file)[0]+'.fasta'
        merged_file = tmp[2]+'.fasta'
        # prepare read1 fasta file
        bashcommand = "seqtk seq -A "+read1_file + ' > ' +read1_fasta
        os.system(bashcommand)
        
        change_rid(read1_fasta, "-r1", "read1_tmp.fasta")
        # prepare read2 fasta file
        bashcommand = "seqtk seq -A "+read2_file + ' > ' +read2_fasta
        os.system(bashcommand)
        change_rid(read2_fasta, "-r2", "read2_tmp.fasta")
        # merge the two fasta file into one
        merge(read1_fasta, read2_fasta, merged_file)
    fin.close()

#============================ work =====================================#
file_list = sys.argv[1]
main(file_list)

