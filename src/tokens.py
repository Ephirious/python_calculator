class Token():
    value: str

    def __init__(self, token: str):
        self.value = token

    def get_token(self) -> str:
        return self.value
    
    def __repr__(self):
        return f"{type(self).__name__}({self.value})"
    
    def __str__(self):
        return self.value
    

class Operator(Token):
    PLUS = "+"
    MINUS = "-"
    MULTIPLICATION = "*"
    POWER = "**"
    DIVISION = "/"
    INTEGER_DIVISION = "//"
    LEFT_BRACKET = "("
    RIGHT_BRACKET = ")"
    REMAINDER_DIVISION = "%"

    def __init__(self, token: str):
        super().__init__(token)


class Number(Token):
    def __init__(self, token: str):
        super().__init__(token)