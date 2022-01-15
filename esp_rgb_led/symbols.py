# The symbols in the light language grammar

from re import compile
from symbol import Symbol

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
MAX = "max"
MIN = "min"
NOT = "not"
OR = 'or'
RBRACKET = ")"
RANDOM = "random"
RANGE = "range"
SAVE = "save"
TRUE = "True"
WAIT = "wait"
WHILE = "while"

keywords = [
    AND, ELIF, ELSE, FALSE, FOR, IF, IN, MAX, MIN, NOT, OR, RANDOM, RANGE, SAVE, TRUE, WAIT, WHILE
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
        return cls.regex.match(token) is not None and not any([token == word for word in keywords])