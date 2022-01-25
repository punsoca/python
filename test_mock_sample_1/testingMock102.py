
'''
    mock exercise 2 - we are going to test the my_module evaluate function,
    and each test case will trigger evaluate function to call  send_email, let_down_gently,
    and give_some_time functions based on the data we created for each test case.

    We will be mocking the three functions called within evaluate() method, and use different
    assert methods to check whether the corresponding functions are being called or not
'''
import unittest
from unittest.mock import patch
from my_module import evaluate

class TestEvaluateMethods(unittest.TestCase):

    #  this test case MOCKS 'let_down_gently' function called from evaluate method
    #  this test also shows different assert methods
    @patch("my_module.let_down_gently", spec_set=True)
    def test_person2_dislikes_person1(self, mock_let_down):

        # set up test data for person1 and person2
        person1 = "Billy"
        # for person2, we NEED TO PASS BOTH "likes" and "dislikes" data as the evaluate function checks both lists
        # set person2's data where person1 is only in person2's dislikes list and NOT in person2's likes list
        person2 = {"likes":["Rachel"], "dislikes": ["Billy"]}

        # make the call to evaluate function, this should trigger call to let_down_gently
        # as person1 is person2's dislikes list
        evaluate(person1, person2)

        # use "assert call count" that let_down_gently is called only once
        self.assertEqual(mock_let_down.call_count, 1)
        # the following two lines are variations of asserts that check if the mocked function is called
        mock_let_down.assert_called_once()
        assert mock_let_down.called

        # assertions that mock function is called (one or more) with parameter check
        mock_let_down.assert_called_once_with(person1)
        mock_let_down.assert_called_with(person1) # the most recent call
        mock_let_down.assert_any_call(person1)

    #  this test case MOCKS 'let_down_gently' AND 'send_email' functions called from evaluate method
    @patch("my_module.let_down_gently", spec_set=True)
    @patch("my_module.send_email", spec_set=True)
    def test_person2_likes_person1(self, mock_email, mock_let_down):

        # set up test data for person1 and person2
        person1 = "Rachel"
        # set person2's data where person1 is only in person2's likes list
        person2 = {"likes":["Rachel"], "dislikes": ["Billy"]}

        # make the call to evaluate function, this should trigger call to send_email function
        # as person1 is person2's likes list
        evaluate(person1, person2)

        # use "assert call count" that let_down_gently is called twice
        self.assertEqual(mock_email.call_count, 2)
        # use "assert call count" to confirm that let_down_gently is NOT CALLED for this test case
        self.assertEqual(mock_let_down.call_count, 0)

        # we can run assertions that mock_email function with parameter check (once with person1 and another for person2)
        # use 'assert_any_call(<param>), NOT 'assert_with_called_once_with'!
        mock_email.assert_any_call(person1)
        mock_email.assert_any_call(person2)

        # use 'assert_called_with(param)' to check the param used for the LATEST call
        mock_email.assert_called_with(person2) # the most recent call is for person2, NOT person1

        # BONUS:  I want to test that 'mock_email.assert_called_with(person1)' would FAIL, as it was not the param used for the latest call.
        # TIP: Use assertRaises to check that 'mock_email.assert_called_with(person1)' returns an exception.
        with self.assertRaises(Exception) as context:
            mock_email.assert_called_with(person1)
        self.assertTrue('not' in str(context.exception))

    #  this test case MOCKS 'give_some_time' function called from evaluate method
    @patch("my_module.give_some_time", spec_set=True)
    def test_person1_not_in_person2_radar(self, mock_give_some_time):

        # set up test data for person1 and person2
        #  assign person1 value
        person1 = "Helen"
        # this time, set up person2 data so that person1 is NOT in person2's likes AND dislikes list
        person2 = {"likes":["Rachel"], "dislikes": ["Billy"]}

        # make the call to evaluate function, this should trigger call to let_down_gently
        # as person1 is person2's dislike list
        evaluate(person1, person2)

        # use "assert call count" that give_some_time is called once
        self.assertEqual(mock_give_some_time.call_count, 1)

        # use 'assert_called_with(param)' to check the param used for the call to mocked give_some_time function successfully
        mock_give_some_time.assert_called_with(person1)

        # BONUS:  I want to test that when the wrong parameter is sent to the mocked give_some_time() function, it will return an exception.
        # TIP: Use assertRaises to check that passing Person2 instead of Person1 to mock_give_some_time returns an exception.
        with self.assertRaises(Exception) as context:
            mock_give_some_time.assert_called_with(person2)
        self.assertTrue('not' in str(context.exception))

if __name__ == "__main__":
    unittest.main()
