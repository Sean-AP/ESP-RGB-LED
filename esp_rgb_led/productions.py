# The productions in the light language grammar

from production import Production
from symbols import (
    ANY, ASSIGN, BOOLOP, COLON, COMMA, COND, ELIF, ELSE, 
    FALSE, FOR, ID, IF, IN, INTOP, LBRACKET, MANY, MAYBE, 
    NOT, NUM, RANDOM, RANGE, RBRACKET, SAVE, TRUE, WAIT, WHILE)


class Statement(Production):
    __slots__ = ()

class Expr(Production):
    __slots__ = ()

class ExprExt(Production):
    __slots__ = ()

class Range(Production):
    __slots__ = ()

class RangeList(Production):
    __slots__ = ()


Statement.rules = (
    (ID, ASSIGN, Expr),
    (WAIT, LBRACKET, Expr, RBRACKET),
    (SAVE, ),
    (WHILE, Expr, COLON),
    (IF, Expr, COLON),
    (ELIF, Expr, COLON),
    (ELSE, Expr, COLON),
    (FOR, ID, IN, Range, COLON)
)


Expr.rules = (
    (NUM, (ExprExt, MAYBE)),
    (ID, (ExprExt, MAYBE)),
    (TRUE, (ExprExt, MAYBE)),
    (FALSE, (ExprExt, MAYBE)),
    (NOT, Expr, (ExprExt, MAYBE)),
    (RANDOM, LBRACKET, Range, RBRACKET),
    (LBRACKET, Expr, RBRACKET)
)


ExprExt.rules = (
    (INTOP, Expr),
    (BOOLOP, Expr),
    (COND, Expr)
)


Range.rules = (
    (RANGE, LBRACKET, Expr, (RangeList, MAYBE), (RangeList, MAYBE), RBRACKET),
)


RangeList.rules = (
    (COMMA, Expr),
)