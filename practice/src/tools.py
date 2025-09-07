import re
import argparse
from pathlib import Path

def process_entry(entry):
    """
    Process an entry: if it's a link, extract text, URL, and keep original formatting;
    if it's plain text, just return the text.
    
    Args:
        entry (str): The content
        
    Returns:
        tuple: (processed_text, original_link, is_link) 
    """
    entry = entry.strip()
    
    # Check if it's a markdown link: [text](url)
    link_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', entry)
    
    if link_match:
        # It's a link - extract text and keep original formatting
        link_text = link_match.group(1).strip()
        original_link = entry  # Keep the original [text](url) format
        return link_text, '!'+original_link, True
    else:
        # It's plain text
        return entry, None, False

def format_entry(text, original_link=None, is_link=False):
    """
    Format the entry as header style, with original link formatting if applicable.
    
    Args:
        text (str): The text to format
        original_link (str): The original link format [text](url)
        is_link (bool): Whether it's a link
        
    Returns:
        str: Formatted markdown content
    """
    # Convert to title style (header)
    header_text = f"# {text.title()}"
    
    if is_link and original_link:
        # If it was a link, format as header with original link beneath
        return f"{header_text}\n{original_link}\n"
    else:
        # If it was plain text, just format as header
        return f"{header_text}\n"

def process_markdown_entries(input_file, output_file=None, exclude_header=True):
    """
    Process a markdown file with entries and convert to headers.
    
    Args:
        input_file (str): Path to input markdown file
        output_file (str): Path to output file (optional)
        exclude_header (bool): Whether to exclude table header row
    """
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
        
        processed_lines = []
        processing_entries = False
        header_skipped = False
        
        for line in content:
            stripped_line = line.strip()
            
            # Skip empty lines and table separators
            if not stripped_line or '---' in stripped_line or stripped_line == '|':
                continue
            
            # Look for table rows (entries)
            if stripped_line.startswith('|'):
                # Extract the cell content (remove leading/trailing | and whitespace)
                cells = [cell.strip() for cell in stripped_line.split('|') if cell.strip()]
                
                if cells:  # If there's at least one cell
                    # Skip table header if requested
                    if exclude_header and not header_skipped and not processing_entries:
                        header_skipped = True
                        continue
                    
                    original_entry = cells[0]
                    processed_text, original_link, is_link = process_entry(original_entry)
                    formatted_entry = format_entry(processed_text, original_link, is_link)
                    
                    processed_lines.append(formatted_entry)
                processing_entries = True
            else:
                # If we were processing entries and hit non-table content, stop
                if processing_entries:
                    break
                # Keep non-table content before the entries
                processed_lines.append(line)
        
        # If no table was found, treat each non-empty line as an entry
        if not processing_entries:
            processed_lines = []
            for line in content:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#') and '---' not in stripped_line:
                    processed_text, original_link, is_link = process_entry(stripped_line)
                    formatted_entry = format_entry(processed_text, original_link, is_link)
                    processed_lines.append(formatted_entry)
        
        # Determine output file path
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}_headers{input_path.suffix}"
        
        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(processed_lines)
        
        print(f"Processed file saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Convert markdown entries to headers: # Title for text, # Title + original link beneath for links')
    parser.add_argument('input_file', help='Input markdown file path')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    parser.add_argument('--include-header', action='store_true', 
                       help='Include table header row (default: exclude header)')
    
    args = parser.parse_args()
    
    process_markdown_entries(args.input_file, args.output, exclude_header=not args.include_header)

if __name__ == "__main__":
    main()
    # python3 practice/src/tools.py practice/chars_3500_linked.md -o practice/chars_3500_with_image.md