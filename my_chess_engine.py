import chess
import sys
import pygame
import time
import math

# square table
PST = [ # pawn
        [ 0,   0,   0,   0,   0,   0,   0,   0, 
        30,  30,  30,  40,  40,  30,  30,  30,
        20,  20,  20,  30,  30,  30,  20,  20,
        10,  10,  15,  25,  25,  15,  10,  10,
        5,   5,   5,  20,  20,   5,   5,   5,
        5,   0,   0,   5,   5,   0,   0,   5,
        5,   5,   5, -10, -10,   5,   5,   5,
        0,   0,   0,   0,   0,   0,   0,   0],
        # kinght
        [-5,  -5, -5, -5, -5, -5,  -5, -5,
        -5,   0,  0, 10, 10,  0,   0, -5,
        -5,   5, 10, 10, 10, 10,   5, -5,
        -5,   5, 10, 15, 15, 10,   5, -5,
        -5,   5, 10, 15, 15, 10,   5, -5,
        -5,   5, 10, 10, 10, 10,   5, -5,
        -5,   0,  0,  5,  5,  0,   0, -5,
        -5, -10, -5, -5, -5, -5, -10, -5],
        # bishop
        [0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,  10,   0,   0,   0,   0,  10,   0,
        5,   0,  10,   0,   0,  10,   0,   5,
        0,  10,   0,  10,  10,   0,  10,   0,
        0,  10,   0,  10,  10,   0,  10,   0,
        0,   0, -10,   0,   0, -10,   0,   0],
        # rook
        [10,  10,  10,  10,  10,  10,  10,  10,
        10,  10,  10,  10,  10,  10,  10,  10,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,
        0,   0,   0,  10,  10,   0,   0,   0,
        0,   0,   0,  10,  10,   5,   0,   0],
        # queen
        [-20, -10, -10, -5, -5, -10, -10, -20,
        -10,   0,   0,  0,  0,   0,   0, -10,
        -10,   0,   5,  5,  5,   5,   0, -10,
        -5,   0,   5,  5,  5,   5,   0,  -5,
        -5,   0,   5,  5,  5,   5,   0,  -5,
        -10,   5,   5,  5,  5,   5,   0, -10,
        -10,   0,   5,  0,  0,   0,   0, -10,
        -20, -10, -10,  0,  0, -10, -10, -20],
        # king
        [0, 0,  0,  0,   0,  0,  0, 0,
        0, 0,  0,  0,   0,  0,  0, 0,
        0, 0,  0,  0,   0,  0,  0, 0,
        0, 0,  0,  0,   0,  0,  0, 0,
        0, 0,  0,  0,   0,  0,  0, 0,
        0, 0,  0,  0,   0,  0,  0, 0,
        0, 0,  0, -5,  -5, -5,  0, 0,
        0, 0, 10, -5,  -5, -5, 10, 0]]

# constants for the board
PIECES = {
    chess.PAWN : 100,
    chess.KNIGHT : 320,
    chess.BISHOP : 330,
    chess.ROOK : 500,
    chess.QUEEN : 900,
    chess.KING : 60000
}
WIDTH = HEIGHT = 640
SQ_SIZE = WIDTH//8
FPS = 15

# Colors for the squares
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)

# Global dictionary to store images
IMAGES = {}


def move_order_score(board, move):
    victim = board.piece_at(move.to_square)
    if victim == None:
        return 0
    return PIECES[victim.piece_type]


def evaluate_board(board):
    score = 0.0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece == None: continue

        if piece.color == chess.WHITE:
            score += PIECES[piece.piece_type]
            r, c = square // 8, square % 8
            r = 7-r
            score += PST[piece.piece_type-1][r*8 + c]
        else :
            score -= PIECES[piece.piece_type]
            score -= PST[piece.piece_type-1][square]
    return score


def minimax(board, depth, alpha, beta, maximizing_player):
    if board.is_game_over() or depth == 0:
        return evaluate_board(board)
    
    legal_moves = list(board.legal_moves)
    legal_moves.sort(key = lambda x : move_order_score(board, x), reverse=True)

    if maximizing_player:
        for move in legal_moves:
            board.push(move)
            val = minimax(board, depth-1, alpha, beta, not maximizing_player)
            if val > alpha :
                alpha = val
            if val >= beta:
                board.pop()
                return val
            board.pop()
        return alpha
    
    else :
        for move in legal_moves:
            board.push(move)
            val = minimax(board, depth-1, alpha, beta, not maximizing_player)
            if val < beta :
                beta = val
            if val <= alpha :
                board.pop()
                return val
            board.pop()
        return beta


def get_best_move(board, depth): # assuming there is a valid move to make before game over
    best_move = None
    if board.turn: # its white's turn
        max_val = -math.inf
        for move in board.legal_moves:
            board.push(move)
            val = minimax(board, depth, -math.inf, math.inf, False)
            if val > max_val:
                max_val = val
                best_move = move
            board.pop()
    else : # its black's turn
        min_val = math.inf
        for move in board.legal_moves:
            board.push(move)
            val = minimax(board, depth, -math.inf, math.inf, True)
            if val < min_val:
                min_val = val
                best_move = move
            board.pop()
    return best_move


