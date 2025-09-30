from src.tokens import Token, Operator, Number

class Tokenizer:
    expression: str
    expression_length: int
    pos: int

    def __init__(self):
        self.expression = ""
        self.expression_length = 0
        self.pos = 0


    def analyze(self, expression) -> list[Token]:
        tokens = list()
        self.expression = expression
        self.expression_length = len(self.expression)
        self.pos = 0

        while (self.is_correct_pos()):
            if (self.get_current_letter().isspace()):
                self.next_pos()
            elif (self.get_current_letter().isdigit()):
                number = self.read_number()
                tokens.append(number)
            else:
                operator = self.read_operator()
                tokens.append(operator)

        return tokens

    def remove_spaces(self):
        self.expression = self.expression.replace(" ", "")

    def is_correct_pos(self) -> bool:
        return (self.pos < self.expression_length)
    
    def get_current_letter(self) -> str:
        if (self.is_correct_pos()):
            return self.expression[self.pos]
        else:
            raise Exception("Некорректная позиция курсора в выражении")
        
    def next_pos(self) -> None:
        self.pos += 1

    def read_number(self) -> str:
        start_index = self.pos

        while (self.is_correct_pos() and self.get_current_letter().isdigit()):
            self.next_pos()

        number = self.expression[start_index:self.pos]
        return Number(number)
    
    def read_operator(self):
        operator = self.get_current_letter()
        result = ""

        match(operator):
            case Operator.PLUS | Operator.MINUS | Operator.LEFT_BRACKET | Operator.RIGHT_BRACKET | Operator.REMAINDER_DIVISION:
                result = operator
                self.next_pos()
            
            case Operator.MULTIPLICATION:
                self.next_pos()
                is_power = (self.is_correct_pos() and self.get_current_letter() == Operator.MULTIPLICATION)
                if (is_power):
                    result = Operator.POWER
                    self.next_pos()
                else:
                    result = Operator.MULTIPLICATION
            
            case Operator.DIVISION:
                self.next_pos()
                is_integer_division = (self.is_correct_pos() and self.get_current_letter() == Operator.DIVISION)
                if (is_integer_division):
                    result = Operator.INTEGER_DIVISION
                    self.next_pos()
                else:
                    result = Operator.DIVISION
            
            case _:
                raise Exception("Неизвестный оператор")
        
        return Operator(result)