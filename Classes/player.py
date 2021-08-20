import pygame
from Classes.color import *;

class Player():
    def __init__(self, x, screenW, screenH, screen) -> None:
        self._x = x

        self.screenW = screenW
        self.screenH = screenH
        self.screen = screen

        self.unit = self.screenW // 50

        self._color = color().WHITE

        self.showPlayer()


    # GETTERS

    def color(self):
        return self._color
    
    def pos(self):
        return self._x
    
    def getBodyShape(self):
        return [
            (self._x - self.unit * 2.5, self.screenH),
            (self._x + self.unit * 2.5, self.screenH),

            (self._x + self.unit * 3.5, self.screenH - self.unit),
            (self._x - self.unit * 3.5, self.screenH - self.unit)
        ]
    
    # SETTERS

    def moveLeft(self):
        self.clearPlayer()
        self._x -= self.unit
        if self._x < self.unit * 3.5:
            self._x = self.unit * 3.5
        self.showPlayer()

    def moveRight(self):
        self.clearPlayer()
        self._x += self.unit
        if self._x > self.screenW - self.unit * 3.5:
            self._x = self.screenW - self.unit * 3.5
        self.showPlayer()

    def clearPlayer(self):
        global pygame
        pygame.draw.polygon(self.screen, color().BG, self.getBodyShape())

    def showPlayer(self):
        global pygame
        pygame.draw.polygon(self.screen, self.color(), self.getBodyShape())

    # Ball collision

    def inRange(self, ball):
        ballPos = ball.pos()
        return ballPos[1] + ball.size() > self.screenH - self.unit and \
            abs(ballPos[0] - self.pos()) < 3.6 * self.unit

    def makeBallBounce(self, ball):
        ball.clearBall()

        # Fix vertical pos
        ball._y -= (ball._y + ball.size()) - (self.screenH - self.unit)
        
        ball.bounce(y=True)
        
        self.showPlayer() # Update the player without the ball cliping thought (should not be visible this way)