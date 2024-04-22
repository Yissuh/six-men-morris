import random
import math
import time
import sys


valid_moves = {
        1: [2, 7],
        2: [1, 3, 5],
        3: [2, 10],
        4: [5, 8],
        5: [2, 4, 6],
        6: [5, 9],
        7: [1, 14, 8],
        8: [4, 11, 7],
        9: [6, 13, 10],
        10: [3, 9, 16],
        11: [8, 12],
        12: [11, 13, 15],
        13: [9, 12],
        14: [7, 15],
        15: [12, 14, 16],
        16: [15, 10]
    }
    
def draw_board(board):
    print(f"    {board[0]}---------{board[1]}---------{board[2]}   ")
    print("    |         |         |")
    print(f"    |----{board[3]}----{board[4]}----{board[5]}----|")
    print("    |    |         |    |")
    print(f"    {board[6]}----{board[7]}         {board[8]}----{board[9]}")
    print("    |    |         |    |")
    print(f"    |----{board[10]}---{board[11]}---{board[12]}---|")
    print("    |         |         |")
    print(f"    {board[13]}--------{board[14]}--------{board[15]}   ")
    print()

def is_valid_move(board, move):
    return board[move - 1] == str(move)

def check_mill(board, move, player):
    mills = [
        [1, 2, 3], [1, 7, 14],
        [4, 5, 6], [4, 8, 11],
        [6, 9, 13], [11, 12, 13],
        [3, 10, 16], [14, 15, 16]
    ]
    for mill in mills:
        if move in mill:
            if all(board[pos - 1] == player + str(pos) for pos in mill):
                return mill
    return None



def check_win(board, player):
    num_pieces_player = sum(1 for pos in board if pos.startswith(player))
    return num_pieces_player <= 2




def ai_move(board, player, opponent):
    best_move, best_score = None, -float('inf')
    mills = [
        [1, 2, 3], [1, 7, 14],
        [4, 5, 6], [4, 8, 11],
        [6, 9, 13], [11, 12, 13],
        [3, 10, 16], [14, 15, 16]
    ]
    
    # Function to check if a mill can be formed with a move
    def can_form_mill(move, player):
        temp_board = board.copy()
        temp_board[move - 1] = player + str(move)
        for mill in mills:
            if all(temp_board[pos - 1] == player + str(pos) for pos in mill):
                return True
        return False
    
    # Function to check if the opponent can form a mill with a move
    def can_opponent_form_mill(move):
        temp_board = board.copy()
        temp_board[move - 1] = opponent + str(move)
        for mill in mills:
            if all(temp_board[pos - 1] == opponent + str(pos) for pos in mill):
                return True
        return False

    # Check if any mill can be formed with the current move
    for i in range(len(board)):
        if board[i] == str(i + 1):
            if can_form_mill(i + 1, player):
                best_move = i + 1
                break

    # If no mill can be formed, place piece in position that blocks opponent's mills
    if best_move is None:
        for i in range(len(board)):
            if board[i] == str(i + 1):
                if can_opponent_form_mill(i + 1):
                    best_move = i + 1
                    break

    # If no mill can be formed or opponent's mills can be blocked, check if any potential mill can be formed
    if best_move is None:
        for mill in mills:
            if board[mill[0]-1] == player + str(mill[0]) and \
               board[mill[1]-1] == str(mill[1]) and \
               board[mill[2]-1] == str(mill[2]):
                best_move = mill[1]  # Select middle position in potential mill
                break

        # Check if AI has a middle piece, then check for availability of other positions to form a mill
        for i in range(len(board)):
            if board[i] == player + str(i + 1):
                middle_piece = i + 1
                for mill in mills:
                    if middle_piece == mill[1] and \
                       board[mill[0] - 1] == str(mill[0]) and \
                       board[mill[2] - 1] == str(mill[2]):
                        if board[mill[0] - 1] == str(mill[0]) and board[mill[2] - 1] == str(mill[2]):
                            best_move = mill[0]  # Select first position to form mill
                        elif board[mill[0] - 1] == str(mill[0]) and board[mill[2] - 1] == player + str(mill[2]):
                            best_move = mill[2]  # Select third position to form mill
                        break

    # If no mill can be formed or opponent's mills can be blocked or no potential mill, make a random move
    if best_move is None:
        valid_moves = [i + 1 for i in range(len(board)) if board[i] == str(i + 1)]
        if valid_moves:
            best_move = random.choice(valid_moves)

    return best_move




