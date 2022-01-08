# The symbols in the light language grammar

from re import compile
from .symbol import Symbol

# Literal keywords

AND = 'and'
COLON = ":"
COMMA = ","
ELIF = "elif"
ELSE = "else"
FALSE = "False"
FOR = "for"
IF = "if"
IN = "in"
LBRACKET = "("
NOT = "not"
OR = 'or'
RBRACKET = ")"
RANDOM = "random"
RANGE = "range"
SAVE = "save"
TRUE = "True"
WAIT = "wait"
WHILE = "while"

# Modifiers

MAYBE = "?"
ANY = "*"
MANY = "+"

# Regex literals

def wholetext(s: str) -> str:
    return "^" + s + "$"

class NUM(Symbol):
    __slots__ = ()
    literal = "[0-9]+"
    regex = compile(wholetext(literal))

class ASSIGN(Symbol):
    __slots__ = ()
    literal = "\+=|\-=|\*=|\/\/=|%=|="
    regex = compile(wholetext(literal))

class INTOP(Symbol):
    __slots__ = ()
    literal = "\+|\-|\*|\/\/|%"
    regex = compile(wholetext(literal))

class COMPARE(Symbol):
    __slots__ = ()
    literal = "[<>]=?"
    regex = compile(wholetext(literal))

class EQUATE(Symbol):
    __slots__ = ()
    literal = "[=!]="
    regex = compile(wholetext(literal))

class ID(Symbol):
    __slots__ = ()
    literal = "[a-zA-Z][a-zA-Z0-9_]*"
    regex = compile(wholetext(literal))
    
    @classmethod
    def match(cls, token):
        # Prevent conflicting matches with keywords 
        return cls.regex.match(token) is not None and not (
            token == TRUE   or token == FALSE or
            token == WAIT   or token == SAVE  or
            token == WHILE  or token == IF    or
            token == ELIF   or token == ELSE  or
            token == FOR    or token == IN    or
            token == RANDOM or token == RANGE
        )