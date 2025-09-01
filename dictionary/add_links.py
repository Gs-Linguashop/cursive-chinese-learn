import argparse
from pathlib import Path
import re
import os

def find_glyph_svg(glyph_name, svg_folder):
    """
    Find SVG file for a glyph name in the specified folder
    
    Args:
        glyph_name (str): The glyph name to search for
        svg_folder (Path): Path to the SVG folder
    
    Returns:
        Path or None: Path to SVG file if found, None otherwise
    """
    # Remove any hex prefix if present (like "uni" or "u")
    if len(glyph_name) == 1: # the unicode character itself
        clean_name = f"{ord(glyph_name):04X}"
    else:
        clean_name = re.sub(r'^(uni|u)', '', glyph_name)
    
    # Possible SVG filenames to check
    possible_filenames = [
        f"uni{clean_name}.svg",
        f"u{clean_name}.svg",
        f"uni{glyph_name}.svg",
        f"u{glyph_name}.svg",
        f"{clean_name}.svg",
        f"{glyph_name}.svg"
    ]
    
    # Check each possible filename
    for filename in possible_filenames:
        svg_path = svg_folder / filename
        if svg_path.exists():
            return svg_path
    
    return None

def add_glyph_links_to_markdown(input_md_file, svg_folder_path, output_file=None, 
                               glyph_column=0, link_svg_folder=None):
    """
    Add SVG hyperlinks to glyph names in a Markdown table
    
    Args:
        input_md_file (str): Path to input markdown file (relative to current directory)
        svg_folder_path (str): Path to folder containing SVG files (relative to current directory)
        output_file (str): Path to output markdown file (relative to current directory)
        glyph_column (int): Column index containing glyph names (0-based)
        link_svg_folder (str): Folder path to use in the hyperlinks (optional)
    """
    # Convert paths to Path objects relative to current working directory
    current_dir = Path.cwd()
    input_path = current_dir / input_md_file
    svg_folder = current_dir / svg_folder_path
    
    # Check if files and folders exist
    if not input_path.exists():
        print(f"Error: Input file '{input_md_file}' does not exist in current directory")
        print(f"Current directory: {current_dir}")
        return False
    
    if not svg_folder.exists() or not svg_folder.is_dir():
        print(f"Error: SVG folder '{svg_folder_path}' does not exist or is not a directory")
        print(f"Current directory: {current_dir}")
        return False
    
    # Create output file path if not provided
    if output_file is None:
        output_file = f"{Path(input_md_file).stem}_with_links.md"
    
    output_path = current_dir / output_file
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into lines
        lines = content.split('\n')
        
        # Process each line to find table rows
        processed_lines = []
        in_table = False
        header_processed = False
        
        for line in lines:
            # Check if this is a table row (starts and ends with |)
            if line.strip().startswith('|') and line.strip().endswith('|'):
                if not in_table:
                    in_table = True
                    header_processed = False
                
                # Split table row into cells
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                
                # Skip separator line (contains only ---, :--, --:, etc.)
                if all(re.match(r'^[\-:\s]+$', cell) for cell in cells if cell):
                    processed_lines.append(line)
                    header_processed = True
                    continue
                
                # Process data rows (not header)
                if header_processed and glyph_column < len(cells):
                    glyph_name = cells[glyph_column].strip()
                    
                    # Remove existing markdown links if any
                    clean_glyph_name = re.sub(r'\[.*?\]\(.*?\)', '', glyph_name).strip()
                    
                    if clean_glyph_name:
                        svg_file = find_glyph_svg(clean_glyph_name, svg_folder)
                        if svg_file:
                            # Determine the link path
                            if link_svg_folder:
                                # Use the manually specified folder + filename
                                filename = svg_file.name
                                link_path = f"{link_svg_folder.rstrip('/')}/{filename}"
                            else:
                                # Use relative path from current directory
                                link_path = svg_file.relative_to(current_dir)
                            
                            # Create hyperlink (without ! for embedding)
                            cells[glyph_column] = f"[{clean_glyph_name}]({link_path})"
                
                # Reconstruct the table row
                processed_line = '| ' + ' | '.join(cells) + ' |'
                processed_lines.append(processed_line)
                
            else:
                # Not a table row
                in_table = False
                header_processed = False
                processed_lines.append(line)
        
        # Write processed content to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(processed_lines))
        
        print(f"Successfully processed: {input_md_file}")
        print(f"Output saved to: {output_file}")
        print(f"SVG source folder: {svg_folder_path}")
        if link_svg_folder:
            print(f"Link folder used: {link_svg_folder}")
        print(f"Working directory: {current_dir}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description='Add SVG hyperlinks to glyph names in Markdown table')
    parser.add_argument('input_md', help='Path to the input markdown file (relative to current directory)')
    parser.add_argument('svg_folder', help='Path to the folder containing SVG files (relative to current directory)')
    parser.add_argument('-o', '--output', help='Path to the output markdown file (relative to current directory, optional)')
    parser.add_argument('--glyph-col', type=int, default=0, help='Column index containing glyph names (0-based, default: 0)')
    parser.add_argument('--link-folder', help='Folder path to use in the hyperlinks (e.g., "https://example.com/glyphs" or "../assets/glyphs")')
    
    args = parser.parse_args()
    
    # Print current working directory for clarity
    print(f"Current working directory: {Path.cwd()}")
    
    success = add_glyph_links_to_markdown(
        args.input_md, 
        args.svg_folder, 
        args.output, 
        args.glyph_col,
        args.link_folder
    )
    
    if success:
        print("Processing completed successfully!")
    else:
        print("Processing failed.")

if __name__ == "__main__":
    main()
    # Example use: python3 dictionary/add_links.py dictionary/dictionary.md dictionary/src/ -o dictionary/dictionary.md --link-folder "src/"