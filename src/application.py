"""
Модуль приложения
"""

from src.tokenizer import Tokenizer
from src.validator import Validator
from src.calculator import Calculator
from src.exception import ExpressionError, DigitsOverFlow
from src.tokens import Token


class Application:
    """
    Класс-приложения

    Атрибуты:
        validator (Validator): валидатор
        tokenizer (Tokenizer): токенизатор
        calculator (Calculator): калькулятор
    """

    validator: Validator
    tokenizer: Tokenizer
    calculator: Calculator

    def __init__(
        self, validator: Validator, tokenizer: Tokenizer, calculator: Calculator
    ) -> None:
        """
        Внедрение зависимостей
        """
        self.validator = validator
        self.tokenizer = tokenizer
        self.calculator = calculator

    def execute(self) -> None:
        """
        Функция, запускаяющая работу приложения

        Вовзращаемое значение:
            None
        """
        self._start_main_loop()

    def _start_main_loop(self) -> None:
        """
        Вспомогательная функция, организующая запуск главного цикла программы

        Возвращаемое значение:
            None
        """
        PROGRAMM_QUESTION = "Введите ваше выражение: "
        STOP_SYMBOL = "q"

        while (user_input := input(PROGRAMM_QUESTION)) != STOP_SYMBOL:
            result = None

            try:
                self.validator.check_correctness_expression(user_input)
                tokens = self.tokenizer.tokenize(user_input)
                result = self.calculator.calculate(tokens)
            except ExpressionError as exception:
                print(exception)
            except ZeroDivisionError as exception:
                print("Запрещено делить на ноль")
                print(f"Эта часть выражения вызывает ошибку -> '{exception.args[0]}'")
            except TypeError as exception:
                print("Операнд слева и справа должны быть целыми для операция % и //")
                print(f"Эта часть выражения вызывает ошибку -> '{exception.args[0]}'")
            except DigitsOverFlow as exception:
                print(f"Слишком большие размеры операндов -> {exception.log}")
            else:
                self._output_result(tokens, result)

    def _output_result(self, tokens: list[Token], result: int | float) -> None:
        """
        Вспомогательная функция для удобного отображения результатов вычислений

        Аргументы:
            tokens (list[Token]): токены выражения
            result (int | float): результат выражения

        Возвращаемое значение:
            None
        """
        for token in tokens:
            print(token.get_token(), end=" ")
        print(f"= {result}")
