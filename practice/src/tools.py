import re
import argparse
from pathlib import Path

IMG_WIDTH = 160
IMG_STYLE = 'max-width:100%; height:auto;'
ENTRIES_PER_FILE = 100


def process_entry(entry):
    """
    Process an entry:
    - If it's a markdown link [text](url), extract text and image src
    - Otherwise treat as plain text
    """
    entry = entry.strip()

    link_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', entry)

    if link_match:
        text = link_match.group(1).strip()
        img_src = link_match.group(2).strip()
        return text, img_src
    else:
        return entry, None


def format_entry(text, img_src=None):
    """
    Format a single entry as:
      ### Title
      <img ...>   (if image exists)
    """
    lines = [f"### {text.title()}"]

    if img_src:
        lines.append(
            f'<img src="{img_src}" width="{IMG_WIDTH}" style="{IMG_STYLE}">'
        )

    return "\n".join(lines) + "\n\n"


def split_and_write(entries, output_base: Path):
    """
    Split entries into chunks and write numbered markdown files.
    """
    for i in range(0, len(entries), ENTRIES_PER_FILE):
        chunk = entries[i:i + ENTRIES_PER_FILE]
        index = i // ENTRIES_PER_FILE + 1

        output_path = output_base.with_name(
            f"{output_base.stem}-{index}{output_base.suffix}"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# 常用草书字形表{index:02d}\n\n")
            f.writelines(chunk)

        print(f"Wrote {output_path}")


def process_markdown_entries(input_file, output_file=None, exclude_header=True):
    input_path = Path(input_file)

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    processing_table = False
    header_skipped = False

    for line in lines:
        stripped = line.strip()

        if not stripped or '---' in stripped or stripped == '|':
            continue

        if stripped.startswith('|'):
            processing_table = True
            cells = [c.strip() for c in stripped.split('|') if c.strip()]

            if not cells:
                continue

            if exclude_header and not header_skipped:
                header_skipped = True
                continue

            text, img_src = process_entry(cells[0])
            entries.append(format_entry(text, img_src))

        else:
            if processing_table:
                break

    # Fallback: no table found → line-based entries
    if not processing_table:
        entries = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and '---' not in stripped:
                text, img_src = process_entry(stripped)
                entries.append(format_entry(text, img_src))

    # Determine output base path
    if output_file:
        output_base = Path(output_file)
    else:
        output_base = input_path.with_stem(input_path.stem + "_glyphs")

    split_and_write(entries, output_base)


def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown tables of glyph links into paginated glyph showcase files"
    )
    parser.add_argument("input_file", help="Input markdown file")
    parser.add_argument("-o", "--output", help="Base output file name (optional)")
    parser.add_argument("--include-header", action="store_true",
                        help="Include table header row")

    args = parser.parse_args()

    process_markdown_entries(
        args.input_file,
        args.output,
        exclude_header=not args.include_header
    )


if __name__ == "__main__":
    main()

    # python3 practice/src/tools.py practice/chars_3500_linked.md -o practice/chars_3500_with_image.md