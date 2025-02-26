#!/usr/bin/python3
"""
Nom: Li
Prénom: Min-Tchun
But du programme: Réaliser une mini-IA en Python capable de dtéerminer quel coup jouer au mancal à l'aide du backtracking
"""

# reconnaitre si case adverse ? abs(player - 1) ? 
#si player = 0 => abs(0 - 1) = 1
#si player = 1 => abs(1 - 1) = 0

def play(board, player: int, cell: int) -> int:

  count = 0
  tmpCell = cell
  tmpPlayer = player
  seeds = board[player][cell]

  board[player][cell] -= board[player][cell]
  while count < seeds:
    if tmpCell >= 5:
      tmpPlayer = abs(tmpPlayer - 1)
      #si player = 0 => abs(0 - 1) = 1
      #si player = 1 => abs(1 - 1) = 0
      tmpCell = -1 # car après, incrémantation de tmpCell
    tmpCell += 1
    board[tmpPlayer][tmpCell] += 1
    count += 1


  leftSeeds = 0
  while tmpPlayer != player and board[tmpPlayer][tmpCell] in [2, 3] and tmpCell >= 0:
    leftSeeds += board[tmpPlayer][tmpCell]
    board[tmpPlayer][tmpCell] -= board[tmpPlayer][tmpCell]
    tmpCell -= 1

  return leftSeeds


def is_end(board, player: int) -> bool:
  for i in board[player]:
    if i != 0:
      return False
  return True

def enum(board, player: int, depth: int) -> list[tuple[list[int], int]]:
  pass

def suggest(board, player: int, depth: int) -> int:
  pass


BOARD4 = [ [0,1,2,0,4,0],
           [0,0,0,0,0,0] ]
print(is_end(BOARD4, 1))
