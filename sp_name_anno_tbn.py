#!/bin/py

# Usage:
#       python sp_name_anno_tbn.py blastoutfile.fmt6 ac2sciname.mapfile prNtAc_table statfile 
#
# Asign species name and genus name to each mapped read
# according to accession number.

import re
import sys

# Load parameters
infile = sys.argv[1]
mapfile = sys.argv[2]
prNtAc_table = sys.argv[3]
statfile = sys.argv[4]

# Load accession and species relation map file
fmap = open(mapfile, 'r')
header = fmap.readline()
ac_map = {}
for line in fmap:
    tmp = re.split('\t\|\t', line.rstrip())
    if tmp[0] not in ac_map.keys():
        ac_map[tmp[0]] = (tmp[1], tmp[2])
fmap.close()

# Load relation table of protein and nuclei acid accessions
prNt_map = {}
fin = open(prNtAc_table, 'r')
fst_line = fin.readline()
for line in fin:
    tmp = re.split('\t', line.rstrip())
    if tmp[0] not in pr_nt_map.keys():
        prNt_map[tmp[0]] = tmp[1]
fin.close()


# get species name and genus name for each read
fin = open(infile, 'r')
stat = {}
for line in fin:
    tmp = re.split('\t', line.rstrip())
    pr_acc = re.split('\|', tmp[0])[3]
    pr_acc = re.split('\.', acc)[0]
    nt_acc = prNt_map[pr_acc][0]
    if nt_acc not in stat.keys():
        stat[nt_acc] = 1  # count read number mapped to this virus
    else:
        stat[nt_acc] += 1
fin.close()

fstat = open(statfile, 'w')
fstat.write("accession\tspecies\tgenus\tread No.\n")
# output statistic info
for each in stat.keys():
    fstat.write(each+'\t'+'\t'.join(ac_map[each])+'\t'+str(stat[each])+'\n')
fstat.close()



