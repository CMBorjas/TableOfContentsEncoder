import asyncio
import sys
import argparse
from src.core.controller import TOCController
from src.core.models import EncodingResult

async def main():
    parser = argparse.ArgumentParser(description="Table of Contents Encoder (Enterprise Edition)")
    parser.add_argument("input_file", help="Path to the PDF file")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Output format")
    parser.add_argument("--mnemonic", action="store_true", help="Enable mnemonic encoding (Loci/Actors)")
    
    args = parser.parse_args()
    
    controller = TOCController()
    
    try:
        result = await controller.process_file(args.input_file)
        
        if args.format == "markdown":
            print_markdown(result)
        else:
            # Simple JSON dump placeholder
            print(result)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_markdown(result: EncodingResult):
    print(f"# Mnemonic Encoding for {result.source_file}\n")
    
    for item in result.items:
        print(f"## {item.toc_item.title}")
        print(f"- **Page**: {item.toc_item.page}")
        print(f"- **Locus**: {item.locus}")
        print(f"- **Actor**: {item.actor}")
        print(f"- **Imagery**: {item.imagery}")
        print(f"- **Scent (+)**: {item.scent_positive}")
        print(f"- **Scent (-)**: {item.scent_negative}")
        print()

if __name__ == "__main__":
    asyncio.run(main())
