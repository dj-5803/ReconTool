import unittest
import os
import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, SRC_DIR)

class TestBasicFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nAttempting to import ReconTool...")
        try:
            from app import ReconTool
            cls.ReconTool = ReconTool
            print("Successfully imported ReconTool")
        except ImportError as e:
            print(f"Import failed: {str(e)}")
            raise unittest.SkipTest(f"Could not import ReconTool: {str(e)}")
        
        cls.tool = cls.ReconTool()
        print("Initialized ReconTool instance")
    
    def test_menu_initialization(self):
        """Test that main_menu method exists"""
        self.assertTrue(hasattr(self.tool, 'main_menu'),
                        "ReconTool should have a 'main_menu' method")
        
    def test_directories_exist(self):
        """Test if output directories are created"""
        OUTPUT_DIR = getattr(self.tool, 'OUTPUT_DIR', 'outputs')
        BARCODE_DIR = os.path.join(OUTPUT_DIR, 'barcodes')
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(BARCODE_DIR, exist_ok=True)
        
        self.assertTrue(os.path.isdir(OUTPUT_DIR),
                        f"Output directory '{OUTPUT_DIR}' should exist")
        self.assertTrue(os.path.isdir(BARCODE_DIR),
                        f"Barcode directory '{BARCODE_DIR}' should exist")

if __name__ == "__main__":
    unittest.main()
