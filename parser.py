from re import compile, sub
from symbols import IF, ELIF, ELSE, FOR, WAIT, SAVE, ASSIGN, ID, INTOP, BOOLOP, COND, COLON
from productions import Statement

patterns = [COND.literal, ASSIGN.literal, INTOP.literal, BOOLOP.literal, r"[\(\):,]"]
leading = compile("(\w|[\(\)])({0})".format("|".join(patterns)))
trailing = compile("({0})(\w|[\(\)])".format("|".join(patterns)))
whitespace = compile(r"\s+")


def parse(text: str) -> list:
    # Strip comments
    text = sub("#[^\n]*\n", '\n', text)

    # Ensure operators and other special characters have leading and trailing spaces
    text_length = 0
    while len(text) != text_length:
        text_length = len(text)
        text = leading.sub(r"\1 \2", text)
        text = trailing.sub(r"\1 \2", text)
        
    # Split by line and discard empty lines - each line should represent a complete statement
    lines = (line for line in text.split('\n') if len(line) > 0 and not line.isspace())
    script = "async def __script(vars, led, lookup, random):\n"

    # Track state
    prev_indent = 0
    indent_increase = False # Does the current line end with :?
    indent_seq = None       # What character sequence is used for an indent (spaces/tabs)?
    indent_seq_len = 0

    allow_else = set()      # Which indentation levels have an open if/elif clause?
    for_loop = False        # Is the current line declaring a for loop?
    
    # Begin parsing
    for line in lines:
        indent = 0

        # On first indented line - determine the indent chars and length
        if indent_seq is None:
            if indent_increase:
                stripped = line.lstrip()
                
                indent_seq_len = len(line) - len(stripped)
                if indent_seq_len == 0:
                    raise RuntimeError("Invalid indentation on line '{0}'".format(stripped))
                
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
        tokens = whitespace.split(line)
        result = Statement.match(tokens, 0)

        if result is None:
            raise RuntimeError("Failed to parse script: error with line '{0}'".format(line))

        # Handle if/elif/else
        if (tokens[0] == ELIF or tokens[0] == ELSE) and not indent in allow_else:
            raise RuntimeError("Cannot match conditional branch to an 'if' token on line '{0}'".format(line))

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
                parsed.append(token.value + " ")
                extra = "{0}\tvars[\"{1}\"] = {2}".format(tabs, token.value, token.value)
            
            else:
                parsed.append(process_token(token, tabs))

        script = "".join([script, tabs, "".join(parsed), '\n', extra])
        prev_indent = indent

    return script


def process_token(token, tabs) -> str:
    # Handle special cases where the matched token can't be directly substituted
    if isinstance(token, ID):
        return "vars[\"{0}\"] ".format(token.value)

    elif token == WAIT:
        return "await uasyncio.sleep_ms "

    elif token == SAVE:
        return tabs.join(["led[0].duty(lookup[vars[\"r\"]])\n", "led[1].duty(lookup[vars[\"g\"]])\n", "led[2].duty(lookup[vars[\"b\"]])"])

    # Return the matched token
    elif isinstance(token, str):
        return token + " "
    
    else:
        return token.value + " "