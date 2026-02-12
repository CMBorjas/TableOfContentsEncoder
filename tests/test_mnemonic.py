import unittest
from src.mnemonic.loci_engine import LociEngine
from src.mnemonic.actor_engine import ActorEngine
from src.mnemonic.scent_engine import ProustScentEngine
from src.mnemonic.imagery_engine import AbsurdImageryEngine

class TestMnemonicEngines(unittest.TestCase):
    
    def test_loci_engine(self):
        # Test known loci
        self.assertIn("The Void", LociEngine.get_locus(0))
        self.assertIn("24-hour neon diner", LociEngine.get_locus(24)) # Using "The Diner" from file, checking partial match or key words
        
        # Test fallback logic (modifiers for > 99)
        locus_124 = LociEngine.get_locus(124)
        self.assertIn("24-hour neon diner", locus_124) # Base match
        self.assertIn("Underwater", locus_124) # Modifier match
        
    def test_actor_engine(self):
        # Test keyword matching
        self.assertEqual(ActorEngine.get_actor("Network Basics"), "The Neon Spider")
        self.assertEqual(ActorEngine.get_actor("Security Policies"), "The Iron Golem")
        
        # Test fallback
        self.assertEqual(ActorEngine.get_actor("Random Topic"), "The Stranger")

    def test_scent_engine(self):
        # Test loading and generation
        scent = ProustScentEngine.get_scent("Chapter 1")
        self.assertIn("and", scent) # Should differ from old engine "Positive and Negative"
        
        pos, neg = ProustScentEngine.get_scent_pair("Chapter 1")
        self.assertNotEqual(pos, "None")
        self.assertNotEqual(neg, "None")

    def test_imagery_engine(self):
        imd = AbsurdImageryEngine.get_imagery("Test Topic")
        self.assertNotEqual(imd, "No imagery available")
        self.assertIsInstance(imd, str)

if __name__ == '__main__':
    unittest.main()
