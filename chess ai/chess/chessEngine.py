from typing import Callable
from chessEnums import PieceColor, PieceName
from utils import string_to_enum


class Move:
    def __init__(self, startSq: tuple[int, int], endSq: tuple[int, int], board: list[list[str]]):
        """
        :param startSq: tuple holding the coordinates of piece start square (row, column)
        :param endSq: tuple holding the coordinates of piece end square (row, column)
        :param board: state of the board as a 2D list the Move is based on
        """
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

"""Stores information about current state of the board and determines valid moves at that state"""
class State():
    def __init__(self):
        self.board = [
            ["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"],
            ["b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn"],
            ["w_rook", "w_knight", "w_bishop", "w_queen", "w_king", "w_bishop", "w_knight", "w_rook"],
        ]
        self.white_move = True
        self.movelog = []
    
    def makeMove(self, move: Move) -> bool:
        self.board[move.startRow][move.startCol] == "--"
        self.board[move.endRow][move.endCol] == move.pieceMoved
        self.movelog.append(move)
        self.white_move = not self.white_move
        return True

    def get_all_allowed_moves(self, team: PieceColor) -> list[Move]:
        """
        list of all allowed moves for this board
        """
        pass
    
    def get_all_possible_moves(self, team: PieceColor) -> list[Move]:
        """
        :param team: team to enumerate all moves
        :return: list of all allowed moves for team
        """
        moves: list[Move] = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if (self.get_piece_color(r, c) == team):
                    piece = self.get_piece_name(r, c)
                    piece_moves = self.get_move_function(piece)(r, c)
                    moves.extend(piece_moves)
        return moves
        
    def get_move_function(self, piece: PieceName) -> Callable[[int, int], list[Move]]:
        match piece:
            case PieceName.QUEEN:
                return self.get_queen_moves
            case PieceName.KING:
                return self.get_king_moves
            case PieceName.PAWN:
                return self.get_pawn_moves
            case PieceName.ROOK:
                return self.get_rook_moves
            case PieceName.KNIGHT:
                return self.get_knight_moves
            case PieceName.BISHOP:
                return self.get_bishop_moves

    def get_piece_name(self, row: int, col: int, start_of_piece_name = 2) -> PieceName:
        """
        b_rook
          ^
        012

        :param row:
        :param col:
        :param start_of_piece_name: start of the piece name based on the string names in board
        :return: the name of the piece at (row, col)
        """
        return string_to_enum(self.board[row][col][start_of_piece_name:], PieceName)
    
    def get_piece_color(self, row: int, col: int) -> PieceColor:
        # In b_rook and w_pawn the first char is the color of the piece
        return PieceColor.BLACK if self.board[row][col][0] == "b" else PieceColor.WHITE
    

    def get_queen_moves(self, row:int, col: int)-> list[Move]:
        self.get_rook_moves(row, col)
        self.get_bishop_moves(row, col)
        return moves


    def get_king_moves(self, row:int, col: int)-> list[Move]:
        dir = ((1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1))
        if self.white_move:
            teamColor = 'w'
        else:
            teamColor = 'b'
        for i in range(8):
            endRow = row + dir[i][0]
            endcol = col + dir[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != teamColor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))
        return moves

    def get_pawn_moves(self, row:int, col: int)-> list[Move]:
        if self.white_move:
            if self.board[row-1][c] == "--": # 1 square moves
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == "--": # two square moves
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col-1 >= 0: #capture to left
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col+1 <= 7: #capture to right
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))

        else: #black pawn
            if self.board[row+1][c] == "--": # 1 square moves
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == "--": # two square moves
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col-1 >= 0: #capture to right
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col+1 <= 7: #capture to left
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))
        return moves


    def get_rook_moves(self, row:int, col: int)-> list[Move]:
        dir = ((-1,0), (0,-1), (1,0),(0,1))
        if self.white_move:
            oppColor = 'b'
        else:
            oppColor = 'w'
        for d in dir:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece == self.board[endRow][endCol]
                    if endPiece == "--": #move if able to
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == oppColor: #capture enemy piece
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else: #same team, cannot do anything
                        break
                else: # escaped the board
                    break # after every break, find new direction
        return moves

    def get_knight_moves(self, row:int, col: int)-> list[Move]:
        kMoves = ((2,1), (2,-1), (1,2), (1,-2), (-2,1), (-2,-1), (-1,2), (-1,-2))
        if self.white_move:
            teamColor = 'w'
        else:
            teamColor = 'b'
        for k in kMoves:
            endRow = row + k[0]
            endCol = col + k[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece == self.board[endRow][endCol]
                if endPiece[0] != teamColor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))
        return moves


    def get_bishop_moves(self, row:int, col: int)-> list[Move]:
        dir = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.white_move:
            oppColor = 'b'
        else:
            oppColor = 'w'
        for d in dir:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece == self.board[endRow][endCol]
                    if endPiece == "--":  # move if able to
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == oppColor:  # capture enemy piece
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:  # same team, cannot do anything
                        break
                else:  # escaped the board
                    break  # after every break, find new direction
        return moves
