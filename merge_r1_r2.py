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
def main(read1_file, read2_file, merged_file):
	read1_fasta = re.split('\.', read1_file)[0]+'.fasta'
        read2_fasta = re.split('\.', read2_file)[0]+'.fasta'
        merged_file = merged_file+'.fasta'
        # prepare read1 fasta file
        bashcommand = "seqtk trimfq "+read1_file + ' > ' +read1_file+".fq"
        os.system(bashcommand)
        bashcommand = "seqtk seq -A "+read1_file+".fq" + ' > ' +read1_fasta
        os.system(bashcommand)
        os.system("rm -rf "+read1_file+".fq")
        
        change_rid(read1_fasta, "-r1", "read1_tmp.fasta")
        # prepare read2 fasta file
        bashcommand = "seqtk trimfq "+read2_file + ' > ' +read2_file+".fq"
        os.system(bashcommand)
        bashcommand = "seqtk seq -A "+read2_file+".fq" + ' > ' +read2_fasta
        os.system(bashcommand)
        os.system("rm -rf "+read1_file+".fq")
        change_rid(read2_fasta, "-r2", "read2_tmp.fasta")
        # merge the two fasta file into one
        merge(read1_fasta, read2_fasta, merged_file)

#============================ work =====================================#
read1_file = sys.argv[1]
read2_file = sys.argv[2]
merged_file = sys.argv[3]

main(read1_file, read2_file, merged_file)

