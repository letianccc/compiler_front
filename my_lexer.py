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
        self.id_type = None

    def __str__(self):
        return str(self.value)


class Lexer:
    def __init__(self, inputs):
        self.inputs = inputs
        self.tokens = list()
        self.index = 0
        self.len = len(inputs)

    def cur_char(self):
        if self.index < self.len:
            c = self.inputs[self.index]
            self.index += 1
            return c
        else:
            return None

    def return_char(self):
        self.index -= 1

    def match(self, chars):
        if self.index == self.len:
            return None

        i = self.index
        for c in chars:
            if self.inputs[i] == c:
                i += 1
            else:
                return False
        self.index = i
        return True

    def scan(self):
        while self.index < self.len:
            self.skip_space()

            if self.match_symbol():
                continue

            c = self.cur_char()
            if c is None:
                return

            if c.isalpha():
                self.return_char()
                self.match_word()

            elif c.isdigit():
                self.return_char()
                self.match_num()

            else:
                t = Token()
                t.name = c
                t.value = c
                self.tokens.append(t)

    def match_symbol(self):
        index = self.index
        s = ""
        for i in range(2):
            if index == self.len:
                return False
            c = self.inputs[index]
            s += c
            index += 1

        if s == "==" or s == "!=" or s == "&&":
            self.index = index
            t = Token()
            t.name = s
            t.value = s
            self.tokens.append(t)
            return True

        return False

    def match_num(self):
        c = self.cur_char()
        s = ""
        while c.isdigit() or c == '.':
            s += c
            c = self.cur_char()
        self.return_char()

        t = Token()
        t.type = TokenType.Number
        t.name = s
        t.value = s
        self.tokens.append(t)

    def match_word(self):
        c = self.cur_char()
        s = ""
        while c.isalnum() or c == '_':
            s += c
            c = self.cur_char()
        self.return_char()

        t = Token()
        if s in keys:
            t.type = TokenType.Key
        else:
            t.type = TokenType.Identifier
        t.name = s
        t.value = s
        self.tokens.append(t)

    def skip_space(self):
        while self.inputs[self.index].isspace():
            self.index += 1






