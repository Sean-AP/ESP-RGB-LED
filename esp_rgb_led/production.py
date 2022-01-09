# Production definition

from .symbol import isterminal
from .symbols import ANY, MANY, MAYBE

def allow_omission(lexeme):
        return isinstance(lexeme, tuple) and (lexeme[1] == MAYBE or lexeme[1] == ANY)

def allow_many(lexeme):
        return isinstance(lexeme, tuple) and (lexeme[1] == MANY or lexeme[1] == ANY)


class Production:
    __slots__ = ()

    rules = ()

    @classmethod
    def match(cls, tokens: list, index: int) -> int:
        for rule in cls.rules:
            index_prime = cls.match_rule(rule, tokens, index)
            
            if index_prime is not None:
                return index_prime

        return None


    @staticmethod
    def match_rule(rule: list, tokens: list, index: int) -> int:
        # Copy the tokens to prevent mutating on a partial match
        tokens_prime = list(tokens)

        i = 0
        found = False

        # Find the first matching lexeme
        while i < len(rule) and index < len(tokens):
            lexeme = rule[i]
            
            can_omit = allow_omission(lexeme)
            can_repeat = allow_many(lexeme)

            if isinstance(lexeme, tuple):
                lexeme = lexeme[0]

            if isinstance(lexeme, str):
                result = match_terminal(lexeme, tokens_prime, index)

            else:
                result = (
                    match_nonterminal(lexeme, tokens_prime, index) if issubclass(lexeme, Production) else 
                    match_terminal(lexeme, tokens_prime, index))

            if result is None:
                # In some cases, a non-match doesn't mean the rule fails:
                # - ?,* modifier
                # - +,* modifier with >= 1 occurrence already found
                if not can_omit and not found:
                    return None

            else:
                index = result

            found = result is not None

            # Only increment i if the next symbol definitely won't be the same:
            # - the previous token failed to match
            # - the previous token matched, and the lexeme does not have a +,* modifier
            if not (found and can_repeat):         
                i += 1

        # Check in case end of token stream but not end of rule:
        # - the current lexeme is the last one, has a +,* modifier, and has already been matched
        # - the remaining lexemes all have ?,* modifiers
        if index >= len(tokens) and i < len(rule):
            if i == len(rule) - 1 and allow_many(rule[i]) and found:
                tokens[:index] = tokens_prime[:index]
                return index

            for lexeme in rule[i:]:
                if not allow_omission(lexeme):
                    return None

        tokens[:index] = tokens_prime[:index]
        return index