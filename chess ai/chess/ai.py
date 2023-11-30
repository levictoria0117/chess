from abc import ABC, abstractclassmethod
from chessEnums import PieceColor
from chessEngine import state

class AI(ABC):
    def __init__(self, team: PieceColor):
        self.team = team
    @abstractclassmethod
    def move(self, board: state) -> bool:
        """
        returns True and makes move found else False and no move made

        :param board: object of state that holds the board that contains current board state
        :return: True if move found else False
        """
        ...

class MiniMaxAlphaBeta(AI):
    def __init__(self, team: PieceColor, depth: int):
        super().__init__(team)
        self.depth = depth
    
    def move(self, board: state):
        pass

    def minimax(self, board: state) -> str:
        """
        :param: board object with current board state
        :return: the best move found as a string
        """
        pass

    def min_value(self, board: state, depth: int, team: PieceColor, alpha: int, beta: int) -> tuple[float, str | None]:
        """
        :param board: state object representing representing a chess board state
        :param depth: minimax depth
        :param team: teaming being evaluated black | white
        :param alpha: alpha-beta pruning, alpha, for minimax algorithm 
        :param beta: alpha-beta pruning, beta, for minimax algorithm
        :return: return tuple (float value of the state evaluation of board, best move string)
        """
        pass

    def max_value(self, board: state, depth: int, team: PieceColor, alpha: int, beta: int) -> (float, str):
        """
        :param board: state object representing representing a chess board state
        :param depth: minimax tree depth
        :param team: teaming being evaluated black | white
        :param alpha: alpha-beta pruning, alpha, for minimax algorithm 
        :param beta: alpha-beta pruning, beta, for minimax algorithm
        :return: return tuple (float value of the state evaluation of board, best move string)
        """
        pass

