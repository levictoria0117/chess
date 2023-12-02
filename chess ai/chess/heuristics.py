from chessEngine import State
from chessEnums import PieceName, PieceColor
from abc import ABC, abstractclassmethod

# abstract base class
class Heuristic(ABC):
    @abstractclassmethod
    def evaluate(self, board: State) -> float:
        ...

class ScoreMaterial(Heuristic):
    def __init__(self, piece_score: dict[str, float] = {
        PieceName.KING.value: 0.0,
        PieceName.QUEEN.value: 10.0,
        PieceName.ROOK.value: 5.0,
        PieceName.BISHOP.value: 3.0,
        PieceName.KNIGHT.value: 3.0,
        PieceName.PAWN.value: 1.0
    }) -> None:
        super().__init__()
        self.piece_score = piece_score


    def evaluate(self, board: State) -> float:
        """
        Score based on board material

        what is good for white is bad for black and vise versa
        if White has material advantage then the score will be positive
        if black has material advantage then the score will be negative
        if perfectly even game score will equal 0
        """
        score = 0.0
        for row in board.board:
            for square in row:
                if State.get_piece_color(row, square) == PieceColor.WHITE:
                    score += self.piece_score[board.get_piece_name(row, square).value]
                elif State.get_piece_color(row, square) == PieceColor.BLACK:
                    score += self.piece_score[board.get_piece_name(row, square).value]
        return score