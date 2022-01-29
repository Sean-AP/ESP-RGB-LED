# The productions in the light language grammar

from production import Production
from symbols import (
    AND, ANY, ASSIGN, BREAK, CEIL, COLON, COMMA, COMPARE, ELIF, ELSE, EQUATE,
    FALSE, FLOOR, FOR, ID, IF, IN, INTOP, LBRACKET, MANY, MAYBE, MAX, MIN,
    NOT, NUM, OR, RAD, RANDOM, RANGE, ROUND, RBRACKET, SAVE, SIN, TRUE, WAIT, WHILE)

class Statement(Production):
    __slots__ = ()

class Expr(Production):
    __slots__ = ()

class ExprExt(Production):
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
    (BREAK, ),
    (WHILE, Expr, COLON),
    (IF, Expr, COLON),
    (ELIF, Expr, COLON),
    (ELSE, COLON),
    (FOR, ID, IN, Range, COLON))

Expr.rules = (
    (NUM, (ExprExt, MAYBE)),
    (ID, (ExprExt, MAYBE)),
    (TRUE, (BoolExt, MAYBE)),
    (FALSE, (BoolExt, MAYBE)),
    (NOT, Expr),
    (RANDOM, LBRACKET, Range, RBRACKET, (ExprExt, MAYBE)),
    (MAX, LBRACKET, Expr, COMMA, Expr, RBRACKET, (ExprExt, MAYBE)),
    (MIN, LBRACKET, Expr, COMMA, Expr, RBRACKET, (ExprExt, MAYBE)),
    (ROUND, LBRACKET, Expr, RBRACKET, (ExprExt, MAYBE)),
    (CEIL, LBRACKET, Expr, RBRACKET, (ExprExt, MAYBE)),
    (FLOOR, LBRACKET, Expr, RBRACKET, (ExprExt, MAYBE)),
    (RAD, LBRACKET, Expr, RBRACKET, (ExprExt, MAYBE)),
    (SIN, LBRACKET, Expr, RBRACKET, (ExprExt, MAYBE)),
    (LBRACKET, Expr, RBRACKET, (ExprExt, MAYBE)))

ExprExt.rules = (
    (INTOP, Expr),
    (COMPARE, Expr),
    (BoolExt,))

BoolExt.rules = (
    (EQUATE, Expr),
    (AND, Expr),
    (OR, Expr),
    (IF, Expr, ELSE, Expr))

Range.rules = (
    (RANGE, LBRACKET, Expr, (RangeList, MAYBE), (RangeList, MAYBE), RBRACKET),)

RangeList.rules = (
    (COMMA, Expr),)