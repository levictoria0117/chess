from abc import ABC, abstractclassmethod
from typing import Callable
from chessEnums import PieceColor
from chessEngine import State

class AI(ABC):
    def __init__(self, team: PieceColor):
        self.team = team
    @abstractclassmethod
    def move(self, board: State) -> bool:
        """
        returns True and makes move found else False and no move made

        :param board: object of State that holds the board that contains current board State
        :return: True if move found else False
        """
        ...

class MiniMaxAlphaBeta(AI):
    def __init__(self, team: PieceColor, depth: int, heuristic_func: Callable[..., float]):
        super().__init__(team)
        self.depth = depth
        self.heuristic_func = heuristic_func
    
    def move(self, board: State):
        best_move = self.minimax(board)
        if best_move is None:
            name = board.get_piece_name(best_move)
            board.makeMove(best_move)


    def minimax(self, board: State) -> str:
        """
        :param: board object with current board State
        :return: the best move found as a string
        """
        pass

    def min_value(self, board: State, depth: int, team: PieceColor, alpha: int, beta: int) -> tuple[float, str | None]:
        """
        :param board: State object representing representing a chess board State
        :param depth: minimax depth
        :param team: teaming being evaluated black | white
        :param alpha: alpha-beta pruning, alpha, for minimax algorithm 
        :param beta: alpha-beta pruning, beta, for minimax algorithm
        :return: return tuple (float value of the State evaluation of board, best move string)
        """
        pass

    def max_value(self, board: State, depth: int, team: PieceColor, alpha: int, beta: int) -> tuple[float, str | None]:
        """
        :param board: State object representing representing a chess board State
        :param depth: minimax tree depth
        :param team: teaming being evaluated black | white
        :param alpha: alpha-beta pruning, alpha, for minimax algorithm 
        :param beta: alpha-beta pruning, beta, for minimax algorithm
        :return: return tuple (float value of the State evaluation of board, best move string)
        """
        pass

