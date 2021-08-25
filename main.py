#!/usr/bin/env python3
import pygame; # library to generate the graphic interface
import time; # to set a delay between each iteration
from Classes.color import color;
from Classes.ball import Ball;
from Classes.player import Player;
# from Classes.brick import Brick, BrickHeavy;
from levelLoader.levelLoader import *

pygame.init() # Init pygame
pygame.display.set_caption("Breakout") # Set the title of the game

# CONSTANTS
width, height = 800, 1000
COLOR = color() # Get the color class with the constants

screen = pygame.display.set_mode((width, height)) # Set the size of the window

# Setup
setup(width, height, screen) # Setup level loader properties

# VARIABLES
currentLvl = 1
player, ball, bricks = loadLevel(currentLvl)

gameRunning = True # If false, the game execution ends
timeRunning = True # If true, time runs
while gameRunning:
    time.sleep(0.04) # set a delay between each iteration
    # time.sleep(0.4) # set a delay between each iteration
    if timeRunning:
        # Update the ball
        ball.move()
        # ball.clear()
        # pos = pygame.mouse.get_pos()
        # ball._x = pos[0]
        # ball._y = pos[1]
        # ball.show()

        if player.inRange(ball):
            player.makeBallBounce(ball)

        # Check bricks
        bricksDestroyed = set()
        for b in bricks:
            b.attemptHit(ball)
            if b.destroyed():
                bricksDestroyed.add(b)
        
        bricks -= bricksDestroyed # Remove all bricks destroyed
        if len(bricks) == 0:
            timeRunning = False
            # currentLvl += 1
            # loadLevel(currentLvl)


        # Update the screen
        pygame.display.flip() # Update the screen

        # Hold key control
        k = pygame.key.get_pressed()  #checking pressed keys
        if k[pygame.K_LEFT] or k[pygame.K_a]: # arrow left
            player.moveLeft()
        elif k[pygame.K_RIGHT] or k[pygame.K_d]: # arrow right
            player.moveRight()

    for event in pygame.event.get(): # for each event
        if (event.type == pygame.ACTIVEEVENT and event.state == 2): # If change on the focus of the window
            if event.gain == 0: # If focus lost
                print("lost focus")
                timeRunning = True
            elif event.gain == 1: # If focus recovered
                print("focus")
                timeRunning = False

        elif event.type == pygame.QUIT: # if quit btn pressed
            gameRunning = False # no longer running game
        
        elif event.type == pygame.KEYDOWN: # Key pressed
            if event.key == 32: # Space pressed
                timeRunning = not timeRunning # Toggle the run of iterations
            elif event.key == 276 or event.key == 97: # Arrow left
                player.moveLeft()
            elif event.key == 275 or event.key == 100: # Arrow right
                player.moveRight()

print("\nThanks for playing, I hope you liked it.")
print("See more projects like this one on https://github.com/jkutkut/")
pygame.quit() # End the pygame