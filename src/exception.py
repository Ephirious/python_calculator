from src.tokens import *
from src.tokenizer import *

class ExpressionError(Exception):
    tokens: list[Token]
    invalid_position: int
    message: str

    UNKNOWN_POSITION = -1

    def __init__(self, tokens, invalid_position, message):
        self.tokens = tokens
        self.invalid_position = invalid_position
        self.message = message

    def __str__(self):
        tokens_str = ""

        temp_invalid_position = 0
        for index in range(len(self.tokens)):
            if (index == self.invalid_position):
                temp_invalid_position = len(tokens_str)
            tokens_str += self.tokens[index].get_token()
        self.invalid_position = temp_invalid_position

        tokens_str += "\n"
        if self.invalid_position != ExpressionError.UNKNOWN_POSITION:
            tokens_str += (self.invalid_position * " ")
            tokens_str += "^\n"
        tokens_str += self.message
        
        return tokens_str

class BracketsBalanceError(ExpressionError):
    ERROR_MESSAGE = "Invalid brackets balance"

    def __init__(self, tokens):
        super().__init__(tokens, ExpressionError.UNKNOWN_POSITION, BracketsBalanceError.ERROR_MESSAGE)


class EmptyBracketsError(ExpressionError):
    ERROR_MESSAGE = "Incorrect empty brackets"

    def __init__(self, tokens, invalid_position):
        super().__init__(tokens, invalid_position, EmptyBracketsError.ERROR_MESSAGE)


class InvalidBinaryOperatorError(ExpressionError):
    ERROR_MESSAGE = "Invalid usage of binary operator"

    def __init__(self, tokens, invalid_position):
        super().__init__(tokens, invalid_position, InvalidBinaryOperatorError.ERROR_MESSAGE)

class TwiceNumberError(ExpressionError):
    ERROR_MESSAGE = "Two numbers in a row are not supported"

    def __init__(self, tokens, invalid_position):
        super().__init__(tokens, invalid_position, TwiceNumberError.ERROR_MESSAGE)


if (__name__ == "__main__"):
    tokenizer = Tokenizer()
    print(EmptyBracketsError(tokenizer.analyze("1 + 2)"), 2))