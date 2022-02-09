'''
    this is a basic sample of python unit testing using unittest framework 
    in this file we have two parts:
    - main section containing one method named isValid
    - unittest section containing test cases to test the main method isValid

'''
# ------- main section -------
import typing
import unittest

# 
def isValid(s: typing.AnyStr):
    result = None
    open_seen = []
    open_char =   ["(", "{", "["]
    closed_char = [")", "}", "]"]


    for char in s:
        if char in open_char:
            open_seen.append(char)
        else:
            pos = closed_char.index(char)
            if len(open_seen) > 0 and open_char[pos] == open_seen[-1]:
                open_seen.pop()
            else:
                break

    # result must be either True or False 
    result = True if not open_seen else False

    return result

# ------- unittest section -------
class TestisValid(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(isValid('()'), True)
        self.assertEqual(isValid('()[]{}'), True)
        self.assertEqual(isValid('{{{[{[{}]}]}}}'), True)

    def test_notValid(self):
        self.assertEqual(isValid('([)'), False)
        self.assertEqual(isValid('{{{()}}'), False)

if __name__ == "__main__":
    unittest.main()
