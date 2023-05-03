#!/bin/bash
grep -A13 -f "$1" "$2" | sed -r ':a;N;$!ba;s/^(>.+)(\n--\n)/\1\2/g' | sed '/^--$/d' >"$3"

#use: ./extract_sequences.sh gene_names.txt all_sequences.fasta selected_sequences.fasta

#Produces a fasta file of sequences if given a list of genes

#gene_names.txt is a file containing TAIR identifiers for genes of interest in the format: 
#AT2G14960
#AT4G37390
#AT2G23170
#AT1G14120

#all_sequences.fasta is a fasta file containing sequences for 1000bp upstream of translation start

#selected_sequences.fasta is output, can be named anything.fasta