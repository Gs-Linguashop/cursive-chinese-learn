import re
import argparse
from pathlib import Path

def remove_markdown_links(content):
    """
    Remove only inline markdown links from content while keeping the link text.
    
    Args:
        content (str): The markdown content to process
        
    Returns:
        str: Content with inline links removed (only text preserved)
    """
    # Pattern for inline links only: [text](url)
    inline_pattern = r'\[([^\]]+)\]\([^)]+\)'
    
    # Remove inline links (keep the text)
    content = re.sub(inline_pattern, r'\1', content)
    
    return content

def process_markdown_file(input_file, output_file=None):
    """
    Process a markdown file to remove inline links only.
    
    Args:
        input_file (str): Path to input markdown file
        output_file (str): Path to output file (optional)
    """
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove inline links only
        processed_content = remove_markdown_links(content)
        
        # Determine output file path
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}_no_inline_links{input_path.suffix}"
        
        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        print(f"Processed file saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Remove inline markdown links while keeping link text')
    parser.add_argument('input_file', help='Input markdown file path')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    process_markdown_file(args.input_file, args.output)

if __name__ == "__main__":
    # Example usage as script
    main()
    # python3 src/remove_links.py practice/chars_3500.md -o practice/chars_3500.md