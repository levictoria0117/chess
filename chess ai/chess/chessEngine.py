"""Stores information about current state of the board and determines valid moves at that state"""

class state():
    def __init__(self):
        self.board = [
            ["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"],
            ["b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn"],
            ["w_rook", "w_knight", "w_bishop", "w_queen", "w_knight", "w_bishop", "w_knight", "w_rook"],
        ]
        self.white_move = True
        self.movelog = []