from chessEngine import State, Move
from chessEnums import PieceName, PieceColor
from abc import ABC, abstractclassmethod
import random

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
            [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
            [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
            [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
            [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
            [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
            [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
            [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
            [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {(PieceColor.WHITE, PieceName.KNIGHT): knight_scores,
                         (PieceColor.BLACK, PieceName.KNIGHT): knight_scores[::-1],
                         (PieceColor.WHITE, PieceName.BISHOP): bishop_scores,
                         (PieceColor.BLACK, PieceName.BISHOP): bishop_scores[::-1],
                         (PieceColor.WHITE, PieceName.QUEEN): queen_scores,
                         (PieceColor.BLACK, PieceName.QUEEN): queen_scores[::-1],
                         (PieceColor.WHITE, PieceName.ROOK): rook_scores,
                         (PieceColor.BLACK, PieceName.ROOK): rook_scores[::-1],
                         (PieceColor.WHITE, PieceName.PAWN): pawn_scores,
                         (PieceColor.BLACK, PieceName.PAWN): pawn_scores[::-1]}

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
        for row in range(len(board.board)):
            for col in range(row):
                piece_color = board.get_piece_color(row, col)
                if piece_color != None:
                    if piece_color == PieceColor.WHITE:
                        score += self.piece_score[board.get_piece_name(row, col).value]
                    elif board.get_piece_color(row, col) == PieceColor.BLACK:
                        score += self.piece_score[board.get_piece_name(row, col).value]
        return score
    
class TestHeuristic(Heuristic):
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
        Score the board. A positive score is good for white, a negative score is good for black.
        """
        score = 0
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.get_piece_name(row, col)
                piece_color = board.get_piece_color(row, col)
                if piece == None or piece_color == None:
                    continue
                piece_position_score = 0
                if piece != PieceName.KING:
                    piece_position_key = (piece_color, piece)
                    piece_position_score = piece_position_scores[piece_position_key][row][col]
                if piece == PieceColor.WHITE:
                    score += self.piece_score[piece] + piece_position_score
                if piece == PieceColor.BLACK:
                    score -= self.piece_score[piece] + piece_position_score

        return score
# def findRandomMove(valid_moves):
#     """
#     Picks and returns a random valid move.
#     """
#     return random.choice(valid_moves)

class RandomHeuristic(Heuristic):
    def __init__(self) -> None:
        super().__init__()
    
    def evaluate(self, board: State) -> float:
        return random.randint(-100, 100)
