import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "esp_rgb_led"))

import unittest
import parser



class TestParser(unittest.TestCase):

    def try_parse(self, valid, invalid):
        for text in valid:
            try:
                self.assertIsInstance(parser.parse(text), str)
            except RuntimeError as e:
                self.fail(e)

        for text in invalid:
            self.assertRaises(RuntimeError, lambda: parser.parse(text))


    # Test simple statements with one level of nesting at most
    def test_statement(self):
        valid = [
            "r = 255",
            "wait(10)",
            "save",
            "\n".join(["while r > 0:", "\tr -= 1"]),
            "\n".join(["if flag:", "\tr = 255"]),
            "\n".join(["for i in range(256):", "\tr = i"]),
            "r = 255 # Set r to 255",
            "# This script only contains comments!"
        ]

        invalid = [
            "wait",          # partial match
            "while r > 0:",  # partial match
            "r * 2",         # match different production
            "elif r > 128:", # elif with no if
            "else:"          # else with no if
        ]

        self.try_parse(valid, invalid)


    # Test complex statements
    def test_statement_complex(self):
        valid = [
            "\n".join([ # Nesting
                "while True:", "\tr += 1",
                "\twhile r < 255:", "\t\tg += 1", 
                "\t\twhile g < 255:", "\t\t\tb += 1"
            ]),

            "\n".join([ # If/elif/else
                "if r == 0:", "\tr += 1",
                "elif r < 128:", "\tr *= 2", 
                "elif r == 128:", "\tr = 255", 
                "else:", "\tr = 0", 
                "save"
            ])
        ]

        invalid = [
            "\n".join([ # Interrupted if/else
                "if r == 0:", "\tr = 255",
                "b = 128",
                "else:", "\tr = 255"
            ])
        ]

        self.try_parse(valid, invalid)


    # Test simple expressions
    def test_expr(self):
        valid = [
            "r = 255",
            "r = g",
            "r = random(range(256))",
            "r = max(g, b)",
            "flag = True",
            "flag = False",
            "flag = not True",
            "r = (g)"
        ]

        invalid = [
            "r = random",   # partial match
            "r = (g",       # incomplete brackets
            "r = g)",       # incomplete brackets
            "flag = !True"  # unrecognised operator
        ]

        self.try_parse(valid, invalid)


    # Test complex expressions
    def test_expr_complex(self):
        valid = [
            "r = ((g * g) + b) % 255",
            "r = random(range(128)) + 128",
            "r = (((((250)+1)+1)+1)+1)+1",
            "r = max(max(r, g), b)",
            "flag = (True and not False) and (not True or False)",
            "flag = r >= 128 and g < r and b == 255"
        ]

        invalid = [
            "r = 255 && True",    # invalid operator
            "flag = False + 1",   # invalid operator
            "flag = False < True" # invalid operator
        ]

        self.try_parse(valid, invalid)


    # Test range expressions
    def test_range(self):
        valid = [
            "r = random(range(256))",        # stop
            "r = random(range(128, 256))",   # start, stop
            "r = random(range(128, 256, 2))" # start, stop, step
        ]

        invalid = [
            "r = random(range())",             # empty
            "r = random(range(,))",            # missing required arg
            "r = random(range(256, ))",        # trailing comma
            "r = random(range(128, 256, ))",   # trailing comma
            "r = random(range(128, 256, 2, ))" # trailing comma
        ]

        self.try_parse(valid, invalid)
    

    # Test ID tokens
    def test_id(self):
        valid = [
            "i = 0",       # 1 char
            "num = 0",     # multi-char
            "NUM = 0",     # uppercase
            "numVar = 0",  # mixed case
            "i2 = 0",      # separated alphanumeric
            "fl4g = True", # mixed alphanumeric
            "i_3 = 0"      # underscore 
        ]

        invalid = [
            "save = 255",  # keyword
            "wait = 255",  # keyword
            "+ = 255",     # operator
            "1 = 1",       # numeric
            "1plus = 2",   # leading numeric
            "_i = 0"       # leading underscore  
        ]

        self.try_parse(valid, invalid)


if __name__ == '__main__':
    unittest.main()