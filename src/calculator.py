from src.tokens import Token, Number, Operator

class Calculator():
    tokens: list[Token]
    tokens_length: int
    pos: int
    
    def __init__(self):
        self.tokens = None
        self.tokens_length = 0
        self.pos = 0

    def calculate(self, tokens: list[Token]):
        self.tokens = tokens
        self.tokens_length = len(self.tokens)
        self.pos = 0

        return self.expr()

    def current_token(self) -> Token:
        if self.has_next():
            return self.tokens[self.pos]
        raise Exception("No such tokens")
    
    def next_pos(self) -> None:
        self.pos += 1

    def has_next(self):
        if (self.pos < self.tokens_length):
            return True
        return False

    def expr(self) -> int:
        return self.add()

    def add(self) -> int:
        left = self.mul()
        
        while self.has_next() and (token := self.current_token()) and (token.get_token() in (Operator.PLUS, Operator.MINUS)):
            self.next_pos()
            right = self.mul()

            if (token.get_token() is Operator.PLUS):
                left += right
            else:
                left -= right

        return left

    def mul(self) -> int:
        left = self.pow()

        while self.has_next() and (token := self.current_token()) and \
            (token.get_token() in (Operator.MULTIPLICATION, Operator.DIVISION, Operator.INTEGER_DIVISION, Operator.REMAINDER_DIVISION)):
            self.next_pos()
            right = self.pow()

            match(token.get_token()):
                case Operator.MULTIPLICATION:
                    left *= right
                case Operator.DIVISION:
                    left /= right
                case Operator.INTEGER_DIVISION:
                    left //= right
                case Operator.REMAINDER_DIVISION:
                    left %= right
        
        return left

    def pow(self) -> int:
        left = self.unary()

        while self.has_next() and (token := self.current_token()) and (token.get_token() is Operator.POWER):
            self.next_pos()
            right = self.pow()
            
            left **= right

        return left

    def unary(self) -> int:
        token = self.current_token()

        is_operator = token.get_token() in (Operator.PLUS, Operator.MINUS)
        if is_operator:
            self.next_pos()
            value = self.unary()
            
            if token.get_token() is Operator.PLUS:
                return +value
            else:
                return -value

        else:
            return self.primary()
                
    def primary(self) -> int:
        if self.has_next():
            token = self.current_token()
            self.next_pos()
            
            if isinstance(token, Number):
                return int(token.get_token())
            elif token.get_token() is Operator.LEFT_BRACKET:
                result = self.expr()
                self.next_pos()
                return result