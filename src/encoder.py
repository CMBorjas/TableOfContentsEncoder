import os
import json
import re
from src.scent_imagery_engine import correlate_topic

def normalize_word(word):
    return re.sub(r'[^\w\-]', '', word).lower()


"""
    Encodes unique words in the text based on user input.
    Keeps a mapping dictionary and returns the full encoded text and mapping.
    """
def encode_text(text, prompt_callback):
    mapping = {}
    encoded_lines = []

    for line in text.splitlines():
        encoded_line = []
        words = line.split()
        for word in words:
            word_clean = normalize_word(word)
            if word_clean == '' or word_clean.isdigit():
                encoded_line.append(word)
                continue

            if word_clean not in mapping:
                encoded_value = prompt_callback(word_clean)
                if encoded_value is None:  # user canceled
                    encoded_value = word_clean
                mapping[word_clean] = encoded_value
            
            encoded_line.append(mapping[word_clean])
        encoded_lines.append(" ".join(encoded_line))

    return "\n".join(encoded_lines), mapping

def encode_toc_structure(toc_items):
    """
    Encodes a structured TOC list using the Absurd Imagery and Proust Scent engine.
    
    Args:
        toc_items (list): List of dicts {'title': str, 'page': int}
        
    Returns:
        list: List of enhanced TOC items with correlations.
    """
    enhanced_toc = []
    for item in toc_items:
        title = item['title']
        correlation = correlate_topic(title)
        
        enhanced_item = item.copy()
        enhanced_item['imagery'] = correlation['imagery']
        enhanced_item['scent'] = correlation['scent']
        enhanced_toc.append(enhanced_item)
        
    return enhanced_toc

def save_encoding(source_path, data, suffix='.json'):
    """
    Saves the encoding mapping/data to a file.
    """
    base_name = os.path.basename(source_path).rsplit('.', 1)[0] + suffix
    save_path = os.path.join("encodings", base_name)

    os.makedirs("encodings", exist_ok=True)
    
    # Determine format based on suffix or data type
    if suffix == '.json':
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    elif suffix == '.md':
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(data)
    
    return save_path
