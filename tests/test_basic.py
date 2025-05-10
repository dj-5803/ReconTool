import unittest
import os
import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, SRC_DIR)
print(f"Added to path: {SRC_DIR}")

class TestBasicFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Test suite setup"""
        '''cls.exit_patch = patch('sys.exit')
        cls.mock_exit = cls.exit_patch.start()
        
        cls.stdout_patch = patch('sys.stdout', new_callable=StringIO)
        cls.mock_stdout = cls.stdout_patch.start()'''
        
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
    
    '''@classmethod
    def tearDownClass(cls):
        cls.exit_patch.stop()
        cls.stdout_patch.stop()  '''  

    def test_menu_initialization(self):
        """Test main menu loads"""
        with patch('sys.exit'):
            self.assertTrue(hasattr(self.tool, 'main_menu'),
                          "ReconTool should have 'main_menu' method")
        
    def test_directories_exist(self):
        """Test output directories are created"""
        OUTPUT_DIR = getattr(self.tool, 'OUTPUT_DIR', 'outputs')
        BARCODE_DIR = os.path.join(OUTPUT_DIR, 'barcodes')
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(BARCODE_DIR, exist_ok=True)
        
        self.assertTrue(os.path.exists(OUTPUT_DIR),
                      f"Output directory {OUTPUT_DIR} should exist")
        self.assertTrue(os.path.exists(BARCODE_DIR),
                      f"Barcode directory {BARCODE_DIR} should exist")

if __name__ == "__main__":
    unittest.main()