from typing import Callable
from chessEnums import PieceColor, PieceName
from utils import string_to_enum


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
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
        self.pieceMoved = board[int(self.startRow)][int(self.startCol)]
        self.pieceCaptured = board[int(self.endRow)][int(self.endCol)]
    def getChessNotation(self):
        #you can add to make this ilke real chess notation
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)
    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
    
    def compareMoves(self, move) -> bool:
        return (
            move.startRow == self.startRow and
            move.startCol == self.startCol and
            move.endRow == self.endRow and
            move.endCol == self.endCol
        )

"""Stores information about current state of the board and determines valid moves at that state"""
class State():
    def __init__(self, white_move: bool):
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
        self.white_move = white_move
        self.movelog = []


    def onMove(self, move: Move, team: PieceColor) -> bool:
        piece = self.get_piece_name(move.startRow, move.startCol)
        if not self.get_piece_color(move.startRow, move.startCol) == team:
            print(f"{self.get_piece_color == team =}")
            return False
        
        moves = self.get_move_function(piece)(move.startRow, move.startCol)
        # slow...
        for legalMoves in moves:
            if move.compareMoves(legalMoves):
                return self.makeMove(move)

    """
        Takes a Move as parameter ans executes it
    """
    def makeMove(self, move: Move) -> bool:
        self.board[int(move.startRow)][int(move.startCol)] = "--"
        self.board[int(move.endRow)][int(move.endCol)] = move.pieceMoved
        self.movelog.append(move)
        self.white_move = not self.white_move
        return True
    """
    Undo the last move made
    """
    def undoMove(self):
        if len(self.movelog) !=0:#make sure that there is a move to undo
            move = self.movelog.pop()
            self.board[int(move.startRow)][int(move.startCol)] = move.pieceMoved
            self.board[int(move.endRow)][int(move.endCol)] = move.pieceCaptured
            self.white_move = not self.white_move #switch turns back

    """
    All moves considering checks
    """
    def getValidMoves(self):
        return self.get_all_possible_moves1()#for now we will not worry about checks




    def get_all_allowed_moves(self, team: PieceColor) -> list[Move]:
        """
        list of all allowed moves for this board
        """
        pass

    """
        All moves without considering checks
    """
    def get_all_possible_moves1(self):
        moves: list[Move] = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_move) and (turn == 'b' and not self.white_move):
                    piece = self.board[r][c][1]
                    if piece == '_pawn':
                        self.get_pawn_moves(r,c,moves)
                    elif piece == '_rook':
                        self.get_rook_moves(r,c,)
        return moves
    def get_all_possible_moves(self, team: PieceColor) -> list[Move]:
        """
        :param team: team to enumerate all moves
        :return: list of all allowed moves for team
        """
        moves: list[Move] = []
        for r in range(len(self.board)):#number of rows
            for c in range(len(self.board[r])):#number of col
                if ((self.board[r][c] != "--") and (self.get_piece_color(r, c) == team)):
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

    def get_piece_name(self, row: int, col: int, start_of_piece_name = 2) -> PieceName | None:
        """
        b_rook
          ^
        012

        :param row:
        :param col:
        :param start_of_piece_name: start of the piece name based on the string names in board
        :return: the name of the piece at (row, col)
        """
        if (self.board[row][col] == "--"):
            return None
        return string_to_enum(self.board[int(row)][int(col)][start_of_piece_name:], PieceName)
    
    def get_piece_color(self, row: int, col: int) -> PieceColor | None:
        # In b_rook and w_pawn the first char is the color of the piece
        if (self.board[row][col] == "--"):
            return None
        return PieceColor.BLACK if self.board[int(row)][int(col)][0] == "b" else PieceColor.WHITE

    def get_queen_moves(self, row: int, col: int) -> list[Move]:
        moves = []
        moves += self.get_rook_moves(row, col)
        moves += self.get_bishop_moves(row, col)
        return moves

    def get_king_moves(self, row:int, col: int)-> list[Move]:
        moves: list[Move] = []
        dir = ((1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1))
        if self.white_move:
            teamColor = 'w'
        else:
            teamColor = 'b'
        for i in range(8):
            endRow = row + dir[i][0]
            endCol = col + dir[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != teamColor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))
        return moves

    def get_pawn_moves(self, row:int, col: int)-> list[Move]:
        moves: list[Move] = []
        if self.white_move:
            endRow = row - 1
            if self.board[endRow][col] == "--": # 1 square moves
                moves.append(Move((row, col), (endRow, col), self.board))
                if row == 6 and self.board[endRow - 1][col] == "--": # two square moves
                    moves.append(Move((row, col), (endRow - 1, col), self.board))
            if col-1 >= 0: #capture to left
                if self.board[endRow][col-1][0] == 'b':
                    moves.append(Move((row, col), (endRow, col-1), self.board))
            if col+1 <= 7: #capture to right
                if self.board[endRow][col+1][0] == 'b':
                    moves.append(Move((row, col), (endRow, col+1), self.board))

        else: #black pawn
            endRow = row+1
            if self.board[endRow][col] == "--": # 1 square moves
                moves.append(Move((row, col), (endRow, col), self.board))
                if row == 1 and self.board[endRow+1][col] == "--": # two square moves
                    moves.append(Move((row, col), (endRow + 1, col), self.board))
            if col-1 >= 0: #capture to right
                if self.board[endRow][col-1][0] == 'w':
                    moves.append(Move((row, col), (endRow, col-1), self.board))
            if col+1 <= 7: #capture to left
                if self.board[endRow][col+1][0] == 'w':
                    moves.append(Move((row, col), (endRow, col+1), self.board))
        return moves


    def get_rook_moves(self, row:int, col: int)-> list[Move]:
        moves: list[Move] = []
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
                    endPiece = self.board[endRow][endCol]
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
        moves: list[Move] = []
        kMoves = ((2,1), (2,-1), (1,2), (1,-2), (-2,1), (-2,-1), (-1,2), (-1,-2))
        if self.white_move:
            teamColor = 'w'
        else:
            teamColor = 'b'
        for k in kMoves:
            endRow = row + k[0]
            endCol = col + k[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != teamColor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))
        return moves


    def get_bishop_moves(self, row:int, col: int)-> list[Move]:
        moves: list[Move] = []
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
                    endPiece = self.board[endRow][endCol]
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
