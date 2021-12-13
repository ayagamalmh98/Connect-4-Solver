import numpy as np
import pygame
import sys
import math


COLUMNS=7
ROWS=6
SQUARESIZE=100
def validTransaction(board, col):
    if board[0][col]==0:
        for row in range(ROWS-1,-1,-1):
            if board[row][col]==0:
                return row
    return -1
def makeTransaction(board, col, row, piece):
    board[row][col]= piece

def showBoard(board):
    for col in range(COLUMNS):
        for row in range(ROWS):
            pygame.draw.rect(screen, (218,190,167), (col*SQUARESIZE+SQUARESIZE,row*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            if board[row][col]==0:
                pygame.draw.circle(screen, (222,210,197), (int(col*SQUARESIZE+SQUARESIZE+SQUARESIZE/2),
                                                           int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), int(SQUARESIZE/2-10))
            elif board[row][col]==1:
                pygame.draw.circle(screen, (166,128,105), (int(col*SQUARESIZE+SQUARESIZE+SQUARESIZE/2),
                                                           int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), int(SQUARESIZE/2-10))
            elif board[row][col]==2:
                pygame.draw.circle(screen, (198, 91, 80), (int(col*SQUARESIZE+SQUARESIZE+SQUARESIZE/2),
                                                           int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), int(SQUARESIZE/2-10))
    pygame.display.update()
def fullBoard(board):
    for j in range (COLUMNS):
        if board[0][j] == 0:
            return 0
    return 1;
def checkWinner(board):
  player=0
  AIagent=0
  rows=len(board)
  columns=len(board[0])
  for i in range (rows):
    for j in range (columns):
      count=0
      m=i
      while m+1 < rows and board[m+1][j]==board[i][j] :
        count=count+1
        m=m+1
        if count == 3:
          print("horizontal")
          print(board[i][j])
          print(i,j)
          if board[i][j]==1:
            player=player+1
          else:
            AIagent=AIagent+1
      count=0
      n=j
      while n+1 < columns and board[i][n+1]==board[i][j]:
        count=count+1
        n=n+1
        if count == 3:
          print("vertical")
          print(board[i][j])
          print(i,j)
          if board[i][j]==1:
            player=player+1
          else:
            AIagent=AIagent+1
      count=0
      m=i
      n=j
      while m+1 < rows and n+1 < columns and board[m+1][n+1]==board[i][j]:
        count=count+1
        m=m+1
        n=n+1
        if count == 3:
          print("diagonal")
          print(board[i][j])
          print(i,j)
          if board[i][j]==1:
            player=player+1
          else:
            AIagent=AIagent+1
      count = 0
      m = i
      n = j
      while m + 1 < rows and n - 1 >= 0 and board[m + 1][n - 1] == board[i][j]:
          count = count + 1
          m = m + 1
          n = n - 1
          if count == 3:
              print("diagonal")
              print(board[i][j])
              print(i, j)
              if board[i][j] == 1:
                  player = player + 1
              else:
                  AIagent = AIagent + 1
  print(player)
  print(AIagent)
  if(player==AIagent):
      print("stalement!")
  elif(player>AIagent):
      print("player wins congratulations !")
  else:
      print("AI agent wins !")


board = np.zeros((ROWS,COLUMNS))
boardFull = False
turn = 1
pygame.init()

width = (COLUMNS+2)*SQUARESIZE
length=(ROWS+1)*SQUARESIZE
screen =pygame.display.set_mode((width,length))

showBoard(board)
pygame.display.update()
while not fullBoard(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0,0,0), (0, 0, width, SQUARESIZE))
            posx=event.pos[0]
            if turn == 1:
                pygame.draw.circle(screen,(166,128,105), (posx,int(SQUARESIZE / 2)),  int(SQUARESIZE / 2 - 10))
            elif turn == 2:
                pygame.draw.circle(screen, (198, 91, 80), (posx,int(SQUARESIZE / 2)),  int(SQUARESIZE / 2 - 10))
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #player turn

            print("for player", turn)
            print("choose col")
            if turn == 1:
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARESIZE)-1)
                row = validTransaction(board, col)
                if row != -1:
                    makeTransaction(board, col, row, turn)
                    turn = 2
                print("row is")
                print(row)

            # AI agent turn
            elif turn == 2:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE)-1)
                row = validTransaction(board, col)
                if row != -1:
                    makeTransaction(board, col, row, turn)
                    turn = 1
            print(board)
            showBoard(board)
checkWinner(board)
