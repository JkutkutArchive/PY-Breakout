import time
import pygame
from Classes.color import color
from Classes.brick import *
from Classes.player import Player
from Classes.ball import Ball
from levelLoader.levelLoader import setup, loadLevel

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
    player, ball, bricks = (None, None, set())

    def __init__(self, title, logo, width, height) -> None:
        Breakout.title =  title
        Breakout.logoURL = logo

        pygame.init() # Init pygame
        pygame.display.set_caption(Breakout.title) # Set the title of the game

        Breakout.gameIcon = pygame.image.load(Breakout.logoURL)
        pygame.display.set_icon(Breakout.gameIcon)

        self.resize(width, height)

        setup(Breakout)

        self.mainMenu()

    def resize(self, width=None, height=None):
        if width != None:
            Breakout.width = width
            # update brick size
            unit = width // 30
            brick.width = unit
            brick.height = unit // 2

            # update player size
            Player.unit = width // 50

            # update ball size
            Ball.radius = 5
        
        if height != None:
            Breakout.height = height
        
        Breakout.screen = pygame.display.set_mode((Breakout.width, Breakout.height))

    def updateFullScreen():
        '''Clear the screen and update it with the new level'''
        Breakout.screen.fill(Breakout.COLOR.BG) # Clear screen
        if Breakout.player != None:
            Breakout.player.show()
        if Breakout.ball != None:
            Breakout.ball.show()
        for b in Breakout.bricks:
            b.show()
        pygame.display.flip() # Update the screen

    def loadNextLevel(self):
        Breakout.player, Breakout.ball, Breakout.bricks = loadLevel(Breakout.currentLvl + 1)
        Breakout.currentLvl = (Breakout.currentLvl + 1) % 3
        Breakout.updateFullScreen()


    def loop(self):
        while Breakout.gameRunning:
            time.sleep(0.04) # set a delay between each iteration
            if Breakout.timeRunning:
                # Update the ball
                Breakout.ball.move()

                if Breakout.player.inRange(Breakout.ball):
                    Breakout.player.makeBallBounce(Breakout.ball)

                # Check bricks
                bricksDestroyed = set()
                for b in Breakout.bricks:
                    b.attemptHit(Breakout.ball)
                    if b.destroyed():
                        bricksDestroyed.add(b)
                
                Breakout.bricks -= bricksDestroyed # Remove all bricks destroyed
                if len(Breakout.bricks) == 0:
                    self.loadNextLevel()
                    continue


                # Update the screen
                pygame.display.flip() # Update the screen

                # Hold key control
                k = pygame.key.get_pressed()  #checking pressed keys
                if k[pygame.K_LEFT] or k[pygame.K_a]: # arrow left
                    Breakout.player.moveLeft()
                elif k[pygame.K_RIGHT] or k[pygame.K_d]: # arrow right
                    Breakout.player.moveRight()
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
                    if event.key == pygame.K_SPACE: # Space pressed
                        Breakout.timeRunning = not Breakout.timeRunning # Toggle the run of iterations
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT: # Arrow left
                        Breakout.player.moveLeft()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: # Arrow right
                        Breakout.player.moveRight()
                    elif event.key == 110: # n pressed
                        self.loadNextLevel()

    def mainMenu(self):
        # Setup

        # Buttons
        offset = 50

        bigText = pygame.font.SysFont(None, Breakout.height // 15)
        playG = bigText.render('Play game', True, (0, 0, 200))
        playG_pos = [(Breakout.width - playG.get_width()) // 2, Breakout.height * 0.2]
        playG_size = [(playG.get_width() + offset), (playG.get_height() + offset)]
        playG_container = tuple([(Breakout.width - playG.get_width() - offset) // 2, Breakout.height * 0.2 - offset // 2] + playG_size)

        change = True # Whenever a change has been made        
        while Breakout.gameRunning:
            if change:
                Breakout.screen.fill(Breakout.COLOR.BG) # Clear screen

                pygame.draw.rect(Breakout.screen, (200, 200, 200), playG_container)
                Breakout.screen.blit(playG, playG_pos)

                pygame.display.flip() # Update the screen
                change = False


            for event in pygame.event.get(): # for each event
                if event.type == pygame.QUIT: # if quit btn pressed
                    Breakout.gameRunning = False # no longer running game
                
                elif event.type == pygame.KEYDOWN: # Key pressed
                    if event.key == pygame.K_w or event.key == pygame.K_UP: # Up arrow
                        print("Up")
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN: # Down arrow
                        print("Down")
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT: # Arrow left
                        print("Left")
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: # Arrow right
                        print("Right")
                
                change = True
            

        print("\nThanks for playing, I hope you liked it.")
        print("See more projects like this one on https://github.com/jkutkut/")
        pygame.quit() # End the pygame