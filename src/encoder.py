import os

import json

def encode_text(text):
    """
    Encodes the given text using a simple character mapping.
    """
    words = text.split() # Split the text into words
    mapping = {} # Initialize an empty mapping
    encoded_words = [] # Initialize an empty list for encoded words

    for word in words:
        word_clean = word.strip('.,:-()') # Clean the word
        if word_clean not in mapping:
            encoded_value = input("Enter the encoded value for '{word_clean}': ") # Prompt the user for the encoded value
            mapping[word_clean] = encoded_value
        encoded_words.append(mapping.get(word_clean,word)) # Append the encoded value or the original word if not found
    
    return ' '.join(encoded_words), mapping # Return the encoded text and the mapping

def save_encoding(pdf_path, mapping):
    """
    Saves the encoding mapping to a JSON file.
    """
    base_name = os.path.basename(pdf_path).replace('.pdf', '.json') # Get the base name of the PDF file
    save_path = os.path.join("encodings", base_name) # Create the save path

    os.makedirs("encodings", exist_ok=True) # Create the encodings directory if it doesn't exist
    with open(save_path, 'w', encoding='utf-8') as f: # Open the file for writing
        json.dump(mapping, f, indent=4) # Save the mapping as JSON