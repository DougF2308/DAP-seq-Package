import sys
import os
from multiprocessing import Process, Manager
import time

# Get the file paths from the command line arguments
promoter_sequences_path = sys.argv[1]
dap_data_v4_path = sys.argv[2]
Output_file = sys.argv[3]

# Create the output directory if it doesn't already exist
if not os.path.exists(Output_file):
    os.makedirs(Output_file)

promoter_sequences = []

# Read in the promoter sequences from a fasta file
with open(promoter_sequences_path, 'r') as fasta_file:
    for line in fasta_file:
        if line.startswith('>'):
            promoter_sequences.append({'name': line.strip()[1:], 'sequence': ''})
        else:
            promoter_sequences[-1]['sequence'] += line.strip()

# Read in the narrow peaks from the .narrowPeak files in the TF_family directories
narrow_peaks = []
for tf_family_dir in os.listdir(os.path.join(dap_data_v4_path, 'peaks')):
    tf_family_path = os.path.join(dap_data_v4_path, 'peaks', tf_family_dir)
    if os.path.isdir(tf_family_path):
        for tf_gene_dir in os.listdir(tf_family_path):
            tf_gene_path = os.path.join(tf_family_path, tf_gene_dir)
            if os.path.isdir(tf_gene_path):
                for chromosome_dir in os.listdir(tf_gene_path):
                    chromosome_path = os.path.join(tf_gene_path, chromosome_dir)
                    if os.path.isdir(chromosome_path):
                        for narrow_peak_file in os.listdir(chromosome_path):
                            if narrow_peak_file.endswith('.narrowPeak'):
                                try:
                                    with open(os.path.join(chromosome_path, narrow_peak_file), 'r') as f:
                                        for line in f:
                                            try:
                                                fields = line.strip().split('\t')
                                                peak = {
                                                    'chr': fields[0],
                                                    'start': int(fields[1]),
                                                    'end': int(fields[2]),
                                                    'tf_family': tf_family_dir,
                                                    'gene': tf_gene_dir,
                                                }
                                                narrow_peaks.append(peak)
                                            except ValueError:
                                                print("Error: Invalid narrow peak data found in file", narrow_peak_file)
                                except FileNotFoundError:
                                    print("Error: File not found: ", os.path.join(chromosome_path, narrow_peak_file))

# Search for instances of peaks in the promoter sequences and count the number of instances per TF gene
peaks_in_promoters = {}


#def search_for_instances(narrow_peaks, promoter_sequences, peaks_in_promoters):
def search_for_instances():
    for peak in narrow_peaks:
        for promoter in promoter_sequences:
            # split the promoter name to get the chromosome and chromosomal positions
            promoter_name, promoter_chr_pos = promoter['name'].split(' | ')
            promoter_chr, promoter_positions = promoter_chr_pos.split(':')
            promoter_positions_temp = promoter_positions.split(' ')[0]
            promoter_start, promoter_end = map(int, promoter_positions_temp.split('-'))
            # Check if the peak is on the same chromosome as the promoter and if its position is within the promoter's boundaries
            if peak['chr'] == promoter_chr and peak['start'] >= promoter_start and peak['end'] <= promoter_end:
                if promoter['name'] not in peaks_in_promoters:
                    peaks_in_promoters[promoter['name']] = {}

                if peak['tf_family'] not in peaks_in_promoters[promoter['name']]:
                    peaks_in_promoters[promoter['name']][peak['tf_family']] = {}
                if peak['gene'] not in peaks_in_promoters[promoter['name']].get(peak['tf_family'], {}):
                    peaks_in_promoters[promoter['name']][peak['tf_family']][peak['gene']] = 1
                else:
                    peaks_in_promoters[promoter['name']][peak['tf_family']][peak['gene']] += 1


search_for_instances()

#MULTIPROCESSING TEST - NOT WORKING
#if __name__ == '__main__':
#    NUM_PROCESSES = 4
#    manager = Manager()
#    peaks_in_promoters = manager.dict()
#    processes = []
#    chunk_size = len(narrow_peaks) // NUM_PROCESSES
#    for i in range(NUM_PROCESSES):
#        start = i * chunk_size
#        end = (i + 1) * chunk_size
#        p = Process(target=search_for_instances, args=(narrow_peaks, promoter_sequences, peaks_in_promoters))
#        processes.append(p)
#        p.start()
#
#    for p in processes:
#        p.join()

# Create the output directories and write the peak counts to the  files
for promoter_name, tf_families in peaks_in_promoters.items():
    promoter_dir = os.path.join(Output_file, promoter_name.split(' | ')[0])
    if not os.path.exists(promoter_dir):
        os.makedirs(promoter_dir)
    for tf_family, genes in tf_families.items():
        tf_family_dir = os.path.join(promoter_dir, tf_family)
        if not os.path.exists(tf_family_dir):
            os.makedirs(tf_family_dir)
        with open(os.path.join(tf_family_dir, 'peak_counts.txt'), 'w') as f:
            for gene, count in genes.items():
                f.write(f'{gene}: {count}\n')

# Use (command line): python dap_seq_script.py promoter_sequences.fasta dap_data_v4 output_file_name

#Takes in a fasta file of sequences, outputs instances of all TF binding sites in DAP-seq library

#promoter_sequences.fasta is a fasta file of the promoter sequences of genes of interest, obtained from extract_sequences.sh

#dap_data_v4 is the DAP-seq library

#output_file_name is the name of the output DIRECTORY. NO FILE EXTENSION
