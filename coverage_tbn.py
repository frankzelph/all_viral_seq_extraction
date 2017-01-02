#!/bin/py
# draw coverage figure of a virus.
# Usage:
#       python coverage_tbn.py bn6_file ac2sci_file threshold pr_nt_ac_table

import re
import sys
from Bio import SeqIO
from rpy2 import robjects
from rpy2.robjects.packages import importr

r = robjects.r
grdevices = importr('grDevices')

# Load relation table of protein and nuclei acid accessions
pr_nt_map = {}
nt_len = {}
fin = open(pr_nt_ac_table, 'r')
fst_line = fin.readline()
for line in fin:
    tmp = re.split('\t', line.rstrip())
    if tmp[0] not in pr_nt_map.keys():
        pr_nt_map[tmp[0]] = tmp[1:]
    if tmp[1] not in nt_len.keys():
        nt_len[tmp[1]] = tmp[2]
fin.close()


# Convert protein coordinates into nuclei acid coordinates
def convt(pr_acc, pr_start, pr_end):
    if pr_start > pr_end:
        tmp = pr_start
        pr_start = pr_end
        pr_end = tmp
    nt_start = pr_start*3 + int(pr_nt_map[pr_acc][2])
    nt_end = pr_end*3 + int(pr_nt_map[pr_acc][2])
    # if nt_end > int(pr_nt_map[pr_acc][3]):
    #    print "Error: protein end out of cds range!"
    #    return -1
	return (nt_start, nt_end)
	
# Calculate the coverage of each nucleotide 
def coverage(mapped_region, accession):
    cov = [0]*nt_len[accession]
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
        nt_acc = tmp[0]
        if nt_acc not in mapped_region.keys():
            mapped_region[nt_acc] = []
    fstat.close()        
    
    # load all mapped reads of each target sequence        
    fin = open(bn6_file, 'r')
    for line in fin:
        tmp = re.split('\t', line.rstrip())
        pr_acc = re.split('\|', tmp[0])[3]
        pr_acc = re.split('\.', acc)[0]
        nt_acc = pr_nt_map[pr_acc][0]
        if nt_acc in mapped_region.keys():
            mapped_region[nt_acc].append(convt(pr_acc, int(tmp[6]), int(tmp[7])))
    fin.close()
    
    # draw coverage figures for each target sequence
    for key in mapped_region.keys():
        cov_fig(coverage(mapped_region[key], key), virus_name(key, stat_file))
    
        


#===================begin work===========================#
bn6_file = sys.argv[1]
stat_file = sys.argv[2]
threshold = int(sys.argv[3])
# Database location
pr_nt_ac_table = sys.argv[4]

main(bn6_file, stat_file, threshold)

