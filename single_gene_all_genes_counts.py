import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input file containing TF names")
    parser.add_argument("counts_directory", help="path to directory containing count.txt files")
    parser.add_argument("output_file", help="path to output file")
    args = parser.parse_args()

    # Create a set of TF names to search for
    with open(args.input_file, 'r') as f:
        tf_names = set(line.strip().split(':')[0] for line in f.readlines())

    # Loop through the count.txt files in the directory and count the number of unique TFs
    # that appear in each file
    tf_counts = {tf: 0 for tf in tf_names}
    for file_name in os.listdir(args.counts_directory):
        if not file_name.endswith('.txt'):
            continue

        file_path = os.path.join(args.counts_directory, file_name)
        file_tf_counts = {tf: False for tf in tf_names}
        with open(file_path, 'r') as f:
            for line in f.readlines():
                tf = line.strip().split('_')[0]
                if tf in tf_names and not file_tf_counts[tf]:
                    file_tf_counts[tf] = True
                    tf_counts[tf] += 1

    # Write the results to the output file
    with open(args.output_file, 'w') as f:
        for tf, count in tf_counts.items():
            f.write(f"{tf}: {count}\n")

if __name__ == '__main__':
    main()
