#!/bin/py
# Creat a relation table of protein and nuclei acid accession 
# according to viral.genomic genbank format file.
# Usage:
#       python prNtAc_map.py viral_nt.gbff prNtAc_map.txt
#
#-------------------------------------------------------------------#

import re
from Bio import SeqIO
import sys

# read a genbank file and extract some info
def gb_extract(gbfile, outfile, pr_seqfile):
    fgb = open(gbfile, 'r')
    fout = open(outfile, 'w')
    fseq = open(pr_seqfile, 'w')
    fout.write("protein_ac\tgenome_ac\tgenome_length\tcds_start\tcds_end\n")
    for record in SeqIO.parse(fgb, 'genbank'):
        ac = re.split('\.', record.id)[0]
        seqlen = len(record.seq)
        for fet in record.features:
            if fet.type == "CDS":
                if 'protein_id' not in fet.qualifiers:
                    continue
                pr_ac = re.split('\.', fet.qualifiers['protein_id'][0])[0]
                if 'translation' not in fet.qualifiers:
                    continue
                pr_seq = fet.qualifiers['translation'][0]
                start = int(fet.location.start)
                end = int(fet.location.end)
                fout.write('\t'.join([pr_ac, ac, str(seqlen), str(start), str(end)])+'\n')
                fseq.write('>gi|123456|ref|'+pr_ac+'|\n')
                fseq.write(pr_seq+'\n')
    fgb.close()
    fout.close()
    fseq.close()


#================begin job======================#
gbfile = sys.argv[1]
outfile = sys.argv[2]
pr_seqfile = sys.argv[3]

gb_extract(gbfile, outfile, pr_seqfile)
