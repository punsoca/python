'''
    test_process_json - we are going to test the process_json.py's open_json_file method.

    For this exercise, we shall:

    - mock the built-in open() function

    - shows to ways to elicit a ValueError / IOError response and test their respective exception message:
         1. using patch as a decorator and assertRaises as a context manager to simulate exception error
         2. using patch as a context manager with assertRaises as a nested context manager to simulate exception error
        RECOMMENDED: #2 using patch as context manager with assertRaises as a nested context 
'''

import json
import unittest
from unittest import mock, TestCase
from process_json import open_json_file

# this unittest exercise demonstrate mocking built-in function open()
class TestReadJSON(TestCase):
    def test_read_json_file(self):
        # before mock the open() function, prepare a variable data to be passed to the mocked open function
        test_data = json.dumps({'a': 1, 'b': 2, 'c': 3})

        # mock_open() is a part of the unittest.mock framework that create a mock to replace the use of open()
        # then we pass our test_data created in the previous line to be passed to the mock_open function
        # finally, create a mock object - here we name it mocked_open
        mocked_open = mock.mock_open(read_data=test_data)

        # using patch as a context manager, open can be patched with the new object, mock_open
        with mock.patch('builtins.open', mocked_open):
            # Within this context, a call to open returns mock_open, the MagicMock object:
            result = open_json_file('filename')
            self.assertEqual({'a': 1, 'b': 2, 'c': 3}, result)


    # using patch decorator for mock_open, and  using mock_open.read().side effect to raise ValueError exception
    @mock.patch("builtins.open", spec_set=True)
    def test_invalid_json_using_patch_n_sideEffect(self, mocked_open):
        # mock_open sets up the mock to behave like open, where using it as a context manager returns itself.
        mock.mock_open(mocked_open)
        mocked_open().read.side_effect = ValueError("oops")

        # IMPORTANT: you need the self.assertRaises part as seen below - if you remove the assertRaises parts, then
        #  the test will fail with an error because the f.read() will raise ValueError
        with self.assertRaises(ValueError) as context:
            open_json_file('filename')
        self.assertTrue('filename is not valid JSON.' in str(context.exception))

    # a better version is to use the patched object as a context manager to raise exception
    # using patch as a context manager, open can be patched with the new object, mock_open
    # then use assertRaises as a nested context to test for the raised exception
    def test_invalid_json_using_context_mgr(self):
        # before mock the open() function, prepare a variable data to be passed to the mocked open function
        test_data = ''
        mocked_open = mock.mock_open(read_data=test_data)
        # again, using the patch as a context manager
        with mock.patch("builtins.open", mocked_open):
            # With assertRaises as a nested context, we can then test for the raised exception when the file does not contain valid JSON
            with self.assertRaises(ValueError) as context:
                open_json_file('filename')
            self.assertTrue('filename is not valid JSON.' in str(context.exception))

    # using patch decorator for mock_open, and  using mock_open.read().side effect to raise IOError exception
    @mock.patch("builtins.open", spec_set=True)
    def test_missing_json_using_side_effect(self, mocked_open):
        # note that if you do not use unittest.mock.mock_open then you will want to say mock().__enter__().read.side_effect = ... instead
        mocked_open().__enter__().read.side_effect = IOError("oops")

        # IMPORTANT: you need the self.assertRaises part as seen below so the f.read() would raise the IOError
        with self.assertRaises(IOError) as context:
            open_json_file('filename')
        self.assertTrue('filename does not exist.' in str(context.exception))

    # a better version - we do not even need to create a patched object, just use assertRaises as a context manager to raise
    # IOError exception, since IOError is detected before the attempt to read the file (hence no need to mock the open function)
    def test_file_not_exists_with_assertRaises(self):
        # no need to mock patch open file because we are asserting IOError exception
        with self.assertRaises(IOError) as context:
            open_json_file('null')
        self.assertTrue('null does not exist.' in str(context.exception))

if __name__ == "__main__":
    unittest.main()
