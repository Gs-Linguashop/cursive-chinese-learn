#!/usr/bin/env python3
import csv
import sys
import os

def main():
    # Check arguments
    if len(sys.argv) != 3:
        print("Usage: python tsv_to_md.py <input.tsv> <output.md>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: input file '{input_file}' does not exist.")
        sys.exit(1)

    # Markdown header
    markdown_header = (
        "| 字/链接 | Unicode | 分类 | 分类 | 字形 |\n"
        "|---|---|---|---|---|\n"
    )

    rows_md = []

    # Read TSV input
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) < 5:
                print(f"Warning: skipped malformed row: {row}")
                continue
            md_row = f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |"
            if md_row in rows_md:
                print(f"Warning: skipped duplicate row: {md_row}")
                continue
            rows_md.append(md_row)

    # Write Markdown output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_header)
        f.write("\n".join(rows_md))

    print(f"Success! Markdown saved to: {output_file}")


if __name__ == "__main__":
    main()
