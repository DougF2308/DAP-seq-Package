import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory", help="path to input directory containing gene directories")
    parser.add_argument("output_file", help="path to output file")
    parser.add_argument("threshold", type=float, help="minimum percentage of genes a TF must bind to be included")
    args = parser.parse_args()

    gene_files = os.listdir(args.input_directory)
    tf_counts = {}

    for gene_file in gene_files:
        gene_path = os.path.join(args.input_directory, gene_file)
        if not os.path.isdir(gene_path):
            continue

        tf_directories = os.listdir(gene_path)
        for tf_directory in tf_directories:
            tf_path = os.path.join(gene_path, tf_directory, 'peak_counts.txt')
            if not os.path.isfile(tf_path):
                continue

            with open(tf_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    tf, count = line.strip().split(': ')
                    count = int(count)
                    tf_name = tf.split('_')[0]  # extract the TF name before the first "_"
                    if tf_name not in tf_counts:
                        tf_counts[tf_name] = 0
                    tf_counts[tf_name] += count

    with open(args.output_file, 'w') as f:
        for tf, count in tf_counts.items():
            percentage = count / len(gene_files) * 100
            if percentage >= args.threshold:
                f.write(f"{tf}: {percentage:.2f}%\n")

if __name__ == '__main__':
    main()
