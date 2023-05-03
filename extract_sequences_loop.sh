#!/bin/bash

if [ ! -d "$3" ]
then
	mkdir ./$3
fi

for filename in "$1"*; do
	#name=$(echo "$filename" | cut -f 1 -d '.')
	./extract_sequences.sh "$filename" "$2" "$3""$(basename "$filename" .fasta).fasta"
done

#Use: ./extract_sequences_loop.sh path/to/gene/lists path/to/promoter/library path/to/output/directory

#Runs the extract_sequences.sh file over a directory of lists of genes, useful if you have a directory of clusters of genes for example