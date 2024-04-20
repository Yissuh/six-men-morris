import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RADIUS = 20
PADDING = 30
FPS = 60
DEPTH = 3

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("6 Men's Morris")

# Board positions
positions = [(75, 75), (300, 75), (525, 75), (180, 180), (300, 180), (420, 180),
             (75, 300), (180, 300), (420, 300), (525, 300), (180, 420), (300, 420),
             (420, 420), (75, 525), (300, 525), (525, 525)]

# Initialize game variables
player1_pieces = 6
player2_pieces = 6  # AI player
current_player = 1
selected_piece = None
board_state = [0] * 16  # 0 represents an empty position, 1 represents player 1's piece, 2 represents player 2's piece
phase = 1  # 1: Placing phase, 2: Moving phase


# Draw the board
def draw_board():
    screen.fill(WHITE)
    rect1 = pygame.Rect(75, 75, 450, 450)
    pygame.draw.rect(screen, BLACK, rect1, 2)
    rect2 = pygame.Rect(180, 180, 240, 240)
    line_pairs = [(1, 4), (6, 7), (8, 9), (11, 14)]  # Assuming indices start from 0
    for start_index, end_index in line_pairs:
        start_pos = positions[start_index]
        end_pos = positions[end_index]
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)
    pygame.draw.rect(screen, BLACK, rect2, 2)
    for pos in positions:
        pygame.draw.circle(screen, BLACK, pos, RADIUS, 1)


# Draw player pieces
def draw_pieces():
    for i, state in enumerate(board_state):
        if state == 1:
            pygame.draw.circle(screen, RED, positions[i], RADIUS)
        elif state == 2:
            pygame.draw.circle(screen, BLUE, positions[i], RADIUS)


# Check for winning condition
def check_win():
    # Check if either player has 2 pieces remaining
    if player1_pieces == 2 or player2_pieces == 2:
        # Check if the player with 2 pieces can form a mill or make a capture
        can_form_mill = False
        can_capture = False
        for i in range(16):
            if board_state[i] == (2 if player1_pieces == 2 else 1):
                if check_mill(i):
                    can_form_mill = True
                    break
                for j in range(16):
                    if board_state[j] == (1 if player1_pieces == 2 else 2) and not check_mill(j):
                        can_capture = True
                        break
                if can_capture:
                    break
        
        # If the player with 2 pieces cannot form a mill or make a capture, they lose
        if not can_form_mill and not can_capture:
            return True
    
    return False


# Check for mill formation
def check_mill(piece_index):
    row = piece_index // 3
    col = piece_index % 3
    
    # Check row
    if 0 <= row * 3 < 16 and 0 <= row * 3 + 1 < 16 and 0 <= row * 3 + 2 < 16:
        if board_state[row * 3] == board_state[row * 3 + 1] == board_state[row * 3 + 2] == current_player:
            return True
    
    # Check column
    if 0 <= col < 16 and 0 <= col + 3 < 16 and 0 <= col + 6 < 16:
        if board_state[col] == board_state[col + 3] == board_state[col + 6] == current_player:
            return True
    
    return False



def capture_piece(player):
    global player1_pieces, player2_pieces
    opponent = 1 if player == 2 else 2
    for i in range(16):
        if board_state[i] == opponent and not check_mill(i):
            board_state[i] = 0
            if opponent == 1:
                player1_pieces -= 1
            else:
                player2_pieces -= 1
            return  # Exit the function after capturing a piece not in a mill
    # If no pieces were captured, remove any piece of the opponent
    for i in range(16):
        if board_state[i] == opponent:
            board_state[i] = 0
            if opponent == 1:
                player1_pieces -= 1
            else:
                player2_pieces -= 1
            return



def get_valid_moves(piece_index):
    valid_moves = []
    row = piece_index // 3  # Assuming 3 positions per row

    if row > 0 and board_state[piece_index - 3] == 0:  # Up
        valid_moves.append(piece_index - 3)
    if row < 2 and board_state[piece_index + 3] == 0:  # Down
        valid_moves.append(piece_index + 3)
    if piece_index % 3 != 0 and board_state[piece_index - 1] == 0:  # Left
        valid_moves.append(piece_index - 1)
    if (piece_index + 1) % 3 != 0 and board_state[piece_index + 1] == 0:  # Right
        valid_moves.append(piece_index + 1)  # Append result of the last if statement
    
    print(f"Valid moves for piece at index {piece_index}: {valid_moves}")
    return valid_moves






