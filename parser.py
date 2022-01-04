from re import compile, sub
from symbols import IF, ELIF, ELSE, FOR, WAIT, SAVE, ASSIGN, ID, INTOP, BOOLOP, COND, COLON
from productions import Statement

patterns = [COND.literal, ASSIGN.literal, INTOP.literal, BOOLOP.literal, r"[\(\):,]"]
leading = compile("(\w)({0})".format("|".join(patterns)))
trailing = compile("({0})(\w)".format("|".join(patterns)))
whitespace = compile(r"\s+")


def parse(text: str) -> list:
    # Replace groups of 4 spaces with tabs
    text = sub("    ", '\t', text)

    # Strip comments
    text = sub("#[^\n]*\n", '\n', text)

    # Ensure operators and other special characters have leading and trailing spaces
    text = leading.sub(r"\1 \2", text)
    text = trailing.sub(r"\1 \2", text)

    # Split by line and discard empty lines - each line should represent a complete statement
    lines = (line for line in text.split('\n') if len(line) > 0)
    script = "async def __script(vars, led, lookup, rng):\n"

    # Track previous state
    prev_indent = 0
    allow_else = False      # Can the next line start with elif/else?
    for_loop = False        # Is the current line declaring a for loop?
    indent_increase = False # Does the current line end with :?

    # Begin parsing
    for line in lines:
        # Count leading tabs
        stripped = line.lstrip('\t')
        indent = len(line) - len(stripped)
        tabs = '\t' * (indent + 1)

        # Check for incorrect indentation from previous line
        if (indent > prev_indent and not indent_increase) or (indent < prev_indent and indent_increase):
            raise RuntimeError("Invalid indentation on line '{0}'".format(stripped))

        # Parse the line as a statement
        tokens = whitespace.split(stripped)
        result = Statement.match(tokens, 0)

        if result is None:
            raise RuntimeError("Failed to parse script: error with line '{0}'".format(stripped))

        # Check for illegal usage of elif/else
        if (tokens[0] == ELIF or tokens[0] == ELSE) and not allow_else:
            raise RuntimeError("Cannot match conditional branch to an 'if' token on line '{0}'".format(stripped))

        # Set flags
        allow_else = tokens[0] == IF or (allow_else and tokens[0] == ELIF)
        for_loop = tokens[0] == FOR
        indent_increase = tokens[-1] == COLON
        
        extra = ""
        parsed = []

        for token in tokens:
            # Skip processing for the first ID in a for loop
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
    print(token)
    # Handle special cases where the token match can't be directly substituted
    if isinstance(token, ID):
        return "vars[\"{0}\"] ".format(token.value)

    elif token == WAIT:
        return "await uasyncio.sleep_ms "

    elif token == SAVE:
        return tabs.join(["led[0].duty(lookup[vars[\"r\"]])\n", "led[1].duty(lookup[vars[\"g\"]])\n", "led[2].duty(lookup[vars[\"b\"]])"])

    # For all other literals, return the token that matched it
    elif isinstance(token, str):
        return token + " "
    
    else:
        return token.value + " "