import pygame;
from Classes.color import *;


class Ball():
    def __init__(self, x, y, screenW, screenH, screen) -> None:
        self._x = x
        self._y = y

        self.screenW = screenW
        self.screenH = screenH
        self.screen = screen

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
        self.clearBall()
        
        self._x += self._dirX
        self._y += self._dirY

        # if edge reached, bounce
        extraX, extraY = (0, 0)
        bounceX, bounceY = (False, False)
        if self._x < 0:
            extraX = self._x - self.size()
            bounceX = True
        elif self._x > self.screenW - self.size():
            extraX = self._x % (self.screenW - self.size())
            bounceX = True
        
        if self._y < self.size():
            extraY = self._y - self.size()
            bounceY = True
        elif self._y > self.screenH:
            self._y = 0
            # TODO Add logic for ball eliminated

        if bounceX:
            self._x -= extraX
            self.bounce(x=True)
        if bounceY:
            self._y -= extraY
            self.bounce(y=True)
        
        self.showBall()
        
    def clearBall(self):
        pygame.draw.circle(self.screen, color().BG, self.pos(), self.size())
    
    def showBall(self):
        pygame.draw.circle(self.screen, self.color(), self.pos(), self.size())