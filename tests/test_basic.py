import unittest
from src.app import ReconTool

class TestBasicFunctionality(unittest.TestCase):
    def test_tool_initialization(self):
        """Test that the tool initializes without errors"""
        tool = ReconTool()
        self.assertIsInstance(tool, ReconTool)

if __name__ == "__main__":
    unittest.main()