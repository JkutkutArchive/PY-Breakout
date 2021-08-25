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

def getLevel(lvl, type="classic"):
    if not isinstance(lvl, int):
        raise Exception("The lvl must be an integer.")
    return levels[type][lvl - 1]

def loadLevel(lvl, type="classic"):
    global width, height, screen
    level = getLevel(lvl, type)

    bricks = set()

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