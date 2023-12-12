"""User input and displaying current state of all pieces"""

import pygame as p
import chessEngine
from chessEnums import PieceColor
from ai import MiniMaxAlphaBeta, AI
from heuristics import Heuristic, ScoreMaterial

WIDTH = 600
HEIGHT = 600
DIMENSIONS = 8
SQUARE = HEIGHT/DIMENSIONS
MAX_FPS = 15
IMAGES = {}

def loadingPieces():
    pieces = ["b_pawn", "b_rook", "b_knight", "b_bishop", "b_queen", "b_king", 
              "w_pawn", "w_rook", "w_knight", "w_bishop", "w_queen", "w_king"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('./chessPieces/' + piece + '.png'), (SQUARE, SQUARE))
                                         
def ask_user_name(screen):
    font = p.font.Font(None, 32)
    input_box = p.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 20, 200, 40)
    color_inactive = p.Color('lightskyblue3')
    color_active = p.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                done = True
                return None
            if event.type == p.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == p.KEYDOWN:
                if active:
                    if event.key == p.K_RETURN:
                        done = True
                    elif event.key == p.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        p.draw.rect(screen, color, input_box, 2)

        p.display.flip()

    return text


def drawChessGameState(screen, gameState, user_name):
    drawChessBoard(screen)
    drawChessPieces(screen, gameState.board)
    if user_name:
        font = p.font.SysFont(None, 30)
        text_surface = font.render(f"Player: {user_name}", True, p.Color('Black'))
        screen.blit(text_surface, (5, 5))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess Game")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = chessEngine.State()
    #validMove = gameState.getValidMoves()
    moveMade = False #flag variable for a move is made
    loadingPieces()
    user_name = ask_user_name(screen)  # Get user name
    user_color = PieceColor.BLACK
    ai_color = PieceColor.WHITE if user_color == PieceColor.BLACK else PieceColor.BLACK
    heuristic: Heuristic = ScoreMaterial()
    ai: AI = MiniMaxAlphaBeta(ai_color, depth=2, heuristic_func=heuristic)

    if user_name is None:
        return  # Exit if the user closed the window
    running = True
    sqSelected = ()# no square is selected , keep track of the last click of the user(tuple:(row:col))
    playerClick = [] #keep track of player clicks (two tuples:[(6,4),(4,4)])
    while running:
        has_user_moved = False
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            # user turn
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0] // SQUARE
                row = location[1] //SQUARE
                if sqSelected == (row,col):#the user clicked the same square
                    sqSelected = () #dselect
                    playerClick = [] #clear player clicks
                else:
                    # if (gameState.get_piece_color(int(row), int(col)) == user_color):
                    print(int(row), int(col))
                    sqSelected = (int(row),int(col))
                    playerClick.append(sqSelected)
                if len(playerClick) == 2:#after 2nd click
                    move = chessEngine.Move(playerClick[0],playerClick[1],gameState.board)
                    print(move.getChessNotation())
                    has_user_moved = gameState.onMove(move, user_color)
                    sqSelected = () #reset user click
                    playerClick = []

            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:#undo when "z" is pressed
                    gameState.undoMove()
                    moveMade = True

        # ai turn
        # if has_user_moved:
        #     ai.move(gameState)

        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
        drawChessGameState(screen, gameState, user_name)  # Pass the user name here
        clock.tick(MAX_FPS)
        p.display.flip()



    
def drawChessBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))
            
def drawChessPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE)) 

                  
if __name__ == "__main__":
    main()

