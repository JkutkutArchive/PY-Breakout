import pygame, math;
from Classes.color import *;

class Ball():

    '''Ball class for the game Breakout.'''
    
    def __init__(self, x, y, screenW, screenH, screen) -> None:
        # Store position
        self._x = x
        self._y = y

        self.screenW = screenW
        self.screenH = screenH
        self.screen = screen

        # store direction
        self._dirX = None
        self._dirY = None
        self.mag = 18 # Velocity of the ball
        self.changeAngle(- math.pi /3)

        self._color = color().WHITE

        self._size = 5 # Radius of the ball

    # GETTERS

    def color(self) -> tuple:
        '''RGB tuple with the current color of the ball.'''
        return self._color

    def pos(self) -> tuple:
        '''Position of the ball as a tuple (horizontal, vertical).'''
        return (self._x, self._y)
    
    def direction(self) -> tuple:
        '''Current vector used to move the ball (velocity).'''
        return (self._dirX, self._dirY)

    def size(self) -> int:
        '''Radius of the ball.'''
        return self._size
    
    def angle(self):
        '''Angle of the current direction relative to the vector (1, 0)'''
        return math.atan2(self._dirY, self._dirX)

    # SETTERS
    
    def bounce(self, x=False, y=False) -> None:
        '''Make the ball bounce on the axis given.'''
        if x: self._dirX *= -1
        if y: self._dirY *= -1

    def move(self) -> None:
        '''Move the ball in the current direction. If a wall is reached, make it bounce.'''
        self.clear() # Make the ball dissapear of the screen
        
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

        self.show() # Show the ball again
        
    def clear(self) -> None:
        '''Clears the ball from the pygame screen.'''
        pygame.draw.circle(self.screen, color().BG, self.pos(), self.size())
    
    def show(self) -> None:
        '''Shows the ball from the pygame screen.'''
        pygame.draw.circle(self.screen, self.color(), self.pos(), self.size())
    
    # Angle

    def changeAngle(self, angle):
        '''Changes the direction of the ball with the given angle (radians).'''
        self._dirX = self.mag * math.cos(angle)
        self._dirY = self.mag * math.sin(angle)
    
    def redirect(self, amount):
        ''' When the ball bounces on player, this method is executed with the ratio (per-one) representing how far the ball has bounced from the player.

            Amount: -1 < left side < 0 < right side < 1
        '''
        angle = -(math.pi / 2) + (math.pi / 3 * amount)
        self.changeAngle(angle)
