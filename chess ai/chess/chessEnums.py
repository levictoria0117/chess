from enum import Enum

class PieceName(Enum):
    QUEEN = "queen"
    KING = "king"
    KNIGHT = "knight"
    ROOK = "rook"
    PAWN = "pawn"
    BISHOP = "bishop"

class PieceColor(Enum):
    BLACK = "black"
    WHITE = "white"