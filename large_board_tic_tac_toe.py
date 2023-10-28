"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
                                                                                 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""
from math import floor
import string
from turtle import pos
import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random
    

mode = "player_vs_ai" # default mode for playing the game (player vs AI)

class Button:
    def __init__(self, text:string, size:int, x:int, y:int, margin:int, color:tuple = (255, 255, 255), buttonColor:tuple = (173, 173, 173), buttonHighlight:tuple = (100, 50, 50)):
        self.text = text
        self.font = pygame.font.Font("freesansbold.ttf", size)
        self.color = color
        self.margin = margin
        self.buttonColor = buttonColor
        self.buttonHighlight = buttonHighlight
        self.textBox = self.font.render(self.text, True, self.color, self.buttonColor)
        self.highlightTextBox = self.font.render(self.text, True, self.color, self.buttonHighlight)
        self.pos = (x,y)
        self.rect = self.textBox.get_rect().inflate(self.margin,self.margin)
        self.rect.topleft = (self.pos[0] - self.margin / 2, self.pos[1] - self.margin / 2 )

    # Return collision rectangle
    def GetRect(self):
        return self.rect
    
    def draw(self, screen, isHighlight):
        if isHighlight:
            pygame.draw.rect(screen,self.buttonHighlight,self.rect)
            screen.blit(self.highlightTextBox, self.pos)
        else:
            pygame.draw.rect(screen,self.buttonColor,self.rect)
            screen.blit(self.textBox, self.pos)
        
        
    
    

