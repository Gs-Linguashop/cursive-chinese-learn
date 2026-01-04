import argparse
from pathlib import Path

ENTRIES_PER_FILE = 500  # split every 500 rows


def split_markdown_table(input_file: Path, output_base: Path, entries_per_file=ENTRIES_PER_FILE):
    lines = input_file.read_text(encoding="utf-8").splitlines()

    header_lines = []
    table_rows = []

    # Parse table
    table_started = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|'):
            table_started = True
            if '---' in stripped:
                # skip separator row
                continue
            if not header_lines:
                # first non-separator row = header
                header_lines.append(line)
                continue
            # all others = entries
            table_rows.append(line)
        else:
            if table_started:
                # End of table
                break

    if not table_rows:
        raise ValueError("No table rows found in input file.")

    # Split into chunks
    chunks = [table_rows[i:i + entries_per_file] for i in range(0, len(table_rows), entries_per_file)]

    for idx, chunk in enumerate(chunks, start=1):
        output_path = output_base.with_name(f"{output_base.stem}-{idx}{output_base.suffix}")
        with open(output_path, "w", encoding="utf-8") as f:
            # write header
            for hline in header_lines:
                f.write(hline + "\n")
            # write separator
            f.write('|---|\n')
            # write chunk
            for row in chunk:
                f.write(row + "\n")
        print(f"Wrote {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Split a Markdown table file into multiple files, keeping header and format."
    )
    parser.add_argument("input_file", help="Input Markdown file")
    parser.add_argument("-o", "--output", help="Base output file name (optional)")
    args = parser.parse_args()
    input_path = Path(args.input_file)

    if args.output:
        output_base = Path(args.output)
    else:
        output_base = input_path.with_stem(input_path.stem + "_split")

    split_markdown_table(input_path, output_base)


if __name__ == "__main__":
    main()
