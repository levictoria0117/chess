from abc import ABC, abstractclassmethod
from typing import Callable
from copy import deepcopy
from chessEnums import PieceColor, PieceName
from chessEngine import State, Move
from heuristics import Heuristic

# abstract base class
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
    def __init__(self, team: PieceColor, depth: int, heuristic_func: Heuristic):
        super().__init__(team)
        self.depth = depth
        self.heuristic_func = heuristic_func
    
    def move(self, board: State) -> bool:
        """
        on best move found performs move and makes move else no move found and made

        :param board:
        :return: True is move is found Else False
        """
        best_move = self.minimax(board)
        if best_move is not None:
            name: PieceName = board.get_piece_name(best_move)
            board.makeMove(best_move)
            print(f"\nAI: moving {name} {(best_move.startRow, best_move.startCol)} -> {(best_move.endRow, best_move.endCol)}")
            return True
        return False


    def minimax(self, board: State) -> Move | None:
        """
        :param: board object with current board State
        :return: the best move found as a string
        """
        alpha = -100000
        beta = 100000
        if self.team == PieceColor.BLACK:
            _, best_move = self.min_value(board, self.depth, PieceColor.BLACK, alpha, beta)
        elif self.team == PieceColor.WHITE:
            _, best_move = self.max_value(board, self.depth, PieceColor.BLACK, alpha, beta)
        else:
            raise Exception("Error AI: team not defined")
        return best_move

    def min_value(self, board: State, depth: int, team: PieceColor, alpha: int, beta: int) -> tuple[float, Move | None]:
        """
        :param board: State object representing representing a chess board State
        :param depth: minimax depth
        :param team: teaming being evaluated black | white
        :param alpha: alpha-beta pruning, alpha, for minimax algorithm 
        :param beta: alpha-beta pruning, beta, for minimax algorithm
        :return: return tuple (float value of the State evaluation of board, best move string)
        """
        if depth == 0:
            return self.heuristic_func.evaluate(board), None
        value = 9999
        best_move = None
        allowed_moves = board.get_all_allowed_moves(team)

        for move in allowed_moves:
            temp_board = deepcopy(board.board)
            temp_state = State()
            temp_state.board = temp_board

            if temp_state.makeMove(move):
                opposite_team = PieceColor.BLACK if team == PieceColor.WHITE else PieceColor.WHITE
                val, _ = self.max_value(temp_state, depth - 1, opposite_team, alpha, beta)

                if val < value:
                    value = val
                    best_move = move
                
                beta = min(value, beta)
                
                if beta <= alpha:
                    return value, best_move
        return value, best_move


    def max_value(self, board: State, depth: int, team: PieceColor, alpha: int, beta: int) -> tuple[float, Move | None]:
        """
        :param board: State object representing representing a chess board State
        :param depth: minimax tree depth
        :param team: teaming being evaluated black | white
        :param alpha: alpha-beta pruning, alpha, for minimax algorithm 
        :param beta: alpha-beta pruning, beta, for minimax algorithm
        :return: return tuple (float value of the State evaluation of board, best move string)
        """
        # base condition
        if depth == 0:
            return self.heuristic_func.evaluate(board), None
        value = -9999
        best_move = None
        allowed_moves = board.get_all_allowed_moves(team)

        for move in allowed_moves:
            temp_board = deepcopy(board.board)
            temp_state = State()
            temp_state.board = temp_board

            if temp_state.makeMove(move):
                opposite_team = PieceColor.BLACK if team == PieceColor.WHITE else PieceColor.WHITE
                val, _ = self.min_value(temp_state, depth - 1, opposite_team, alpha, beta)

                if val > value:
                    value = val
                    best_move = move
                
                # alpha update
                alpha = min(value, alpha)
                
                # prune
                if beta <= alpha:
                    return value, best_move
        return value, best_move

