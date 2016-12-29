#!/bin/bash

# The file of target sequences to be extracted in fasta format
query_seqfile=/home/immu/database/blastdb/viral/viral_all/viral.fna

# Accession and taxonomy relation database
ac_mapfile=/home/immu/database/blastdb/viral/ac2name/ac2sciname.txt

# num_threads used in blastn
num_threads=10

# the limitation of the number of mapped reads to be extracted
threshold=100

# blast all fastq.gz file in this directory

for item in `ls `
do
	if [ -f "$item" ] && [[ $item == *"fastq.gz" ]] ; then
		./viral_blastn.sh $item $query_seqfile $ac_mapfile $num_threads $threshold
	fi
done


