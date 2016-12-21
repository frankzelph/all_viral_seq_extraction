#!/bin/py
#---------------------------------------------------------------------------------------------------------#
# Get read ids of the viral sequences of interest from bn6 file.
#
# usage: python get_read_ids.py blastoutfile_fmt6 accession outfile
#
# eg. :  python get_read_ids.py hcv_r1.bn6 NC_018464 NC_018464.ids
#
# Parameter info:
#         blastoutfile_fmt6        blast result file in format 6
#         accession                Accession number of the virus of which the sequence would be extracted
#         outfile                  output the read ids into this fil, one id each line
#
#-----------------------------------------------------------------------------------------------------------#

import re
import sys

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

#===================begin work===========================#
bn6_file = sys.argv[1]
accession = sys.argv[2]
ids_outfile = sys.argv[3]

read_id(bn6_file, accession, ids_outfile)





