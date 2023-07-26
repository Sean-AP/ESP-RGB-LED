# ESP-RGB-LED
[![Tests](https://github.com/Sean-AP/ESP-RGB-LED/actions/workflows/main.yml/badge.svg)](https://github.com/Sean-AP/ESP-RGB-LED/actions/workflows/main.yml)
[![MicroPython](https://badgen.net/badge/micropython/v1.17/blue?icon=pypi)](https://github.com/micropython/micropython)

MicroPython module for controlling an RGB LED strip <br>
For use with an ESP8266 or similar microcontroller <br>
<br>

## How to Use
- Duplicate the led_template.py and net_template.py files in src/setup
- Add a network SSID and password, port, and human-friendly name to the new net setup file
- Add the output pin numbers and a maximum incoming file size to the new led setup file
- Upload all the .py files in this project to the microcontroller
<br>

With the files uploaded and main.py executing:
- Send 'ping' to the open port to check the device name, current colour, and whether the lights are changing or static
- Send scripts to the open port to parse and run them

Scripts can be written using the language described below <br>
This prevents arbitrary code execution on the device <br>
<br>

## upload.sh
upload.sh provides a way to upload software to the microcontroller using ampy <br>
Usage: ./upload.sh --port \<dir> --baud \<int> --net \<\*.py> --led \<\*.py> 
  - port is the USB port the device is connected on
  - baud is the baudrate of the device
  - net is the path to the net configuration file
  - led is the path to the led configuration file
<br>
<br>

## Grammar
The parser assumes the grammar is unambiguous with 1 token lookahead <br>
<br>

The grammar describes a simple Python-like language:
- Indentation is significant 
  - The first indentation encountered is used as the INDENT token for the rest of the file
  - Tabs are recommended as they provide more spacing per character
- Variables may be unsigned integers or booleans
- Single-line comments are supported using '#'
- 0 is falsy, all other int values are truthy
<br>

```
script : statement+

statement : ID ASSIGN expr
          | 'wait' '(' expr ')'
          | 'led' '(' expr ',' expr ',' expr ')'
          | 'break'
          | 'while' expr        ':' INDENT script DEDENT
          | 'if'    expr        ':' INDENT script DEDENT
          | 'elif'  expr        ':' INDENT script DEDENT
          | 'else'              ':' INDENT script DEDENT
          | 'for' ID 'in' range ':' INDENT script DEDENT
          ;

expr : NUM     exprExt?
     | ID      exprExt?
     | 'True'  boolExt?
     | 'False' boolExt?
     | 'not' expr
     | 'random' '(' range ')' exprExt?
     | 'max' '(' expr ',' expr ')' exprExt?
     | 'min' '(' expr ',' expr ')' exprExt?
     | 'round' '(' expr ')' exprExt?
     | 'sin' '(' expr ')' exprExt?
     | '(' expr ')' exprExt?
     ;

exprExt : INTOP expr
        | COMPARE expr
        | boolExt
        ;

boolExt : EQUATE expr
        | 'and' expr
        | 'or' expr
        | 'if' expr 'else' expr
        ;

range : 'range' '(' expr rangeList? rangeList? ')' ;

rangeList : ',' expr ;


ID  : [a-zA-Z][a-zA-Z0-9_]* ;
NUM : [0-9]+ ;

ASSIGN  : '='  | '+=' | '-=' | '*=' | '/=' | '%=' ;
INTOP   : '+'  | '-'  | '*'  | '//' | '%' ;
COMPARE : '<'  | '<=' | '>=' | '>' ; 
EQUATE  : '==' | '!=' ;
```

Some notes:
- waiting expects milliseconds, so wait(1000) will wait for 1s
- led sets the output of the GPIO pins, so the lights only change colour when this is called
- When led is called, the variables r, g, b are updated to the values given
- Argument specifiers cannot be used in range
  - The function will follow the same behaviour as Python's range when used without argument specifiers
  - For example, range(10, step=2) is not valid, use range(0, 10, 2) instead

## Parsing and Execution
The parser handles some syntax rules, such as ensuring elif/else has a matching if <br>
The values of variables r, g, and b should be kept between 0 and 255 
- These are the values passed to the pins when save is called
- Values outside of this range will be raised to 0 or lowered to 255
<br>
Errors are handled as follows:
- The lights turn red
- If the error occurs during parsing and a previous script is still executing, that script continues to execute
- If the error occurs during execution, the lights remain red until a new script is parsed and executed
<br>

## Example Script
The script below will cycle through the colour spectrum on repeat <br>
The delay starts at 40 ms, halving every cycle until 5 ms, then doubling until 40 ms, and repeats <br>

```python
# Start at red
led(255, 0, 0)

min_delay = 5
max_delay = 40

delay = max_delay
decrease = True

while True:
      if decrease:
            delay //= 2
            decrease = delay > min_delay

      else:
            delay *= 2
            decrease = delay == max_delay

      # Red -> Yellow
      while g < 255:
            wait(delay)
            led(r, g + 1, b)

      # Yellow -> Green
      while r > 0:
            wait(delay)
            led(r - 1, g, b)

      # Green -> Cyan
      while b < 255:
            wait(delay)
            led(r, g, b + 1)

      # Cyan -> Blue
      while g > 0:
            wait(delay)
            led(r, g - 1, b)

      # Blue -> Magenta
      while r < 255:
            wait(delay)
            led(r + 1, g, b)

      # Magenta -> Red
      while b > 0:
            wait(delay)
            led(r, g, b - 1)
```