def minimax(board, depth, alpha, beta, is_maximizing, player, opponent):
    if check_win(board, player):
        return 1000
    elif check_win(board, opponent):
        return -1000
    elif depth == 0:
        return evaluate(board, player)  

    if is_maximizing:
        max_eval = -math.inf
        for i in range(len(board)):
            if board[i] == str(i + 1):
                board[i] = player + str(i + 1)
                eval_score = minimax(board, depth - 1, alpha, beta, False, player, opponent)
                board[i] = str(i + 1)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(len(board)):
            if board[i] == str(i + 1):
                board[i] = opponent + str(i + 1)
                eval_score = minimax(board, depth - 1, alpha, beta, True, player, opponent)
                board[i] = str(i + 1)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval


def evaluate(board, player):
    score = 0
    opponent = "H" if player == "A" else "A"
    mills = [
        [1, 2, 3], [1, 7, 14],
        [4, 5, 6], [4, 8, 11],
        [6, 9, 13], [11, 12, 13],
        [3, 10, 16], [14, 15, 16]
    ]
    for mill in mills:
        count_player = sum(board[pos - 1] == player + str(pos) for pos in mill)
        count_opponent = sum(board[pos - 1] == opponent + str(pos) for pos in mill)
        if count_player == 3:
            score += 100
        elif count_player == 2 and count_opponent == 0:
            score += 10
        elif count_player == 1 and count_opponent == 0:
            score += 1
        elif count_opponent == 3:
            score -= 100
        elif count_opponent == 2 and count_player == 0:
            score -= 10
        elif count_opponent == 1 and count_player == 0:
            score -= 1
    return score

def remove_piece(board, move):
    board[move - 1] = str(move)

def player_move(board, player):
    while True:
        try:
            move = int(input(f"Enter your move, {player}: "))
            if is_valid_move(board, move):
                return move
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def handle_mill_capture(board, player, opponent, cur_mill, used_mills):
    if tuple(cur_mill) in used_mills[player]:
        print(f"{player} formed a mill!")
        while True:
            try:
                if player == "H":
                    captured_move = int(input(f"Enter a piece to capture for {player}: "))
                else:
                    captured_move = ai_capture(board, player, opponent)
                    print(f"{player} chooses to capture {captured_move}")
                
                # Adjust for 0-based indexing
                captured_move -= 1

                if board[captured_move] == opponent + str(captured_move + 1):
                    print(f"{player} captures {board[captured_move]}")
                    remove_piece(board, captured_move + 1)  # Add 1 to get position
                    
                    # Reset used_mills for player
                    used_mills[player] = set()
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print(f"{player} formed a mill!")
        while True:
            try:
                if player == "H":
                    captured_move = int(input(f"Enter a piece to capture for {player}: "))
                else:
                    captured_move = ai_capture(board, player, opponent)
                    print(f"{player} chooses to capture {captured_move}")
                
                # Adjust for 0-based indexing
                captured_move -= 1

                if board[captured_move] == opponent + str(captured_move + 1):
                    print(f"{player} captures {board[captured_move]}")
                    remove_piece(board, captured_move + 1)  # Add 1 to get position
                    
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def ai_capture(board, player, opponent):
    opponent_pieces = [i + 1 for i, pos in enumerate(board) if pos == opponent + str(i + 1)]
    potential_mills = [
        [1, 2, 3], [1, 7, 14],
        [4, 5, 6], [4, 8, 11],
        [6, 9, 13], [11, 12, 13],
        [3, 10, 16], [14, 15, 16]
    ]

    # Check if there are any opponent pieces in potential mills
    for mill in potential_mills:
        if all(board[pos - 1] == opponent + str(pos) for pos in mill):
            for pos in mill:
                if pos in opponent_pieces:
                    return pos

    # If no opponent pieces in potential mills, prioritize capturing non-potential mill pieces
    non_potential_mill_pieces = [pos for pos in opponent_pieces if all(board[pos - 1] != opponent + str(pos) for mill in potential_mills if pos in mill)]
    
    # Prioritize capturing pieces that are not part of potential mills or blocking opponent's mills
    if non_potential_mill_pieces:
        return min(non_potential_mill_pieces)  # Choose the lowest numbered piece to capture
    else:
        # If no non-potential mill pieces, then capture a random opponent piece
        return min(opponent_pieces) if opponent_pieces else None


