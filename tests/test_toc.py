import unittest
import sys
import os

# Adjust path to include project root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.scent_imagery_engine import AbsurdImageryEngine, ProustScentEngine, correlate_topic
from src.encoder import encode_toc_structure

class TestTOCEncoder(unittest.TestCase):
    def test_imagery_determinism(self):
        """Test that the same input always yields the same imagery."""
        text = "Test Topic"
        img1 = AbsurdImageryEngine.get_imagery(text)
        img2 = AbsurdImageryEngine.get_imagery(text)
        self.assertEqual(img1, img2)
        
    def test_scent_determinism(self):
        """Test that the same input always yields the same scent."""
        text = "Test Topic"
        scent1 = ProustScentEngine.get_scent(text)
        scent2 = ProustScentEngine.get_scent(text)
        self.assertEqual(scent1, scent2)
        
    def test_correlation(self):
        """Test the correlation function returns expected structure."""
        result = correlate_topic("Chapter 1")
        self.assertIn("imagery", result)
        self.assertIn("scent", result)
        self.assertEqual(result["topic"], "Chapter 1")

    def test_structure_encoding(self):
        """Test that TOC structure is preserved and enriched."""
        toc = [{'title': 'Chapter 1', 'page': 1}]
        encoded = encode_toc_structure(toc)
        self.assertEqual(len(encoded), 1)
        self.assertEqual(encoded[0]['title'], 'Chapter 1')
        self.assertTrue(len(encoded[0]['imagery']) > 0)
        self.assertTrue(len(encoded[0]['scent']) > 0)

if __name__ == '__main__':
    unittest.main()
