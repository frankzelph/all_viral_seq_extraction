# all_viral_seq_extraction
Extract all viral sequences from NGS data.
These codes build a blast database from the NGS data and blast search the database for the target sequences (eg. all_viral.fa). It would draw the coverage figures and extract fasta sequences for each virus whose mapped reads numbers is above a defined parameter "threshold" in "extract_seq.py" code file, the default of which is 100, and which could be modified as demand.

# Note: these codes are only tested in bio-linux system.
1. Some preparation.
    a. Install sqlite3, blast-2.5+, python2.7, 
firstly convert illumina fastq.gz file into fasta format

