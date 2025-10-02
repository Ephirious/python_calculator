from src.tokens import Token, Number, Operator
from src.exception import DigitsOverFlow
from sys import get_int_max_str_digits
import math


class Calculator:
    MAX_INTEGER_COUNT_DIGITS = get_int_max_str_digits()

    tokens: list[Token]
    tokens_length: int
    pos: int
    log: str

    def __init__(self):
        self.tokens = None
        self.tokens_length = 0
        self.pos = 0
        self.log = ""

    def calculate(self, tokens: list[Token]) -> int | float:
        self.tokens = tokens
        self.tokens_length = len(self.tokens)
        self.pos = 0
        self.log = ""

        result = round(self._expr(), 2)

        return result

    def _current_token(self) -> Token:
        if self._has_next():
            return self.tokens[self.pos]
        raise Exception("No such tokens")

    def _next_pos(self) -> None:
        self.pos += 1

    def _has_next(self):
        if self.pos < self.tokens_length:
            return True
        return False

    def _expr(self) -> int | float:
        return self._add()

    def _add(self) -> int | float:
        left = self._mul()

        while (
            self._has_next()
            and (token := self._current_token())
            and (token.get_token() in (Operator.PLUS, Operator.MINUS))
        ):
            self.log += token.get_token()
            self._next_pos()
            right = self._mul()

            self._check_digits_overflow(left, right, token)

            if token.get_token() is Operator.PLUS:
                left += right
            else:
                left -= right

        return left

    def _mul(self) -> int | float:
        left = self._pow()

        while self._has_next() and self._is_mul_groups(self._current_token()):
            token = self._current_token()
            self.log += token.get_token()
            self._next_pos()
            right = self._pow()

            self._check_digits_overflow(left, right, token)

            match token.get_token():
                case Operator.MULTIPLICATION:
                    left *= right
                case Operator.DIVISION:
                    self._check_zero_division(right)
                    left /= right
                case Operator.INTEGER_DIVISION:
                    self._check_zero_division(right)
                    self._check_integer_types(left, right)
                    left //= right
                case Operator.REMAINDER_DIVISION:
                    self._check_zero_division(right)
                    self._check_integer_types(left, right)
                    left %= right

        return left

    def _pow(self) -> int | float:
        left = self._unary()

        while (
            self._has_next()
            and (token := self._current_token())
            and (token.get_token() is Operator.POWER)
        ):
            self.log += token.get_token()
            self._next_pos()
            right = self._pow()

            self._check_digits_overflow(left, right, token)

            left **= right

        return left

    def _unary(self) -> int | float:
        token = self._current_token()

        is_operator = token.get_token() in (Operator.PLUS, Operator.MINUS)

        if is_operator:
            self.log += token.get_token()
            self._next_pos()
            value = self._unary()

            if token.get_token() is Operator.PLUS:
                return +value
            else:
                return -value

        else:
            return self._primary()

    def _primary(self) -> int | float:
        if self._has_next():
            token = self._current_token()
            self.log += token.get_token()
            self._next_pos()

            if isinstance(token, Number):
                if token.is_float():
                    return float(token.get_token())
                return int(token.get_token())

            elif token.get_token() is Operator.LEFT_BRACKET:
                result = self._expr()
                self.log += self._current_token().get_token()
                self._next_pos()
                return result

    def _check_zero_division(self, right):
        if right == 0:
            raise ZeroDivisionError(self.log)

    def _check_integer_types(self, left, right):
        if isinstance(left, float) or isinstance(right, float):
            raise TypeError(self.log)

    def _get_integer_digits_count(self, number: int) -> int:
        count = 0

        while number != 0:
            count += 1
            number = int(number / 10)

        return count

    def _is_mul_groups(self, token: Operator):
        return token.get_token() in (
            Operator.MULTIPLICATION,
            Operator.DIVISION,
            Operator.INTEGER_DIVISION,
            Operator.REMAINDER_DIVISION,
        )

    def _check_digits_overflow(
        self, num1: int | float, num2: int | float, operator: Operator
    ) -> None:
        if (
            isinstance(num1, int)
            and isinstance(num2, int)
            and operator != Operator.DIVISION
        ):
            self._check_integer_overflow(num1, num2, operator)
        else:
            self._check_float_overflow(num1, num2, operator)

    def _check_integer_overflow(self, num1: int, num2: int, operator: Operator) -> None:
        NUM1_DIGITS_COUNT = self._get_integer_digits_count(num1)
        NUM2_DIGITS_COUNT = self._get_integer_digits_count(num2)

        digits_in_results = None

        match operator.get_token():
            case Operator.PLUS | Operator.MINUS:
                digits_in_results = max(NUM1_DIGITS_COUNT, NUM2_DIGITS_COUNT) + 1

            case Operator.MULTIPLICATION:
                digits_in_results = NUM1_DIGITS_COUNT + NUM2_DIGITS_COUNT

            case Operator.REMAINDER_DIVISION:
                digits_in_results = NUM2_DIGITS_COUNT

            case Operator.INTEGER_DIVISION:
                digits_in_results = NUM1_DIGITS_COUNT

            case Operator.POWER:
                if (num1 == 0) or (num2 == 0) or abs(num1) == 1:
                    digits_in_results = 1
                else:
                    digits_in_results = num2 * math.log10(abs(num1)) + 1

            case Operator.DIVISION:
                self._check_float_overflow(num1, num2, operator)
                return

        if digits_in_results > Calculator.MAX_INTEGER_COUNT_DIGITS:
            raise DigitsOverFlow(self.log)

    def _check_float_overflow(
        self, num1: float, num2: float, operator: Operator
    ) -> None:
        result = None

        match operator.get_token():
            case Operator.PLUS:
                result = num1 + num2

            case Operator.MINUS:
                result = num1 - num2

            case Operator.MULTIPLICATION:
                result = num1 * num2

            case Operator.DIVISION:
                self._check_zero_division(num2)
                result = num1 / num2

            case Operator.POWER:
                result = num1**num2

        if result is not None and math.isinf(result):
            raise DigitsOverFlow(self.log)
