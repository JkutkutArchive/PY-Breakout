#!/usr/bin/env python3
import pygame; # library to generate the graphic interface
import time; # to set a delay between each iteration
from Classes.color import color;
from Classes.ball import Ball;

pygame.init() # Init pygame
pygame.display.set_caption("Breakout") # Set the title of the game

# CONSTANTS
width, height = 1000, 1000 
# sizeX, sizeY = 50, 50 # Number of cell spots in each axis
# sizeWidthX = width / sizeX # Size of each spot
# sizeWidthY = height / sizeY
COLOR = color() # Get the color class with the constants

screen = pygame.display.set_mode((width, height)) # Set the size of the window

# VARIABLES
ball = Ball(500, 500)

screen.fill(COLOR.BG) # Clean screen
gameRunning = True # If false, the game stops
timeRunning = True # If true, time runs (so iterations occur)
while gameRunning:
    # screen.fill(COLOR.BG) # Clean screen

    time.sleep(0.04) # set a delay between each iteration
    if timeRunning:
        # Update the ball
        pygame.draw.circle(screen, COLOR.BG, ball.pos(), ball.size())
        ball.move()
        pygame.draw.circle(screen, ball.color(), ball.pos(), ball.size())

        ballX, ballY = ball.pos()
        if ballX < 0 or ballX > width:
            ball.bounce(x=True)
        if ballY < 0 or ballY > width:
            ball.bounce(y=True)

        # Update the screen
        pygame.display.flip() # Update the screen

    for event in pygame.event.get(): # for each event
        # if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
        #     if mouse pressed down and it is left click: 
        #     pos = pygame.mouse.get_pos()
        #     x = floor(pos[0] / sizeWidthX)
        #     y = floor(pos[1] / sizeWidthY)

        # if event.type == pygame.MOUSEMOTION: # If mouse moved
        #     pos = pygame.mouse.get_pos()
        #     x = floor(pos[0] / sizeWidthX)
        #     y = floor(pos[1] / sizeWidthY)
        #     if event.buttons[0] == 1: # If left click hold
        #         pass
        #     if event.buttons[2] == 1: # Right click
        #         pass
        
        if event.type == pygame.QUIT: # if quit btn pressed
            gameRunning = False # no longer running game
        
        elif event.type == pygame.KEYDOWN: # Key pressed
            if event.key == 32: # Space pressed
                timeRunning = not timeRunning # Toggle the run of iterations

print("\nThanks for playing, I hope you liked it.")
print("See more projects like this one on https://github.com/jkutkut/")
pygame.quit() # End the pygame