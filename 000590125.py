#!/usr/bin/python3
"""
Nom: Li
Prénom: Min-Tchun
But du programmme: Réaliser une mini-IA en Python3 capable de déterminer quel coup jouer au "mancal" à l'aide du backtracking

Documentation utilisée: 
    https://medium.com/@mol02office/ai-implementation-for-owar%C3%A9-awal%C3%A9-part-1-80c4e679e01c
    https://medium.com/@mol02office/ai-implementation-for-owar%C3%A9-part-2-187b00ccbf09
"""

def play(board, player: int, cell: int) -> int:
    """
    Joue un coup sur le plateau de jeu
    Prend en paramètre un plateau de jeu, le joueur, la cellule de départ.
    Retourne le nombre de graines capturées après le coup.
    """

    # Initialisation des variables nécessaires au calcul du score de player
    count = 0
    tmpCell = cell
    tmpPlayer = player
    seeds = board[player][cell]

    # Vider la cellule de départ
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

def will_starve_opponent(board, player: int, cell: int) -> bool:
    """
    Vérifie si un coup va affamer l'adversaire.
    Prend en paramètre un plateau de jeu, le joueur et une case.
    Retourne un booléen, True si le coup va affamer l'adversaire, sinon False.
    """

    # Une cellule vide ne peut pas être jouée
    if board[player][cell] == 0:
        return False
    
    # Copie le plateau pour ensuite simuler le coup
    temp_board = [row[:] for row in board]
    play(temp_board, player, cell)
    
    opponent = abs(player -1)
    return sum(temp_board[opponent]) == 0

def get_valid_moves(board, player: int) -> list:
    """
    Reçoit tous les coups valides pour un joueur.
    Prend en paramètre un plateau de jeu et un joueur.
    Retourne une liste des indices de cellules valides.
    """
    valid_moves = []
    has_non_starving_moves = False
    
    # Vérifie si le coup va affamer l'adversaire
    for cell in range(6):
        if board[player][cell] > 0:
            if not will_starve_opponent(board, player, cell):
                has_non_starving_moves = True
                valid_moves.append(cell)
    
    # Sinon retourne les coups valides
    if has_non_starving_moves:
        return valid_moves
    
    # Si tout les coups affament l'adversaire, retourne toutes les cellules non vides
    return [cell for cell in range(6) if board[player][cell] > 0]

def is_end(board, player: int) -> bool:
    """
    Vérifie si le jeu est terminé.
    Prend en paramètre un plateau de jeu et un joueur.
    Retourne un booléen, True si le jeu est terminé, sinon False. 
    """

    for i in board[player]:
        if i != 0:
            return False
    return True

def enum(board, player: int, depth: int) -> list[tuple[list[int], int]]:
    """
    Enumère toutes les séquences possibles de coups jusqu'à une profondeur donnée.
    Prend un plateau de jeu, un joueur et la profondeur de recherche.
    Retourne une liste de tuples tel que (séquence de coups, score final)
    """

    # Cas de base pour éviter une récursion infinie
    if depth == 0 or is_end(board, player):
        return [([], 0)]

    # construction de la liste des résultats
    results = []
    valid_moves = get_valid_moves(board, player)
    
    for move in valid_moves:
        # Copie le plateau de jeu
        temp_board = [row[:] for row in board]
        
        # Simule le coup du joueur
        collected = play(temp_board, player, move)
        
        # score négatif si c'est l'adversaire, sinon le score est positif
        score_adjustment = collected if player == 0 else -collected
        
        # Appel récursif avec le prochain coup du joueur et d'une profondeur réduite
        next_player = abs(player - 1)
        next_sequences = enum(temp_board, next_player, depth - 1)
        
        # Ajoute les coup actuel avec ajustement du score
        for seq, score in next_sequences:
            results.append(([move] + seq, score + score_adjustment))

    return results


def suggest(board, player: int, depth: int) -> int:
    """
    Suggère le meilleur coup pour un joueur en utilisant l'algorithme MinMax
    Prend un plateau de jeu, un joueur et la profondeur de recherche.
    Retourne la meilleure cellule à jouer
    """

    valid_moves = get_valid_moves(board, player)
    
    if not valid_moves:
        return -1
    
    best_move = valid_moves[0] # Début à partir du premier coup valide
    
    if player == 0:  # Joueur 1 (à maximiser)
        best_score = float('-inf')

        for move in valid_moves:
            temp_board = [row[:] for row in board]
            collected = play(temp_board, player, move)
            
            if depth == 1:
                score = collected 
            else:
                next_player = abs(player - 1)
                # Evalue les coups suivants
                score = collected + minmax(temp_board, next_player, depth - 1, False)
                
            if score > best_score:
                best_score = score
                best_move = move

    else:  # Joueur 2 (à minmiser)
        best_score = float('inf')
        for move in valid_moves:
            temp_board = [row[:] for row in board]
            
            collected = play(temp_board, player, move)
            
            if depth == 1:
                score = -collected
            else:
                next_player = abs(player - 1)
                # Evalue les coups suivants
                score = -collected + minmax(temp_board, next_player, depth - 1, True)
                
            if score < best_score:
                best_score = score
                best_move = move
                
    return best_move


def minmax(board, player: int, depth: int, maximizing: bool) -> int:
    """
    Algorithme MinMax pour évaluer les coups possibles.
    Prend en paramètre un plateau de jeu, un joueur, la profondeur de recherche et une variable déterminant s'il faut maximiser le coup.
    Retourne le meilleur score
    """
    # Cas de base: profondeur atteinte ou jeu terminé
    if depth == 0 or is_end(board, player):
        return 0
    
    valid_moves = get_valid_moves(board, player)
    
    if not valid_moves:  
        return 0
    
    if maximizing:  # Tour du joueur 1 (à maximiser)
        best_score = float('-inf')
        for move in valid_moves:
            temp_board = [row[:] for row in board]
            
            collected = play(temp_board, player, move)
            
            next_player = abs(player - 1)
            score = collected + minmax(temp_board, next_player, depth - 1, False)
            
            best_score = max(best_score, score)
        return best_score
    
    else:  # Tour du joeur 2 (à minimiser)
        best_score = float('inf')
        for move in valid_moves:
            temp_board = [row[:] for row in board]
            
            collected = play(temp_board, player, move)
            
            next_player = abs(player - 1)
            score = -collected + minmax(temp_board, next_player, depth - 1, True)
            
            best_score = min(best_score, score)
        return best_score
