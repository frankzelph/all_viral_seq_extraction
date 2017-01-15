#!/bin/bash

# The file of target sequences to be extracted in fasta format
query_seqfile=/home/immu/database/blastdb/viral/viral_all/viral_pr_from_gb.fna

# Accession and taxonomy relation database
ac_mapfile=/home/immu/database/blastdb/viral/ac2name/ac2sciname.txt

# num_threads used in blastn
num_threads=10

# If the number of the reads mapped to target A is above "threshold",
# all the reads mapped to this target would be extracted.
threshold=100

# A relation table of viral protein accession and genome accession
prNtAc_mapfile=/home/immu/database/blastdb/viral/viral_all/prNtAc_map.txt



# Merge read1 and read2 into one file.
# "file_list.txt" includes 3 columns gapped with a tab character "\t" in each line.
# 	column1		column2		column3
#	read1file	read2file	merged_file #(with no extension)
# The read files (NGS data) are in ".fastq.gz" file format.
# Then blast all merged fasta files in this directory.

while read read1_file read2_file merge_file;
do
	# check if there three columns for each line
	if [[ -z "${read1_file// }" ]] || [[ -z "${read2_file// }" ]] || [[ -z "${merge_file// }" ]]; then
		echo "Error: no three columns in a line."
		exit 1
	fi
	# Merge read1 and read2 into one fasta file
	if [ ! -f ${merge_file}.fasta ]; then
		python merge_r1_r2.py $read1_file $read2_file ${merge_file}.fasta
	fi
	# blastn search and target sequence extraction
	./viral_tblastn.sh ${merge_file}.fasta $query_seqfile $ac_mapfile $num_threads $threshold $prNtAc_mapfile
	
done < "$1" # file_list.txt