class RandomBoardTicTacToe:
    def __init__(self, size = (600, 600)):

        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Grid Size
        self.GRID_SIZE = 7
        self.OFFSET = 10

        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.size[0]/self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.size[1]/self.GRID_SIZE - self.OFFSET

        # This sets the margin between each cell
        self.MARGIN = 5

        # This is for menus before starting the game.
        self.gameStarted = False

        # This is for storing and interpreting board changes
        self.board:dict = { (i,j):0 for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE) }
        self.game_state = GameStatus(self.board, True, self.GRID_SIZE)

        # Initialize pygame
        pygame.init()
        
        # This is for GUI buttons
        self.startButton = Button("Start", 18, self.OFFSET * 2, self.OFFSET * 4 + self.GRID_SIZE * self.HEIGHT, self.WHITE, 10, self.GREEN, self.RED)

        self.game_reset()

    def draw_game(self):
        
        pygame.init()
        
        
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.BLACK)
        
        # Draw the grid
        
        """
        YOUR CODE HERE TO DRAW THE GRID OTHER CONTROLS AS PART OF THE GUI
        """
        # add ai choice here or after game start
        # Add control for selecting ai search type       

        for x in range(0,self.GRID_SIZE):
            for y in range(0,self.GRID_SIZE):
                pygame.draw.rect(self.screen,self.WHITE,(self.WIDTH * x + self.OFFSET/2, self.HEIGHT * y + self.OFFSET, self.WIDTH + self.MARGIN, self.HEIGHT + self.MARGIN), self.MARGIN)
                # add logic here for drawing

        pygame.display.flip();
        
    # changes the active turn on the UI, but not the boolean in backend
    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")


    def draw_circle(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CIRCLE FOR THE NOUGHTS PLAYER
        """
        
        pygame.draw.circle(self.screen, self.WHITE, (x, y), (self.WIDTH / 2 * 0.80) * 0.90, self.MARGIN)

    def draw_cross(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CROSS FOR THE CROSS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
        """
        # Locates the center point of the cell and draws a cross
        pygame.draw.line(self.screen, self.WHITE, (x - self.WIDTH / 2 * 0.6, y - self.HEIGHT / 2 * 0.6), (x + self.WIDTH / 2 * 0.6, y + self.HEIGHT / 2 * 0.6), self.MARGIN)
        pygame.draw.line(self.screen, self.WHITE, (x - self.WIDTH / 2 * 0.6, y + self.HEIGHT / 2 * 0.6), (x + self.WIDTH / 2 * 0.6, y - self.HEIGHT / 2 * 0.6), self.MARGIN)

    def is_game_over(self):

        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)
        
        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """       

        return self.game_state.is_terminal()

    def move(self, move):
        self.game_state.set_new_state(move)
        self.game_state.turn_O = not self.game_state.turn_O


    def play_ai(self):
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)
        
        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """
        if self.game_state.is_terminal():
            return
        value, location = minimax(self.game_state, 2, self.game_state.turn_O)
        self.move(location)
        self.draw_cross(location[0] * self.WIDTH + self.WIDTH * 0.5 + self.OFFSET, location[1] * self.HEIGHT + self.HEIGHT * 0.5 + self.OFFSET)
        self.change_turn()
        pygame.display.update()
        terminal = self.game_state.is_terminal()
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """



    def game_reset(self):
        self.draw_game()
        """
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """
         # Initialize a GameStatus instance
        board = { (i,j):0 for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE) }
        self.game_state = GameStatus(board, True, self.GRID_SIZE) # true while the logic for choosing which player (cross/circle) is which is WIP
        

        pygame.display.update()

    def play_game(self, mode = "player_vs_ai"):
        done = False

        clock = pygame.time.Clock()


        while not done:
            for event in pygame.event.get():  # User did something
                """
                YOUR CODE HERE TO CHECK IF THE USER CLICKED ON A GRID ITEM. EXIT THE GAME IF THE USER CLICKED EXIT
                """
                
                """
                YOUR CODE HERE TO HANDLE THE SITUATION IF THE GAME IS OVER. IF THE GAME IS OVER THEN DISPLAY THE SCORE,
                THE WINNER, AND POSSIBLY WAIT FOR THE USER TO CLEAR THE BOARD AND START THE GAME AGAIN (OR CLICK EXIT)
                """
                    
                if event.type == pygame.QUIT:
                    done = True

                """
                YOUR CODE HERE TO NOW CHECK WHAT TO DO IF THE GAME IS NOT OVER AND THE USER SELECTED A NON EMPTY CELL
                IF CLICKED A NON EMPTY CELL, THEN GET THE X,Y POSITION, SET ITS VALUE TO 1 (SELECTED BY HUMAN PLAYER),
                DRAW CROSS (OR NOUGHT DEPENDING ON WHICH SYMBOL YOU CHOSE FOR YOURSELF FROM THE gui) AND CALL YOUR 
                PLAY_AI FUNCTION TO LET THE AGENT PLAY AGAINST YOU
                """
                    
                if event.type == pygame.MOUSEBUTTONUP and self.game_state.turn_O:
                    
                    

                    location = pygame.mouse.get_pos()
                    # Only detect inside the bounds of the grid
                    if (not location[0] >= self.WIDTH * self.GRID_SIZE + self.MARGIN and not location[0] <= self.OFFSET and not location[1] >= self.HEIGHT * self.GRID_SIZE + self.MARGIN and not location[1] <= self.OFFSET):
                        # Converts the coordinates of the mouse into the row and column in the board array
                        cellX = floor((location[0] - self.MARGIN) / self.WIDTH)
                        cellY = floor((location[1] - self.MARGIN) / self.HEIGHT)
                        if self.game_state.board_state[(cellX, cellY)] == 0 and self.game_state.turn_O:
                            # Finds the center point of the grid cell the mouse clicked
                            self.draw_circle(cellX * self.WIDTH + self.WIDTH * 0.5 + self.OFFSET, cellY * self.HEIGHT + self.HEIGHT * 0.5 + self.OFFSET )
                            self.move((cellX, cellY))
                            print(self.game_state.board_state)
                            print('\n')
                            self.play_ai()
                    

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        for i in range(self.GRID_SIZE):
                            for j in range(self.GRID_SIZE):
                                if self.game_state.board_state[(i, j)] == 1:
                                    self.draw_circle(i * self.WIDTH + self.WIDTH * 0.5 + self.OFFSET, j * self.HEIGHT + self.HEIGHT * 0.5 + self.OFFSET )
                                elif self.game_state.board_state[(i, j)] == -1:
                                    self.draw_cross(i * self.WIDTH + self.WIDTH * 0.5 + self.OFFSET, j * self.HEIGHT + self.HEIGHT * 0.5 + self.OFFSET)


                if self.startButton.GetRect().collidepoint(pygame.mouse.get_pos()):
                    self.startButton.draw(self.screen, True)
                else:
                    self.startButton.draw(self.screen, False)    
                    # If we decide to not make cells the set size of 50 pixels, we'll need a private data member for it
                    # Get the position
                    
                    # Change the x/y screen coordinates to grid coordinates
                    
                    # Check if the game is human vs human or human vs AI player from the GUI. 
                    # If it is human vs human then your opponent should have the value of the selected cell set to -1
                    # Then draw the symbol for your opponent in the selected cell
                    # Within this code portion, continue checking if the game has ended by using is_terminal function
                    
            # Update the screen with what was drawn.
            pygame.display.update()

        pygame.quit()

tictactoegame = RandomBoardTicTacToe()
tictactoegame.play_game()
"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""