def valid_piece(board, piece, player):
    if piece.isdigit() and 1 <= int(piece) <= 16:
        piece_on_board = board[int(piece) - 1]
        if piece_on_board == player + piece:
            # Check if the valid moves for this piece have an empty position
            for valid_move in valid_moves[int(piece)]:
                if board[valid_move - 1] == str(valid_move):
                    return True
    return False


def get_piece_to_move(board, player):
    while True:
        try:
            piece = input(f"Select piece to move for {player}: ").upper()
            if valid_piece(board, piece[1:], player):
                return int(piece[1:])
            else:
                print("Invalid piece selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a piece in the format 'X#'.")

def is_valid_move_p2(board, move, position):
    # Dictionary to store valid moves for each position


    # Check if the move is valid based on the position's valid moves
    if move not in valid_moves[position]:
        return False
    
    # Check if the destination is empty
    if board[move - 1] != str(move):
        return False

    return True

def player_move_p2(board, player):
    piece_to_move = get_piece_to_move(board, player)
    while True:
        try:
            destination = int(input(f"Select position for {player}: "))
            if is_valid_move_p2(board, destination, piece_to_move):
                # Add your logic to check if the move is valid
                # For example, you can add a function to check if the destination is an adjacent position
                old_position = board[piece_to_move - 1]
                board[piece_to_move - 1] = str(piece_to_move)
                board[destination - 1] = player + str(destination)
                print(f"{player} moves {old_position} to {destination}")
                return piece_to_move, destination
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def ai_move_p2(board, player, opponent):
    best_move, best_score = None, -math.inf
    mills = [
        [1, 2, 3], [1, 7, 14],
        [4, 5, 6], [4, 8, 11],
        [6, 9, 13], [11, 12, 13],
        [3, 10, 16], [14, 15, 16]
    ]
    
    # Check if the AI has any pieces on the board
    ai_pieces = [i + 1 for i, pos in enumerate(board) if pos == player + str(i + 1)]

    # Function to check for AI mills on the board
    def check_ai_mills(board, player):
        ai_mills = []
        for mill in mills:
            if all(board[pos - 1] == player + str(pos) for pos in mill):
                ai_mills.append(mill)
        return ai_mills

    ai_mills = check_ai_mills(board, player)

    if ai_mills:
        # If AI has mills, move a piece from one of the mills
        for mill in ai_mills:
            for piece_pos in mill:
                if board[piece_pos - 1] == player + str(piece_pos):
                    for destination in valid_moves[piece_pos]:
                        if is_valid_move_p2(board, destination, piece_pos):
                            old_position_ai = board[piece_pos - 1]
                            board[piece_pos - 1] = str(piece_pos)
                            board[destination - 1] = player + str(destination)
                            score = evaluate_move(board, piece_pos, destination, player, opponent)
                            board[piece_pos - 1] = old_position_ai
                            board[destination - 1] = str(destination)
                            if score > best_score:
                                best_score = score
                                best_move = (piece_pos, destination)
                            break  # Move only one piece from the mill

    # If no mill move was possible, move any other piece
    if best_move is None and ai_pieces:
        for piece_pos in ai_pieces:
            for destination in valid_moves[piece_pos]:
                if is_valid_move_p2(board, destination, piece_pos):
                    old_position_ai = board[piece_pos - 1]
                    board[piece_pos - 1] = str(piece_pos)
                    board[destination - 1] = player + str(destination)
                    score = evaluate_move(board, piece_pos, destination, player, opponent)
                    board[piece_pos - 1] = old_position_ai
                    board[destination - 1] = str(destination)
                    if score > best_score:
                        best_score = score
                        best_move = (piece_pos, destination)

    if best_move:
        old_position_ai, new_position_ai = board[best_move[0] - 1], player + str(best_move[1])
        board[best_move[0] - 1] = str(best_move[0])
        board[best_move[1] - 1] = new_position_ai
        print(f"{player} moves {old_position_ai} to {best_move[1]}")
    else:
        print(f"No valid move for {player}")

    return best_move


