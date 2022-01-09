# ESP-RGB-LED
[![Tests](https://github.com/Sean-AP/ESP-RGB-LED/actions/workflows/main.yml/badge.svg)](https://github.com/Sean-AP/ESP-RGB-LED/actions/workflows/main.yml)]

MicroPython module for controlling an RGB LED strip <br>
For use with an ESP8266 or similar microcontroller <br>
<br>

## How to Use
- Add a network SSID and password, port, and human-friendly name to setup_net
- Add the output pin numbers and a maximum incoming file size to setup_led
- Upload all the .py files in this project to the microcontroller
  - upload.sh provides a way to do this using ampy
  - Usage: ./upload.sh --port \<dir> --baud \<int> --net \<\*.py> --led \<\*.py> 

With the files uploaded and main.py executing:
- Send 'ping' to the open port to check the device name, current colour, and whether the lights are changing or static
- Send scripts to the open port to parse and run them

Scripts can be written using the language described below <br>
This prevents arbitrary code execution on the device <br>
<br>

## Grammar
The grammar is (and must be) LL(1), which greatly simplifies the parser
- Not checked: The first symbol of every rule in a production must be unique
- Checked: The first symbol of a rule cannot be optional
- Checked: Left recursion is disallowed
<br>

The grammar describes a simplified Python-like language:
- Indentation is significant 
  - The first indentation encountered will be used as the INDENT token for the rest of the file
- Variables may be unsigned integers or booleans
- Single-line comments are supported using '#'
- expr rules are not typechecked
<br>

```
script : statement+

statement : ID ASSIGN expr
          | 'wait' '(' expr ')'
          | 'save'
          | 'while' expr        ':' INDENT script DEDENT
          | 'if'    expr        ':' INDENT script DEDENT
          | 'elif'  expr        ':' INDENT script DEDENT
          | 'else'              ':' INDENT script DEDENT
          | 'for' ID 'in' range ':' INDENT script DEDENT
          ;

expr : NUM     intExt?
     | ID      exprExt?
     | 'True'  boolExt?
     | 'False' boolExt?
     | 'random' '(' range ')' intExt?
     | '(' expr ')' exprExt?
     | 'not' expr
     ;

exprExt : INTOP expr
        | COMPARE expr
        | EQUATE expr
        | BOOLOP expr
        ;

intExt  : INTOP expr
        | COMPARE expr
        | EQUATE expr
        ;

boolExt : EQUATE expr
        | 'and' expr
        | 'or' expr
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
- save sets the output of the GPIO pins, so the lights only change colour when this is called
- Argument specifiers cannot be used in range
  - range(10, step=2) is not valid, use range(0, 10, 2) instead
- Very simple type validation is done by operators on expression literals 

## Parsing and Execution
The parser handles some syntax rules, such as ensuring elif/else has a matching if <br>
The parser does not check types <br>
The values of variables r, g, and b must be kept between 0 and 255 
- These are the values passed to the pins when save is called 
<br>
Errors are handled as follows:
- The lights turn red
- If the error occurrs during parsing and a previous script is still executing, that script continues to execute
- If the error occurrs during execution, the lights remain red until a new script is parsed and executed
<br>

## Example Script
The script below will cycle through the colour spectrum on repeat <br>
The delay starts at 40 ms, halving every cycle until 5 ms, then doubling until 40 ms, and repeats <br>

```
# Start at red
r = 255
g = 0
b = 0
save

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
            g += 1
            wait(delay)
            save

      # Yellow -> Green
      while r > 0:
            r -= 1
            wait(delay)
            save

      # Green -> Cyan
      while b < 255:
            b += 1
            wait(delay)
            save

      # Cyan -> Blue
      while g > 0:
            g -= 1
            wait(delay)
            save

      # Blue -> Magenta
      while r < 255:
            r += 1
            wait(delay)
            save

      # Magenta -> Red
      while b > 0:
            b -= 1
            wait(delay)
            save
```