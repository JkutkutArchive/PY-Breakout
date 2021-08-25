import pygame
from Classes.color import *;

class Player():
    '''Class for the player in breakout.'''

    unit = 0 # Used to define the size of the player.

    def __init__(self, x, screenW, screenH, screen) -> None:
        self._x = x # Only horizontal position is stored, the other is constant

        self.screenW = screenW
        self.screenH = screenH # Also the vertical position
        self.screen = screen

        self._color = color().WHITE

        self.show()


    # GETTERS

    def color(self) -> tuple:
        '''Color of the player.'''
        return self._color
    
    def pos(self) -> tuple:
        '''Position of the player.'''
        return self._x
    
    def getBodyShape(self) -> pygame.Rect:
        '''Object representing the shape of the player.'''
        return pygame.Rect(\
            self._x - Player.unit * 3.5, self.screenH - Player.unit,
            Player.unit * 7, Player.unit\
        )


    # SETTERS

    def moveLeft(self) -> None:
        '''Attempts to move the player to the left.'''
        self.clear()
        self._x -= Player.unit
        if self._x < Player.unit * 3.5:
            self._x = Player.unit * 3.5
        self.show()

    def moveRight(self) -> None:
        '''Attempts to move the player to the right.'''
        self.clear()
        self._x += Player.unit
        if self._x > self.screenW - Player.unit * 3.5:
            self._x = self.screenW - Player.unit * 3.5
        self.show()

    def clear(self) -> None:
        '''Clears the player from the pygame screen.'''
        pygame.draw.rect(self.screen, color().BG, self.getBodyShape())

    def show(self) -> None:
        '''Shows the player on the pygame screen.'''
        pygame.draw.rect(self.screen, self.color(), self.getBodyShape(), 0, 7)



    # Ball collision logic

    def inRange(self, ball) -> bool:
        '''Whenever the current ball is in range of the player.'''
        ballPos = ball.pos()
        return ballPos[1] + ball.size() > self.screenH - Player.unit and \
            abs(ballPos[0] - self.pos()) < 3.6 * Player.unit

    def makeBallBounce(self, ball) -> None:
        '''Fixes the cliping and makes the ball bounce.'''
        ball.clear()

        # Fix vertical pos
        ball._y -= (ball._y + ball.size()) - (self.screenH - Player.unit)
        
        self.show() # Update the player without the ball cliping thought (should not be visible this way)

        # Change direction based on the location of the hit
        amount = (ball._x - self._x) / (3.5 * Player.unit) # per-one representing the amount to the side (1 > right side > 0 > left side > -1)

        if abs(amount) > 0.5: # If on the extreme-side of player
            ball.redirect(amount)
        else:
            ball.bounce(y=True) # Just make it bounce