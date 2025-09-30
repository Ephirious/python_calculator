from src.tokenizer import Tokenizer
from src.tokens import Token, Operator, Number
from src.exception import *

class Validator:
    tokenizer: Tokenizer

    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
    
    def check_correctness_expression(self, expression: str) -> None:
        tokens = self.tokenizer.analyze(expression)

        self._check_correctness_brackets_balance(tokens)
        self._check_absence_empty_brackets(tokens)
        self._check_correctness_binary_operators(tokens)
        self._check_absence_double_twice_numbers(tokens)
        
    def _check_correctness_brackets_balance(self, tokens: list[Token]) -> None:
        brackets = list()

        for token in tokens:
            str_token = token.get_token()
            if str_token == Operator.LEFT_BRACKET:
                brackets.append(str_token)
            elif str_token == Operator.RIGHT_BRACKET:
                if (len(brackets) == 0):
                    raise BracketsBalanceError(tokens)
                brackets.pop()
        
        if len(brackets) != 0:
            raise BracketsBalanceError(tokens)

    def _check_absence_empty_brackets(self, tokens: list[Token]) -> None:
        tokens_size = len(tokens)

        for index in range(tokens_size):
            str_token = tokens[index].get_token()
            if (str_token == Operator.LEFT_BRACKET):
                next_index = index + 1
                if (next_index < tokens_size) and tokens[next_index].get_token() == Operator.RIGHT_BRACKET:
                    raise EmptyBracketsError(tokens, index)
            
    def _check_correctness_binary_operators(self, tokens: list[Token]) -> None:
        TOKENS_SIZE = len(tokens)
        START_INDEX = 0
        LAST_INDEX = TOKENS_SIZE - 1

        is_first_token_not_number = not self._is_number(tokens[START_INDEX])
        is_last_token_operator = self._is_operator(tokens[LAST_INDEX]) and tokens[LAST_INDEX].get_token() != Operator.RIGHT_BRACKET

        if (is_first_token_not_number):
            self._check_if_first_token_not_number(tokens, TOKENS_SIZE)
        elif (is_last_token_operator):
            raise InvalidBinaryOperatorError(tokens, LAST_INDEX)
        else:
            self._check_correctness_operators_inside(tokens, TOKENS_SIZE)
        
    def _check_if_first_token_not_number(self, tokens: list[Token], tokens_size: int) -> None:
        LAST_INDEX = tokens_size - 1
        for index in range(tokens_size):
            token = tokens[index]

            is_start_token_is_binary = self._is_binary_operator(token)
            is_token_number = self._is_number(token)
            is_index_equal_last = (index == LAST_INDEX) and (not is_token_number)

            if is_start_token_is_binary or is_index_equal_last:
                raise InvalidBinaryOperatorError(tokens, index)
            elif is_token_number:
                break

    def _check_correctness_operators_inside(self, tokens: list[Token], tokens_size: int) -> None:
        for index in range(tokens_size):
            if self._is_operator(tokens[index]) and (not self._is_bracket(tokens[index])):
                for cursor in range (index + 1, tokens_size):
                    index = cursor
                    if self._is_number(tokens[index]) or tokens[cursor].get_token() == Operator.LEFT_BRACKET:
                        break
                    raise InvalidBinaryOperatorError(tokens, cursor)

    def _check_absence_double_twice_numbers(self, tokens: list[Token]) -> None:
        tokens_size = len(tokens)

        for index in range(tokens_size):
            if self._is_number(tokens[index]):
                next_index = index + 1
                
                while (next_index < tokens_size and self._is_bracket(tokens[next_index])):
                    next_index += 1

                if (next_index < tokens_size) and self._is_number(tokens[next_index]):
                    raise TwiceNumberError(tokens, next_index)

    def _is_unary_operator(self, token: Token) -> bool:
        if isinstance(token, Operator):
            if token.get_token() in (Operator.PLUS, Operator.MINUS):
                return True
        return False
    
    def _is_binary_operator(self, token: Token) -> bool:
        if isinstance(token, Operator):
            if token.get_token() in (
                Operator.MULTIPLICATION,
                Operator.DIVISION,
                Operator.INTEGER_DIVISION,
                Operator.POWER,
                Operator.REMAINDER_DIVISION):
                return True
        return False
    
    def _is_bracket(self, token: Token) -> bool:
        if isinstance(token, Operator):
            if token.get_token() in (Operator.LEFT_BRACKET, Operator.RIGHT_BRACKET):
                return True
        return False
    
    def _is_number(self, token: Token) -> bool:
        return isinstance(token, Number)
    
    def _is_operator(self, token: Token) -> bool:
        return isinstance(token, Operator)

if (__name__ == "__main__"):
    tokenizer = Tokenizer()
    validator = Validator(tokenizer)
    print(validator.check_correctness_expression("( )"))