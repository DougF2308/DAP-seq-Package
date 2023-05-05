import re
from collections import Counter
import sys
import os

def main(output_dir, input_file=None, output_file=None):
    # counter to count the occurrences of each gene
    gene_counter = Counter()

    # if no genes to process given
    if input_file is None:
        # If no input file is given, process all of the genes (all genes from output file)
        promoter_dirs = os.listdir(output_dir)
    else:
        # If an input file is given, read the names and use to filter the output directory
        with open(input_file) as f:
            promoter_dirs = [line.strip() for line in f]

    # loop over the output directory
    for promoter_dir in os.listdir(output_dir):
        if promoter_dir in promoter_dirs:
            promoter_path = os.path.join(output_dir, promoter_dir)
            # loop over the TF family directories in the gene directory
            for tf_family_dir in os.listdir(promoter_path):
                tf_family_path = os.path.join(promoter_path, tf_family_dir)
                # loop over the peak count files in the TF family directory
                for peak_count_file in os.listdir(tf_family_path):
                    # Read the count from the file and add it to the counter
                    with open(os.path.join(tf_family_path, peak_count_file)) as f:
                        # loop over the lines in the file
                        for line in f:
                            # Split the line on the colon character to get number of occurances
                            gene, count = re.split(r':\s*', line, maxsplit=1)
                            gene_counter[gene] += int(count)

    # write output file
    with open(output_file, 'w') as outfile:
        for gene, count in gene_counter.most_common():
            outfile.write(f'{gene}: {count}\n')

# main program           
if __name__ == '__main__':
    # output directory from the command line
    output_dir = sys.argv[1]
    # Get the input file name from the command line
    input_file = sys.argv[2] if len(sys.argv) > 2 else None
    # Get the output file name from the command line
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'TF_counts.txt'
    main(output_dir, input_file, output_file)


#use (command line): python abundance.py Output_file chosen_genes.txt output_name.txt

# Output_file is from dap_seq_script.py
#chosen_genes.txt is a sublist of genes from Output_file that you want to investigate abundance of peak genes in.
#Can even give in the original gene list the dap_seq_script ran off of if you want the abundance over the whole dataset.

