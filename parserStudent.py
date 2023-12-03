class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0

    def tokenize(self):
        tokens = []
        while self.position < len(self.input):
            char = self.input[self.position]
            print("char: ", char, self.position)
            if char in [' ', '\n']:
                self.position += 1
                continue
            if char.isalpha():
                tokens.append(Token('VARIABLE', char))
            elif char.isdigit():
                num = ''
                while self.position < len(self.input) and self.input[self.position].isdigit():
                    num += self.input[self.position]
                    self.position += 1
                self.position -= 1
                tokens.append(Token('INTEGER', int(num)))
            elif char in "+-*/":
                tokens.append(Token('OPERATOR', char))
            elif char in'()':
                tokens.append(Token('PARENTHESIS', char))
            elif char == '=':
                tokens.append(Token('ASSIGN', char))
            elif char == ';':
                tokens.append(Token('SEMICOLON', char))
            else:
                raise ValueError(f"Invalid character: {char}")
            self.position += 1
        # print(tokens)
        return tokens


input_code = """
a = 5 + 3;
b = a * 2 - 1;
c = (a + b) * 2;
"""
# lexer = Lexer(input_code)
# tokens = lexer.tokenize()
# print(tokens)
# parser = Parser(tokens)



class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __str__(self, level=0):
        ret = "\t" * level + f'{self.type}: {self.value}\n'
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def consume(self, expected_type=None):
        print("**Consume** expected_type = ", expected_type)
        if self.position >= len(self.tokens):
            raise SyntaxError("Syntax error: unexpected end of input")
        print("self.tokens[", self.position, "]", self.tokens[self.position])
        if self.tokens[self.position].type != expected_type: # .type?
            print(self.tokens[self.position])
            print("expected_type ", expected_type)
            raise SyntaxError("unexpected end of input")
            # raise Exception("Syntax error: unexpected end of input")
            # raise Exception(f"Current token {self.tokens[self.position]} type does not match expected type: {expected_type}") # failed type:{type(self.tokens[self.position].type)}
        print("increment self.position", self.position)
        self.position += 1
        # if self.position >= len(self.tokens):
        #     raise SyntaxError("unexpected end of input")
        print("increment self.position", self.position)
        return self.tokens[self.position-1] # .type?

    def peek(self):
        print('**Peek**')
        # print(self.tokens[self.position])
        if self.position >= len(self.tokens):
            print("peek index out of range")
            return False
        index = self.position
        print(self.position)
        print(self.tokens[self.position])
        return self.tokens[index] # .type?

    def parse(self):
        root = self.parse_statement()
        return root

    def parse_statement(self):
        print("**Parse statement**")
        if self.peek() and self.peek().type == 'VARIABLE':
            return self.parse_assignment()
        else:
            return self.parse_expression()

    def parse_assignment(self):
        print("**Runnning parse assignment**")
        variable_token = self.consume('VARIABLE')
        print("\nvar_tok ", variable_token, " self.position: ", self.position)
        assign_token = self.consume('ASSIGN')
        print("\nassgn_tok", assign_token, " self.position: ", self.position)
        expression = self.parse_expression()
        print("\nexpr ", expression)
        semicolon_token = self.consume('SEMICOLON')
        print("semi_tok ", semicolon_token)
        return Node('Assignment', value=variable_token.value, children=[expression])

    def parse_expression(self):
        print("**Runnning parse expression**")
        # if self.peek().type() == 'ASSIGN':
        #     print("AHAHHAHAHHAHAHAHA ITS ASSIGN")
        term = self.parse_term()
        print("\tthe term: ", term)
        print('why the end?')
        print("self.peek()", self.peek())
        print("no end")
        while self.peek() and self.peek().type == 'OPERATOR':
            print('in while loop')
            operator_token = self.consume('OPERATOR')
            right_term = self.parse_term()
            term = Node('Expression', value=operator_token.value, children=[term, right_term])
        print("\tafter while term: ", term)
        # if self.peek().type == 'ASSIGN':
        #     raise SyntaxError("Syntax error")
        print('here')
        return term

    def parse_term(self):
        print("**Parse Term**")
        print("self.position", self.position)
        print("self.peek() ", self.peek())
        print("self.peek().type ", self.peek().type)
        if self.peek() and self.peek().type == 'PARENTHESIS' and self.peek().value == '(':
            self.consume('PARENTHESIS')  # Consume the open parenthesis
            expression = self.parse_expression()
            self.consume('PARENTHESIS')  # Consume the closing parenthesis
            return expression
        elif self.peek() and self.peek().type == 'INTEGER':
            print("trying to consume integer")
            integer_token = self.consume('INTEGER')
            print("integer consumed")
            return Node('Term', value=integer_token.value)
        elif self.peek() and self.peek().type == 'VARIABLE':
            variable_token = self.consume('VARIABLE')
            return Node('Term', value=variable_token.value)
        else:
            print("invalid term!")
            raise SyntaxError("Syntax error")

