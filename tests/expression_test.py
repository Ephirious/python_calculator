import pytest

from src.calculator import Calculator
from src.tokenizer import Tokenizer
from src.validator import Validator
from src.exception import (
    BracketsBalanceError,
    EmptyBracketsError,
    InvalidBinaryOperatorError,
    NumberDotError,
    TwiceNumberError,
)


@pytest.mark.parametrize(
    "expression, result",
    [
        ["0", 0],
        ["1", 1],
        ["42", 42],
        ["-5", -5],
        ["+7", 7],
        ["--3", 3],
        ["-+4", -4],
        ["+-8", -8],
        ["++9", 9],
        ["-(-10)", 10],
        ["1 + 2", 3],
        ["10 - 4", 6],
        ["5 + 3 - 2", 6],
        ["10 - 20", -10],
        ["0 + 0", 0],
        ["100 - 50 + 25", 75],
        ["2 * 3", 6],
        ["10 / 2", 5],
        ["9 // 2", 4],
        ["15 % 4", 3],
        ["20 // 5", 4],
        ["7 * 3 // 2", 10],
        ["100 / 10 * 2", 20],
        ["2 + 3 * 4", 14],
        ["2 * 3 + 4", 10],
        ["10 - 2 * 3", 4],
        ["20 // 4 + 1", 6],
        ["15 % 4 * 2", 6],
        ["1 + 2 * 3 - 4 // 2", 5],
        ["2 ** 3", 8],
        ["3 ** 2 ** 2", 81],
        ["2 ** 3 ** 2", 512],
        ["(-2) ** 2", 4],
        ["(-3) ** 3", -27],
        ["5 ** 3", 125],
        ["(-2) ** 4", 16],
        ["(5)", 5],
        ["(2 + 3) * 4", 20],
        ["2 * (3 + 4)", 14],
        ["(10 - 2) * (3 + 1)", 32],
        ["((2 + 3) * 4) - 1", 19],
        ["(2 ** 3) + (4 * 5)", 28],
        ["(100 // (5 + 5)) * 3", 30],
        ["- (2 + 3)", -5],
        ["+ (4 * 5)", 20],
        ["- (- (3))", 3],
        ["- (2 ** 3)", -8],
        ["(-2) ** 3", -8],
        ["-2 ** 2", 4],
        ["-(2 ** 2)", -4],
        ["-2 ** 3 + 1", -7],
        ["-7 // 2", -4],
        ["7 // -2", -4],
        ["-7 // -2", 3],
        ["-7 % 3", 2],
        ["7 % -3", -2],
        ["-10 % 3", 2],
        ["1000000 + 500000", 1500000],
        ["2 ** 20", 1048576],
        ["123456789 // 123", 1003713],
        ["987654321 % 1000", 321],
        ["0 * 100", 0],
        ["0 // 5", 0],
        ["0 % 7", 0],
        ["1 ** 100", 1],
        ["5 ** 0", 1],
        ["0 ** 1", 0],
        ["100 // 1", 100],
        ["2 + 3 * 4 ** 2 - 5 // 2", 48],
        ["((2 + 3) ** 2 - 1) // 2", 12],
        ["- (3 + 4) * 2", -14],
        ["-3 + 4 * -2", -11],
        ["2 ** 3 * 4 // 2", 16],
        ["100 - 50 // 5 * 2", 80],
        ["(10 - 2) ** (3 - 1)", 64],
        ["3 ** 3 // 2", 13],
        ["100 % 7 * 3", 6],
        ["(1 + 2) * (3 + 4) // (5 - 2)", 7],
    ],
)
def test_correctness_integer_expression(expression, result):
    calculator = Calculator()
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expression)
    assert calculator.calculate(tokens) == result


@pytest.mark.parametrize(
    "expression",
    [
        "1 + (2 * 3",
        "(1 + 2))",
        "((3 + 4)",
        ")(1+2)",
        "(()",
        "())(",
        "((1 + (2*3))",
        "1 + 2)",
        "((()))))",
        "(((((",
        "2 * (3 + (4 - 1)",
        "(1+(2*(3+4))",
    ],
)
def test_correctnes_brackets_balance(expression):
    tokenizer = Tokenizer()
    validator = Validator(tokenizer)
    with pytest.raises(BracketsBalanceError):
        validator.check_correctness_expression(expression)


