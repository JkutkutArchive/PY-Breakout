import pygame;
from Classes.color import *;

class Ball():

    '''Ball class for the game Breakout'''
    
    def __init__(self, x, y, screenW, screenH, screen) -> None:
        # Store position
        self._x = x
        self._y = y

        self.screenW = screenW
        self.screenH = screenH
        self.screen = screen

        # store Δ-direction
        self._dirX = 15
        self._dirY = 10

        self._color = color().WHITE

        self._size = 5 # Radius of the ball

    # GETTERS

    def color(self) -> tuple:
        '''RGB tuple with the current color of the ball'''
        return self._color

    def pos(self) -> tuple:
        '''Position of the ball as a tuple (horizontal, vertical)'''
        return (self._x, self._y)
    
    def size(self) -> int:
        '''Radius of the ball'''
        return self._size

    # SETTERS
    
    def bounce(self, x=False, y=False) -> None:
        '''Make the ball bounce on the axis given'''
        if x: self._dirX *= -1
        if y: self._dirY *= -1

    def move(self) -> None:
        '''Move the ball in the current direction. If a wall is reached, make it bounce'''
        self.clearBall() # Make the ball dissapear of the screen
        
        # Move the ball
        self._x += self._dirX
        self._y += self._dirY

        # if edge reached, bounce
        # horizontal edges
        extraX = 0
        bounceX = False
        if self._x < 0:
            extraX = self._x - self.size()
            bounceX = True
        elif self._x > self.screenW - self.size():
            extraX = self._x % (self.screenW - self.size())
            bounceX = True
        if bounceX:
            self._x -= extraX
            self.bounce(x=True)

        # vertical edges
        if self._y < self.size():
            self._y -= self._y - self.size()
            self.bounce(y=True)
        elif self._y > self.screenH: # If bottom reached
            self._y = 0
            # TODO Add logic for ball eliminated

        self.showBall() # Show the ball again
        
    def clearBall(self) -> None:
        '''Clears the ball from the pygame screen'''
        pygame.draw.circle(self.screen, color().BG, self.pos(), self.size())
    
    def showBall(self) -> None:
        '''Shows the ball from the pygame screen'''
        pygame.draw.circle(self.screen, self.color(), self.pos(), self.size())