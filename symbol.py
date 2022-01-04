# Terminal and non-terminal symbol definitions

class Symbol:
    # Regex-based symbol for capturing terminals
    __slots__ = "value"

    literal = ""
    regex = None

    @classmethod
    def match(cls, token):
        return cls.regex.match(token) is not None


def match_terminal(symbol, tokens: list, index: int) -> int:
    # Consume the token if it matches the terminal symbol
    if isinstance(symbol, str):
        return index + 1 if tokens[index] == symbol else None

    elif symbol.match(tokens[index]):
        # Create a new instance of the terminal symbol, saving the token that it matched
        match = symbol()
        match.value = tokens[index]

        tokens[index] = match
        print(tokens[index])
        return index + 1

    else:
        return None


def match_nonterminal(symbol, tokens: list, index: int) -> int:
        return symbol.match(tokens, index)