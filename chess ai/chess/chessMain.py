"""User input and displaying current state of all pieces"""

import pygame as p
import chessEngine

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
        IMAGES[piece] = p.transform.scale(p.image.load('chessPieces/' + piece + '.png'), (SQUARE, SQUARE))
                                         

def main():
    p.init()     
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = chessEngine.state()
    loadingPieces()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawChessGameState(screen)
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawChessGameState(screen):
    drawChessBoard(screen)
    drawChessPieces(screen, chessEngine.state().board)
    
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

    
    
            
                  
if __name__ == "__main__":
    main()
