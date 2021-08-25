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

    def attemptHit(self, ball):
        '''Checks if ball colliding with brick. Code based on code from http://jeffreythompson.org/collision-detection/circle-rect.php'''
        # temporary variables to set edges for testing
        cx, cy = ball.pos()
        rx, ry = self.pos()

        deltaX = rx - cx
        deltaY = ry - cy

        if abs(deltaX) > abs(deltaY) * 2: # Horizontal collision
            # print("Checking horizontal")
            if abs(deltaX) - ball.size() < self.width: # If vertical hit
                ball.bounce(x=True)
                
                # fix vertical position
                amount = (ball._x + ball.size()) - (self._x - self.width)
                if deltaX > 0:
                    amount *= -1
                ball.clear()
                ball._y += amount
                ball.show()
        else: # Vertical collision
            # print(f"Checking vertical: {int(deltaY)} -> {self.height} {ball.size()}")
            if abs(deltaY) - ball.size() < self.height: # If vertical hit
                ball.bounce(y=True)
                
                # fix vertical position
                amount = (ball._y + ball.size()) - (self._y - self.height)
                if deltaY > 0:
                    amount *= -1
                ball.clear()
                ball._y += amount
                ball.show()
    
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
    