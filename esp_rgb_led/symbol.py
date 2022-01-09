# Regex-based symbol for capturing terminals
# Strings are used for literal tokens
class Symbol:
    __slots__ = "value"
    literal = ""
    regex = None

    def __init__(self, value):
        self.value = value

    @classmethod
    def match(cls, token):
        return cls.regex.match(token) is not None


def isterminal(lexeme):
    return isinstance(lexeme, str) or issubclass(lexeme, Symbol)