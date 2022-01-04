# RGB-Lights
MicroPython module for controlling an RGB LED strip <br>
For use with an ESP8266 or similar microcontroller <br>
<br>

## How to Use
- Add a network SSID and password, port, and human-friendly name to setup_net
- Add the output pin numbers and a maximum incoming file size to setup_led
- Upload all the .py files in this project to the microcontroller

With the files uploaded and main.py executing:
- Send 'ping' to the open port to check the device name, current colour, and whether the lights are changing or static
- Send scripts to the open port on to parse and run them

Scripts can be written using the language described below <br>
This prevents arbitrary code execution on the device <br>
<br>

## Grammar
The language is a subset of micropython <br>
Therefore whitespace is significant, which is not shown in the grammar <br>
Single-line comments are supported <br>

```
Script := ping | Block

Block := Statement+

Statement := ID ASSIGN Expr
           | wait ( Expr )
           | save
           | while Expr : Block
           | if Expr : Block
           | elif Expr : Block
           | else Expr : Block
           | for ID in Range : Block

Expr := NUM ExprExt?
      | ID ExprExt?
      | TRUE ExprExt?
      | FALSE ExprExt?
      | NOT Expr ExprExt?
      | random ( Range )
      | ( Expr )

ExprExt := INTOP Expr
         | BOOLOP Expr
         | COND Expr

Range := range ( Expr RangeList? RangeList? )

RangeList := , Expr

ID := [a-zA-Z][a-zA-Z0-9_]*
NUM := [0-9]+

INTOP := [+\-\*/%]
BOOLOP := &&|\|\|
COND := [=!<>]=?
ASSIGN := [+\-\*/]?=
```
<br>

## Parsing and Execution
The parser takes care of some syntax rules, such as ensuring elif/else has a matching if <br>
The parser does not handle type checking, so using a bool in place of an int may cause problems <br>
The values of variables r, g, and b must be kept between 0 and 255 - these are the values passed to the pins when save is called <br>
If an error is encountered while parsing or executing, the lights will be set to red <br>
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
            delay /= 2
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
