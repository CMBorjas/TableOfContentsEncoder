import hashlib
import os

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
