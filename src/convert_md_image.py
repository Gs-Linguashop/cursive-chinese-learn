import re
from pathlib import Path

IMG_WIDTH = 144

# Markdown image: ![alt](path)
MD_IMAGE_PATTERN = re.compile(
    r'!\[[^\]]*\]\(([^)]+)\)'
)

# HTML img with width attribute
HTML_IMG_WITH_WIDTH_PATTERN = re.compile(
    r'<img\s+[^>]*src="([^"]+)"[^>]*width="\d+"[^>]*>'
)

def convert_md_images(text: str) -> str:
    return MD_IMAGE_PATTERN.sub(
        rf'<img src="\1" width="{IMG_WIDTH}" style="max-width:100%; height:auto;">',
        text
    )

def normalize_html_img_width(text: str) -> str:
    def repl(match):
        src = match.group(1)
        return f'<img src="{src}" width="{IMG_WIDTH}" style="max-width:100%; height:auto;">'
    return HTML_IMG_WITH_WIDTH_PATTERN.sub(repl, text)

def process_md_file(md_path: Path):
    original = md_path.read_text(encoding="utf-8")
    text = original
    # text = convert_md_images(text)
    text = normalize_html_img_width(text)

    if text != original:
        md_path.write_text(text, encoding="utf-8")

def main():
    # repo root = parent of src/
    repo_root = Path(__file__).resolve().parents[1]

    for md_file in repo_root.rglob("*.md"):
        process_md_file(md_file)

if __name__ == "__main__":
    main()
