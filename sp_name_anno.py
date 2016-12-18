#!/bin/py

# Usage:
#       python sp_name_anno.py blastoutfile.fmt6 ac2sciname.mapfile statfile 
#
# Asign species name and genus name to each mapped read
# according to accession number.

import re
import sys

# Load parameters
infile = sys.argv[1]
mapfile = sys.argv[2]
statfile = sys.argv[3]

# Load accession and species relation map file
fmap = open(mapfile, 'r')
header = fmap.readline()
ac_map = {}
for line in fmap:
    tmp = re.split('\t\|\t', line.rstrip())
    if tmp[0] not in ac_map.keys():
        ac_map[tmp[0]] = (tmp[1], tmp[2])
fmap.close()

# get species name and genus name for each read
fin = open(infile, 'r')
stat = {}
for line in fin:
    tmp = re.split('\t', line.rstrip())
    acc = re.split('\|', tmp[0])[3]
    acc = re.split('\.', acc)[0]
    if acc not in stat.keys():
        stat[acc] = [tmp[1]] # add readname
    else:
        stat[acc].append(tmp[1])
fin.close()

fstat = open(statfile, 'w')
fstat.write("accession\tspecies\tfamily\tread No.\n")
# output statistic info
for each in stat.keys():
    fstat.write(each+'\t'+'\t'.join(ac_map[each])+'\t'+str(len(stat[each]))+'\n')
fstat.close()



