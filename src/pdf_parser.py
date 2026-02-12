import fitz # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    try:
        text = ""
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_toc(pdf_path):
    """
    Extracts the Table of Contents from a PDF.
    Tries to retrieve the embedded TOC first. If not found, falls back to text parsing.
    """
    toc_items = []
    try:
        doc = fitz.open(pdf_path)
        
        # 1. Try embedded TOC
        toc_list = doc.get_toc() 
        if toc_list:
            print(f"Found embedded TOC with {len(toc_list)} items.")
            for item in toc_list:
                toc_items.append({
                    'title': item[1],
                    'page': item[2]
                })
            return toc_items
            
        # 2. Fallback: Smart Text Parsing
        print("No embedded TOC found. Attempting smart text parsing...")
        toc_items = parse_toc_from_text(doc)

    except Exception as e:
        print(f"Error extracting TOC: {e}")
        
    return toc_items

def parse_toc_from_text(doc):
    """
    Scans the PDF for TOC pages and parses them using regex.
    """
    toc_items = []
    start_page = -1
    max_scan_pages = 50 # Heuristic: TOC usually in first 50 pages
    
    # Identify TOC start
    # Priority: "Brief Contents" -> "Table of Contents" -> "Contents"
    limit = min(max_scan_pages, len(doc))
    
    # 1. Look for Brief Contents
    for i in range(limit):
        page = doc[i]
        header_text = page.get_text("text", clip=fitz.Rect(0, 0, page.rect.width, 150))
        if "Brief Contents" in header_text:
            start_page = i
            print(f"Found 'Brief Contents' at page {i+1}")
            break
            
    # 2. If no brief contents, look for standard TOC
    if start_page == -1:
        for i in range(limit):
            page = doc[i]
            header_text = page.get_text("text", clip=fitz.Rect(0, 0, page.rect.width, 150))
            if "Table of Contents" in header_text or "Contents" in header_text or "CONTENTS" in header_text:
                start_page = i
                print(f"Found TOC at page {i+1}")
                break
            
    if start_page == -1:
        print("Could not locate 'Table of Contents' header in first 50 pages.")
        return []

    print(f"Located TOC starting at page {start_page + 1}")
    
    # Scan from start_page until we hit a likely end or max limit
    # We'll scan up to 20 pages for the TOC, but stop if we see a new "Contents" header implies Detailed starts
    toc_range = 20 
    end_page = min(start_page + toc_range, len(doc))
    
    found_items = False
    
    for i in range(start_page, end_page):
        page = doc[i]
        
        # Stop condition: If we found brief contents, and now we see "Contents" again, it's likely the detailed one
        if i > start_page and found_items:
             header_text = page.get_text("text", clip=fitz.Rect(0, 0, page.rect.width, 150))
             if "Contents" in header_text and "Brief" not in header_text:
                 print(f"Stopping at page {i+1} (found Detailed Contents start)")
                 break
        
        # Use blocks to better handle layout, but text with splitlines is often sufficient if we handle multiline
        text = page.get_text("text") 
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            
            # Strategy 1: Title ... Page (Same line)
            # Regex: Title followed by spaces/dots then number
            match = re.search(r'^(.*?)(?:\.{2,}|\s{2,})(\d+)$', line)
            if match:
                title = match.group(1).strip(" .")
                page_str = match.group(2)
                
                if is_valid_toc_item(title, page_str, len(doc)):
                    toc_items.append({'title': title, 'page': int(page_str)})
                    found_items = True
                idx += 1
                continue
                
            # Strategy 2: Title \n Page (Next line is number)
            # Check if current line is text and next line is a number
            if idx + 1 < len(lines):
                next_line = lines[idx+1]
                if next_line.isdigit():
                    # Potential match: line is title, next_line is page
                    if is_valid_toc_item(line, next_line, len(doc)):
                        toc_items.append({'title': line, 'page': int(next_line)})
                        found_items = True
                        idx += 2 # Consume both
                        continue
            
            # Strategy 3: Chapter X \n Title \n Page (3 lines)
            if idx + 2 < len(lines):
                next_line = lines[idx+1]
                next_next_line = lines[idx+2]
                if next_next_line.isdigit() and (line.lower().startswith("chapter") or line.lower().startswith("module")):
                     # Combine header + title
                     full_title = f"{line}: {next_line}"
                     if is_valid_toc_item(full_title, next_next_line, len(doc)):
                        toc_items.append({'title': full_title, 'page': int(next_next_line)})
                        found_items = True
                        idx += 3
                        continue

            idx += 1

    return toc_items

def is_valid_toc_item(title, page_str, max_pages):
    if len(title) < 3: return False
    if title.isdigit(): return False
    if "ISBN" in title: return False
    try:
        p = int(page_str)
        if p > max_pages: return False
        return True
    except:
        return False