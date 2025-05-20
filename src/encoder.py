import os
import json
import re

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

def save_encoding(pdf_path, mapping):
    """
    Saves the encoding mapping to a JSON file.
    """
    base_name = os.path.basename(pdf_path).replace('.pdf', '.json')
    save_path = os.path.join("encodings", base_name)

    os.makedirs("encodings", exist_ok=True)
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=4)
