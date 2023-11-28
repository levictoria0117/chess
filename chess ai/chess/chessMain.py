"""User input and displaying current state of all pieces"""

import pygame as p
from Chess import ChessEngine

WIDTH = 600
HEIGHT = 600
DIMENSIONS = 8
SQUARE = HEIGHT//DIMENSIONS
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
    gameState = ChessEngine.GameState()
    loadingPieces()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawChessGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    
def drawChessBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r1 in range[DIMENSIONS]:
        for r2 in range[DIMENSIONS]:
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(r2*SQUARE, r1*SQUARE, SQUARE, SQUARE))
            
        
    
#def drawChessPieces(screen, gs):
    
    
    
            
                  
if __name__ == "__main__":
    main()
