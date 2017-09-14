


class Stmt:
    def gen(self, generator):
        return generator.generate(self)


class SeqStmt(Stmt):
    def __init__(self):
        self.left = None
        self.right = None

    # def gen(self, generator):
    #     generator.generate(self)

    # def traverse(self):
    #     print(type(self))
    #     print(type(self.left))
    #     if self.left.__class__ == SeqStmt:
    #         self.left.traverse()
    #     if self.right.__class__ == SeqStmt:
    #         self.right.traverse()


class DeclStmt(Stmt):
    def __init__(self, variable):
        self.variable = variable

    # def gen(self, generator):
    #     generator.generate(self)


class AllocStmt(Stmt):
    def __init__(self):
        self.variable = None
        self.value = None

    # def gen(self, generator):
    #     # print(self.__class__ == AllocStmt)
    #     generator.generate(self)


class IfStmt(Stmt):
    def __init__(self):
        self.cond = None
        self.block = None

    # def gen(self, generator):
    #     generator.generate(self)


class ElseStmt(Stmt):
    def __init__(self):
        self.cond = None
        self.if_block = None
        self.else_block = None

    # def gen(self, generator):
    #     generator.generate(self)


class Expression:
    def gen(self, generator):
        return generator.generate(self)


class OrExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None

    # def gen(self, generator):
    #     generator.generate(self)


class AndExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None

    # def gen(self, generator):
    #     generator.generate(self)


class EqualExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None
        self.op = None

    # def gen(self, generator):
    #     generator.generate(self)


class RelExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None
        self.rel = None

    # def gen(self, generator):
    #     generator.generate(self)


class LowTermExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None
        self.op = None

    # def gen(self, generator):
    #     generator.generate(self)


class UpTermExpr(Expression):
    def __init__(self):
        self.left = None
        self.right = None
        self.op = None

    # def gen(self, generator):
    #     generator.generate(self)


class UnaryEpxr(Expression):
    def __init__(self):
        self.prefix = None
        self.expression = None

    # def gen(self, generator):
    #     generator.generate(self)


class FactorExpr(Expression):
    def __init__(self):
        self.expression = None

    # def gen(self, generator):
    #     generator.generate(self)

