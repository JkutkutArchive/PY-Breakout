from Classes.color import *


class Ball():
    def __init__(self, x, y) -> None:
        self._x = x
        self._y = y

        self._dirX = 15
        self._dirY = 10

        self._color = color().WHITE

        self._size = 5

    # GETTERS

    def color(self):
        return self._color

    def pos(self):
        return (self._x, self._y)
    
    def size(self):
        return self._size

    # SETTERS
    
    def bounce(self, x=False, y=False):
        if x: self._dirX *= -1
        if y: self._dirY *= -1

    def move(self):
        self._x += self._dirX
        self._y += self._dirY