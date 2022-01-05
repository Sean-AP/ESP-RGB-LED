# The symbols in the light language grammar

from re import compile
from symbol import Symbol

# Literal keywords

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

class INTOP(Symbol):
    __slots__ = ()
    literal = "\+|\-|\*|\/\/|%"
    regex = compile(wholetext(literal))

class BOOLOP(Symbol):
    __slots__ = ()
    literal = "&&|\|\|"
    regex = compile(wholetext(literal))

class COND(Symbol):
    __slots__ = ()
    literal = "[=!]=|[<>]=?"
    regex = compile(wholetext(literal))

class ASSIGN(Symbol):
    __slots__ = ()
    literal = "\+=|\-=|\*=|\/\/=|%=|="
    regex = compile(wholetext(literal))

class ID(Symbol):
    __slots__ = ()
    literal = "[a-zA-Z][a-zA-Z0-9_]*"
    regex = compile(wholetext(literal))
    
    @classmethod
    def match(cls, token):
        return (
            cls.regex.match(token) is not None and
            # Prevent conflicting matches with keywords 
            not token == TRUE and
            not token == FALSE and 
            not token == WAIT and
            not token == SAVE and
            not token == WHILE and
            not token == IF and
            not token == ELSE and
            not token == FOR and
            not token == IN and
            not token == RANGE and
            not token == RANDOM 
        )