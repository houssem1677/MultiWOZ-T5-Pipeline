import argparse

def merge_jsonl_files(output_path, *input_paths):
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for file_path in input_paths:
            with open(file_path, 'r', encoding='utf-8') as infile:
                for line in infile:
                    if line.strip():
                        outfile.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple JSONL files into one")
    parser.add_argument("output", help="Output merged JSONL file path")
    parser.add_argument("inputs", nargs="+", help="Input JSONL file paths to merge")
    args = parser.parse_args()

    merge_jsonl_files(args.output, *args.inputs)
    print(f"Merged {len(args.inputs)} files into {args.output}")
