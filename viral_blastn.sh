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

# the limitation of the number of mapped reads to be extracted
threshold=$5


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
if [ ! -f "${file}.fasta" ]; then
    echo "Convert \"${gz_file}\" into fasta format."
    seqtk seq -A $gz_file > ${file}.fasta
fi

echo " Change directory to \"${file}\"."
cd $file
# make a folder to store blast database files
if [ ! -d "blastdb" ]; then
    echo " Make a directory named \"blastdb\"."
    mkdir "blastdb"
fi
# make a folder to store blast results
if [ ! -d "blastout" ]; then
    echo " Make a directory named \"blastout\"."
    mkdir "blastout"
fi

# makeblastdb
if [ ! -f "blastdb/${file}.nhr" ] && [ ! -f "blastdb/${file}.00.nhr" ]; then
    echo " Build a blast database from \"${file}.fasta\" file..."
    makeblastdb -in ../${file}.fasta -dbtype nucl -parse_seqids -out blastdb/$file
fi

# blast all viral sequences against the read database
if [ ! -f "blastout/${file}.bn6" ]; then
    echo " Blastn search all viral sequences from the built database..."
    blastn -query $query_seqfile -out "blastout/${file}.bn6" -db blastdb/$file -outfmt 6 -evalue 1e-5 -num_threads $num_threads -max_target_seqs 100000000
fi

# delete the database
# rm -rf ${file}/blastdb/${file}*

# do statistics and annotation
if [ ! -f "${file}.stat" ]; then
    echo " Do statistics of the mapped viral reads..."
    python ../sp_name_anno.py "blastout/${file}.bn6" $ac_mapfile ${file}.stat
fi

# extract all viral sequences with the No. of mapped reads above threshold
echo " Drawing coverage figures for those viruses of whose mapped reads number are above threshold..."
rm -rf cov_figs
if [ ! -d "cov_figs" ]; then
    mkdir "cov_figs"
fi

python ../coverage.py "blastout/${file}.bn6" "${file}.stat" $threshold

# extract all viral sequences with the No. of mapped reads above threshold
echo " Extracting those reads from the original fasta file..."
rm -rf seqs
if [ ! -d "seqs" ]; then
    mkdir "seqs"
fi
python ../extract_seq.py ../${file}.fasta blastout/${file}.bn6 ${file}.stat $threshold

echo " Finished searching from $gz_file."
echo
echo




























