# The productions in the light language grammar

from .production import Production
from .symbols import (
    AND, ANY, ASSIGN, COLON, COMMA, COMPARE, ELIF, ELSE, EQUATE,
    FALSE, FOR, ID, IF, IN, INTOP, LBRACKET, MANY, MAYBE, NOT, NUM, OR, 
    RANDOM, RANGE, RBRACKET, SAVE, TRUE, WAIT, WHILE)

class Statement(Production):
    __slots__ = ()

class Expr(Production):
    __slots__ = ()

class ExprExt(Production):
    __slots__ = ()

class IntExt(Production):
    __slots__ = ()

class BoolExt(Production):
    __slots__ = ()

class Range(Production):
    __slots__ = ()

class RangeList(Production):
    __slots__ = ()

# Set rules once all productions are defined
Statement.rules = (
    (ID, ASSIGN, Expr),
    (WAIT, LBRACKET, Expr, RBRACKET),
    (SAVE, ),
    (WHILE, Expr, COLON),
    (IF, Expr, COLON),
    (ELIF, Expr, COLON),
    (ELSE, COLON),
    (FOR, ID, IN, Range, COLON))

Expr.rules = (
    (NUM, (IntExt, MAYBE)),
    (ID, (ExprExt, MAYBE)),
    (TRUE, (BoolExt, MAYBE)),
    (FALSE, (BoolExt, MAYBE)),
    (RANDOM, LBRACKET, Range, RBRACKET, (IntExt, MAYBE)),
    (LBRACKET, Expr, RBRACKET, (ExprExt, MAYBE)),
    (NOT, Expr))

ExprExt.rules = (
    (IntExt,),
    (BoolExt,))

IntExt.rules = (
    (INTOP, Expr),
    (COMPARE, Expr),
    (EQUATE, Expr))

BoolExt.rules = (
    (EQUATE, Expr),
    (AND, Expr),
    (OR, Expr))

Range.rules = (
    (RANGE, LBRACKET, Expr, (RangeList, MAYBE), (RangeList, MAYBE), RBRACKET),)

RangeList.rules = (
    (COMMA, Expr),)