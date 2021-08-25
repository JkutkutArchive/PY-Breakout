import pygame
from Classes.color import *;

class Player():
    '''Class for the player in breakout.'''
    def __init__(self, x, screenW, screenH, screen) -> None:
        self._x = x # Only horizontal position is stored, the other is constant

        self.screenW = screenW
        self.screenH = screenH # Also the vertical position
        self.screen = screen

        self.unit = self.screenW // 50 # unit used to define the height of the player. Works as a base for the shape and movements of this class

        self._color = color().WHITE

        self.show()


    # GETTERS

    def color(self) -> tuple:
        '''Color of the player.'''
        return self._color
    
    def pos(self) -> tuple:
        '''Position of the player.'''
        return self._x
    
    def getBodyShape(self) -> list:
        '''List with tuples representing the vertices of the player shape as (horizontal, vertical) vectors.'''
        return [
            (self._x - self.unit * 2.5, self.screenH),
            (self._x + self.unit * 2.5, self.screenH),

            (self._x + self.unit * 3.5, self.screenH - self.unit),
            (self._x - self.unit * 3.5, self.screenH - self.unit)
        ]


    # SETTERS

    def moveLeft(self) -> None:
        '''Attempts to move the player to the left.'''
        self.clear()
        self._x -= self.unit
        if self._x < self.unit * 3.5:
            self._x = self.unit * 3.5
        self.show()

    def moveRight(self) -> None:
        '''Attempts to move the player to the right.'''
        self.clear()
        self._x += self.unit
        if self._x > self.screenW - self.unit * 3.5:
            self._x = self.screenW - self.unit * 3.5
        self.show()

    def clear(self) -> None:
        '''Clears the player from the pygame screen.'''
        pygame.draw.polygon(self.screen, color().BG, self.getBodyShape())

    def show(self) -> None:
        '''Shows the player from the pygame screen.'''
        pygame.draw.polygon(self.screen, self.color(), self.getBodyShape())


    # Ball collision logic

    def inRange(self, ball) -> bool:
        '''Whenever the current ball is in range of the player.'''
        ballPos = ball.pos()
        return ballPos[1] + ball.size() > self.screenH - self.unit and \
            abs(ballPos[0] - self.pos()) < 3.6 * self.unit

    def makeBallBounce(self, ball) -> None:
        '''Fixes the cliping and makes the ball bounce.'''
        ball.clear()

        # Fix vertical pos
        ball._y -= (ball._y + ball.size()) - (self.screenH - self.unit)
        
        self.show() # Update the player without the ball cliping thought (should not be visible this way)

        # Change direction based on the location of the hit
        amount = (ball._x - self._x) / (3.5 * self.unit) # per-one representing the amount to the side (1 > right side > 0 > left side > -1)

        if abs(amount) > 0.5: # If on the extreme-side of player
            ball.redirect(amount)
        else:
            ball.bounce(y=True) # Just make it bounce