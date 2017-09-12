from debug import log_list
from my_lexer import TokenType

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
        block_head = None
        if self.match('{'):
            # self.env.next = Env()
            # self.env.next.prior = self.env
            # self.env = self.env.next

            stmt = self.stmt()
            block_head = stmt
            while not self.match('}'):
                # print("dd")
                # self.log_tok()
                seq_stmt = SeqStmt()
                seq_stmt.left = stmt
                seq_stmt.right = self.stmt()
                stmt = seq_stmt


            # self.env = self.env.prior

        else:
            block_head = self.stmt()

        return block_head

    def stmt(self):
        value = self.cur_tok().value

        if value == "int" or value == "float":
            stmt = self.decl_stmt(value)
            self.check_semicolon()

        elif value == "if":
            stmt = self.if_stmt()

        else:
            stmt = self.alloc_stmt(value)
            self.check_semicolon()

        return stmt

    def decl_stmt(self, type):
        identifier = self.cur_tok()
        assert identifier.type == TokenType.Identifier
        identifier.id_type = type
        self.env.save.append(identifier)

        return DeclStmt(type, identifier.name)

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

    def alloc_stmt(self, value):
        id = value
        # if id in self.env.save.keys():
        #     self.log_tok()
        if self.match('='):
            value = self.expr()
            # self.env.save[id] = value
            stmt = AllocStmt()
            stmt.variable = id
            stmt.value = value

            return stmt
        else:
            raise Exception("allocate stmt error", id)

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
            factor_expr.expression = self.cur_tok()

        return factor_expr


class Env:
    def __init__(self):
        self.save = list()
        self.next = None
        self.prior = None


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


class AllocStmt(Stmt):
    def __init__(self):
        self.variable = None
        self.value = None


class IfStmt(Stmt):
    def __init__(self):
        self.cond = None
        self.block = None


class ElseStmt(Stmt):
    def __init__(self):
        self.cond = None
        self.if_block = None
        self.else_block = None


class Expression:
    pass


class OrExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None


class AndExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None


class EqualExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None
        self.op = None


class RelExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None
        self.rel = None


class LowTermExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None
        self.op = None


class UpTermExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None
        self.op = None


class UnaryEpxr(Expression):
    def __init__(self):
        self.prefix = None
        self.expression = None


class FactorExpr(Expression):
    def __init__(self):
        self.expression = None

