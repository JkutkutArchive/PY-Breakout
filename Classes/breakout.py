import pygame
from Classes.color import color
from levelLoader.levelLoader import *

class Breakout():
    # UI properties
    title = ""
    logoURL = ""
    gameIcon = None

    # Screen properties
    width = 0
    height = 0
    screen = None

    # Constants
    COLOR = color()

    # VARIABLES
    gameRunning = True
    timeRunning = True
    currentLvl = 0
    player, ball, bricks = (None, None, None)

    def __init__(self, title, logo, width, height) -> None:
        Breakout.title =  title
        Breakout.logoURL = logo

        pygame.init() # Init pygame
        pygame.display.set_caption(Breakout.title) # Set the title of the game

        Breakout.gameIcon = pygame.image.load(Breakout.logoURL)
        pygame.display.set_icon(Breakout.gameIcon)

        self.resize(width, height)

        self.loop()

    def resize(self, width=None, height=None):
        if width:
            Breakout.width = width
        if height:
            Breakout.height = height
        
        Breakout.screen = pygame.display.set_mode((Breakout.width, Breakout.height))
    
    def loadNextLevel(self):
        Breakout.currentLvl += 1
        Breakout.player, Breakout.ball, Breakout.bricks = loadLevel(Breakout.currentLvl)


    def loop(self):
        while Breakout.gameRunning:
            for event in pygame.event.get(): # for each event
                if (event.type == pygame.ACTIVEEVENT and event.state == 2): # If change on the focus of the window
                    if event.gain == 0: # If focus lost
                        print("lost focus")
                        Breakout.timeRunning = True
                    elif event.gain == 1: # If focus recovered
                        print("focus")
                        Breakout.timeRunning = False

                elif event.type == pygame.QUIT: # if quit btn pressed
                    Breakout.gameRunning = False # no longer running game
                
                elif event.type == pygame.KEYDOWN: # Key pressed
                    if event.key == 32: # Space pressed
                        Breakout.timeRunning = not Breakout.timeRunning # Toggle the run of iterations
                    elif event.key == 276 or event.key == 97: # Arrow left
                        Breakout.player.moveLeft()
                    elif event.key == 275 or event.key == 100: # Arrow right
                        Breakout.player.moveRight()
                    elif event.key == 110: # n pressed
                        currentLvl = (currentLvl + 1) % 3 + 1
                        # player, ball, bricks = loadLevel(currentLvl)

        print("\nThanks for playing, I hope you liked it.")
        print("See more projects like this one on https://github.com/jkutkut/")
        pygame.quit() # End the pygame