#!/bin/bash

# merge read1 and read2 into one file
# "file_list.txt" includes 3 columns gapped with a tab character "\t" in each line.
# 	column1		column2		column3
#	read1file	read2file	merged_file #(with no extension)
# The read files (NGS data) are in ".fastq.gz" file format
# if [ ! -f ".*fasta" ] ; then
python merge_r1_r2.py file_list.txt
# fi

# blast all fasta file in this directory
for item in `ls `
do
	if [ -f "$item" ] && [[ $item == *"fasta" ]] ; then
		./viral_blast.sh $item /home/immu/database/blastdb/viral/viral_all/viral.fna
	fi
done


