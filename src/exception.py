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
        result = self._from_token_to_str() + "\n"
        
        if self.invalid_position != ExpressionError.UNKNOWN_POSITION:
            result += (self.invalid_position * " ")
            result += "^\n"
        result += self.message
        
        return result
    
    def _from_token_to_str(self) -> str:
        result = ""
        for token in self.tokens:
            result += token.get_token()
        return result


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
    ERROR_MESSAGE = "Еwo numbers in a row are not supported"

    def __init__(self, tokens, invalid_position):
        super().__init__(tokens, invalid_position, InvalidBinaryOperatorError.ERROR_MESSAGE)


if (__name__ == "__main__"):
    tokenizer = Tokenizer()
    print(EmptyBracketsError(tokenizer.analyze("1 + 2)"), 2))