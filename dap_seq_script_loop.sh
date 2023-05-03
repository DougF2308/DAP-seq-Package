#!/bin/bash

for filename in "$1"*.fasta; do
	name=$(echo "$filename" | cut -f 1 -d '.')
	python dap_seq_script.py "$filename" "$2" "$3""_""$name" &
done

#Use: ./dap_seq_script_loop.sh path/to/promoter/sequence/files path/to/dap_data path/to/output/file

#Runs the dap_seq_script over a directory of promoter sequences, produces a file containing output files for all input files. Again useful for the likes of a group of clusters you want to run it on for example.
#This adds the name of the promoter sequences file onto the end of the output file name you provide.