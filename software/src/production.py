# Production definition

from symbol import isterminal
from symbols import ANY, MANY, MAYBE

def allow_omission(lexeme):
        return isinstance(lexeme, tuple) and (lexeme[1] == MAYBE or lexeme[1] == ANY)

def allow_many(lexeme):
        return isinstance(lexeme, tuple) and (lexeme[1] == MANY or lexeme[1] == ANY)

# Determine which rule to use given the first token to match
def match_first(rules: tuple, token: str) -> tuple:
    stack = []
    r_index = 0

    while True:
        rule = rules[r_index]

        if allow_omission(rule[0]):
            raise RuntimeError("Invalid grammar: optional leading token in a rule")

        lexeme = rule[0][0] if isinstance(rule[0], tuple) else rule[0]

        # First lexeme in rule is terminal
        if isterminal(lexeme):
            literal = isinstance(lexeme, str)
            match = (literal and token == lexeme) or (not literal and lexeme.match(token))

            if match:
                while len(stack) > 0:
                    rules, r_index = stack.pop()
                    rule = rules[r_index]
                return rule
            
            # No match, try next rule 
            r_index += 1

        # First lexeme in rule is non-terminal
        elif rule in stack:
            raise RuntimeError("Invalid grammar: left recursion detected")

        else:
            stack.append((rules, r_index))
            rules = lexeme.rules
            r_index = 0

        # Reached end of rules without match
        while r_index == len(rules):
            if len(stack) == 0:
                return None
            
            rules, r_index = stack.pop()
            r_index += 1


class Production:
    __slots__ = ()
    rules = ()

    @classmethod
    def match(cls, tokens: list, t_index: int = 0) -> bool:
        stack = []
        rules = cls.rules

        omit_nt = False # The next non-terminal symbol can be omitted
        many_t  = False # The next terminal symbol can be repeated

        while True:
            # Assume LL(1) grammar, so check 1 token to determine rule
            matched_rule = match_first(rules, tokens[t_index])
            r_index = 0

            # If no rules matched, immediately reject unless omit flag is set and there is a parent state to load
            if matched_rule is None:
                if not omit_nt or len(stack) == 0:
                    return False

                # Load parent non-terminal's state
                matched_rule, r_index = stack.pop()
                
                while r_index + 1 == len(matched_rule):
                    if len(stack) == 0:
                        return False

                    matched_rule, r_index = stack.pop()
                r_index += 1

            # Match every token in the rule
            while r_index < len(matched_rule):
                lexeme = matched_rule[r_index]
                can_omit = allow_omission(lexeme)
                can_repeat = allow_many(lexeme)

                if isinstance(lexeme, tuple):
                    lexeme = lexeme[0]

                # Terminal
                if isterminal(lexeme):
                    literal = isinstance(lexeme, str)
                    match = (literal and tokens[t_index] == lexeme) or (not literal and lexeme.match(tokens[t_index]))

                    if match:
                        # Create instance of regex symbols
                        if not literal:
                            tokens[t_index] = lexeme(tokens[t_index])

                        t_index += 1
                        many_t = can_repeat

                        if not can_repeat:
                            r_index += 1

                    # Can be omitted, or can repeat and have seen an occurrence
                    elif can_omit or many_t:
                        r_index += 1

                    else:
                        return False

                # Non-Terminal
                else:
                    # Push current state to the stack
                    stack.append((matched_rule, r_index))
                    rules = lexeme.rules
                    omit_nt = can_omit
                    break

                # End of current rule
                while r_index == len(matched_rule):
                    # End of base rule - match iff all tokens have been consumed
                    if len(stack) == 0:
                        return t_index == len(tokens)

                    # Load parent non-terminal's state
                    matched_rule, r_index = stack.pop()
                    omit_nt = allow_many(matched_rule[r_index])

                    # Increment rule index if parent non-terminal is not repeatable
                    if not omit_nt:
                        r_index += 1

                # End of token stream:
                if t_index == len(tokens):
                    # Check all remaining lexemes in the rule
                    while r_index < len(matched_rule):
                        # Check for + modifier and already matched
                        if many_t or omit_nt:
                            many_t = False
                            omit_nt = False

                        # Check for ?,* modifier
                        elif not (allow_omission(matched_rule[r_index])):
                            return False

                        r_index += 1

                        # End of current rule
                        while r_index == len(matched_rule):
                            # End of base rule - match
                            if len(stack) == 0:
                                return True

                            # Load parent non-terminal's state
                            matched_rule, r_index = stack.pop()
                            r_index += 1
