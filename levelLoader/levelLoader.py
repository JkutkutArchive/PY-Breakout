import json
import pygame
from Classes.color import color
from Classes.player import Player
from Classes.ball import Ball
from Classes.brick import *;

COLOR = color()
width = None
height = None
screen = None
levels = json.load(open("levelLoader/levels.json", "r"))

def setup(w, h, s):
    global width, height, screen
    width = w
    height = h
    screen = s

    # update brick size
    unit = width // 30
    brick.width = unit
    brick.height = unit // 2

    # update player size
    Player.unit = width // 50

    # update ball size
    Ball.radius = 5

def getLevel(lvl, type="classic"):
    if not isinstance(lvl, int):
        raise Exception("The lvl must be an integer.")
    return levels[type][lvl - 1]

def loadLevel(lvl, type="classic"):
    global width, height, screen
    level = getLevel(lvl, type)

    bricks = set()
    for brickClass, x, y in getIterator(level):
        bricks.add(brickClass(x, y, screen))

    ball = Ball(width / 2, height - 100, width, height, screen)
    player = Player(width / 2, width, height, screen)

    # Clear the screen and update it with the new level
    screen.fill(COLOR.BG) # Clean screen
    player.show()
    ball.show()
    for b in bricks:
        b.show()
    pygame.display.flip() # Update the screen
    return player, ball, bricks


def getIterator(level):
    ite = set()
    for l in level["bricks"]:
        f = None
        if l["type"] == "wall":
            f = getWallIterator
        elif l["type"] == "centralMass":
            f = getCentralMassIterator
        
        ite = ite.union(f(l))
    return ite

def getWallIterator(level):
    global width
    ite = set()

    brickType = getBrickType(level)
    
    for r in range(level["rows"]):
        row = level["verticalStart"] + r * level["gap"]
        startOffset = brick.width
        if level["oddRow"]:
            startOffset = brick.width * 2
            ite.add((brickType, width / 2, 2 * row * brick.height))

        for w in range(level["horizontalHalfAmount"]):
            amount = startOffset + w * brick.width * 2
            for m in (-1, 1):
                ite.add((brickType, width / 2 + m * amount, 2 * row * brick.height))
    return ite

def getCentralMassIterator(level):
    global width
    ite = set()

    brickType = getBrickType(level)

    deltaGrow = level["hRadius"] - level["startRadius"]
    growRate = deltaGrow // level["vRadius"]
    
    currentRadius = level["startRadius"]
    row = level["verticalStart"]
    for growDir in (1, -1):
        for _ in range(level["vRadius"]):
            startOffset = brick.width
            if level["oddStart"]:
                startOffset = brick.width * 2
                ite.add((brickType, width / 2, 2 * row * brick.height))
            
            for w in range(currentRadius):
                amount = startOffset + w * brick.width * 2
                for m in (-1, 1):
                    ite.add((brickType, width / 2 + m * amount, 2 * row * brick.height))
            currentRadius += growDir * growRate
            row += 1
        currentRadius -= 1
    return ite


# Help functions

def getBrickType(level):
    if level["brickType"] == "normalBrick":
        return Brick
    else:
        return BrickHeavy