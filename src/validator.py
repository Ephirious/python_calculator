"""
Модуль валидации
Содержит класс Validator, ответственный за многоуровневую
входной строки выражения
"""

from src.tokenizer import Tokenizer
from src.tokens import Token, Operator, Number
from src.exception import (
    BracketsBalanceError,
    EmptyBracketsError,
    InvalidBinaryOperatorError,
    NumberDotError,
    UnknownSymbolError,
    TwiceNumberError,
)


class Validator:
    """
    Класс, выполняющий валидацию входного выражения
    """

    tokenizer: Tokenizer
    alphabet: set

    def __init__(self, tokenizer: Tokenizer) -> None:
        """
        Внедрение токенайзера как зависимости.
        Установка рабочего алфавита программы
        """
        self.tokenizer = tokenizer
        self.alphabet = set(".0123456789()+-/*% ")

    def check_correctness_expression(self, expression: str) -> None:
        """
        Выполняет многоуровневую проверку валидности выражения

        Аргумент:
            expression (str): выражение

        Возвращает:
            None

        Исключения:
            BracketsBalanceError: если нарушен баланс скобок в выражении
            UnknownSymbolError: если найден неизвестный символ
            NumberDotError: если нарушены правила расставление точки числа с плавающей точкой
            EmptyBracketsError: если есть в выражении пустые скобки '()'
            InvalidBinaryOperatorError: если нарушены правила расстановки операторов
            TwiceNumberError: если есть два числа, между которыми нет оператора
        """
        self._check_correctness_by_alphabet(expression)
        self._check_correctness_number_dot(expression)

        tokens = self.tokenizer.tokenize(expression)

        self._check_correctness_brackets_balance(tokens)
        self._check_absence_empty_brackets(tokens)
        self._check_correctness_binary_operators(tokens)
        self._check_absence_double_twice_numbers(tokens)

    def _check_correctness_brackets_balance(self, tokens: list[Token]) -> None:
        """
        Выполняет проверку баланса скобок в выражении

        Аргументы:
            tokens (list[Token]): токены выражения

        Возвращает:
            None

        Исключения:
            BracketsBalanceError: если нарушен баланс скобок в выражении
        """
        brackets = list()

        for token in tokens:
            str_token = token.get_token()
            if str_token == Operator.LEFT_BRACKET:
                brackets.append(str_token)
            elif str_token == Operator.RIGHT_BRACKET:
                if len(brackets) == 0:
                    raise BracketsBalanceError(tokens)
                brackets.pop()

        if len(brackets) != 0:
            raise BracketsBalanceError(tokens)

    def _check_correctness_by_alphabet(self, expression: str) -> None:
        """
        Выполняет проверку корректности выражения относительно алфавита

        Аргументы:
            expression (str): выражение

        Возвращает:
            None

        Исключения:
            UnknownSymbolError: если найден неизвестный символ
        """
        expression_length = len(expression)

        for index in range(expression_length):
            if expression[index] not in self.alphabet:
                raise UnknownSymbolError(expression, index)

    def _check_correctness_number_dot(self, expression: str) -> None:
        """
        Выполняет проверку корректности выражения расстановки плавающей точки

        Аргументы:
            expression (str): выражение

        Возвращает:
            None

        Исключения:
            NumberDotError: если нарушены правила расставление точки числа с плавающей точкой
        """
        expression_length = len(expression)

        if expression[expression_length - 1] == Number.NUMBER_DOT:
            raise NumberDotError(expression, expression_length - 1)

        for index in range(expression_length):
            if expression[index] == Number.NUMBER_DOT:
                index += 1

                while index < expression_length and expression[index].isdigit():
                    index += 1

                if index < expression_length and expression[index] == Number.NUMBER_DOT:
                    raise NumberDotError(expression, index)
                elif expression[index - 1] == Number.NUMBER_DOT:
                    raise NumberDotError(expression, index - 1)

    def _check_absence_empty_brackets(self, tokens: list[Token]) -> None:
        """
        Выполняет проверку на отсутствие пустых скобок в выражении

        Аргументы:
            tokens (list[Token]): токены выражения

        Возвращает:
            None

        Исключения:
            EmptyBracketsError: если есть в выражении пустые скобки '()'
        """
        tokens_size = len(tokens)

        for index in range(tokens_size):
            str_token = tokens[index].get_token()
            if str_token == Operator.LEFT_BRACKET:
                next_index = index + 1
                if (next_index < tokens_size) and tokens[
                    next_index
                ].get_token() == Operator.RIGHT_BRACKET:
                    raise EmptyBracketsError(tokens, index)

    def _check_correctness_binary_operators(self, tokens: list[Token]) -> None:
        """
        Выполняет проверку отсутствия ввода двух операторов подряд

        Аргументы:
            tokens (list[Token]): токены выражения

        Возвращает:
            None

        Исключения:
            InvalidBinaryOperatorError: если нарушены правила расстановки операторов
        """
        TOKENS_SIZE = len(tokens)
        LAST_INDEX = TOKENS_SIZE - 1

        is_last_token_operator = (
            self._is_operator(tokens[LAST_INDEX])
            and tokens[LAST_INDEX].get_token() != Operator.RIGHT_BRACKET
        )

        if is_last_token_operator:
            raise InvalidBinaryOperatorError(tokens, LAST_INDEX)
        else:
            self._check_correctness_operators_inside(tokens, TOKENS_SIZE)

    def _check_correctness_operators_inside(
        self, tokens: list[Token], tokens_size: int
    ) -> None:
        """
        Вспомогательная функция для функции _check_correctness_binary_operators,
        которая сама уже производит проверку корректности операторов

        Аргументы:
            tokens (list[Token]): токены выражения

        Возвращает:
            None

        Исключения:
            InvalidBinaryOperatorError: если нарушены правила расстановки операторов
        """
        if (
            not self._is_bracket(tokens[0])
            and (tokens[0].get_token() not in (Operator.PLUS, Operator.MINUS))
            and not self._is_number(tokens[0])
        ):
            raise InvalidBinaryOperatorError(tokens, 0)
        for index in range(tokens_size):
            if self._is_operator(tokens[index]) and (
                not self._is_bracket(tokens[index])
            ):
                for cursor in range(index + 1, tokens_size):
                    index = cursor
                    if (
                        self._is_number(tokens[index])
                        or tokens[cursor].get_token() == Operator.LEFT_BRACKET
                    ):
                        break
                    raise InvalidBinaryOperatorError(tokens, cursor)

    def _check_absence_double_twice_numbers(self, tokens: list[Token]) -> None:
        """
        Выполняет проверку на отсутствие двух идущих подряд чисел

        Аргументы:
            tokens (list[Token]): токены выражения

        Возвращает:
            None

        Исключения:
            TwiceNumberError: если есть два числа, между которыми нет оператора
        """
        tokens_size = len(tokens)

        for index in range(tokens_size):
            if self._is_number(tokens[index]):
                next_index = index + 1

                while next_index < tokens_size and self._is_bracket(tokens[next_index]):
                    next_index += 1

                if (next_index < tokens_size) and self._is_number(tokens[next_index]):
                    raise TwiceNumberError(tokens, next_index)

    def _is_unary_operator(self, token: Token) -> bool:
        """
        Проверяет, является ли токен унарным оператором

        Аргументы:
            token (Token): токен

        Возвращает:
            bool
        """
        if isinstance(token, Operator):
            if token.get_token() in (Operator.PLUS, Operator.MINUS):
                return True
        return False

    def _is_binary_operator(self, token: Token) -> bool:
        """
        Проверяет, является ли токен бинарным оператором

        Аргументы:
            token (Token): токен

        Возвращает:
            bool
        """
        if isinstance(token, Operator):
            if token.get_token() in (
                Operator.MULTIPLICATION,
                Operator.DIVISION,
                Operator.INTEGER_DIVISION,
                Operator.POWER,
                Operator.REMAINDER_DIVISION,
            ):
                return True
        return False

    def _is_bracket(self, token: Token) -> bool:
        """
        Проверяет, является ли токен скобками

        Аргументы:
            token (Token): токен

        Возвращает:
            bool
        """
        if isinstance(token, Operator):
            if token.get_token() in (Operator.LEFT_BRACKET, Operator.RIGHT_BRACKET):
                return True
        return False

    def _is_number(self, token: Token) -> bool:
        """
        Проверяет, является ли токен числом

        Аргументы:
            token (Token): токен

        Возвращает:
            bool
        """
        return isinstance(token, Number)

    def _is_operator(self, token: Token) -> bool:
        """
        Проверяет, является ли токен оператором в целом

        Аргументы:
            token (Token): токен

        Возвращает:
            bool
        """
        return isinstance(token, Operator)
