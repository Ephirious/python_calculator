from src.tokens import Token


class ExpressionError(Exception):
    invalid_position: int
    message: str

    def __init__(self, invalid_position, message):
        self.invalid_position = invalid_position
        self.message = message


class TokenErrors(ExpressionError):
    tokens: list[Token]

    UNKNOWN_POSITION = -1

    def __init__(self, tokens, invalid_position, message):
        super().__init__(invalid_position, message)
        self.tokens = tokens

    def __str__(self):
        tokens_str = ""

        temp_invalid_position = 0
        for index in range(len(self.tokens)):
            if index == self.invalid_position:
                temp_invalid_position = len(tokens_str)
            tokens_str += self.tokens[index].get_token() + " "
        self.invalid_position = temp_invalid_position

        tokens_str += "\n"
        if self.invalid_position != TokenErrors.UNKNOWN_POSITION:
            tokens_str += self.invalid_position * " "
            tokens_str += "^\n"
        tokens_str += self.message

        return tokens_str


class BracketsBalanceError(TokenErrors):
    ERROR_MESSAGE = "Invalid brackets balance"

    def __init__(self, tokens):
        super().__init__(
            tokens, TokenErrors.UNKNOWN_POSITION, BracketsBalanceError.ERROR_MESSAGE
        )


class EmptyBracketsError(TokenErrors):
    ERROR_MESSAGE = "Incorrect empty brackets"

    def __init__(self, tokens, invalid_position):
        super().__init__(tokens, invalid_position, EmptyBracketsError.ERROR_MESSAGE)


class InvalidBinaryOperatorError(TokenErrors):
    ERROR_MESSAGE = "Invalid usage of binary operator"

    def __init__(self, tokens, invalid_position):
        super().__init__(
            tokens, invalid_position, InvalidBinaryOperatorError.ERROR_MESSAGE
        )


class TwiceNumberError(TokenErrors):
    ERROR_MESSAGE = "Two numbers in a row are not supported"

    def __init__(self, tokens, invalid_position):
        super().__init__(tokens, invalid_position, TwiceNumberError.ERROR_MESSAGE)


class ExpressionStringError(ExpressionError):
    expression: str

    def __init__(self, expression, invalid_position, message):
        super().__init__(invalid_position, message)
        self.expression = expression

    def __str__(self):
        result = self.expression + "\n"
        result += (self.invalid_position * " ") + "^" + "\n"
        result += self.message

        return result


class UnknownSymbolError(ExpressionStringError):
    ERROR_MESSAGE = "В выражении содержиться неизвестный символ"

    def __init__(self, expression, invalid_position):
        super().__init__(expression, invalid_position, UnknownSymbolError.ERROR_MESSAGE)


class NumberDotError(ExpressionStringError):
    ERROR_MESSAGE = "В выражении содержиться ошибка, связанная с плавающей точкой вещественного числа"

    def __init__(self, expression, invalid_position):
        super().__init__(expression, invalid_position, NumberDotError.ERROR_MESSAGE)


class DigitsOverFlow(Exception):
    def __init__(self, log):
        self.log = log
