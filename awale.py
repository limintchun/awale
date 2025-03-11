#!/usr/bin/python3
"""
Nom: Li
Prénom: Min-Tchun
But du programme: Réaliser une mini-IA en Python capable de dtéerminer quel coup jouer au mancal à l'aide du backtracking
"""

def play(board, player: int, cell: int) -> int:
    """
    Joue un coup sur le plateau de jeu
    @param board: list[list[int]]: le plateau de jeu
    @param player: int: le joueur qui joue
    @param cell: int: la cellule de départ
    @return: int: le nombre de graines restant après le coup
    """

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
    """
    Détermine si un joueur ne peut plus jouer
    @param board: list[list[int]]: le plateau de jeu
    @param player: int: le joueur qui joue
    @return: bool: True si le joueur ne peut plus jouer, False sinon
    """
    for i in board[player]:
        if i != 0:
            return False
    return True

def enum(board, player: int, depth: int) -> list[tuple[list[int], int]]:
    """
    Enumère les coups possibles pour un joueur
    @param board: list[list[int]]: le plateau de jeu
    @param player: int: le joueur qui joue
    @param depth: int: la profondeur de recherche
    """
    # cas de base pour éviter une récursion infinie
    if depth == 0 or is_end(board, player):
        return [([], 0)]

    # construction de la liste des résultats
    results = []
    for cell in range(6):
        if board[player][cell] > 0:
            # évite d'affamer le joueur adverse
            if valid_move(board, player, cell):
                new_board = [row.copy() for row in board]
                score = play(new_board, player, cell)
                if player == 0:
                    move_score = score
                else:
                    move_score = -score

                next_player = abs(player - 1)
                sub_sequ = enum(new_board, next_player, depth - 1)

                for sub_moves, sub_score in sub_sequ:
                    moves = [cell] + sub_moves
                    total_score = move_score + sub_score
                    results.append((moves, total_score))
    return results

def valid_move(board, player, cell) -> bool:
    """
    Détermine si un coup est valide
    @param board: list[list[int]]: le plateau de jeu
    @param player: int: le joueur qui joue
    @param cell: int: la cellule de départ
    """

    if board[player][cell] == 0:
        return False

    temp_board = [row.copy() for row in board]
    play(temp_board, player, cell)

    opps = 1 - player
    if sum(temp_board[opps]) == 0:
        for other_cell in range(6):
            if other_cell != cell and board[player][other_cell] > 0:
                other_tmp_board = [row.copy() for row in temp_board]
                play(other_tmp_board, player, other_cell)

                if sum(other_tmp_board[opps]) > 0:
                    return False
        return True
    return True


def suggest(board, player: int, depth: int) -> int:

    if depth <= 0:
        return -1
    # simple déclaration de la variable best_move
    best_move = -1

    if player == 0:
        best_score = float('-inf')

        for cell in range(6):
            if board[player][cell] > 0 and valid_move(board, player, cell):

                new_board = [row.copy() for row in board]
                score = play(new_board, player, cell)

                # if depth <= 1 or is_end(new_board, 1 - player):
                #     current_score = score
                if is_end(new_board, 1 - player):
                    current_score = score
                else:
                    next_score = min_max(new_board, abs(player - 1), depth - 1, float('-inf'), float('inf'))
                    current_score = score + min_max(new_board, abs(player - 1), depth - 1, float('-inf'), float('inf'))

                if current_score > best_score:
                    best_score = current_score
                    best_move = cell
    else:
        best_score = float('inf')

        for cell in range(6):
            if board[player][cell] > 0 and valid_move(board, player, cell):

                new_board = [row.copy() for row in board]
                score = play(new_board, player, cell)

                # if depth <= 1 or is_end(new_board, 1 - player):
                #     current_score = -score
                if is_end(new_board, abs(player - 1)):
                    current_score = -score
                else:
                    new_score = min_max(new_board, abs(player - 1), depth - 1, float('-inf'), float('inf'))
                    current_score = -score + new_score

                if current_score < best_score:
                    best_score = current_score
                    best_move = cell
    return best_move



            # if is_end(new_board, abs(player - 1)):
            #     score = final_score(new_board, score, player)
            # else:
            #     if player == 0:
            #         player_score = score
            #     else:
            #         player_score = -score

            #     next_score = min_max(new_board, abs(player - 1), depth - 1, player_score)
            #     score = next_score

            # if player == 0:
            #     if score > best_score:
            #         best_score = score
            #         best_cell = cell
            #     else:
            #         if score < best_score:
            #             best_score = score
            #             best_cell = cell

def min_max(board, player: int, depth: int, alpha : int, beta :int) -> int:
    if depth <= 0 or is_end(board, player):
        return 0

    if player == 0:
        best_score = float('-inf')
        for cell in range(6):
            if board[player][cell] > 0 and valid_move(board, player, cell):
                new_board = [row.copy() for row in board]
                score = play(new_board, player, cell)

                if is_end(new_board, abs(player - 1)):
                    current_score = score
                else:
                    opps_best = min
                    current_score = score + min_max(new_board, abs(player - 1), depth - 1, alpha, beta)

                best_score = max(best_score, current_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float('inf')

        for cell in range(6):
            if board[player][cell] > 0 and valid_move(board, player, cell):
                new_board = [row.copy() for row in board]
                score= play(new_board, player, cell)

                if is_end(new_board, abs(player - 1)):
                    current_score = -score
                else:
                    opps_best = min_max(new_board, abs(player - 1), depth - 1, alpha, beta)
                    current_score = -score + opps_best

                best_score = min(best_score, current_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score

def final_score(board, score, player: int) -> int:
    if player == 0:
        return score
    else:
        return -score

BOARD1 = [ [1,7,2,7,2,0],
           [0,3,4,2,2,5] ]
enum(BOARD1, 0, 1)
