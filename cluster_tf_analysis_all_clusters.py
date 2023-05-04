import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tf_list", help="path to file containing list of TFs")
    parser.add_argument("input_directory", help="path to input directory containing cluster directories")
    parser.add_argument("output_file", help="path to output file")
    args = parser.parse_args()

    # Read in list of TFs
    tf_list = {}
    with open(args.tf_list, 'r') as f:
        for line in f:
            tf = line.strip().split(':')[0]
            tf_list[tf] = set()

    # Traverse through all peak counts files and count number of genes each TF appears in
    for root, dirs, files in os.walk(args.input_directory):
        for file in files:
            if file == 'peak_counts.txt':
                tf_path = os.path.join(root, file)
                with open(tf_path, 'r') as f:
                    lines = f.readlines()
                    gene = os.path.basename(os.path.dirname(os.path.dirname(tf_path)))
                    for line in lines:
                        tf = line.strip().split('_')[0]
                        if tf in tf_list:
                            tf_list[tf].add(gene)

    # Write output to file
    with open(args.output_file, 'w') as f:
        for tf, genes in tf_list.items():
            f.write(f"{tf}: {len(genes)}\n")

if __name__ == '__main__':
    main()
