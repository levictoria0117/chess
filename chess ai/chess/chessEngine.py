from chessEnums import PieceColor

class Move:
    def __init__(self, startSq: tuple[int, int], endSq: tuple[int, int], board: list[list[str]]):
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
    
    def makeMove(self, move: Move):
        self.board[move.startRow][move.startCol] == "--"
        self.board[move.endRow][move.endCol] == move.pieceMoved
        self.movelog.append(move)
        self.white_move = not self.white_move
    
    def get_all_allowed_moves(self, team: PieceColor):
        """
        :param team: team to enumerate all moves
        : return: list of all allowed moves for team
        """
        pass

    
