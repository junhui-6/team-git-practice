"""一个基础命令行计算器。

支持：
- 加、减、乘、除四则运算
- 运算符优先级（乘除先于加减）和括号
- 连续运算（链式表达式，以及用 ``ans`` 引用上一次结果）
- 除以零等异常输入的友好处理

用法：:

    # 进入交互模式
    python -m calculator

    # 也可以在代码里直接调用
    from calculator import calculate
    calculate("1 + 2 * 3")  # -> 7.0
"""

from __future__ import annotations

import re
from typing import List, Union

# 支持的运算符与括号
OPERATORS = {"+", "-", "*", "/", "(", ")"}

# 匹配独立的 "ans" 单词（用于替换为上一次结果）
_ANS_RE = re.compile(r"\bans\b")


class CalculatorError(Exception):
    """计算器自定义异常：表达式无法解析或计算时抛出。"""


# ---------------------------------------------------------------------------
# 第一步：词法分析（tokenize）
# 把 "1 + 2 * 3" 拆成一串 token：数字、运算符、括号。
# ---------------------------------------------------------------------------

def tokenize(expr: str) -> List[Union[float, str]]:
    """把表达式字符串拆成 token 列表。

    例：``tokenize("1 + 2.5 * 3")`` -> ``[1.0, '+', 2.5, '*', 3.0]``
    """
    tokens: List[Union[float, str]] = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]

        # 跳过空白字符
        if ch.isspace():
            i += 1
            continue

        # 数字（支持小数）
        if ch.isdigit() or ch == ".":
            j = i
            while j < n and (expr[j].isdigit() or expr[j] == "."):
                j += 1
            try:
                tokens.append(float(expr[i:j]))
            except ValueError:
                raise CalculatorError(f"无法解析数字: {expr[i:j]!r}")
            i = j
            continue

        # 运算符或括号
        if ch in OPERATORS:
            tokens.append(ch)
            i += 1
            continue

        # 不认识的字符
        raise CalculatorError(f"不支持的字符: {ch!r}")

    return tokens


# ---------------------------------------------------------------------------
# 第二步：语法分析 + 求值（递归下降 parser）
# 优先级从低到高：加减 < 乘除 < 括号/数字/一元正负号。
# ---------------------------------------------------------------------------

class Parser:
    def __init__(self, tokens: List[Union[float, str]]):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    # 表达式层：加减（优先级最低）
    def parse_expr(self) -> float:
        value = self.parse_term()
        while self.peek() in ("+", "-"):
            op = self.advance()
            right = self.parse_term()
            if op == "+":
                value += right
            else:
                value -= right
        return value

    # 项层：乘除
    def parse_term(self) -> float:
        value = self.parse_factor()
        while self.peek() in ("*", "/"):
            op = self.advance()
            right = self.parse_factor()
            if op == "*":
                value *= right
            else:
                if right == 0:
                    raise CalculatorError("除以零是不允许的")
                value /= right
        return value

    # 因子层：数字、括号、一元正负号
    def parse_factor(self) -> float:
        token = self.peek()
        if token is None:
            raise CalculatorError("表达式意外结束")
        if isinstance(token, float):
            self.advance()
            return token
        if token == "(":
            self.advance()
            value = self.parse_expr()
            if self.peek() != ")":
                raise CalculatorError("缺少右括号 )")
            self.advance()
            return value
        if token == "-":
            # 一元负号，如 -3 或 -(1+2)
            self.advance()
            return -self.parse_factor()
        if token == "+":
            # 一元正号，如 +3
            self.advance()
            return self.parse_factor()
        raise CalculatorError(f"意外的符号: {token!r}")


def calculate(expr: str) -> float:
    """计算一个表达式，返回数值结果。

    解析失败或除零时会抛出 :class:`CalculatorError`。
    """
    tokens = tokenize(expr)
    if not tokens:
        raise CalculatorError("表达式为空")
    parser = Parser(tokens)
    result = parser.parse_expr()
    if parser.pos != len(tokens):
        raise CalculatorError(f"表达式末尾有多余内容: {parser.tokens[parser.pos:]!r}")
    return result


def format_result(value: float) -> str:
    """把结果格式化成易读字符串：整数不带小数点，小数去掉多余尾零。"""
    if value == int(value):
        return str(int(value))
    # round 掉浮点运算产生的噪声，如 0.30000000000000004
    return str(round(value, 10))


def substitute_ans(expr: str, ans: float) -> str:
    """把表达式里独立的 ``ans`` 替换为上一次的结果。"""
    return _ANS_RE.sub(str(ans), expr)


def main() -> None:
    """交互式命令行：支持连续运算，``ans`` 表示上一次结果。"""
    print("基础计算器（输入 exit/quit 退出；ans 表示上一次结果）")
    ans: Union[float, None] = None
    while True:
        try:
            line = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue
        if line.lower() in ("exit", "quit", "q"):
            break

        try:
            expr = substitute_ans(line, ans) if ans is not None else line
            result = calculate(expr)
            ans = result
            print(format_result(result))
        except CalculatorError as exc:
            print(f"错误: {exc}")
        except ZeroDivisionError:
            # 防御性兜底，正常应在上层 parse_term 里被 CalculatorError 捕获
            print("错误: 除以零是不允许的")


if __name__ == "__main__":
    main()
