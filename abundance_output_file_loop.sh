#!/bin/bash

if [ ! -d "$3" ]
then
	mkdir ./$3
fi

for filename in "$1"*; do
	#echo $filename
	#name=$(echo "$filename" | cut -d/ -f2)
	#echo "$2"$(basename "$filename")
	./abundance_loop.sh "$filename" "$2"$(basename "$filename") "$3"
done

#Use: ./abundance_output_file_loop.sh path/to/dap_seq_script/output_files/ path/to/gene/list/files/directory/ path/to/output/directory/

#Runs abundance.sh over many output directories. This is pretty much only for use with clusters, it runs the abundance_loop.sh file over a directory
#of output files, matching them up with lists of genes in a directory with the same name, so for clusters itd match cluster_1 output with cluster_1 gene list
#Not needed outside of clusters really

#files in gene list directory must be named the same as the corresponding output file, eg. output named cluster_1 will be matched with gene list named cluster_1