def draw_valid_moves(piece_index):
    valid_moves = get_valid_moves(piece_index)
    for move in valid_moves:
        pygame.draw.circle(screen, GREEN, positions[move], RADIUS // 2)
        pygame.display.flip()




# Define the Minimax function with Alpha-Beta Pruning
def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or check_win():  # Terminal state or maximum depth reached
        return evaluate(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval

# Modify the ai_move() function to use Minimax
def ai_move():
    global board_state, player2_pieces
    best_score = float('-inf')
    best_move = None
    for move in get_possible_moves(board_state):
        new_board = make_move(board_state, move)
        if check_mill(move):  # Check if forming a mill
            capture_piece(2)  # If so, capture opponent's piece
            player2_pieces -= 1
        score = minimax(new_board, DEPTH, False, float('-inf'), float('inf'))  # Use DEPTH constant here
        if score > best_score:
            best_score = score
            best_move = move
    # Make the best move
    board_state = make_move(board_state, best_move)
    player2_pieces -= 1


# Define evaluation function (a simple one for demonstration)
def evaluate(board):
    # Evaluate the board state based on number of pieces, mills, etc.
    # Return a score indicating desirability for the AI
    ai_pieces = count_pieces(board, 2)
    human_pieces = count_pieces(board, 1)
    ai_mills = count_mills(board, 2)
    human_mills = count_mills(board, 1)
    score = (ai_pieces - human_pieces) + (ai_mills - human_mills) * 10
    return score

# Define helper functions (make_move(), get_possible_moves(), count_pieces(), count_mills(), and check_win())

def make_move(board, move):
    new_board = board.copy()
    new_board[move] = 2  # Assuming AI player is always 2
    return new_board

def get_possible_moves(board):
    return [move for move in range(16) if board[move] == 0]

def count_pieces(board, player):
    return sum(1 for piece in board if piece == player)

def count_mills(board, player):
    mills = 0
    for i in range(16):
        if board[i] == player and check_mill(i):
            mills += 1
    return mills

def check_win():
    global current_player, board_state, phase

    # Placement Phase
    if phase == 1:
        # Check for a mill formation during placement
        for i in range(3):
            if (board_state[i] == board_state[i + 3] == board_state[i + 6] == current_player) or \
               (board_state[i * 3] == board_state[i * 3 + 1] == board_state[i * 3 + 2] == current_player):
                return True
    
    # Movement Phase
    elif phase == 2:
        # Check if the current player reduced the opponent to 2 pieces
        if current_player == 1:
            if player2_pieces == 2:
                return True
        else:
            if player1_pieces == 2:
                return True

        # Check if the opponent cannot make a legal move
        if current_player == 1:
            for i in range(16):
                if board_state[i] == 2:
                    if get_valid_moves(i):
                        return False
            return True
        else:
            for i in range(16):
                if board_state[i] == 1:
                    if get_valid_moves(i):
                        return False
            return True

    return False







# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if phase == 1:
                if current_player == 1 and player1_pieces > 0:
                    color = RED
                    for i, pos in enumerate(positions):
                        if pos[0] - RADIUS <= event.pos[0] <= pos[0] + RADIUS and pos[1] - RADIUS <= event.pos[1] <= pos[1] + RADIUS:
                            if board_state[i] == 0:
                                board_state[i] = current_player
                                player1_pieces -= 1
                                current_player = 3 - current_player  # Switch players

                                # Check if placing phase is over
                                if player1_pieces == 0:
                                    current_player = 2  # Switch to AI player
                                    phase = 2  # Transition to moving phase
                                break

                elif current_player == 2 and player2_pieces > 0:  # AI player's turn
                    for i in range(len(board_state)):
                        if board_state[i] == 0:
                            board_state[i] = current_player
                            player2_pieces -= 1
                            current_player = 3 - current_player  # Switch players

                            # Check if placing phase is over
                            if player2_pieces == 0:
                                current_player = 1  # Switch to human player
                                phase = 2  # Transition to moving phase
                            break

            # Movement Phase
            elif phase == 2:
                if current_player == 1:  # Human player's turn in moving phase
                    clicked_position = pygame.mouse.get_pos()
                    for i, pos in enumerate(positions):
                        if pos[0] - RADIUS <= clicked_position[0] <= pos[0] + RADIUS and pos[1] - RADIUS <= clicked_position[1] <= pos[1] + RADIUS:
                            if board_state[i] == current_player:
                                if selected_piece is None:
                                    selected_piece = i
                                else:
                                    if i in get_valid_moves(selected_piece):
                                        # Valid move
                                        board_state[selected_piece] = 0
                                        board_state[i] = current_player
                                        if check_mill(i):
                                            phase = 3  # Transition to capturing phase
                                        else:
                                            current_player = 3 - current_player  # Switch players
                                        selected_piece = None  # Reset selected piece
                                    else:
                                        # Invalid move, provide feedback to the player
                                        print("Invalid move. Please select a valid position.")
                            break
                else:  # AI player's turn
                    ai_move()
                    current_player = 3 - current_player  # Switch back to human player



            elif phase == 3:
                for i, pos in enumerate(positions):
                    if pos[0] - RADIUS <= event.pos[0] <= pos[0] + RADIUS and pos[1] - RADIUS <= event.pos[1] <= pos[1] + RADIUS:
                        if current_player == 1:  # Human player turn
                            if board_state[i] == 3 - current_player:  # Capture opponent's piece
                                board_state[i] = 0
                                player2_pieces -= 1  # Assuming AI player is always 2
                                current_player = 3 - current_player  # Switch players
                                phase = 2  # Transition back to moving phase
                        break



    # Update the display
    draw_board()
    draw_pieces()
    pygame.display.flip()



