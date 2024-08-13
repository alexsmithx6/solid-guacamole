import sys, os
# Get the base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the base directory to sys.path
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
# Unittest import for generating test cases
import unittest

def run_tests():
    # Discover and load tests from the current directory
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir=os.path.dirname(__file__), pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(tests)