#!/bin/bash

# blast all fastq.gz file in this directory

for item in `ls `
do
	if [ -f "$item" ] && [[ $item == *"fastq.gz" ]] ; then
		./viral_blast.sh $item /home/immu/database/blastdb/viral/viral_all/viral.fna
	fi
done


