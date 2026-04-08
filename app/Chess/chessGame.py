
from chessPieces import *

class Game:
    def __init__(self):
        self.board, self.white_king, self.black_king = self.initialize_board()
        self.white_turn = True
        self.checkmate = False
        self.stalemate = False
        self.check = False
        self.update_opponent_moves()

    @staticmethod
    def initialize_board():
        order = ["r", "k", "b", "q", "k", "b", "k", "r"]
        board: list[list[ChessPiece | None]] = [[None for _ in range(8)] for _ in range(8)]
        white_king = None
        black_king = None
        for j in [0, 7]:
            for i in range(8):
                piece = None
                match order[i]:
                    case "r": piece = Rook(j == 0, (j, i))
                    case "k": piece = Knight(j == 0, (j, i))
                    case "b": piece = Bishop(j == 0, (j, i))
                    case "q": piece = Queen(j == 0, (j, i))
                    case "k": piece = King(j == 0, (j, i))
                if piece is not None:
                    board[j][i] = piece
                if isinstance(piece, King):
                    if j == 0:
                        white_king = piece
                    else:
                        black_king = piece
        for j in [1, 6]:
            for i in range(8):
                board[j][i] = Pawn(j == 0, (j, i))
        return board, white_king, black_king
    
    def update_opponent_moves(self):
        opponent_moves = {}
        king = self.white_king if self.white_turn else self.black_king
        if king is None:
            return
        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.clear_pin()
                    if piece.color != self.white_turn:
                        moves = piece.get_moves(self.board)
                        opponent_moves[piece.position] = moves
                        self.check = self.check or (king.position in moves)
                        self.check_pins(piece, king)

    def check_pins(self, piece: ChessPiece, king: King):
        piece_directions = piece.get_move_directions()
        dir_2_king = (king.position[0] - piece.position[0], king.position[1] - piece.position[1])
        dir_2_king_normalized = (dir_2_king[0] // max(1, abs(dir_2_king[0])), dir_2_king[1] // max(1, abs(dir_2_king[1])))
        if dir_2_king_normalized in piece_directions:
            pinned_piece = None
            for i in range(1, 8):
                pos = (piece.position[0] + dir_2_king_normalized[0] * i, piece.position[1] + dir_2_king_normalized[1] * i)
                if not (0 <= pos[0] < 8 and 0 <= pos[1] < 8):
                    break
                square = self.board[pos[0]][pos[1]]
                if square is not None:
                    if pinned_piece is None and square.color == piece.color:
                        pinned_piece = square
                    else:
                        pinned_piece = None
                        break
            if pinned_piece is not None:
                pinned_piece.set_pinned(dir_2_king_normalized)
                    

        
    
