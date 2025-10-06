"""
Модуль, отвечающий за токенизацию выражения
"""

from src.tokens import Token, Operator, Number


class Tokenizer:
    """
    Класс-токенизатор, выполнаяющий единственную функцию: токенизация выражения

    Атрибуты:
        expression (str): выражение, которое предстоит токенезировать
        expression_length (int): длина выражения (строки)
        pos (int): индекс на символ, с которым токенизатору предстоит работать
    """

    expression: str
    expression_length: int
    pos: int

    def __init__(self) -> None:
        """
        Выполняет установку всех значений по умолочанию
        """
        self.expression = ""
        self.expression_length = 0
        self.pos = 0

    def tokenize(self, expression: str) -> list[Token]:
        """
        Главная функция данного класса, которая выполняет токенизацию выражения

        Аргументы:
            expression (str): выражение

        Возвращаемое значение:
            list[Token]: список готовых токенов, идущих по порядку согласно выражению
        """
        tokens = list()
        self.expression = expression
        self.expression_length = len(self.expression)
        self.pos = 0

        while self._is_correct_pos():
            if self._get_current_letter().isspace():
                self._next_pos()
            elif (
                self._get_current_letter().isdigit()
                or self._get_current_letter() == Number.NUMBER_DOT
            ):
                number = self._read_number()
                tokens.append(number)
            else:
                operator = self._read_operator()
                tokens.append(operator)

        return tokens

    def _is_correct_pos(self) -> bool:
        """
        Вспомогательная функция, проверяющая, не вашел ли индекс за пределы длины выражения

        Возвращаемое значение:
            bool
        """
        return self.pos < self.expression_length

    def _get_current_letter(self) -> str:
        """
        Вспомогательная функция, возвращающся элемент на текущей позиции

        Возвращаемое значение:
            str

        Исключения:
            IndexError: вызывается, если была вызвана функция, но индекс уже вышел за границы
        """
        if self._is_correct_pos():
            return self.expression[self.pos]
        else:
            raise IndexError("Некорректная индекс в выражении")

    def _next_pos(self) -> None:
        """
        Вспомогательная функция, итерирующая индекс на 1 символ

        Возвращаемое значение:
            None
        """
        self.pos += 1

    def _is_digit(self) -> bool:
        """
        Вспомогательная функция, определяющая, является ли символ числом или точкой

        Возвращаемое значение:
            bool
        """
        return (self._get_current_letter().isdigit()) or (
            self._get_current_letter() == Number.NUMBER_DOT
        )

    def _read_number(self) -> Number:
        """
        Функция, которая считывает число, пока не будет обнаружено вхождение
        не численного символа. Функция также проверяет, является ли число
        целочисленным или с плавающей точкой, указывая это при создании объекта Number

        Возвращаемое значение:
            Number: объект типа Number
        """
        start_index = self.pos
        is_integer = True

        while self._is_correct_pos() and self._is_digit():
            if self._get_current_letter() == Number.NUMBER_DOT:
                is_integer = False
            self._next_pos()

        number = self.expression[start_index : self.pos]

        return Number(number, is_integer)

    def _read_operator(self) -> str:
        """
        Функция, которая считывает оператор, создавая под него конкретный токен, указывая оператор

        Аргументы:
            expression (str): выражение

        Возвращаемое значение:
            list[Token]: список готовых токенов, идущих по порядку согласно выражению

        Исключения:
            SyntaxError: вызывается при нахождении неизвестного символа
        """
        operator = self._get_current_letter()
        result = ""

        match operator:
            case (
                Operator.PLUS
                | Operator.MINUS
                | Operator.LEFT_BRACKET
                | Operator.RIGHT_BRACKET
                | Operator.REMAINDER_DIVISION
            ):
                result = operator
                self._next_pos()

            case Operator.MULTIPLICATION:
                self._next_pos()
                is_power = (
                    self._is_correct_pos()
                    and self._get_current_letter() == Operator.MULTIPLICATION
                )
                if is_power:
                    result = Operator.POWER
                    self._next_pos()
                else:
                    result = Operator.MULTIPLICATION

            case Operator.DIVISION:
                self._next_pos()
                is_integer_division = (
                    self._is_correct_pos()
                    and self._get_current_letter() == Operator.DIVISION
                )
                if is_integer_division:
                    result = Operator.INTEGER_DIVISION
                    self._next_pos()
                else:
                    result = Operator.DIVISION

            case _:
                raise SyntaxError("Неизвестный оператор")

        return Operator(result)