def evaluate_move(board, piece_pos, destination, player, opponent):
    mills = [
        [1, 2, 3], [1, 7, 14],
        [4, 5, 6], [4, 8, 11],
        [6, 9, 13], [11, 12, 13],
        [3, 10, 16], [14, 15, 16]
    ]
    old_position_ai = board[piece_pos - 1]
    board[piece_pos - 1] = str(piece_pos)
    board[destination - 1] = player + str(destination)
    score = 0

    # Check if the move forms a mill
    for mill in mills:
        if destination in mill and all(board[pos - 1] == player + str(pos) for pos in mill):
            score += 100

    # Check if the move blocks opponent's mill
    for mill in mills:
        if destination in mill and any(board[pos - 1] == opponent + str(pos) for pos in mill):
            score += 50

    # Check if the move contributes to potential mills
    for mill in mills:
        if destination in mill and sum(board[pos - 1] == player + str(pos) for pos in mill) == 1:
            score += 10

    # Check if the move breaks opponent's potential mill
    for mill in mills:
        if destination in mill and sum(board[pos - 1] == opponent + str(pos) for pos in mill) == 2:
            score += 20




    # Additional evaluation based on position
    if destination in [1, 3, 5, 7, 9, 11, 13, 15]:
        score += 5
    elif destination in [2, 4, 6, 8, 10, 12, 14, 16]:
        score += 3

    board[piece_pos - 1] = old_position_ai
    board[destination - 1] = str(destination)
    return score





   

def coin_toss():
    frames = ["  ___   ", " /   \\  ", "|  O  | ", " \\___/  "]
    tosses = random.randint(6, 12)

    print("Flipping the coin...")
    for _ in range(tosses):
        for frame in frames:
            sys.stdout.write("\r" + frame)
            sys.stdout.flush()
            time.sleep(0.1)

    return random.choice([0, 1])

def play_game():
    board = [str(i) for i in range(1, 17)]
    draw_board(board)

    toss = coin_toss()
    if toss == 0:
        player1 = "H"
        player2 = "A"
        print("Player 1 (Human) goes first!")
    else:
        player1 = "A"
        player2 = "H"
        print("Player 1 (AI) goes first!")

    used_mills = {"H": set(), "A": set()}

    # Phase 1: Placing pieces
    for _ in range(12):
        if player1 == "H":
            move = player_move(board, player1)
        else:
            move = ai_move(board, player1, player2)
            print(f"{player1} chooses position {move}")
        board[move - 1] = player1 + str(move)
        draw_board(board)
        player1, player2 = player2, player1

    # Phase 2: Movement
    while True:
        if player1 == "H":
            print("\nHuman's turn:")
            piece_to_move, destination = player_move_p2(board, player1)
        else:
            print("\nAI's turn:")
            piece_to_move, destination = ai_move_p2(board, player1, player2)
        
        print(f"{player1} moves piece {piece_to_move} to {destination}")
        
        draw_board(board)
        
        mill = check_mill(board, destination, player1)
        if mill:
            cur_mill = mill
            print(f"{player1} formed a mill with positions: {mill}")
            handle_mill_capture(board, player1, player2, cur_mill, used_mills)
            draw_board(board)
            
        if check_win(board, player1):
            print(f"{player2} wins!")
            break




        player1, player2 = player2, player1

        


if __name__ == "__main__":
   play_game()    
            