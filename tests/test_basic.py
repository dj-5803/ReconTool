import unittest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, SRC_DIR)

class TestBasicFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nImporting ReconTool...")
        try:
            with patch('builtins.input', return_value='0'), \
                 patch('pyfiglet.Figlet'), \
                 patch('socket.gethostbyname'), \
                 patch('requests.get'), \
                 patch('barcode.EAN13'), \
                 patch('pyqrcode.create'), \
                 patch('phonenumbers.parse'), \
                 patch('concurrent.futures.ThreadPoolExecutor'):
                     
                from app import ReconTool
                cls.ReconTool = ReconTool
                cls.tool = cls.ReconTool()

                cls.tool.BARCODE_DIR = os.path.join(cls.test_output_dir, "barcodes")
                cls.tool.QRCODE_DIR = os.path.join(cls.test_output_dir, "qrcodes")
                cls.tool.WORDLIST_DIR = os.path.join(cls.test_output_dir, "wordlists")
                cls.tool.SCAN_DIR = os.path.join(cls.test_output_dir, "scans")
                     
        except ImportError as e:
            raise unittest.SkipTest(f"Cannot import ReconTool: {e}")

    def test_menu_initialization(self):
        self.assertTrue(hasattr(self.tool, 'main_menu'),
                        "ReconTool should have a 'main_menu' method or attribute")
        self.assertTrue(callable(self.tool.main_menu),
                      "main_menu should be a callable method")

    def setUp(self):
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
            
    def test_directories_exist(self):
        output_dir = getattr(self.tool, 'OUTPUT_DIR', 'outputs')
        barcode_dir = os.path.join(output_dir, 'barcodes')

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(barcode_dir, exist_ok=True)

        self.assertTrue(os.path.exists(output_dir), f"{output_dir} should exist")
        self.assertTrue(os.path.exists(barcode_dir), f"{barcode_dir} should exist")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_output_dir):
            shutil.rmtree(cls.test_output_dir)
        print("\nTest environment cleaned up")

if __name__ == "__main__":
    unittest.main()
