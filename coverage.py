#!/bin/py
# draw coverage figure of a virus.
# Usage:
#       python coverage.py bn6_file stat_file threshold viralseq_db

import re
import sys
from Bio import SeqIO
from rpy2 import robjects
from rpy2.robjects.packages import importr

r = robjects.r
grdevices = importr('grDevices')


# get the viral sequence length according to the accession and viral_db
def seq_len(accession):
    for record in SeqIO.parse(VIRAL_DB, 'fasta'):
        tmp = record.id
        if "|" in tmp:
            tmp = re.split('\|', tmp)[3]
            tmp = re.split('\.', tmp)[0]
        if accession == tmp:
            return len(record.seq)
    return -1

# Calculate the coverage of each nucleotide 
def coverage(mapped_region, accession):
    if seq_len(accession) == -1:
        return -1
    cov = [0]*seq_len(accession)
    for each_read in mapped_region:
        for i in range(each_read[0]-1, each_read[1]):
            cov[i] += 1
    return cov

# define a function for drawing figures by using R
def cov_fig(cov, viral_name):
    x = robjects.IntVector(range(1, len(cov)+1))
    y = robjects.IntVector(cov)
    grdevices.png(file='cov_figs/'+viral_name+'.png', width = 1000, height = 300)
    r.plot(x=x, y=y, xlab="Nucleotide Position", ylab="Coverage", \
           main = viral_name, type='l')
    grdevices.dev_off()
    
# get virus name according to accession
def virus_name(accession, stat_file):
    fin = open(stat_file, 'r')
    fstline = fin.readline()
    viral_name = ""
    for line in fin:
        tmp = re.split('\t', line.rstrip())
        if tmp[0] == accession:
            viral_name = tmp[0]+'-'+re.sub('[\W\s]+', '_', tmp[1])
    fin.close()
    return viral_name

# get read ids from .bn6 file according to accession
def main(bn6_file, stat_file, threshold):
    # Load viral accessions with the mapped reads No. of which are above threshold
    mapped_region = {}
    fstat = open(stat_file, 'r')
    fstline = fstat.readline()
    for line in fstat:
        tmp = re.split('\t', line.rstrip())
        if int(tmp[-1]) < threshold:
            continue
        if tmp[0] not in mapped_region.keys():
            mapped_region[tmp[0]] = []
    fstat.close()        
    
    # load all mapped reads of each target sequence        
    fin = open(bn6_file, 'r')
    for line in fin:
        tmp = re.split('\t', line.rstrip())
        acc = re.split('\|', tmp[0])[3]
        acc = re.split('\.', acc)[0]
        if acc in mapped_region.keys():
            mapped_region[acc].append((int(tmp[6]), int(tmp[7])))
    fin.close()
    
    # draw coverage figures for each target sequence
    for key in mapped_region.keys():
        cov_fig(coverage(mapped_region[key], key), virus_name(key, stat_file))
    
        


#===================begin work===========================#
bn6_file = sys.argv[1]
stat_file = sys.argv[2]
threshold = int(sys.argv[3])
# Database location
VIRAL_DB = sys.argv[4] # "/home/immu/database/blastdb/viral/viral_all/viral.fna"

main(bn6_file, stat_file, threshold)

