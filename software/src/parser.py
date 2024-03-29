from re import compile
from symbols import ASSIGN, COLON, COMMA, COMPARE, ELIF, ELSE, EQUATE, FOR, ID, IF, INTOP, LBRACKET, LED, RBRACKET, WAIT 
from productions import Statement

patterns = [ASSIGN.literal, INTOP.literal, COMPARE.literal, EQUATE.literal, "\{0}".format(LBRACKET), "\{0}".format(RBRACKET), COLON, COMMA]
adjacent = "\w|[()]"

leading = compile("({0})({1})".format(adjacent, "|".join(patterns)))
trailing = compile("({0})({1})".format("|".join(patterns), adjacent))

newline = compile("[\r\n]+")
whitespace = compile("\s+")
comment = compile("#[^\n]*")


def parse(text: str) -> list:
    # Strip comments
    text = comment.sub("", text)

    # Ensure operators and other special characters have leading and trailing spaces
    text_length = 0
    while len(text) != text_length:
        text_length = len(text)
        text = leading.sub(r"\1 \2", text)
        text = trailing.sub(r"\1 \2", text)
        
    # Split by line and discard empty lines - each line should represent a complete statement
    lines = (line for line in newline.split(text) if len(line) > 0 and not line.isspace())
    script = "async def __script(vars, pins, lookup, led, random, sin):\n"

    # Track state
    prev_indent = 0
    indent_increase = False # Does the current line end with :?
    indent_seq = None       # What character sequence is used for an indent (spaces/tabs)?
    indent_seq_len = 0

    allow_else = set()      # Which indentation levels have an open if/elif clause?
    for_loop = False        # Is the current line declaring a for loop?
    
    # Begin parsing
    i = 0
    for line in lines:
        indent = 0

        # On first indented line - determine the indent chars and length
        if indent_seq is None:
            if indent_increase:
                stripped = line.lstrip()
                
                indent_seq_len = len(line) - len(stripped)
                if indent_seq_len == 0:
                    raise RuntimeError("Invalid indentation on line '{0}'".format(line))
                
                indent_seq = line[:indent_seq_len]

        # Parse indentation
        if indent_seq is not None:    
            while line.startswith(indent_seq):
                line = line[indent_seq_len:]
                indent += 1

        tabs = '\t' * (indent + 1)

        # Check for incorrect indentation from previous line
        if (indent > prev_indent and not indent_increase) or (indent_increase and indent - prev_indent != 1):
            raise RuntimeError("Invalid indentation on line '{0}'".format(line))

        # Parse the line as a statement
        tokens = whitespace.split(line.strip())
        if not Statement.match(tokens):
            raise RuntimeError("Parsing error on line '{0}'".format(line.strip()))

        # Handle if/elif/else
        if (tokens[0] == ELIF or tokens[0] == ELSE) and not indent in allow_else:
            raise RuntimeError("Cannot match {0} to an if".format(tokens[0]))

        if tokens[0] == IF or tokens[0] == ELIF:
            allow_else.add(indent)

        elif indent in allow_else:
            allow_else.remove(indent)

        # Set flags
        for_loop = tokens[0] == FOR
        indent_increase = tokens[-1] == COLON
        
        extra = ""
        parsed = []

        for token in tokens:
            # Handle the first ID in a for loop separately
            if for_loop and isinstance(token, ID):
                for_loop = False
                parsed.append("{0} ".format(token.value))
                extra = "{0}\tvars[\"{1}\"] = {2}\n".format(tabs, token.value, token.value)
            
            else:
                parsed.append(process_token(token))

        script = "".join([script, tabs, "".join(parsed), '\n', extra])
        prev_indent = indent
        i += 1

    # Final line opens a new block
    if indent_increase:
        raise RuntimeError("Empty statement on line {0}".format(i))

    # No lines given
    if i == 0:
        return "{0}\tpass".format(script)

    return script


def process_token(token) -> str:
    # Handle special cases where the matched token can't be directly substituted
    if isinstance(token, ID):
        return "vars[\"{0}\"] ".format(token.value)

    elif token == WAIT:
        return "await uasyncio.sleep_ms "

    elif token == LED:
        return "vars[\"r\"], vars[\"g\"], vars[\"b\"] = led"

    # Return the matched token
    elif isinstance(token, str):
        return "{0} ".format(token)
    
    else:
        return "{0} ".format(token.value)