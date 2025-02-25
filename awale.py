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

  while count < seeds:
    if tmpCell >= 5:
      tmpPlayer = abs(player - 1)
      #si player = 0 => abs(0 - 1) = 1
      #si player = 1 => abs(1 - 1) = 0
      tmpCell = -1 # car après, incrémantation de tmpCell
    tmpCell += 1
    board[tmpPlayer][tmpCell] += 1
    count += 1

  board[player][cell] -= board[player][cell]
  leftSeeds = 0
  while tmpPlayer != player and board[tmpPlayer][tmpCell] in [2, 3]:
    leftSeeds += board[tmpPlayer][tmpCell]
    board[tmpPlayer][tmpCell] -= board[tmpPlayer][tmpCell]
    tmpCell -= 1

  return leftSeeds


def is_end(board, player: int) -> bool:
  return True


BOARD1 = [ [1,7,2,7,2,0],
           [0,3,4,2,2,5] ]

print(play(BOARD1, 0, 3))
