'''
CalculatorApp.py - this program introduces basic unittest knowledge

Two classes: CalculatorApp, AddTests(unittest.TestCase)

To run the AddTest test cases in this program, run from terminal (< > indicate optional parameters):

$ python -m unittest <--verbose> tests.calculator_app_tests

'''
from typing import Tuple

def add(*args: Tuple[int]) -> int:
    my_sum = 0
    for arg in args:
        my_sum += arg

    return my_sum

print(add(1,2,3))
