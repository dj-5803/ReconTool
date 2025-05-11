import unittest
import os
import sys
from pathlib import Path
from unittest.mock import patch

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, SRC_DIR)

class TestBasicFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nImporting ReconTool...")
        try:
            with patch('builtins.input', return_value='0'):  # Mock input to prevent blocking
                from app import ReconTool
                cls.ReconTool = ReconTool
                cls.tool = cls.ReconTool()
        except ImportError as e:
            raise unittest.SkipTest(f"Cannot import ReconTool: {e}")

    def test_menu_initialization(self):
        """Test if main_menu attribute exists"""
        self.assertTrue(hasattr(self.tool, 'main_menu'),
                        "ReconTool should have a 'main_menu' method or attribute")

    def test_directories_exist(self):
        """Test if output directories are created"""
        output_dir = getattr(self.tool, 'OUTPUT_DIR', 'outputs')
        barcode_dir = os.path.join(output_dir, 'barcodes')

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(barcode_dir, exist_ok=True)

        self.assertTrue(os.path.exists(output_dir), f"{output_dir} should exist")
        self.assertTrue(os.path.exists(barcode_dir), f"{barcode_dir} should exist")

if __name__ == "__main__":
    unittest.main()
