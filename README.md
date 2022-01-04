# RGB-Lights
MicroPython module for controlling an RGB LED strip <br>
For use with an ESP8266 or similar microcontroller <br>
The setup_*.py files are for storing details such as network credentials and output pins <br>
<br>

## Grammar
The language is a subset of micropython <br>
Therefore whitespace is significant <br>
Comments are supported

```
Script := Statement+

Statement := ID ASSIGN Expr
           | wait ( Expr )
           | save
           | while Expr : Script
           | if Expr : Script
           | elif Expr : Script
           | else Expr : Script
           | for ID in Range : Script

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
The values r, g, and b must be kept between 0 and 255 - these are the values passed to the pins <br>
If an error is encountered while running, the lights will be set to red <br>
<br>

## Example Script
The script below will cycle through the colour spectrum every 15 seconds, on repeat

```
r = 255
g = 0
b = 0
save

delay = 10

while True:
    while g < 255:
        g += 1
        wait(delay)
        save

    while r > 0:
        r -= 1
        wait(delay)
        save

    while b < 255:
        b += 1
        wait(delay)
        save

    while g > 0:
        g -= 1
        wait(delay)
        save

    while r < 255:
        r += 1
        wait(delay)
        save

    while b > 0:
        b -= 1
        wait(delay)
        save
```
