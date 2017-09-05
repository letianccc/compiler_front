from enum import Enum

keys = {"if", "else", "while", "break", "true", "false", "int", "float", }


class TokenType(Enum):
    Identifier = 1,
    Number = 2,
    Key = 3,

class Token:
    def __init__(self):
        self.type = None
        self.name = None
        self.value = None


class Lexer:
    def __init__(self, inputs):
        self.inputs = inputs
        self.tokens = list()
        self.index = 0
        self.len = len(inputs)

    def cur_char(self):
        c = self.inputs[self.index]
        self.index += 1
        return c

    def scan(self):
        while self.index < self.len:
            c = self.cur_char()
            # 过滤空字符
            while c.isspace():
                c = self.cur_char()
            # 变量
            if c.isalpha():
                s = ""
                while c.isalnum() or c == '_':
                    s += c
                    c = self.cur_char()

                t = Token()
                if s in keys:
                    t.type = TokenType.Key
                else:
                    t.type = TokenType.Identifier
                t.name = s
                t.value = s
                self.tokens.append(t)
            # 数字
            elif c.isdigit():
                s = ""
                while c.isdigit():
                    s += c
                    c = self.cur_char()
                t = Token()
                t.type = TokenType.Number
                self.tokens.append(t)








