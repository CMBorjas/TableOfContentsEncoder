import hashlib
import os
import random

def load_data(filename):
    """Loads lines from a text file in the data directory."""
    try:
        # src/mnemonic/ -> src/ -> src/data/
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_path, 'data', filename)
        
        with open(data_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except Exception as e:
        print(f"Warning: Could not load data from {filename}: {e}")
        return ["Error loading data"]

class ProustScentEngine:
    _POSITIVE_SCENTS = None
    _NEGATIVE_SCENTS = None

    @classmethod
    def get_positive_scents(cls):
        if cls._POSITIVE_SCENTS is None:
            cls._POSITIVE_SCENTS = load_data('positive_scents.txt')
        return cls._POSITIVE_SCENTS

    @classmethod
    def get_negative_scents(cls):
        if cls._NEGATIVE_SCENTS is None:
            cls._NEGATIVE_SCENTS = load_data('negative_scents.txt')
        return cls._NEGATIVE_SCENTS

    @staticmethod
    def get_scent(text):
        """Deterministically selects a Proustian scent (positive and negative) based on the input text."""
        if not text:
            return "The absence of memory"
            
        pos_list = ProustScentEngine.get_positive_scents()
        neg_list = ProustScentEngine.get_negative_scents()
        
        if not pos_list or not neg_list:
            return "Scent data unavailable"

        # Positive Scent
        hash_pos = hashlib.sha256(text.encode()) 
        hash_int_pos = int(hash_pos.hexdigest(), 16)
        index_pos = hash_int_pos % len(pos_list)
        pos_scent = pos_list[index_pos]

        # Negative Scent (use a salt/prefix to get a different hash)
        hash_neg = hashlib.sha256(("negative" + text).encode())
        hash_int_neg = int(hash_neg.hexdigest(), 16)
        index_neg = hash_int_neg % len(neg_list)
        neg_scent = neg_list[index_neg]

        return f"{pos_scent} and {neg_scent}"

    @staticmethod
    def get_scent_pair(text):
        """Returns the positive and negative scents as a tuple."""
        if not text:
             return ("None", "None")

        pos_list = ProustScentEngine.get_positive_scents()
        neg_list = ProustScentEngine.get_negative_scents()

        hash_pos = hashlib.sha256(text.encode()) 
        index_pos = int(hash_pos.hexdigest(), 16) % len(pos_list)
        
        hash_neg = hashlib.sha256(("negative" + text).encode())
        index_neg = int(hash_neg.hexdigest(), 16) % len(neg_list)
        
        return (pos_list[index_pos], neg_list[index_neg])
