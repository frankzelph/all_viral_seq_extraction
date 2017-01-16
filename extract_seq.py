#!/bin/py
#---------------------------------------------------------------------------------------------------------#
# Extract all the viral sequences of interest from bn6 file, with a threshold.
#
# usage: python extract_seq.py fasta_file blastoutfile_fmt6 stat_file threshold
#
#
# Parameter info:
#         fasta_file               the NGS data in fasta format
#         blastoutfile_fmt6        blast result file in format 6
#         stat_file                statistics info of the viral sequences
#         threshold                the minimum number of the reads for each virus to be extracted
#
#-----------------------------------------------------------------------------------------------------------#

import re
import sys
#import subprocess
import os


# get read ids from .bn6 file according to accession
def read_id(bn6_file, accession, outfile):
    fin = open(bn6_file, 'r')
    fout = open(outfile, 'w')
    for line in fin:
        tmp = re.split('\t', line.rstrip())
        acc = re.split('\|', tmp[0])[3]
        acc = re.split('\.', acc)[0]
        if acc == accession:
            fout.write(tmp[1]+'\n')
    fin.close()
    fout.close()

# get read ids from .bn6 file according to accession
def main(fasta_file, bn6_file, stat_file, threshold, outfolder):
    # Load viral accessions with the mapped reads No. of which are above threshold
    viral_name = {}
    fstat = open(stat_file, 'r')
    fstline = fstat.readline()
    for line in fstat:
        tmp = re.split('\t', line.rstrip())
        if int(tmp[-1]) < threshold:
            continue
        if tmp[0] not in viral_name.keys():
            viral_name[tmp[0]] = tmp[0]+'-'+re.sub('[\W\s]+', '_', tmp[1])
    fstat.close()
    print "Number of the mapped viruses (reads No. above:", threshold, "):", len(viral_name.keys())
    # Extract reads of each virus by using bash command
    for each in viral_name.keys():
        ids_file = outfolder+'/'+viral_name[each]+'.ids'
        out_seqfile = outfolder+'/'+viral_name[each]+'.fa'
        read_id(bn6_file, each, ids_file)
        bashCommand = 'seqtk subseq '+fasta_file+' '+ids_file+' > '+out_seqfile
        print bashCommand
        #subprocess.Popen(bashCommand)
        os.system(bashCommand)
        bashCommand = 'rm -rf '+ids_file
        print bashCommand
        os.system(bashCommand)

#===================begin work===========================#
fasta_file = sys.argv[1]
bn6_file = sys.argv[2]
stat_file = sys.argv[3]
threshold = int(sys.argv[4])
outfolder = sys.argv[5]

main(fasta_file, bn6_file, stat_file, threshold, outfolder)




