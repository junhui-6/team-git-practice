"""计算器核心逻辑的单元测试。

运行方式（在仓库根目录）::

    python -m unittest discover

或单独跑本文件::

    python -m unittest calculator.test_calculator
"""

import unittest

from calculator import CalculatorError, calculate, format_result, tokenize


class TestTokenize(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(tokenize("1 + 2"), [1.0, "+", 2.0])

    def test_decimal(self):
        self.assertEqual(tokenize("2.5 * 3"), [2.5, "*", 3.0])

    def test_parentheses(self):
        self.assertEqual(tokenize("(1+2)"), ["(", 1.0, "+", 2.0, ")"])

    def test_unknown_char(self):
        with self.assertRaises(CalculatorError):
            tokenize("1 $ 2")


class TestCalculate(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate("1 + 2"), 3)

    def test_subtraction(self):
        self.assertEqual(calculate("5 - 3"), 2)

    def test_multiplication(self):
        self.assertEqual(calculate("3 * 4"), 12)

    def test_division(self):
        self.assertEqual(calculate("8 / 2"), 4)

    def test_precedence(self):
        # 乘除优先于加减
        self.assertEqual(calculate("1 + 2 * 3"), 7)

    def test_parentheses_override(self):
        # 括号改变优先级
        self.assertEqual(calculate("(1 + 2) * 3"), 9)

    def test_continuous_chain(self):
        # 连续运算
        self.assertEqual(calculate("1 + 2 + 3 + 4"), 10)

    def test_decimal_result(self):
        self.assertEqual(calculate("1 / 4"), 0.25)

    def test_negative_number(self):
        self.assertEqual(calculate("-3 + 5"), 2)

    def test_unary_negative(self):
        self.assertEqual(calculate("-(1+2)"), -3)

    def test_extra_spaces(self):
        self.assertEqual(calculate("  10  /  2  "), 5)

    def test_division_by_zero(self):
        with self.assertRaises(CalculatorError):
            calculate("1 / 0")

    def test_empty_expression(self):
        with self.assertRaises(CalculatorError):
            calculate("")

    def test_missing_right_paren(self):
        with self.assertRaises(CalculatorError):
            calculate("(1 + 2")

    def test_trailing_junk(self):
        with self.assertRaises(CalculatorError):
            calculate("1 + 2 3")


class TestFormatResult(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(format_result(4.0), "4")

    def test_decimal(self):
        self.assertEqual(format_result(0.25), "0.25")


if __name__ == "__main__":
    unittest.main()
