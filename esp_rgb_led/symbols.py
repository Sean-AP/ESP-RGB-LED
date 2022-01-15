# The symbols in the light language grammar

from re import compile
from symbol import Symbol

# Literal keywords

AND = "and"
CEIL = "ceil"
COLON = ":"
COMMA = ","
ELIF = "elif"
ELSE = "else"
FALSE = "False"
FLOOR = "floor"
FOR = "for"
IF = "if"
IN = "in"
LBRACKET = "("
MAX = "max"
MIN = "min"
NOT = "not"
OR = "or"
RAD = "rad"
RBRACKET = ")"
RANDOM = "random"
RANGE = "range"
ROUND = "round"
SAVE = "save"
SIN = "sin"
TRUE = "True"
WAIT = "wait"
WHILE = "while"

keywords = [
    AND, CEIL, ELIF, ELSE, FALSE, FLOOR, FOR, IF, IN, MAX, MIN, NOT, OR, RAD, RANDOM, RANGE, ROUND, SAVE, SIN, TRUE, WAIT, WHILE
]

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
    literal = "\+|\-|\*|\/|%"
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
        return cls.regex.match(token) is not None and not any([token == word for word in keywords])