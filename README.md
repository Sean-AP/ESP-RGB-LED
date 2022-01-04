# RGB-Lights
MicroPython module for controlling an RGB LED strip
<br>
For use with an ESP8266 or similar microcontroller
<br>
The setup_*.py files are for storing details such as network credentials and output pins
<br>
<br>

## Grammar

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