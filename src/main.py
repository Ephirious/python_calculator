from src.application import Application
from src.tokenizer import Tokenizer
from src.validator import Validator
from src.calculator import Calculator

if (__name__ == "__main__"):
    tokenizer = Tokenizer()
    validator = Validator(tokenizer)
    calculator = Calculator()
    application = Application(validator, tokenizer, calculator)
    application.execute()