def get_square_from_mouse(pos, flip_board):
    """
    Convert the mouse position (x, y) to a chess square index.
    """
    x, y = pos
    file = x // SQ_SIZE
    rank = 7 - (y // SQ_SIZE)
    if flip_board:
        file = 7 - file
        rank = 7 - rank
    return chess.square(file, rank)


def draw_board(screen, flip_board, selected_sq):
    """
    Draw the chess board with optional highlight for the selected square.
    """
    for rank in range(8):
        for file in range(8):
            # Adjust square positions if board is flipped.
            draw_file = file if not flip_board else 7 - file
            draw_rank = rank if not flip_board else 7 - rank

            x = draw_file * SQ_SIZE
            # Pygame's (0,0) is top-left; we draw from bottom (rank 0 at bottom)
            y = (7 - draw_rank) * SQ_SIZE

            color = LIGHT_COLOR if (file + rank) % 2 == 0 else DARK_COLOR
            rect = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect)

            # Highlight the selected square if applicable.
            if selected_sq is not None:
                sel_file = chess.square_file(selected_sq)
                sel_rank = chess.square_rank(selected_sq)
                if sel_file == draw_file and sel_rank == draw_rank:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 4)
                # Compare with current square coordinates.
                if sel_file == file and sel_rank == rank:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 4)


def draw_pieces(screen, board, flip_board):
    """
    Draw all pieces on the board based on the current board state.
    """
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            if flip_board:
                file = 7 - file
                rank = 7 - rank
            x = file * SQ_SIZE
            y = (7 - rank) * SQ_SIZE
            symbol = piece.symbol()  # Uppercase for white, lowercase for black.
            screen.blit(IMAGES[symbol], pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))


def load_images():
    """
    Load chess piece images from the images folder.
    The mapping from piece symbol to image file is as follows:
      White Pieces:
         'P' -> white-pawn.png
         'N' -> white-knight.png
         'B' -> white-bishop.png
         'R' -> white-rook.png
         'Q' -> white-queen.png
         'K' -> white-king.png
      Black Pieces:
         'p' -> black-pawn.png
         'n' -> black-knight.png
         'b' -> black-bishop.png
         'r' -> black-rook.png
         'q' -> black-queen.png
         'k' -> black-king.png
    """
    pieces = {
        "P": "white-pawn.png",
        "N": "white-knight.png",
        "B": "white-bishop.png",
        "R": "white-rook.png",
        "Q": "white-queen.png",
        "K": "white-king.png",
        "p": "black-pawn.png",
        "n": "black-knight.png",
        "b": "black-bishop.png",
        "r": "black-rook.png",
        "q": "black-queen.png",
        "k": "black-king.png"
    }
    for symbol, filename in pieces.items():
        path = "images/" + filename
        try:
            image = pygame.image.load(path)
        except pygame.error as e:
            print(f"Unable to load image at path: {path}")
            raise e
        IMAGES[symbol] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game: Human vs. AI")
    clock = pygame.time.Clock()
    load_images()
    depth = 3

    board = chess.Board()

    player_color = input("Choose your color (white/black) : ").strip().lower()
    if player_color not in ['white', 'black']:
        print("Invalid Choice! Defaulting to white.")
        player_color = "white"
    human_is_white = (player_color == "white")
    flip_board = not human_is_white # fliping board for human

    selected_sq = None 

    running = True
    while running:
        human_turn = (board.turn == chess.WHITE and human_is_white) or (board.turn == chess.BLACK and not human_is_white)

        if human_turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    sq = get_square_from_mouse(pos, flip_board)
                    if selected_sq is None: # No square selected, select if valid
                        piece = board.piece_at(sq)
                        if piece and ((piece.color == chess.WHITE and human_is_white) or 
                                      (piece.color == chess.BLACK and not human_is_white)):
                            selected_sq = sq
                    else:
                        # re-selecting new piece if a piece of human color on this place
                        piece = board.piece_at(sq)
                        if piece and ((piece.color == chess.WHITE and human_is_white) or (piece.color == chess.BLACK and not human_is_white)):
                            selected_sq = sq
                            continue

                        # performing move based on the selected empty square
                        piece = board.piece_at(selected_sq)
                        to_rank = chess.square_rank(sq)
                        move = None
                        if piece and piece.piece_type == chess.PAWN and to_rank in (0, 7):
                            move = chess.Move(selected_sq, sq, promotion=chess.QUEEN)
                        else:
                            move = chess.Move(selected_sq, sq)
                        if move in board.legal_moves:
                            board.push(move)
                            print("Human played :", move.uci())
                        else :
                            print("Illegal Move, try again.")
                        selected_sq = None
        
        else :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit(0)
            ai_move = get_best_move(board, depth=depth)
            board.push(ai_move)
            print("AI played :", ai_move.uci())
        
        # redraw
        draw_board(screen, flip_board, selected_sq)
        draw_pieces(screen, board, flip_board)
        pygame.display.flip()

        # Check if the game is over.
        if board.is_game_over():
            print("Game over. Result:", board.result())
            time.sleep(3)
            running = False

        clock.tick(FPS)


if __name__ == "__main__":
    main()