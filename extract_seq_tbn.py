#!/bin/py
#---------------------------------------------------------------------------------------------------------#
# Extract all the viral sequences of interest from bn6 file, with a threshold.
#
# usage: python extract_seq_tbn.py fasta_file blastoutfile_fmt6 stat_file threshold pr_nt_ac_table
#
#
# Parameter info:
#         fasta_file               the NGS data in fasta format
#         blastoutfile_fmt6        blast result file in format 6
#         stat_file                statistics info of the viral sequences
#         threshold                the minimum number of the reads for each virus to be extracted
#         pr_nt_ac_table           the relation table of protein and nuclei acid accession
#
#-----------------------------------------------------------------------------------------------------------#

import re
import sys
#import subprocess
import os

# Load relation table of protein and nuclei acid accessions
pr_nt_map = {}
fin = open(pr_nt_ac_table, 'r')
fst_line = fin.readline()
for line in fin:
    tmp = re.split('\t', line.rstrip())
    if tmp[0] not in pr_nt_map.keys():
        pr_nt_map[tmp[0]] = tmp[1]
fin.close()


# get read ids from .tbn6 file according to accession
def read_id(tbn6_file, accession, outfile):
    fin = open(tbn6_file, 'r')
    fout = open(outfile, 'w')
    for line in fin:
        tmp = re.split('\t', line.rstrip())
        pr_acc = re.split('\|', tmp[0])[3]
        pr_acc = re.split('\.', acc)[0]
        nt_acc = pr_nt_map[pr_acc]
        if nt_acc == accession:
            fout.write(tmp[1]+'\n')
    fin.close()
    fout.close()

# get read ids from .bn6 file according to accession
def main(fasta_file, bn6_file, stat_file, threshold):
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
        ids_file = "seqs/"+viral_name[each]+'.ids'
        out_seqfile = "seqs/"+viral_name[each]+'.fa'
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
tbn6_file = sys.argv[2]
stat_file = sys.argv[3]
threshold = int(sys.argv[4])
pr_nt_ac_table = sys.argv[5]

main(fasta_file, tbn6_file, stat_file, threshold)




