#!/bin/py
# Convert read1 and read2 fastq.gz file into fasta file, and merged them into one.
# Usage:
#       python merge_r1_r2.py read1.fastq.gz read2.fastq.gz merged.fasta
#

import sys
import os
import re
import datetime
from Bio import SeqIO




# function: merge two read files into one
def merge(read1_file, read2_file, merged_file):
    print " Merging", read1_file, "and", read2_file+"..."
    bashCommand = "cat "+read1_file+' '+read2_file +' > '+merged_file
    os.system(bashCommand)
    print " Removing "+read1_file+" and "+read2_file+"..."
    os.system("rm -rf "+read1_file)
    os.system("rm -rf "+read2_file)

# function: trim fastq, extract fasta file, and change the read_ids
def prepare_fasta(fastq_gz_file, read_direct, outfile):
    print " Preprocession of", fastq_gz_file
    fasta_file = re.split('\.', fastq_gz_file)[0]+'.fasta'
    bashcommand = "seqtk trimfq "+fastq_gz_file + ' > ' +fastq_gz_file+".fq"
    print " "+bashcommand
    os.system(bashcommand)
    bashcommand = "seqtk seq -A "+fastq_gz_file+".fq" + ' > ' +fasta_file
    print " "+bashcommand
    os.system(bashcommand)
    print " rm -rf "+fastq_gz_file+".fq"
    os.system("rm -rf "+fastq_gz_file+".fq")
    print " Assign read id with direction..."
    fh = open(fasta_file, 'r')
    fout = open(outfile, 'w')
    for record in SeqIO.parse(fh, 'fasta'):
        record.id += read_direct
        record.description = ''
        SeqIO.write(record, fout, 'fasta')
    fh.close()
    fout.close()
    print " rm -rf "+fasta_file
    os.system("rm -rf "+fasta_file)
    print " mv "+outfile+" "+fasta_file
    os.system("mv "+outfile+" "+fasta_file)
    return fasta_file

# function: parse file_list and combine two read file into one
def main(read1_file, read2_file, merged_file):
    print " Start from [", str(datetime.datetime.now())[:19], "]"
    # prepare read1 fasta file
    read1_fasta = prepare_fasta(read1_file, "-r1", "read1_tmp.fasta")
    # prepare read2 fasta file
    read2_fasta = prepare_fasta(read2_file, "-r2", "read2_tmp.fasta")    
    # merge the two fasta file into one    
    merge(read1_fasta, read2_fasta, merged_file)
    print " Finish at [", str(datetime.datetime.now())[:19], "]"

#============================ work =====================================#
read1_file = sys.argv[1]
read2_file = sys.argv[2]
merged_file = sys.argv[3]

main(read1_file, read2_file, merged_file)

