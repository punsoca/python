import unittest
import CalculatorApp


# calculator_app_tests.py
class AddTests(unittest.TestCase):
    def test_add_2_and_2_returns_4(self):
        self.assertEqual(4, CalculatorApp.add(2, 2))

    def test_add_1_and_2_and_3_returns_6(self):
        self.assertEqual(6, CalculatorApp.add(1, 2, 3))

    def test_add_with_no_arguments_returns_0(self):
        self.assertEqual(0, CalculatorApp.add())
