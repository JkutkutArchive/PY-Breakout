import json
from Classes.player import Player;
from Classes.ball import Ball;
from Classes.brick import *;

levels = json.load(open("levelLoader/levels.json", "r"))
Breakout = None

brickTypeIndex = 0
brickTypes = [
    { # Classic
        "Normal": Brick,
        "Heavy": BrickHeavy
    },
    { # ColorFull
        "Normal": Brick_colorFull,
        "Heavy": BrickHeavy_colorFull
    },
    { # SemiRandom
        "Normal": Brick_semiRandomColor,
        "Heavy": BrickHeavy_semiRandomColor
    },
    { # RandomColor
        "Normal": Brick_randomColor,
        "Heavy": BrickHeavy_randomColor
    }
]

def setup(breakoutClass):
    global Breakout
    Breakout = breakoutClass

def getLevel(lvl, type="classic"):
    global levels
    if not isinstance(lvl, int):
        raise Exception("The lvl must be an integer.")
    return levels[type][lvl - 1]

def loadLevel(lvl, type="classic"):
    global Breakout
    level = getLevel(lvl, type)

    bricks = set()
    for brickClass, x, y in getIterator(level):
        bricks.add(brickClass(x, y, Breakout.screen))

    ball = Ball(Breakout.width / 2, Breakout.height - 100, Breakout.width, Breakout.height, Breakout.screen)
    player = Player(Breakout.width / 2, Breakout.width, Breakout.height, Breakout.screen)

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
    global Breakout
    ite = set()

    brickType = getBrickType(level)
    
    for r in range(level["rows"]):
        row = level["verticalStart"] + r * level["verticalGap"]
        startOffset = brick.width + 0.5
        if level["oddRow"]:
            startOffset = brick.width * 2 + 1
            if not level["skipOddRow"]:
                ite.add((brickType, Breakout.width / 2, row * (2 * brick.height + 1)))

        for w in range(level["horizontalHalfAmount"]):
            amount = startOffset + w * (brick.width * 2 * level["horizontalGap"] + 1)
            for m in (-1, 1):
                ite.add((brickType, Breakout.width / 2 + m * amount, row * (2 * brick.height + 1)))
    return ite

def getCentralMassIterator(level):
    global Breakout
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
                startOffset = brick.width * 2 + 1
                ite.add((brickType, Breakout.width / 2, row * (2 * brick.height + 1)))
            
            for w in range(currentRadius):
                amount = startOffset + w * (brick.width * 2 + 1)
                for m in (-1, 1):
                    ite.add((brickType, Breakout.width / 2 + m * amount, row * (2 * brick.height + 1)))
            currentRadius += growDir * growRate
            row += 1
        currentRadius -= 1
    return ite


# Help functions
def nextBrickType():
    global brickTypeIndex, brickTypes
    brickTypeIndex = (brickTypeIndex + 1) % len(brickTypes)

def getBrickType(level):
    if level["brickType"] == "normalBrick":
        return brickTypes[brickTypeIndex]["Normal"]
    else:
        return brickTypes[brickTypeIndex]["Heavy"]