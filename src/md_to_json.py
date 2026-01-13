import re
import json

md_file = "dictionary/dictionary.md"      # your input Markdown file
json_file = "dictionary/links.json"  # output JSON file

char_map = {}

# regex to match markdown link: [CHAR](LINK)
link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

with open(md_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# skip first two lines
for line in lines[2:]:
    line = line.strip()
    if not line or not line.startswith("|"):
        continue

    # split columns by '|', strip spaces
    cols = [col.strip() for col in line.split("|")[1:-1]]  # skip first and last empty after split

    if len(cols) < 3:
        continue

    char_col, _, type_col = cols[0], cols[1], cols[2]

    # skip if type_col is not "字"
    if "字" not in type_col:
        continue

    # extract link from first column
    m = link_pattern.match(char_col)
    if not m:
        continue

    char = m.group(1)
    link = m.group(2)

    char_map[char] = link

# write to JSON
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(char_map, f, ensure_ascii=False, indent=2)

print(f"Saved {len(char_map)} entries to {json_file}")