@pytest.mark.parametrize(
    "expression",
    [
        "()",
        " ( ) ",
        "1 + ()",
        "(( ))",
        "3 * (   )",
        "((1)+())",
        "5 // ( )",
        "(( )) + 3",
        "2*(())",
        "(( ) )",
        "((1) + ( ))",
    ],
)
def test_absence_empty_brackets(expression):
    tokenizer = Tokenizer()
    validator = Validator(tokenizer)
    with pytest.raises(EmptyBracketsError):
        validator.check_correctness_expression(expression)


@pytest.mark.parametrize(
    "expression",
    [
        "--++--",
        "7 + * 8",
        "5 * / 3",
        "+ * 2",
        "1 +",
        "*2",
        "2 **",
        "3 % * 2",
        "1 ++ 2",
        "1 -- 2",
        "1 ** * 2",
        "2 * (3 +) 4",
        "/",
        "-",
        "+",
        "3 * + * 4",
        "10 %",
        "1 + (2 *)",
        "1 - - 1",
    ],
)
def test_correctness_operators(expression):
    tokenizer = Tokenizer()
    validator = Validator(tokenizer)
    with pytest.raises(InvalidBinaryOperatorError):
        validator.check_correctness_expression(expression)


@pytest.mark.parametrize(
    "expression, result",
    [
        ("0", None),
        ("1+2", None),
        (" 1 + 2 ", None),
        ("-3", None),
        ("+4", None),
        ("2**3", None),
        ("2 ** 3 ** 2", None),
        ("4//2", None),
        ("5 % 2", None),
        ("5 % (2+1)", None),
        ("(1+(2*3))-4", None),
        ("-(-5 + 2) * +3", None),
        ("((2))", None),
        ("10 - (3+4)*2", None),
        ("3 * (+5)", None),
        ("2**(1+2)", None),
        ("((1+2)*3) - (4/(2+2))", None),
        ("5 + 6 - 7 * 8 / 3 // 2 % 5", None),
        ("(-1)", None),
        ("+(2)", None),
        ("-(3 + (4 - 5))", None),
        ("3 * (2 + (1 - (4/2)))", None),
        ("2 ** (3 + 1) // 5 % (7 - 2)", None),
        ("123", None),
        ("((1)+((2))+(((3))))", None),
        ("3+(4*5)-6%2//1", None),
    ],
)
def test_valid_expression(expression, result):
    tokenizer = Tokenizer()
    validator = Validator(tokenizer)
    assert validator.check_correctness_expression(expression) == result


@pytest.mark.parametrize(
    "expression",
    [
        "2 2",
        "12 34",
        "123456789 987654321",
        "(2)(3)",
        "(12)34",
        "56(78)",
        "(1+2)(3+4)",
        "2  2",
        "0 0",
        "01 02",
        "5 ( 6 )",
        "3(4)5",
    ],
)
def test_twice_number_situation(expression):
    tokenizer = Tokenizer()
    validator = Validator(tokenizer)
    with pytest.raises(TwiceNumberError):
        validator.check_correctness_expression(expression)


@pytest.mark.parametrize(
    "expression", ["123.", "12.34.56", "..", ".", "12..34", "12 + 3.14.15", "12. + .34"]
)
def test_number_dot(expression):
    tokenizer = Tokenizer()
    validator = Validator(tokenizer)
    with pytest.raises(NumberDotError):
        validator.check_correctness_expression(expression)


@pytest.mark.parametrize(
    "expression, result",
    [
        ("1.5 + 2.3", 3.8),
        ("0.1 + 0.2", 0.3),
        ("-1.7 + 3.4", 1.7),
        ("5.0 + -2.5", 2.5),
        ("10.123 + 0.877", 11.0),
        ("0.0 + 0.0", 0.0),
        ("123.456 + 789.544", 913.0),
        ("-0.01 + -0.02", -0.03),
    ],
)
def test_correctness_float_expression(expression, result):
    calculator = Calculator()
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expression)
    assert calculator.calculate(tokens) == result


@pytest.mark.parametrize(
    "expression",
    [
        "1 / 0",
        "5.0 / 0",
        "10 // 0",
        "-3 % 0",
        "2 ** (1 / 0)",  # деление на ноль внутри степени
        "(4 + 5) / (2 - 2)",
        "1 / (0)",
        "1 / (-0)",  # -0 в Python — это 0
        "((1 + 2) * 3) / 0",
        "10 % (5 - 5)",
        "1 // (0.0)",
        "+0 / 0",  # унарный плюс
        "-0 / 0",  # унарный минус
        "1 / (0 + 0)",
        "100 / ((3 - 3))",
    ],
)
def test_correctness_zero_division(expression):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expression)
    calculator = Calculator()
    with pytest.raises(ZeroDivisionError):
        calculator.calculate(tokens)
