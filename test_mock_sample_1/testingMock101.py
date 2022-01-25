'''
    mock exercise 1 - we are going to test the my_module get_next_person() function.

    The first test case will trigger get_next_person() to call get_random_person() only once.
    The second test case will trigger get_next_person() to call get_random_person() multiple times.

    We shall be mocking the get_random_person() function, and we will use the different assert methods
    to check that the get_random_person return value matches the expected value.
'''
import unittest
from unittest.mock import patch
from  my_module import get_next_person

@patch("my_module.get_random_person", spec_set=True)
class TestGetRandomPerson(unittest.TestCase):

    # test case 1: assign return_value to mocked function
    def test_get_random_person(self, mock_random):
        user = {"people_seen": ['Mark','Henrietta', 'Maria']}
        #get expected and actually values for this test case
        expected = 'Billy'
        mock_random.return_value = 'Billy'
        actual = get_next_person(user)

        # assert
        self.assertEqual(expected, actual)

    # test case 2: use side_effect to make multiple calls to mocked get_random_person function
    # to test get_next_person function's  while-loop logic
    def test_mock_random_multiple_calls(self, mock_random):
        user = {"people_seen": ['Mary','Sarah']}
        #get expected and actually values for this test case
        expected = 'Katie'
        mock_random.side_effect = ['Mary','Sarah', 'Katie'] # side_effect as an iterable
        actual = get_next_person(user)
        # assert
        self.assertEqual(expected, actual)
        # assert call_count
        self.assertEqual(mock_random.call_count, 3)


if __name__ == "__main__":
    unittest.main()
