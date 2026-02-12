import random
import hashlib
import os

def load_data(filename):
    """Loads lines from a text file in the data directory."""
    try:
        # Assuming data is in src/data/ relative to this file
        base_path = os.path.dirname(__file__)
        data_path = os.path.join(base_path, 'data', filename)
        
        with open(data_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except Exception as e:
        print(f"Warning: Could not load data from {filename}: {e}")
        return ["Error loading data"]

class AbsurdImageryEngine:
    _IMAGERY = None

    @classmethod
    def get_imagery_list(cls):
        if cls._IMAGERY is None:
            cls._IMAGERY = load_data('absurd_imagery.txt')
        return cls._IMAGERY

    @staticmethod
    def get_imagery(text):
        """Deterministically selects an absurd image based on the input text."""
        if not text:
            return "A void staring back"
        
        imagery_list = AbsurdImageryEngine.get_imagery_list()
        if not imagery_list:
             return "No imagery available"

        # Use a hash to ensure the same text always gets the same imagery
        hash_object = hashlib.md5(text.encode())
        hash_int = int(hash_object.hexdigest(), 16)
        index = hash_int % len(imagery_list)
        return imagery_list[index]

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

def correlate_topic(topic):
    """Returns a dictionary with the topic and its associated imagery and scent."""
    return {
        "topic": topic,
        "imagery": AbsurdImageryEngine.get_imagery(topic),
        "scent": ProustScentEngine.get_scent(topic)
    }
