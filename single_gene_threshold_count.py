import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory", help="path to input directory containing count_lists")
    parser.add_argument("output_file", help="path to output file")
    parser.add_argument("threshold", type=int, help="minimum number of count_lists a TF must appear in to be included")
    args = parser.parse_args()

    tf_counts = {}

    for root, dirs, files in os.walk(args.input_directory):
        for file in files:
            if not file.endswith(".txt"):
                continue
            count_path = os.path.join(root, file)
            with open(count_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    tf = line.strip().split('_')[0]
                    if tf not in tf_counts:
                        tf_counts[tf] = set()
                    tf_counts[tf].add(count_path)

    with open(args.output_file, 'w') as f:
        for tf, counts in tf_counts.items():
            count = len(counts)
            if count >= args.threshold:
                f.write(f"{tf}: {count}\n")

if __name__ == '__main__':
    main()
