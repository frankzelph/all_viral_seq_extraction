#!/bin/bash
#---------------------------------------------------------------------------------------------------------#
# Extract all reads from the NGS datasets according to viral accession numbers.
# usage: 
#        python extract_seq.py seq_file blastoutfile_fmt6 accession outfile
#
# eg. :  python extract_seq.py HCV22_S27_L003_R1_001.fasta hcv_r1.bn6 NC_018464 NC_018464.fa
#----------------------------------------------------------------------------------------------------------#

python get_read_ids.py ./blastout/HKU28_S25_L003_R1_001.bn6 NC_009019 NC_009019_r1.ids
seqtk subseq HKU28_S25_L003_R1_001.fasta NC_009019_r1.ids > NC_009019_r1.fa

python get_read_ids.py ./blastout/HKU28_S25_L003_R2_001.bn6 NC_009019 NC_009019_r2.ids
seqtk subseq HKU28_S25_L003_R2_001.fasta NC_009019_r2.ids > NC_009019_r2.fa

