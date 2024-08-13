# Unittest import for generating test cases
import unittest
# Project imports
from utils.function_decorators import try_catch_decorator

@try_catch_decorator
def add(x: int, y: int) -> int:
    """Simple supporting function to test our decorator"""
    return x + y

class TestDecorator(unittest.TestCase):

    def test_success(self):
        """Successful case for invocation of decorator"""
        exitCode, exitMessage, result = add(2, 3)
        # Assert success
        self.assertEqual(exitCode, 0, exitMessage)
        # Should equal 5
        self.assertEqual(result, 5, 'Bad test result')

    def test_failure(self):
        """Failure case for invocation of decorator"""
        exitCode, exitMessage, result = add('not an int', 3)
        # Assert failure
        self.assertEqual(exitCode, 1, exitMessage)
        # Return object should be None due to exception
        self.assertEqual(result, None, exitMessage)
