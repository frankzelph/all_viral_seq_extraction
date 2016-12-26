# all_viral_seq_extraction
Extract all viral sequences from NGS data.
These codes build a blast database from the NGS data and blast search the database for the target sequences (eg. all_viral.fa). It would draw the coverage figures and extract fasta sequences for each virus whose mapped reads numbers is above a defined parameter "threshold" in "extract_seq.py" code file, the default of which is 100, and which could be modified as demand.

# Note: these codes are only tested in bio-linux system.
1. Some preparation.
    a. Install softwares including sqlite3, blast-2.5+, python2.7, R, and seqtk
    b. Download all viral sequences from NCBI:
       ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/
    c. Download taxonomy data from NCBI:
       ftp://ftp.ncbi.nih.gov/pub/taxonomy/

2. Asign the sequences with taxonomy information according to accession.
    a. Extract accessions from viral sequence file (in fasta format) by using "ac_extract.py".
    b. Build a SQL database of accession and taxid from "nucl_gb.accession2taxid" file.
    c. Search the SQL database, "names.dmp", "nodes.dmp", and "merged.dmp" by using "ac2sciname.py", to the species and family  scientific name of each accession.
    
3. Put all the other codes in the same directory with the NGS data in ".fastq.gz" format. Open a terminal and run the "blast_all.sh" bash codes as below: (# note: make sure all ".sh" file are excutable. if not, use "chmod u+x *.sh " to enable these code files excutably.)

    $ ./blast_all.sh


# The code will excute in a process as below:
       1. Convert illumina fastq.gz file into fasta format using "seqtk".
       2. Make a directory named as the NGS filename, and change working directory to this newly directory.
       3. Make a directory named "blastdb", and build a blast database in this directory by using the NGS fasta file.
       4. Make a directory named "blastout", blastn search all viral sequences from the database, and output the result file into "blastout"
       5. Do statistic of the mapped reads, including information of virus accession, virus species name, family name, and mapped reads counts.
       6. Draw coverage maps for each virus whose mapped reads number is above a defined paramter "threshold" in "coverage.py", and output the results into a newly made directory "cov_figs".
       7. Extract sequences for each virus whose mapped reads number is above a defined paramter "threshold" in "extract_seq.py", and output the reulsts into a newly made directory "seqs".

# Merge read1 and read2 file into one before blast
Just run as below:
    
    $ ./blast_all_2.sh   
It will call "merge_r1_r2.py" to merge read1 and read2 firstly, and then do blast.
