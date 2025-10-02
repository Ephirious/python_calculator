from src.tokens import Token, Operator, Number


class Tokenizer:
    expression: str
    expression_length: int
    pos: int

    def __init__(self):
        self.expression = ""
        self.expression_length = 0
        self.pos = 0

    def tokenize(self, expression) -> list[Token]:
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
        return self.pos < self.expression_length

    def _get_current_letter(self) -> str:
        if self._is_correct_pos():
            return self.expression[self.pos]
        else:
            raise Exception("Некорректная позиция курсора в выражении")

    def _next_pos(self) -> None:
        self.pos += 1

    def _is_digit(self):
        return (self._get_current_letter().isdigit()) or (
            self._get_current_letter() == Number.NUMBER_DOT
        )

    def _read_number(self) -> str:
        start_index = self.pos
        is_integer = True

        while self._is_correct_pos() and self._is_digit():
            if self._get_current_letter() == Number.NUMBER_DOT:
                is_integer = False
            self._next_pos()

        number = self.expression[start_index : self.pos]

        return Number(number, is_integer)

    def _read_operator(self):
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
                raise Exception("Неизвестный оператор")

        return Operator(result)
