import pygame, math, random;
from Classes.color import color;

class brick():
    
    '''Prototype of the Brick classes.'''

    height = 0
    width = 0

    def __init__(self, x, y, screen) -> None:
        # Store position
        self._x = x
        self._y = y
        
        self.screen = screen

        self._color = color().WHITE

        # brick.width = brick.width
        # brick.height = brick.height

    # GETTERS

    def width(self):
        return brick.width
    
    def height(self):
        return brick.height

    def color(self) -> tuple:
        '''RGB tuple with the current color of the brick.'''
        return self._color

    def pos(self) -> tuple:
        '''Position of the brick as a tuple (horizontal, vertical).'''
        return (self._x, self._y)

    def getBodyShape(self, offset=0) -> pygame.Rect:
        '''Object representing the shape of the brick.'''
        return pygame.Rect(
            self._x - brick.width + offset, self._y - brick.height + offset,
            2 * (brick.width - offset), 2 * (brick.height - offset)
        )
    
    def destroyed(self) -> bool:
        '''Whenever the brick has been destroyed.'''
        return False

    
    # SETTERS

    def clear(self) -> None:
        '''Clears the brick from the pygame screen.'''
        pygame.draw.rect(self.screen, color().BG, self.getBodyShape(offset=-1))
    
    def show(self) -> None:
        '''Shows the brick from the pygame screen.'''
        pygame.draw.rect(self.screen, color().GREY, self.getBodyShape(offset=-1))
        pygame.draw.rect(self.screen, self.color(), self.getBodyShape(offset=2))

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
            collision = abs(deltaX) - ball.size() < brick.width # If horizontal hit
        else: # Vertical collision
            collision = abs(deltaY) - ball.size() < brick.height # If vertical hit

        if not collision: return False

        ball.clear()
        self.show()

        # Fix position
        # Get normal vector of direction of the ball
        ballDirN = ball.direction()
        mag = math.sqrt(ballDirN[0] * ballDirN[0] + ballDirN[1] * ballDirN[1])
        ballDirN = [ballDirN[0] / mag, ballDirN[1] / mag]

        iterations = 0 # Go back until the edge of the brick is reached
        while abs(deltaX) - ball.size() < brick.width and \
            abs(deltaY) - ball.size() < brick.height:

            ball._x -= ballDirN[0]
            ball._y -= ballDirN[1]
            iterations += 1

            cx, cy = ball.pos()
            deltaX = rx - cx; deltaY = ry - cy

        # Now on the edge, check true type of collision and react to it
        epsilon = 1
        hHit = abs((abs(deltaX) - ball.size()) - brick.width) < epsilon
        vHit = abs((abs(deltaY) - ball.size()) - brick.height) < epsilon

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

    def __init__(self, x, y, screen) -> None:
        super().__init__(x, y, screen)

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

    def __init__(self, x, y, screen) -> None:
        super().__init__(x, y, screen)
        self._color = color().BG


# ColorFull
class Brick_colorFull(Brick):
    colors = [
        (240, 241, 78),
        (109, 237, 138),
        (22, 69, 245),
        (255, 95, 133),
        (237, 56, 51)
    ]

    def __init__(self, x, y, screen) -> None:
        super().__init__(x, y, screen)
        cIndex = int(x + y) % len(Brick_colorFull.colors)
        self._color = Brick_colorFull.colors[cIndex]

class BrickHeavy_colorFull(BrickHeavy):
    colors = [tuple([max(0, i - 100) for i in t]) for t in Brick_colorFull.colors]

    def __init__(self, x, y, screen) -> None:
        super().__init__(x, y, screen)
        cIndex = int(x + y) % len(BrickHeavy_colorFull.colors)
        self._color = BrickHeavy_colorFull.colors[cIndex]

# SemiRandom Color
class Brick_semiRandomColor(Brick_colorFull):
    def __init__(self, x, y, screen) -> None:
        super().__init__(x, y, screen)
        self._color = Brick_colorFull.colors[random.randint(0, len(Brick_colorFull.colors) - 1)]
        
class BrickHeavy_semiRandomColor(BrickHeavy_colorFull):
    def __init__(self, x, y, screen) -> None:
        super().__init__(x, y, screen)
        self._color = BrickHeavy_colorFull.colors[random.randint(0, len(BrickHeavy_colorFull.colors) - 1)]
        

# Random color
class Brick_randomColor(Brick):
    def __init__(self, x, y, screen) -> None:
        super().__init__(x, y, screen)
        self._color = tuple([random.randint(50, 255) for _ in range(3)])

class BrickHeavy_randomColor(BrickHeavy):
    def __init__(self, x, y, screen) -> None:
        super().__init__(x, y, screen)
        self._color = tuple([random.randint(0, 200) for _ in range(3)])