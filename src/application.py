from src.tokenizer import Tokenizer
from src.validator import Validator
from src.calculator import Calculator
from src.exception import ExpressionError

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
        user_input = input(PROGRAMM_QUESTION)

        while (user_input != "q"):
            try:
                self.validator.check_correctness_expression(user_input)
            except ExpressionError as exception:
                print(exception)
                user_input = input(PROGRAMM_QUESTION) 
                continue

            tokens = self.tokenizer.analyze(user_input)
            result = self.calculator.calculate(tokens)

            print(f"{user_input} = {result}")           

            user_input = input(PROGRAMM_QUESTION) 