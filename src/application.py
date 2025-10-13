"""
Модуль приложения
"""

from src.tokenizer import Tokenizer
from src.validator import Validator
from src.calculator import Calculator
from src.exception import ExpressionError, DigitsOverFlow
from src.tokens import Token

import logging


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
    logger: logging.Logger

    def __init__(
        self, validator: Validator, tokenizer: Tokenizer, calculator: Calculator
    ) -> None:
        """
        Внедрение зависимостей
        """
        self.validator = validator
        self.tokenizer = tokenizer
        self.calculator = calculator
        self.logger = None

    def execute(self) -> None:
        """
        Функция, запускаяющая работу приложения

        Вовзращаемое значение:
            None
        """
        self._init_logger()
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

            if user_input.replace(" ", "") == "":
                continue

            try:
                self.validator.check_correctness_expression(user_input)
                tokens = self.tokenizer.tokenize(user_input)
                result = self.calculator.calculate(tokens)
            except ExpressionError as exception:
                self.logger.error(exception.__str__())
            except ZeroDivisionError as exception:
                self.logger.error(
                    "ОШИБКА: Запрещено делить на ноль"
                    + "\n"
                    + f"Эта часть выражения вызывает ошибку -> '{exception.args[0]}'"
                )
            except TypeError as exception:
                self.logger.error(
                    "ОШИБКА: Операнд слева и справа должны быть целыми для операция % и //"
                    + "\n"
                    + f"Эта часть выражения вызывает ошибку -> '{exception.args[0]}'"
                )
            except DigitsOverFlow as exception:
                self.logger.error(
                    f"ОШИБКА: Слишком большие размеры операндов -> {exception.log}"
                )
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
        expression = ""
        for token in tokens:
            expression += token.get_token() + " "
        print(f"{expression}= {result}")

    def _init_logger(self):
        LOG_FORMAT = "[%(asctime)s.%(msecs)03d][%(name)s][%(levelname)s]\n%(message)s"
        LOG_LEVEL = logging.ERROR
        LOG_FILENAME = "log.txt"
        HANLDERS = [logging.FileHandler(LOG_FILENAME), logging.StreamHandler()]

        logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, handlers=HANLDERS)

        self.logger = logging.getLogger(__name__)
