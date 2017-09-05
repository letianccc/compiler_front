
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        # self.token = tokens[0]
        self.index = 0
        self.len = len(tokens)

    def cur_tok(self):
        t = self.tokens[self.index]
        self.index += 1
        return t

    def return_tok(self):
        self.index -= 1

    def match(self, char):
        cur_tok = self.tokens[self.index]
        if cur_tok.name == char:
            self.index += 1
            return True
        else:
            return False



    def parse(self):

        stmt = SeqStmt()
        while self.index < self.len:



    def stmt(self):
        t = self.cur_tok()
        if t.name == "int" or t.name == "float":
            stmt = self.decl_stmt(t.name)
        elif t.name == "if":
            self.match('(')
            cond_expr =



    def decl_stmt(self, type):
        identifier = self.cur_tok()
        return DeclStmt(type, identifier)

    def bool_expr(self):

    def or_expr(self):
        expr = and_expr()
        if self.match('|'):











class Stmt:
    pass

class SeqStmt(Stmt):
    def __init__(self):
        self.left = None
        self.right = None


class DeclStmt(Stmt):
    def __init__(self, type, identifier):
        self.type = type
        self.identifier = identifier




