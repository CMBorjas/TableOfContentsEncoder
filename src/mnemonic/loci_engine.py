import os

class LociEngine:
    _LOCATIONS = {}

    @classmethod
    def load_locations(cls):
        """Loads locations from the data file into a dictionary."""
        if cls._LOCATIONS:
            return

        try:
            base_path = os.path.dirname(os.path.dirname(__file__)) # Up one level from 'mnemonic' to 'src'
            data_path = os.path.join(base_path, 'data', 'loci.txt')
            
            with open(data_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    parts = line.split('. ', 1)
                    if len(parts) == 2:
                        try:
                            num = int(parts[0])
                            desc = parts[1]
                            cls._LOCATIONS[num] = desc
                        except ValueError:
                            pass
        except Exception as e:
            print(f"Warning: Could not load loci data: {e}")

    @classmethod
    def get_locus(cls, number):
        """Returns the mnemonic locus for a given number."""
        cls.load_locations()
        
        # If the number is directly mapped, return it
        if number in cls._LOCATIONS:
            return cls._LOCATIONS[number]
        
        # Fallback: Use modulo logic for larger numbers
        index = number % 100
        locus = cls._LOCATIONS.get(index, "A generic white room")
        
        # Add modifier for higher ranges to differentiate
        hundreds = number // 100
        if hundreds > 0:
            modifiers = ["Floating in the sky", "Underwater", "On Mars", "In a dream", "Burning"]
            mod = modifiers[hundreds % len(modifiers)]
            return f"{locus} ({mod})"
            
        return locus
