#!/bin/bash

if [ ! -d "$3" ]
then
	mkdir ./$3
fi

for filename in "$2"*; do
	#name=$(echo "$filename" | cut -f 1 -d '.')
	python abundance.py "$1" "$filename" "$3""$(basename "$filename" .txt).txt"
done

#Use: ./abundance_loop.sh path/to/dap_seq_script/output_file path/to/gene/list/files/ path/to/output/directory

#Runs the abundance script over a file of different gene lists. Useful if for example, you have a dap-seq output file of all YUCCA genes, and want to find the abundance at each YUCCA gene individually.
#All run on same output file.