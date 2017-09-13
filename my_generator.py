from my_parser import *
from my_lexer import Token


class Generator:
    count = 0

    def generate(self, tree):
        func = {SeqStmt: self.seq_gen,
                DeclStmt: self.decl_gen,
                AllocStmt: self.alloc_gen,
                IfStmt: self.if_gen,
                ElseStmt: self.else_gen,
                OrExpr: self.or_gen,
                AndExpr: self.and_gen,
                EqualExpr: self.equal_gen,
                RelExpr: self.rel_gen,
                LowTermExpr: self.low_term_gen,
                UpTermExpr: self.up_term_gen,
                UnaryEpxr: self.unary_gen,
                FactorExpr: self.fact_gen,
                Token: self.tok_gen,
                }
        type = tree.__class__
        # if type == SeqStmt or type == DeclStmt or type == AllocStmt or type == Token or type == FactorExpr:
        return func[type](tree)

    def traverse(self, tree):
        print(type(tree))
        if tree.__class__ == SeqStmt:
            self.traverse(tree.left)
            self.traverse(tree.right)

    def seq_gen(self, seq_stmt):
        seq_stmt.left.gen(self)
        if seq_stmt.right:
            seq_stmt.right.gen(self)

    def decl_gen(self, decl_stmt):
        t = decl_stmt.variable
        t.count = Generator.count
        Generator.count += 1
        print(t.id_type + " " + str(t.gen(self)) + ";")

    def alloc_gen(self, alloc_stmt):
        variable = alloc_stmt.variable.gen(self)
        # print(type(alloc_stmt.value))
        value = alloc_stmt.value.gen(self)
        print(variable + " = " + value + ";")
        # print(alloc_stmt.variable.gen(self) + " = " + alloc_stmt.value.gen(self))

    def if_gen(self, if_stmt):
        print("if false" + if_stmt.cond_expr)

    def else_gen(self, else_stmt):
        return

    def or_gen(self, or_expr):
        code = or_expr.left.gen(self)
        if or_expr.right:
            code += " || "
            code += or_expr.right.gen(self)
        return code

    def and_gen(self, and_expr):
        code = and_expr.left.gen(self)
        if and_expr.right:
            code += " && "
            code += and_expr.right.gen(self)
        return code

    def equal_gen(self, equal_expr):
        code = equal_expr.left.gen(self)
        if equal_expr.right:
            code += " " + equal_expr.op + " "
            code += equal_expr.right.gen(self)
        return code

    def rel_gen(self, rel_expr):
        code = rel_expr.left.gen(self)
        if rel_expr.right:
            code += " " + rel_expr.rel + " "
            code += rel_expr.right.gen(self)
        return code

    def low_term_gen(self, low_term_expr):
        code = low_term_expr.left.gen(self)
        if low_term_expr.right:
            code += " " + low_term_expr.op + " "
            code += low_term_expr.right.gen(self)
        return code

    def up_term_gen(self, up_term_expr):
        code = up_term_expr.left.gen(self)
        if up_term_expr.right:
            code += " " + up_term_expr.op + " "
            code += up_term_expr.right.gen(self)
        return code

    def unary_gen(self, unary_expr):
        code = unary_expr.prefix
        code += unary_expr.expression.gen(self)
        return code

    def fact_gen(self, fact_expr):
        # print(type(fact_expr.expression))
        return fact_expr.expression.gen(self)

    def tok_gen(self, token):
        # print("ddddd")
        if token.type == TokenType.Identifier:
            # print("tttttt", token.count)
            return "t" + str(token.count)
        # print("tttttt", token)
        return str(token.value)

