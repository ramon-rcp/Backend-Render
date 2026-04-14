
from chessPieces import *

class Game:
    def __init__(self):
        self.board, self.white_king, self.black_king = self.initialize_board()
        self.white_turn = True
        self.checkmate = False
        self.stalemate = False
        self.opponent_moves = {}
        self.player_moves = {}
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
                board[j][i] = Pawn(j == 1, (j, i))
        return board, white_king, black_king
    
    def update_opponent_moves(self):
        self.opponent_moves = {}
        king = self.white_king if self.white_turn else self.black_king
        if king is None:
            return
        king.clear_checks()
        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.clear_pin()
                    if piece.color != self.white_turn:
                        moves = piece.get_moves(self.board)
                        self.opponent_moves[piece.position] = moves
                        self.check_pins(piece, king)
                        self.add_checks(king, moves)

    # CHeck if opponent piece is pinning player"S pieces
    def check_pins(self, piece: ChessPiece, king: King):
        piece_directions = piece.get_move_directions()
        dir_2_king = (king.position[0] - piece.position[0], king.position[1] - piece.position[1])
        dir_2_king_normalized = (dir_2_king[0] // max(1, abs(dir_2_king[0])), dir_2_king[1] // max(1, abs(dir_2_king[1])))
        if piece_directions is not None and dir_2_king_normalized in piece_directions:
            pinned_piece = None
            for i in range(1, 8):
                pos = (piece.position[0] + dir_2_king_normalized[0] * i, piece.position[1] + dir_2_king_normalized[1] * i)
                if not (0 <= pos[0] < 8 and 0 <= pos[1] < 8):
                    break
                square = self.board[pos[0]][pos[1]]
                if square is not None:
                    if pinned_piece is None and square.color != piece.color:
                        pinned_piece = square
                    else:
                        pinned_piece = None
                        break
            if pinned_piece is not None:
                pinned_piece.set_pinned(dir_2_king_normalized)

    def add_checks(self, king: King, moves: list[tuple[int, int]]):
        if king.position in moves:
            king.add_check(king.position)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                newX = king.position[0] + dx
                newY = king.position[1] + dy
                if (newX, newY) in moves:
                    king.add_check((newX, newY))
        # Castling checks
        if not king.has_moved:
            for dx in [-3, -2, 2]:
                newX = king.position[0] + dx
                newY = king.position[1]
                if (newX, newY) in moves:
                    king.add_check((newX, newY))

    def update_player_moves(self):
        self.player_moves = {}
        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.clear_pin()
                    if piece.color == self.white_turn:
                        moves = piece.get_moves(self.board)
                        self.player_moves[piece.position] = moves

    def make_move(self, from_pos: tuple[int, int], to_pos: tuple[int, int]):
        piece = self.board[from_pos[0]][from_pos[1]]
        if piece is None or piece.color != self.white_turn:
            return False
        moves = piece.get_moves(self.board)
        if to_pos not in moves:
            return False
        
        # Check for castling
        castling = isinstance(piece, King) and abs(to_pos[1] - from_pos[1]) == 2

        # Move the piece
        if castling:
            rook = self.board[to_pos[0]][to_pos[1]]
            if not isinstance(rook, Rook) or rook.has_moved:
                return False
            self.board[to_pos[0]][to_pos[1]] = piece
            self.board[from_pos[0]][from_pos[1]] = None
            rook_to_pos = (from_pos[0], from_pos[1] + (1 if to_pos[1] > from_pos[1] else -1))
            self.board[rook_to_pos[0]][rook_to_pos[1]] = rook
            rook.move(rook_to_pos)
        else:
            self.board[to_pos[0]][to_pos[1]] = piece
            self.board[from_pos[0]][from_pos[1]] = None
        piece.move(to_pos)
        
        # change turn 
        self.white_turn = not self.white_turn

        # Update moves for next turn and check for checkmate/stalemate
        self.update_opponent_moves()
        self.update_player_moves()
        king = self.white_king if self.white_turn else self.black_king
        if king is None:
            return False
        if self.player_moves[king.position] == []:
            if king.checks:
                self.checkmate = True
            else:
                self.stalemate = True
        return True
                        
        
                    

        
    
