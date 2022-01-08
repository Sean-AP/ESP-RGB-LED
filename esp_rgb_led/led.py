from .setup_led import R_PIN, G_PIN, B_PIN
from machine import Pin, PWM
from math import ceil, log
from random import getrandbits

# Get pins responsible for each colour and set up PWM
led = [
    PWM(x, freq=100, duty=0) for x in [
        Pin(R_PIN, Pin.OUT), 
        Pin(G_PIN, Pin.OUT),
        Pin(B_PIN, Pin.OUT)]
    ]

# Implementation of the CIE 1931 lightness formula to create a lookup table for dimming
def cie1931(L: float) -> float:
    L = L * 100.0
    if L <= 8:
        return (L / 903.3)
    else:
        return ((L + 16.0) / 119.0) ** 3

lookup = [round(cie1931(float(L) / 255) * 1023) for L in range(256)]

# Random number generator function
def random(values) -> int:   
    # Calculate the number of bits needed to represent each index in values
    size = len(values)
    bits = ceil(log(size) / log(2))

    # Generate a random value with that many bits, accounting for out-of-range errors
    # In the worst case scenario, len(values) = (2^n) + 1 so 2^(n+1) - 1 values are out of range
    # This should find a valid value in 2 iterations on average 
    while True:
        index = getrandbits(bits)
        if index < size:
            return values[index]
