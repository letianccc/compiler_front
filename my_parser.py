from debug import log_list
from my_lexer import TokenType
from my_ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        # self.token = tokens[0]
        self.index = 0
        self.len = len(tokens)
        self.env = Env()

    def cur_tok(self):
        t = self.tokens[self.index]
        # print(t.value, end=" ")
        self.index += 1
        return t

    def return_tok(self):
        self.index -= 1

    def log_tok(self):
        t = self.tokens[self.index]
        print(t)

    def match(self, char):
        if self.index == self.len:
            # print(self.tokens[self.index-10])
            return None
        t = self.tokens[self.index]
        if t.value == char:
            self.index += 1
            return True
        else:
            return False

    def parse(self):
        return self.block()

    def block(self):
        if self.match('{'):
            self.env.next = Env()
            self.env.next.prior = self.env
            self.env = self.env.next

            stmt = SeqStmt()
            stmt.left = self.stmt()
            block_head = stmt
            while not self.match('}'):
                stmt.right = SeqStmt()
                seq_stmt = stmt.right
                seq_stmt.left = self.stmt()
                stmt = seq_stmt
            self.env = self.env.prior

        else:
            block_head = self.stmt()

        return block_head

    def stmt(self):
        t = self.cur_tok()
        value = t.value

        if value == "int" or value == "float":
            stmt = self.decl_stmt(value)
            self.check_semicolon()

        elif value == "if":
            stmt = self.if_stmt()

        else:
            variable = self.check_decl(value)
            # variable = self.variable_t(value)
            stmt = self.alloc_stmt(variable)
            self.check_semicolon()

        return stmt

    def decl_stmt(self, type):
        variable_t = self.cur_tok()
        assert variable_t.type == TokenType.Identifier
        variable_t.id_type = type
        self.env.save[variable_t.name] = variable_t

        return DeclStmt(variable_t)

    def if_stmt(self):
        self.match('(')
        cond_expr = self.bool_expr()
        self.match(')')
        if_block = self.block()
        if self.match("else"):
            stmt = ElseStmt()
            stmt.else_block = self.block()
        else:
            stmt = IfStmt()
        stmt.cond = cond_expr
        stmt.if_block = if_block

        return stmt

    def alloc_stmt(self, variable):
        if self.match('='):
            # variable_t = self.variable_t(variable)

            # value = self.expr()
            # variable_t.value = value
            stmt = AllocStmt()
            stmt.variable = variable
            stmt.value = self.expr()

            return stmt
        else:
            raise Exception("allocate stmt error", variable)

    def check_decl(self, variable):
        e = self.env
        while e:
            for variable_name, variable_tok in e.save.items():
                if variable == variable_name:
                    return variable_tok
            e = e.prior
        raise Exception(variable + " is not in env")

    def check_alloc(self, variable):
        t = self.check_decl(variable)
        if not t.value:
            raise Exception(variable + " is not allocated")
        return t

    def check_semicolon(self):
        if not self.match(';'):
            raise Exception("the lack of ';'")

    def expr(self):
        return self.bool_expr()

    def bool_expr(self):
        return self.or_expr()

    def or_expr(self):
        expr = self.and_expr()
        if self.match('|'):
            or_expr = OrExpr()
            or_expr.left = expr
            or_expr.right = self.and_expr()
            expr = or_expr
        return expr

    def and_expr(self):
        expr = self.equal_expr()
        if self.match("&&"):
            and_expr = AndExpr()
            and_expr.left = expr
            and_expr.right = self.equal_expr()
            expr = and_expr
        return expr

    def equal_expr(self):
        expr = self.rel()
        s = self.cur_tok().value
        if s == "==" or s == "!=":
            equal_expr = EqualExpr()
            equal_expr.op = s
            equal_expr.left = expr
            equal_expr.right = self.rel()
            expr = equal_expr
        else:
            self.return_tok()
        return expr

    def rel(self):
        expr = self.low_term()
        t = self.cur_tok()
        if t.value == "<" or t.value == "<=" or t.value == ">" or t.value == ">=":
            rel_expr = RelExpr()
            rel_expr.op = t.value
            rel_expr.left = expr
            rel_expr.right = self.low_term()
            expr = rel_expr
        else:
            self.return_tok()
        return expr

    def low_term(self):
        expr = self.up_term()
        t = self.cur_tok()
        if t.value == "+" or t.value == "-":
            low_term_expr = LowTermExpr()
            low_term_expr.op = t.value
            low_term_expr.left = expr
            low_term_expr.right = self.up_term()
            expr = low_term_expr
        else:
            self.return_tok()
        return expr

    def up_term(self):
        expr = self.unary_expr()
        t = self.cur_tok()
        if t.value == "*" or t.value == "/":
            up_term_expr = UpTermExpr()
            up_term_expr.op = t.value
            up_term_expr.left = expr
            up_term_expr.right = self.unary_expr()
            expr = up_term_expr
        else:
            self.return_tok()
        return expr

    def unary_expr(self):
        t = self.cur_tok()
        if t.value == "!" or t.value == "-":
            unary_expr = UnaryEpxr()
            unary_expr.prefix = t.value
            unary_expr.expression = self.factor_expr()
            expr = unary_expr
        else:
            self.return_tok()
            expr = self.factor_expr()
        return expr

    def factor_expr(self):
        if self.index == self.len:
            return None

        factor_expr = FactorExpr()
        if self.match('('):
            factor_expr.expression = self.expr()
            self.match(')')
        else:
            t = self.cur_tok()
            if t.type == TokenType.Identifier:
                identifier = self.check_alloc(t.name)
                # variable_t = self.variable_t(t.name)
                factor_expr.expression = identifier
                return factor_expr
            else:
                factor_expr.expression = t

        return factor_expr


class Env:
    def __init__(self):
        self.save = dict()
        self.next = None
        self.prior = None
