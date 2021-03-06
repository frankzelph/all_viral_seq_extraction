#!/bin/bash

#===================================================================#
# 1. Build blast database by using the NGS datasets
#   a. Decompression and fastq_to_fasta convertion

#   b. Make blast database

# 2. Blast all viral sequences against the made blast_database

# 3. Do statistics and annotation of the blast result.

#------------------------------------------------------------------#
# Load parameters

# ".fastq.gz" or ".fasta" filename
gz_file=$1

# The file of target sequences to be extracted in fasta format
query_seqfile=$2

# Accession and taxonomy relation database
ac_mapfile=$3

# num_threads used in blastn
num_threads=$4

# If the number of the reads mapped to target A is above "threshold",
# all the reads mapped to this target would be extracted.
threshold=$5

# A relation table of viral protein accession and genome accession
prNtAc_mapfile=$6


echo " NGS data: $gz_file"
echo " Query sequence file: $query_seqfile"


# remove file extension
file=${gz_file%%.*}

# make a folder named as the same with the file
if [ ! -d $file ]; then
    echo " Make a directory named \"${file}\"." 
    mkdir $file
fi

# convert .fastq.gz file into .fasta file
if [ ! -f ${file}.fasta ]; then
    echo "Convert \"${gz_file}\" into fasta format."
    seqtk trimfq $gz_file > ${file}.fq
    seqtk seq -A ${file}.fq > ${file}.fasta
fi

echo " Change directory to \"${file}\"."
cd $file
# make a folder to store blast database files
if [ ! -d blastdb ]; then
    echo " Make a directory named \"blastdb\"."
    mkdir "blastdb"
fi
# make a folder to store blast results
if [ ! -d blastout ]; then
    echo " Make a directory named \"blastout\"."
    mkdir "blastout"
fi

# makeblastdb
if [ ! -f blastdb/${file}.nhr ] && [ ! -f blastdb/${file}.00.nhr ]; then
    echo " Build a blast database from \"${file}.fasta\" file..."
    makeblastdb -in "../${file}.fasta" -dbtype nucl -parse_seqids -out blastdb/$file
fi

# blast all viral sequences against the read database
if [ ! -f "blastout/${file}.tbn6" ]; then
    echo " tblastn search all viral sequences from the built database..."
    tblastn -query $query_seqfile -out "blastout/${file}.tbn6" -db blastdb/$file -outfmt 6 -evalue 1e-5 -num_threads $num_threads -max_target_seqs 100000000
fi

# delete the database
# rm -rf ${file}/blastdb/${file}*

# do statistics and annotation
if [ ! -f "${file}-pr.stat" ]; then
    echo " Do statistics of the mapped viral reads..."
    python ../sp_name_anno_tbn.py "blastout/${file}.tbn6" $ac_mapfile $prNtAc_mapfile ${file}-pr.stat
fi

# extract all viral sequences with the No. of mapped reads above threshold
echo " Drawing coverage figures for those viruses of whose mapped reads number are above $threshold..."
# rm -rf cov_figs
if [ ! -d "tbn_cov_figs" ]; then
    mkdir "tbn_cov_figs"
fi

python ../coverage_tbn.py "blastout/${file}.tbn6" "${file}-pr.stat" $threshold $prNtAc_mapfile tbn_cov_figs

# extract all viral sequences with the No. of mapped reads above threshold
echo " Extracting those reads from the original fasta file..."
# rm -rf seqs
if [ ! -d "tbn_seqs" ]; then
    mkdir "tbn_seqs"
fi
python ../extract_seq_tbn.py ../${file}.fasta blastout/${file}.tbn6 ${file}-pr.stat $threshold $prNtAc_mapfile tbn_seqs

echo " Finished searching from $gz_file."
echo
echo




























