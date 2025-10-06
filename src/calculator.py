"""
Модуль калькулятора производит вычисления согласно заданной грамматике
"""

from src.tokens import Token, Number, Operator
from src.exception import DigitsOverFlow
import sys
import math


class Calculator:
    """
    Класс-калькулятор, который парсит токены согласно заданной грамматике
    вычисляя результат арифметического выражения

    Атрибуты класса:
        MAX_INTEGER_COUNT_DIGITS - максимально возможное количество символов выходной строки

    Атрибуты объекта:
        tokens (list[Token]): токены выражения
        tokens_length (int): длина списка токенов
        pos (int): индекс, на которой находится класс в процессе вычисления
        log (str): строка логирования ошибочных выражений
    """

    MAX_INTEGER_COUNT_DIGITS = sys.get_int_max_str_digits()

    tokens: list[Token]
    tokens_length: int
    pos: int
    log: str

    def __init__(self) -> None:
        """
        Выполняет установку всех значений по умолчанию
        """
        self.tokens = None
        self.tokens_length = 0
        self.pos = 0
        self.log = ""

    def calculate(self, tokens: list[Token]) -> int | float:
        """
        Главная функция данного класса, которая запускает процесс вычисления
        арифметического выражения

        Аргументы:
            tokens (list[Token]): токены арифметического выражения

        Возвращаемое значение:
            int | float: результат расчётов
        """
        self.tokens = tokens
        self.tokens_length = len(self.tokens)
        self.pos = 0
        self.log = ""

        result = round(self._expr(), 2)

        return result

    def _current_token(self) -> Token:
        """
        Вспомогательная функция, которая возвращает токен на текущей позиции

        Возвращаемое значение:
            Token: токен на текующей позиции

        Исключения
            IndexError: вызывается при выходе за границы списка токенов
        """
        if self._has_next():
            return self.tokens[self.pos]
        raise IndexError("Выход за пределы списка токенов")

    def _next_pos(self) -> None:
        """
        Вспомогательная функция, итерирующая индекс

        Возвращаемое значение:
            None
        """
        self.pos += 1

    def _has_next(self) -> bool:
        """
        Вспомогательная функция, проверяющая наличия индекс в границах списка

        Возвращаемое значение:
            bool
        """
        if self.pos < self.tokens_length:
            return True
        return False

    def _expr(self) -> int | float:
        """
        Функция, которая задаёт начало грамматики.
        С неё начинается вычисляться выражение

        Возвращаемое значение:
            int | float: результат выражения
        """
        return self._add()

    def _add(self) -> int | float:
        """
        Функция, ответственная за выполнение сложения\вычитания получившихся членов
        выражений

        Возвращаемое значение:
            int | float: результат выражения
        """
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
        """
        Функция, ответственная за выполнение умножения, деления,
        целочисленного деления, получения отстатка от деления получившихся членов
        выражений

        Возвращаемое значение:
            int | float: результат выражения
        """
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
        """
        Функция, ответственная за возвезедеие в степень получившихся членов
        выражений

        Возвращаемое значение:
            int | float: результат выражения
        """
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
        """
        Функция, ответственная за применение унарных операторов

        Возвращаемое значение:
            int | float: результат выражения
        """
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
        """
        Функция, ответственная за возврат числа, или результата более глубокого выражения

        Возвращаемое значение:
            int | float: результат выражения
        """
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

    def _check_zero_division(self, right: int | float) -> None:
        """
        Функция, проверяющая проблему при делении на 0

        Аргументы:
            right (int | float): делитель

        Возвращаемое значени:
            None

        Исключения:
            ZeroDivisionError: если right равен нулю
        """
        if right == 0:
            raise ZeroDivisionError(self.log)

    def _check_integer_types(self, left: int | float, right: int | float) -> None:
        """
        Функция, соответствие типов левого и правого операнда integer
        для операции целочисленного деления и получения остатка от деления

        Аргументы:
            left (int | float): делимое
            right (int | float): делитель

        Возвращаемое значени:
            None

        Исключения:
            TypeError: если хотя бы один является float
        """
        if isinstance(left, float) or isinstance(right, float):
            raise TypeError(self.log)

    def _get_integer_digits_count(self, number: int) -> int:
        """
        Вспомогательная функция для подсчёта количества цифр в целочисленном
        числе

        Аргументы:
            number (int): целочисленное число

        Возвращаемое значение:
            int: количество цифр в числе
        """
        count = 0
        number = abs(number)

        while number != 0:
            count += 1
            number //= 10

        return count

    def _is_mul_groups(self, token: Operator) -> bool:
        """
        Вспомогательная функция, позволяющая определить, является ли оператор
        * / % //

        Аргументы:
            token (Operator): проверяемый оператор

        Возвращаемое значение:
            bool
        """
        return token.get_token() in (
            Operator.MULTIPLICATION,
            Operator.DIVISION,
            Operator.INTEGER_DIVISION,
            Operator.REMAINDER_DIVISION,
        )

    def _check_digits_overflow(
        self, num1: int | float, num2: int | float, operator: Operator
    ) -> None:
        """
        Вспомогательная функция, выполняющая предварительную оценку применения
        арифметической операции к двум числам. Функция вызывает вспомогательные функции
        для выполнения оценки для целочисленных чисел и чисел с плавающей точкой

        Аргументы:
            num1 (int | float): первое операнд
            num2 (int | float): второй операнд
            operator (Operator): оператор

        Возвращаемое значение:
            None

        Исключения:
            DigitsOverflow: при неудачном результате оценки
        """
        if (
            isinstance(num1, int)
            and isinstance(num2, int)
            and operator != Operator.DIVISION
        ):
            self._check_integer_overflow(num1, num2, operator)
        else:
            self._check_float_overflow(num1, num2, operator)

    def _check_integer_overflow(self, num1: int, num2: int, operator: Operator) -> None:
        """
        Вспомогательная функция, выполняющая предварительную оценку для
        целочисленных чисел для следующих операций: + - * % // ** /

        Аргументы:
            num1 (int): первое операнд
            num2 (int): второй операнд
            operator (Operator): оператор

        Возвращаемое значение:
            None

        Исключения:
            DigitsOverflow: при неудачном результате оценки
        """
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
        """
        Вспомогательная функция, выполняющая предварительную оценку для
        чисел с плавающей точкой для следующих операций: + - * / **

        Аргументы:
            num1 (float): первое операнд
            num2 (float): второй операнд
            operator (Operator): оператор

        Возвращаемое значение:
            None

        Исключения:
            DigitsOverflow: при неудачном результате оценки
        """
        result = None

        try:
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
        except OverflowError:
            raise DigitsOverFlow(self.log)
