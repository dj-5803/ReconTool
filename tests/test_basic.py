import unittest
import os
import sys
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock
import pytest

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, SRC_DIR)

class TestBasicFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nImporting ReconTool...")
        try:
            with patch('builtins.input', return_value='0'), \
                 patch('socket.gethostbyname', return_value='127.0.0.1', \
                 patch('requests.get'), \
                 patch('pyfiglet.Figlet'), \
                 patch('barcode.EAN13'), \
                 patch('pyqrcode.create'), \
                 patch('phonenumbers.parse'), \
                 patch('threading.Thread'), \
                 patch('concurrent.futures.ThreadPoolExecutor'):
                
                from app import ReconTool
                cls.ReconTool = ReconTool
                cls.tool = cls.ReconTool()
                cls.tool.OUTPUT_DIR = "test_outputs"
                cls.tool.BARCODE_DIR = os.path.join(cls.tool.OUTPUT_DIR, "barcodes")
                cls.tool.QRCODE_DIR = os.path.join(cls.tool.OUTPUT_DIR, "qrcodes")
                cls.tool.WORDLIST_DIR = os.path.join(cls.tool.OUTPUT_DIR, "wordlists")
                cls.tool.SCAN_DIR = os.path.join(cls.tool.OUTPUT_DIR, "scans")

        except ImportError as e:
            raise unittest.SkipTest(f"Cannot import ReconTool: {e}")

    def setUp(self):
        """Clean up before each test"""
        if os.path.exists(self.tool.OUTPUT_DIR):
            shutil.rmtree(self.tool.OUTPUT_DIR)
            
    def test_menu_initialization(self):
        """Test if main_menu attribute exists"""
        self.assertIsInstance(self.tool, self.ReconTool)
        self.assertTrue(hasattr(self.tool, 'main_menu'),
                        "ReconTool should have a 'main_menu' method or attribute")
        self.assertTrue(callable(self.tool.main_menu))

    def test_directory_creation(self):
        """Test that directories are created when needed"""
        self.assertFalse(os.path.exists(self.tool.OUTPUT_DIR))
        self.assertFalse(os.path.exists(self.tool.BARCODE_DIR))
        
        with patch('builtins.input', return_value='0'):
            self.tool.barcode_generator()
        
        self.assertTrue(os.path.exists(self.tool.OUTPUT_DIR))
        self.assertTrue(os.path.exists(self.tool.BARCODE_DIR))

    @patch('builtins.input', side_effect=['12', '123456789012'])
    def test_barcode_generator(self, mock_input):
        mock_writer = MagicMock()
        with patch('barcode.EAN13') as mock_ean13:
            mock_ean13.return_value = mock_writer
            self.tool.barcode_generator()
            
            mock_ean13.assert_called_once()
            mock_writer.save.assert_called_once()

    @patch('builtins.input', return_value='https://example.com')
    def test_qrcode_generator(self, mock_input):
        mock_qr = MagicMock()
        with patch('pyqrcode.create', return_value=mock_qr):
            self.tool.qrcode_generator()
            
            mock_qr.svg.assert_called_once()
            mock_qr.png.assert_called_once()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=MagicMock)
    @patch('requests.get')
    def test_subdomain_checker(self, mock_get, mock_open, mock_exists):
        mock_get.return_value.status_code = 200
        mock_open.return_value.__enter__.return_value = ['www', 'api', 'test']
        
        with patch('builtins.input', return_value='example.com'):
            self.tool.subdomain_checker()
            
        self.assertTrue(mock_get.called)

    @pytest.mark.skipif(os.getenv('CI') == 'true', reason="Skip network tests in CI")
    def test_ip_scanner(self):
        with patch('socket.gethostbyname', return_value="127.0.0.1"), \
             patch('requests.get', return_value=Mock(text="1.1.1.1")):
                
            self.tool.ip_scanner()
            
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.tool.OUTPUT_DIR):
            shutil.rmtree(cls.tool.OUTPUT_DIR)
        print("\nTest environment cleaned up")

if __name__ == "__main__":
    unittest.main()
