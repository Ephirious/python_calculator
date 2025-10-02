from src.tokens import Token, Number, Operator


class Calculator:
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

            if token.get_token() is Operator.PLUS:
                left += right
            else:
                left -= right

        return left

    def _mul(self) -> int | float:
        left = self._pow()

        while (
            self._has_next()
            and (token := self._current_token())
            and (
                token.get_token()
                in (
                    Operator.MULTIPLICATION,
                    Operator.DIVISION,
                    Operator.INTEGER_DIVISION,
                    Operator.REMAINDER_DIVISION,
                )
            )
        ):
            self.log += token.get_token()
            self._next_pos()
            right = self._pow()

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
            raise ArithmeticError(self.log)
