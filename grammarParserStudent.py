import re
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
        #   Your task: Import your code from Project #1 and you will need to update the tokenize function to add the following new functionalities: 
            #	Construct regular expressions to support float data types
            #	Construct regular expressions to support multi character variable names
            #	Add support for character data types
            #	Add support for integer data types
        tokens = []
        while self.position < len(self.input):
            char = self.input[self.position]
            print("char: ", char, self.position)
            if char.isspace():
                self.position += 1
                continue
            if char in [' ', '\n']:
                self.position += 1
                continue
            ## elif block to handle float data type
            ## !!! This is your task - Please complete this elif block to handle float data type !!! 

            # Regular expression to check for data types, should be done before processing the VARIABLE token
            elif re.match(r'float|char|int', self.input[self.position:]):
                match = re.match(r'float|char|int', self.input[self.position:])
                value = match.group(0)
                self.position += len(value)
                tokens.append(Token('TYPE', value))
            ## !!!! Complete the rest of the code !!!!
            elif char.isalpha():
                # var = ''
                # while self.position < len(self.input) and (self.input[self.position].isalnum() or self.input[self.position] == '_'):
                #     var += self.input[self.position]
                #     self.position += 1
                tokens.append(Token('VARIABLE', char))
            elif char.isdigit():
                num = ''
                token_is_float = False
                while self.position < len(self.input) and (self.input[self.position].isdigit() or self.input[self.position] == '.'):
                    if self.input[self.position] == '.':
                        token_is_float = True
                    num += self.input[self.position]
                    self.position += 1
                self.position -= 1
                if token_is_float:
                    tokens.append(Token('FLOAT', float(num)))
                else:
                    tokens.append(Token('INTEGER', int(num)))
            elif char == "'":
                self.position += 1
                tokens.append(Token('CHAR', self.input[self.position]))
                self.position += 1
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
        print("Tokens:", tokens)
        return tokens




class SymbolTable:
    def __init__(self):
        self.table = {}

    def add(self, identifier, type, initialized=False):
        pass
        # Your task: Complete the function

    def is_initialized(self, identifier):
        pass
        # Your task: Complete the function

    def set_initialized(self, identifier):
        pass
        # Your task: Complete the function

    def lookup(self, identifier):
        pass
        # Your task: Complete the function

    def update(self, identifier, newType):
        pass
        # Your task: Complete the function

class TypeChecker:

    @staticmethod
    def check_assignment(target_type, value_type):
        pass
        # Your task: Complete the function
    
    @staticmethod
    def result_type_of_op(left_type, op, right_type):
        """
        Determines the resulting type of a binary operation given the types of its operands.

        Args:
            left_type (str): The type of the left operand.
            op (str): The operator being applied.
            right_type (str): The type of the right operand.

        Returns:
            str: The resulting type of the operation.
        """
        valid_ops = ['+', '-', '*', '/'] #Hint
        # Your task: Complete the function

    @staticmethod
    def check_op(left_type, op, right_type):
        pass
        # Your task: Complete the function

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
        self.symbol_table = SymbolTable()

    # Code from project 1
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

    # Code from project 1
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

    # Code from project 1
    def parse(self):
        root = self.parse_statement()
        return root

    # Code from project 1
    def parse_statement(self):
        # Please reuse your code from project #1
        token = self.peek()
        # Parse declaration if token is TYPE
        if token.type == 'TYPE':
            return self.parse_declaration()
        # !! Your task: import the code from your project 1 code here or write your own code!!
        print("**Parse statement**")
        if self.peek() and self.peek().type == 'VARIABLE':
            return self.parse_assignment()
        else:
            return self.parse_expression()

    def parse_declaration(self):
        # Need to consume TYPE token
        type_token = self.consume('TYPE')
        var_token = self.consume('VARIABLE')
        expression_node = None

        declared_type = type_token.value.upper()
        if declared_type == 'INT':
            declared_type = 'INTEGER'  
            
        # !!!!! Your task: Complete the rest of the function !!!!!

    # Code from project 1
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

    # Code from project 1
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

    # Code from project 1
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