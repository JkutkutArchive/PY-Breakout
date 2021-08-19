from Classes.color import *


class Ball():
    def __init__(self, x, y, screenW, screenH) -> None:
        self._x = x
        self._y = y

        self.screenW = screenW
        self.screenH = screenH

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

        # if edge reached, bounce
        extraX, extraY = (0, 0)
        bounceX, bounceY = (False, False)
        if self._x < 0:
            extraX = self._x
            bounceX = True
        elif self._x > self.screenW:
            extraX = self._x % self.screenW
            bounceX = True
        if self._y < 0:
            extraY = self._y
            bounceY = True
        elif self._y > self.screenH:
            extraY = self._y % self.screenH
            bounceY = True
        
        if bounceX:
            self._x -= extraX
            self.bounce(x=True)
        if bounceY:
            self._y -= extraY
            self.bounce(y=True)
        
