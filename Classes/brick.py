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

    def inRange(self, ball):
        '''Checks if ball colliding with brick. Code based on code from http://jeffreythompson.org/collision-detection/circle-rect.php'''
        # temporary variables to set edges for testing
        cx, cy = ball.pos()
        rx, ry = self.pos()
        rw = self.width * 2
        rh = self.height * 2

        rx -= self.width
        ry -= self.height
        
        testX = cx
        testY = cy

        # * which edge is closest?
        closest = ""
        if cx < rx:
            testX = rx # left edge
            closest = "left"
        elif cx > rx + rw:
            testX = rx + rw # right edge
            closest = "right"

        if cy < ry:
            testY = ry # top edge
            closest = "top"
        elif cy > ry + rh:
            testY = ry + rh # bottom edge
            closest = "bottom"

        distX = cx - testX
        distY = cy - testY

        distance = math.sqrt((distX * distX) + (distY * distY))

        if distance <= ball.size():
            print(closest)
        
        return distance <= ball.size()
    
    # SETTERS

    def clear(self) -> None:
        '''Clears the brick from the pygame screen.'''
        pygame.draw.polygon(self.screen, color().BG, self.getBodyShape())
    
    def show(self) -> None:
        '''Shows the brick from the pygame screen.'''
        pygame.draw.polygon(self.screen, color().GREY, self.getBodyShape())
        pygame.draw.polygon(self.screen, self.color(), self.getBodyShape(offset=3))



class Brick(brick):
    '''Class with the logic of the bricks from Breakout.'''

    def __init__(self, x, y, screenW, screenH, screen) -> None:
        super().__init__(x, y, screenW, screenH, screen)

        self.health = 1
    