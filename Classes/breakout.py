import pygame, time, webbrowser
from Classes.color import color
from Classes.brick import *
from Classes.player import Player
from Classes.ball import Ball
from levelLoader.levelLoader import setup, loadLevel, nextBrickType, getIterator;

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
    score = 0
    multipleHits = 0

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
        text = pygame.font.SysFont(None, Breakout.height // 30)
        Breakout.score = 0
        Breakout.multipleHits = 0
        scoreText, scorePosition, scoreContainer = (None, None, None)

        while Breakout.gameRunning:
            time.sleep(0.04) # set a delay between each iteration
            if Breakout.timeRunning:
                Breakout.ball.clear()
                # Update the ball
                Breakout.ball.move()
                if Breakout.player.inRange(Breakout.ball):
                    Breakout.player.makeBallBounce(Breakout.ball)
                    Breakout.multipleHits = 0 # When player hits the ball, this var resets

                # Check bricks
                bricksDestroyed = set(); scoreEarned = 0
                for b in Breakout.bricks:
                    hit = b.attemptHit(Breakout.ball)
                    if hit:
                        scoreBase = 100 # TODO get this value from Brick
                        scoreEarned += scoreBase * (1 + min(3, Breakout.multipleHits // 10))
                        Breakout.multipleHits += 1
                        if b.destroyed():
                            bricksDestroyed.add(b)
                
                Breakout.bricks -= bricksDestroyed # Remove all bricks destroyed
                if len(Breakout.bricks) == 0:
                    self.loadNextLevel()
                    continue
                
                if len(bricksDestroyed) > 0: # If any brick hitted
                    # Print all remaining bricks again to avoid ball-shadow-cliping
                    for b in Breakout.bricks:
                        b.show()
                    
                    # Update score label     
                    Breakout.score += int(scoreEarned)
                    scoreText = text.render(f"{Breakout.score}", True, Breakout.COLOR.WHITE)
                    scorePosition = ((Breakout.width - scoreText.get_width()) // 2, scoreText.get_height() // 2)
                    scoreContainer = [ (Breakout.width - scoreText.get_width() - 20) // 2, scoreText.get_height() // 2 - 10, scoreText.get_width() + 20, scoreText.get_height() + 20]

                Breakout.ball.show()

                if scoreEarned > 0 or Breakout.ball.pos()[1] < 100:
                    pygame.draw.rect(Breakout.screen, Breakout.COLOR.BG, scoreContainer)
                    Breakout.screen.blit(scoreText, scorePosition)

                # Update the screen
                pygame.display.flip() # Update the screen

                # Hold key control
                k = pygame.key.get_pressed()  #checking pressed keys
                if k[pygame.K_LEFT] or k[pygame.K_a]: # arrow left
                    Breakout.player.moveLeft()
                elif k[pygame.K_RIGHT] or k[pygame.K_d]: # arrow right
                    Breakout.player.moveRight()
            for event in pygame.event.get(): # for each event
                if event.type == pygame.WINDOWFOCUSLOST: # If change on the focus of the window
                    print("lost focus")
                    Breakout.timeRunning = False
                elif event.type == pygame.WINDOWFOCUSGAINED: # If focus recovered
                    print("focus")
                    Breakout.timeRunning = True

                elif event.type == pygame.QUIT: # if quit btn pressed
                    Breakout.gameRunning = False # no longer running game
                
                elif event.type == pygame.KEYDOWN: # Key pressed
                    if event.key == pygame.K_ESCAPE: # ESCAPE key pressed
                        Breakout.gameRunning = False
                    elif event.key == pygame.K_SPACE: # Space pressed
                        Breakout.timeRunning = not Breakout.timeRunning # Toggle the run of iterations
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT: # Arrow left
                        Breakout.player.moveLeft()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: # Arrow right
                        Breakout.player.moveRight()
                    elif event.key == 110: # n pressed
                        self.loadNextLevel()

    def mainMenu(self):
        # Setup
        
        # Title bricks
        level = {
            "bricks": [
                {
                    "type": "wall",
                    "brickType": "normalBrick",

                    "oddRow": True,
                    "skipOddRow": False,
                    "horizontalHalfAmount": 4,
                    
                    "verticalStart": 1,
                    "rows": 4,
                    "verticalGap": 1,
                    "horizontalGap": 1
                },
                {
                    "type": "wall",
                    "brickType": "heavyBrick",

                    "oddRow": True,
                    "skipOddRow": False,
                    "horizontalHalfAmount": 4,
                    
                    "verticalStart": 5,
                    "rows": 1,
                    "verticalGap": 1,
                    "horizontalGap": 1
                }
            ]
        }
        bricks = set()
        for brickClass, x, y in getIterator(level):
            bricks.add(brickClass(x, y, Breakout.screen))
        
        # Buttons
        bigText = pygame.font.SysFont(None, Breakout.height // 15)
        mediumText = pygame.font.SysFont(None, Breakout.height // 30)
        offset = 50
        
        btns = [
            {
                "title": "    Play    ",
                "textSize": bigText,
                "textColor": (0, 0, 0),
                "containerColor": (193, 193, 193),
                "heightPerOne": 0.575
            },
            {
                "title": "Type of brick",
                "textSize": mediumText,
                "textColor": (0, 0, 0),
                "containerColor": (193, 193, 193),
                "heightPerOne": 0.7
            },
            {
                "title": "More projects",
                "textSize": mediumText,
                "textColor": (0, 0, 0),
                "containerColor": (193, 193, 193),
                "heightPerOne": 0.8
            },
            {
                "title": "     Controls WASD and ENTER     ",
                "textSize": mediumText,
                "textColor": (0, 0, 0),
                "containerColor": (150, 150, 150),
                "heightPerOne": 0.92
            },
            {
                "title": "(Arrows and mouse also work =D)",
                "textSize": mediumText,
                "textColor": (0, 0, 0),
                "containerColor": (150, 150, 150),
                "heightPerOne": 0.97
            }
        ]

        btnsRendered = []
        
        for b in btns:
            playG = b["textSize"].render(b["title"], True, b["textColor"])

            btnsRendered.append({
                "obj": playG, # Text
                "pos": ((Breakout.width - playG.get_width()) // 2, Breakout.height * b["heightPerOne"]),
                "container": [ # Rectangle container of the text
                    (Breakout.width - playG.get_width() - offset) // 2,
                    Breakout.height * b["heightPerOne"] - offset // 2,
                    playG.get_width() + offset,
                    playG.get_height() + offset
                ],
                "containerColor": b["containerColor"]
            })

        change = True # Whenever a change has been made (to update the screen)
        clickableBtns = 3; current = 0
        mainMenuRunning = True
        while mainMenuRunning:
            if change:
                Breakout.screen.fill(Breakout.COLOR.BG) # Clear screen

                for b in bricks:
                    b.show()

                for i in range(len(btnsRendered)): # For all buttons
                    b = btnsRendered[i]

                    if current == i: # If btn is selected, draw shadow
                        shape = b["container"][:]
                        for j in range(2):
                            shape[j] += 8
                        shadowColor = list(b["containerColor"])
                        for j in range(3):
                            shadowColor[j] -= 120
                        pygame.draw.rect(Breakout.screen, shadowColor, shape)

                    # Draw container
                    pygame.draw.rect(Breakout.screen, b["containerColor"], b["container"])
                    # Write text on top
                    Breakout.screen.blit(b["obj"], b["pos"])

                pygame.display.flip() # Update the screen
                change = False

            btnPressed = False
            for event in pygame.event.get(): # for each event
                if event.type == pygame.QUIT: # if quit btn pressed
                    mainMenuRunning = False # no longer running game
                
                elif event.type == pygame.KEYDOWN: # Key pressed
                    if event.key == pygame.K_ESCAPE: # ESCAPE key pressed
                        mainMenuRunning = False
                    elif event.key == pygame.K_w or event.key == pygame.K_UP: # Up arrow
                        if current <= 0:
                            current = clickableBtns
                        current -= 1
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN: # Down arrow
                        current = (current + 1) % clickableBtns
                    elif event.key == 13: # Enter pressed
                        btnPressed = True

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
                    #if mouse pressed down and it is left click:
                    btnPressed = True # Act as if the enter key has been pressed

                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    current = -1 # At the moment, focus lost
                    if abs(pos[0] - Breakout.width // 2) / Breakout.width < 0.3: # If mouse in range of btns
                        # Get the aimed btn (if there is one)
                        deltaY = 0.1
                        y = pos[1] / Breakout.height # Per-one of the height of the window (0 -> 1)
                        for i in range(clickableBtns):
                            h = btns[i]["heightPerOne"]
                            if abs(y - h) < deltaY:
                                current = i
                                break

                change = True
            
            if btnPressed:
                if current == 0: # If play button pressed, Let's play
                    Breakout.gameRunning = True # Make sure the game is running now
                    Breakout.currentLvl = 0 # Start from the first level
                    self.loadNextLevel()
                    self.loop()
                elif current == 1: # If type of brick selected
                    nextBrickType()
                    bricks = set()
                    for brickClass, x, y in getIterator(level):
                        bricks.add(brickClass(x, y, Breakout.screen))
                elif current == 2: # If "more projects" selected, open the browser tab
                    webbrowser.open("https://github.com/Jkutkut/Jkutkut-projects")

        print("\nThanks for playing, I hope you liked it.")
        print("See more projects like this one on https://github.com/jkutkut/")
        pygame.quit() # End the pygame