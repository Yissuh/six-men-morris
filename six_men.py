import pygame
import sys

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

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("6 Men's Morris")

# Board positions
positions = [(75, 75), (300, 75), (525, 75), (180, 180), (300, 180), (420, 180),
             (75, 300), (180, 300), (420, 300), (525, 300), (180, 420), (300, 420),
             (420, 420), (75, 525), (300, 525), (525, 525)]

# Initialize game variables
player1_pieces = 6
player2_pieces = 6
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
    # Check diagonals
    if piece_index in [0, 4, 8] and board_state[0] == board_state[4] == board_state[8] == current_player:
        return True
    if piece_index in [2, 4, 6] and board_state[2] == board_state[4] == board_state[6] == current_player:
        return True
    return False

# Capture opponent's piece
def capture_piece(player):
    global player1_pieces, player2_pieces
    opponent = 1 if player == 2 else 2
    captured = False
    for i in range(16):
        if board_state[i] == opponent and not check_mill(i):
            board_state[i] = 0
            if opponent == 1:
                player1_pieces -= 1
            else:
                player2_pieces -= 1
            captured = True
            break
    if not captured:
        for i in range(16):
            if board_state[i] == opponent:
                board_state[i] = 0
                if opponent == 1:
                    player1_pieces -= 1
                else:
                    player2_pieces -= 1
                break

# Helper function to get valid moves for a piece
def get_valid_moves(piece_index):
    valid_moves = []
    row = piece_index // 3
    col = piece_index % 3

    # Check horizontal and vertical moves
    if row > 0:
        valid_moves.append(piece_index - 3)  # Up
    if row < 2:
        valid_moves.append(piece_index + 3)  # Down
    if col > 0:
        valid_moves.append(piece_index - 1)  # Left
    if col < 2:
        valid_moves.append(piece_index + 1)  # Right

    # Check diagonal moves
    if row == 1 and col == 1:
        valid_moves.extend([0, 2, 6, 8])
    elif row == 0 and col == 0:
        valid_moves.append(4)
    elif row == 0 and col == 2:
        valid_moves.append(4)
    elif row == 2 and col == 0:
        valid_moves.append(4)
    elif row == 2 and col == 2:
        valid_moves.append(4)

    # Remove invalid moves (occupied positions or out of bounds)
    valid_moves = [move for move in valid_moves if 0 <= move < 16 and board_state[move] == 0]

    return valid_moves

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
            # Phase 1: Placing phase
            if phase == 1:
                if current_player == 1 and player1_pieces > 0:
                    color = RED
                elif current_player == 2 and player2_pieces > 0:
                    color = BLUE
                else:
                    continue

                for i, pos in enumerate(positions):
                    if pos[0] - RADIUS <= event.pos[0] <= pos[0] + RADIUS and pos[1] - RADIUS <= event.pos[1] <= pos[1] + RADIUS:
                        if board_state[i] == 0:
                            board_state[i] = current_player
                            if current_player == 1:
                                player1_pieces -= 1
                            else:
                                player2_pieces -= 1

                            if check_mill(i):
                                capture_piece(current_player)

                            current_player = 3 - current_player  # Switch players
                            break

                if player1_pieces == 0 and player2_pieces == 0:
                    phase = 2  # Move to moving phase

            # Phase 2: Moving phase
            elif phase == 2:
                if current_player == 1:
                    color = RED
                else:
                    color = BLUE

                for i, pos in enumerate(positions):
                    if pos[0] - RADIUS <= event.pos[0] <= pos[0] + RADIUS and pos[1] - RADIUS <= event.pos[1] <=pos[1] + RADIUS:
                        if board_state[i] == current_player:
                            selected_piece = i
                            break

                if selected_piece is not None:
                    for i, pos in enumerate(positions):
                        if pos[0] - RADIUS <= event.pos[0] <= pos[0] + RADIUS and pos[1] - RADIUS <= event.pos[1] <= pos[1] + RADIUS:
                            if i in get_valid_moves(selected_piece):
                                old_piece = selected_piece
                                board_state[selected_piece] = 0
                                board_state[i] = current_player

                                if check_mill(i):
                                    capture_piece(current_player)

                                selected_piece = None
                                current_player = 3 - current_player  # Switch players
                                break
                            else:
                                # Handle invalid position click
                                selected_piece = None

            if check_win():
                print(f"Player {3 - current_player} wins!")
                running = False

    # Update the display
    draw_board()
    draw_pieces()
    pygame.display.flip()