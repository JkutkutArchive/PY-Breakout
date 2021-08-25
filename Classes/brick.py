import pygame, math;
from Classes.color import color;

class brick():
    
    '''Prototype of the Brick classes.'''

    def __init__(self, x, y, screenW, screenH, screen) -> None:
        # Store position
        self._x = x
        self._y = y

        self.screenW = screenW
        self.screenH = screenH
        self.screen = screen

        self._color = color().WHITE

        unit = screenW // 30
        self.height = unit // 2
        self.width = unit

    # GETTERS

    def color(self) -> tuple:
        '''RGB tuple with the current color of the brick.'''
        return self._color

    def pos(self) -> tuple:
        '''Position of the brick as a tuple (horizontal, vertical).'''
        return (self._x, self._y)

    def getBodyShape(self, offset=0) -> list:
        '''List of tuples representing the vertices of the brick shape as (horizontal, vertical) vectors.'''
        return [
            (self._x - self.width + offset, self._y - self.height + offset),
            (self._x - self.width + offset, self._y + self.height - offset),
            (self._x + self.width - offset, self._y + self.height - offset),
            (self._x + self.width - offset, self._y - self.height + offset)
        ]
    
    def destroyed(self) -> bool:
        '''Whenever the brick has been destroyed.'''
        return False

    
    # SETTERS

    def clear(self) -> None:
        '''Clears the brick from the pygame screen.'''
        pygame.draw.polygon(self.screen, color().BG, self.getBodyShape())
    
    def show(self) -> None:
        '''Shows the brick from the pygame screen.'''
        pygame.draw.polygon(self.screen, color().GREY, self.getBodyShape())
        pygame.draw.polygon(self.screen, self.color(), self.getBodyShape(offset=3))

    def attemptHit(self, ball) -> bool:
        '''Checks if ball colliding with brick and reacts to it.
        
        Returns whenever the brick has collided with the ball.'''
        cx, cy = ball.pos()
        rx, ry = self.pos()

        deltaX = rx - cx
        deltaY = ry - cy

        # Check if it apears to be a collision
        collision = False
        if abs(deltaX) > abs(deltaY) * 2: # Horizontal collision
            collision = abs(deltaX) - ball.size() < self.width # If horizontal hit
        else: # Vertical collision
            collision = abs(deltaY) - ball.size() < self.height # If vertical hit

        if not collision: return False

        ball.clear()
        self.show()

        # Fix position
        # Get normal vector of direction of the ball
        ballDirN = ball.direction()
        mag = math.sqrt(ballDirN[0] * ballDirN[0] + ballDirN[1] * ballDirN[1])
        ballDirN = [ballDirN[0] / mag, ballDirN[1] / mag]

        iterations = 0 # Go back until the edge of the brick is reached
        while abs(deltaX) - ball.size() < self.width and \
            abs(deltaY) - ball.size() < self.height:

            ball._x -= ballDirN[0]
            ball._y -= ballDirN[1]
            iterations += 1

            cx, cy = ball.pos()
            deltaX = rx - cx; deltaY = ry - cy

        # Now on the edge, check true type of collision and react to it
        epsilon = 1
        hHit = abs((abs(deltaX) - ball.size()) - self.width) < epsilon
        vHit = abs((abs(deltaY) - ball.size()) - self.height) < epsilon

        if hHit and vHit: # If corner hit
            ball.bounce(x=True, y=True)

        elif hHit: # If horizontal hit
            ball.bounce(x=True)
            ball._x -= iterations * ballDirN[0] / 2
            ball._y += iterations * ballDirN[1] # Restore position

        elif vHit: # If vertical hit
            ball.bounce(y=True)
            ball._x += iterations * ballDirN[0] # Restore position
            ball._y -= iterations * ballDirN[1] / 2

        ball.show()
        self.hitMade()
        return True

    def hitMade(self) -> None:
        '''When the brick has been hitten, this function is executed.'''
        pass



class Brick(brick):
    '''Class with the logic of the bricks from Breakout.'''

    def __init__(self, x, y, screenW, screenH, screen) -> None:
        super().__init__(x, y, screenW, screenH, screen)

        self.health = 1
    
    def hitMade(self):
        super().hitMade()
        self.health -= 1
        if self.destroyed():
            self.clear()
    
    def destroyed(self) -> bool:
        return self.health <= 0


class BrickHeavy(brick):
    '''Indestructible brick.'''

    def __init__(self, x, y, screenW, screenH, screen) -> None:
        super().__init__(x, y, screenW, screenH, screen)
        self._color = color().BG
    