from src.tokenizer import Tokenizer
from src.validator import Validator
from src.calculator import Calculator
from src.exception import ExpressionError, DigitsOverFlow
from src.tokens import Token


class Application:
    validator: Validator
    tokenizer: Tokenizer
    calculator: Calculator

    def __init__(self, validator, tokenizer, calculator):
        self.validator = validator
        self.tokenizer = tokenizer
        self.calculator = calculator

    def execute(self):
        self._start_main_loop()

    def _start_main_loop(self):
        PROGRAMM_QUESTION = "Please write your expression: "

        while (user_input := input(PROGRAMM_QUESTION)) != "q":
            result = None

            try:
                self.validator.check_correctness_expression(user_input)
                tokens = self.tokenizer.tokenize(user_input)
                result = self.calculator.calculate(tokens)
            except ExpressionError as exception:
                print(exception)
            except ZeroDivisionError as exception:
                print("Запрещено делить на ноль.")
                print(f"Эта часть выражения вызывает ошибку -> '{exception.args[0]}'")
            except TypeError as exception:
                print("Операнд слева должен быть целым для операция % и //.")
                print(f"Эта часть выражения вызывает ошибку -> '{exception.args[0]}'")
            except DigitsOverFlow as exception:
                print(f"Слишком большие размеры операндов -> {exception.log}")
            else:
                self._output_result(tokens, result)

    def _output_result(self, tokens: list[Token], result: int | float) -> None:
        for token in tokens:
            print(token.get_token(), end=" ")
        print(f"= {result}")
