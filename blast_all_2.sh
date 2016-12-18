#!/bin/bash

# merge read1 and read2 into one file
python merge_r1_r2.py file_list.txt

# blast all fasta file in this directory
for item in `ls `
do
	if [ -f "$item" ] && [[ $item == *"fasta" ]] ; then
		./viral_blast.sh $item /home/immu/database/blastdb/viral/viral_all/viral.fna
	fi
done


