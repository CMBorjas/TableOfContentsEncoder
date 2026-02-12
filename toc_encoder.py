#!/usr/bin/env python3
import argparse
import sys
import json
import os

# Ensure src is in the python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf_parser import extract_toc
from src.encoder import encode_toc_structure

def format_markdown(enhanced_toc):
    md_output = "# Table of Contents (Encoded)\n\n"
    for item in enhanced_toc:
        md_output += f"## {item['title']}\n"
        md_output += f"- **Page**: {item['page']}\n"
        md_output += f"- **Imagery**: {item['imagery']}\n"
        md_output += f"- **Scent**: {item['scent']}\n\n"
    return md_output

def main():
    parser = argparse.ArgumentParser(description="Table of Contents Encoder with Absurd Imagery & Proust Scents")
    parser.add_argument("input_file", help="Path to the input PDF file")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format (default: json)")
    parser.add_argument("--output", help="Output file path (optional)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)

    print(f"Extracting TOC from {args.input_file}...")
    toc_items = extract_toc(args.input_file)
    
    if not toc_items:
        print("Warning: No TOC items found. Please ensure the PDF has a table of contents or structured headings.")
    
    print("Encoding with Absurd Imagery and Proust Scents...")
    enhanced_toc = encode_toc_structure(toc_items)
    
    # Determine output content
    if args.format == "json":
        output_content = json.dumps(enhanced_toc, indent=4)
    else:
        output_content = format_markdown(enhanced_toc)
        
    # Handle output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_content)
        print(f"Output saved to {args.output}")
    else:
        print("\n--- Encoding Result ---\n")
        print(output_content)

if __name__ == "__main__":
    main()
