# import numpy as np

class ChessPiece:
    def __init__(self, color: bool, position: tuple[int, int], name: str):
        self.color = color
        self.position = position
        self.name = name
        self.pinned: tuple[int, int] = (0, 0)
        self.has_moved = False

    @staticmethod
    def copy_ChessPiece(other: object):
        if not isinstance(other, ChessPiece):
            raise ValueError("Can only copy from another ChessPiece")
        new_piece = ChessPiece(other.color, other.position, other.name)
        new_piece.pinned = other.pinned
        new_piece.has_moved = other.has_moved
        return new_piece

    def set_pinned(self, pinned: tuple[int, int]):
        self.pinned = pinned

    def clear_pin(self):
        self.pinned = (0, 0)

    def get_moves(self, board):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def get_move_directions(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def move(self, new_position: tuple[int, int]):
        self.position = new_position
        self.has_moved = True

    def is_move_along_pin(self, new_pos: tuple[int, int]):
        if self.pinned == (0,0):
            return False
        move_dir = (new_pos[0] - self.position[0], new_pos[1] - self.position[1])
        move_dir = (move_dir[0] // max(1, abs(move_dir[0])), move_dir[1] // max(1, abs(move_dir[1])))
        if not((move_dir == self.pinned) or (move_dir == (-self.pinned[0], -self.pinned[1]))):
            return False
        return True
 

class Pawn(ChessPiece):
    def __init__(self, color: bool, position: tuple[int, int]):
        super().__init__(color, position, "Pawn")
        self.en_passant_target = False

    def get_moves(self, board: list[list[ChessPiece | None]]):
        moves = []
        direction = 1 if self.color else -1
        # Move forward
        if board[self.position[0] + direction][self.position[1]] is None:
            moves.append((self.position[0] + direction, self.position[1]))
            # Move two squares on first move
            if not self.has_moved:
                if board[self.position[0] + 2 * direction][self.position[1]] is None:
                    moves.append((self.position[0] + 2 * direction, self.position[1]))
        # Capture diagonally
        for dy in [-1, 1]:
            if 0 <= self.position[1] + dy < 8:
                target = board[self.position[0] + direction][self.position[1] + dy]
                if target is not None and target.color != self.color:
                    moves.append((self.position[0] + direction, self.position[1] + dy))
        # En passant
        for dy in [-1, 1]:
            if 0 <= self.position[1] + dy < 8:
                target = board[self.position[0]][self.position[1] + dy]
                if target is not None and target.color != self.color and isinstance(target, Pawn) and target.en_passant_target:
                    moves.append((self.position[0] + direction, self.position[1] + dy))
        for move in moves:
            if not self.is_move_along_pin(move):
                moves.remove(move)
        return moves
    
    def move(self, new_position: tuple[int, int]):
        super().move(new_position)
        # Check for en passant
        if abs(new_position[0] - self.position[0]) == 2:
            self.en_passant_target = True
        else:
            self.en_passant_target = False

    def get_move_directions(self):
        return None
    
class Rook(ChessPiece):
    def __init__(self, color: bool, position: tuple[int, int]):
        super().__init__(color, position, "Rook")

    def get_moves(self, board: list[list[ChessPiece | None]]):
        moves = []
        # Horizontal and vertical moves
        for dx in [-1, 1]:
            for step in range(1, 8):
                new_x = self.position[0] + dx * step
                if 0 <= new_x < 8:
                    target = board[new_x][self.position[1]]
                    if target is None:
                        moves.append((new_x, self.position[1]))
                    elif target.color != self.color:
                        moves.append((new_x, self.position[1]))
                        break
                    else:
                        break
                else:
                    break
        for dy in [-1, 1]:
            for step in range(1, 8):
                new_y = self.position[1] + dy * step
                if 0 <= new_y < 8:
                    target = board[self.position[0]][new_y]
                    if target is None:
                        moves.append((self.position[0], new_y))
                    elif target.color != self.color:
                        moves.append((self.position[0], new_y))
                        break
                    else:
                        break
                else:
                    break
        for move in moves:
            if not self.is_move_along_pin(move):
                moves.remove(move)
        return moves
    
    def get_move_directions(self):
        return [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
class Knight(ChessPiece):
    def __init__(self, color: bool, position: tuple[int, int]):
        super().__init__(color, position, "Knight")

    def get_moves(self, board: list[list[ChessPiece | None]]):
        moves = []
        # L-shaped moves
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board[new_x][new_y]
                if target is None or target.color != self.color:
                    moves.append((new_x, new_y))
        for move in moves:
            if not self.is_move_along_pin(move):
                moves.remove(move)
        return moves
    
    def get_move_directions(self):
        return None
    
class Bishop(ChessPiece):
    def __init__(self, color: bool, position: tuple[int, int]):
        super().__init__(color, position, "Bishop")

    def get_moves(self, board: list[list[ChessPiece | None]]):
        moves = []
        # Diagonal moves
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for step in range(1, 8):
                new_x = self.position[0] + dx * step
                new_y = self.position[1] + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    target = board[new_x][new_y]
                    if target is None:
                        moves.append((new_x, new_y))
                    elif target.color != self.color:
                        moves.append((new_x, new_y))
                        break
                    else:
                        break
                else:
                    break
        for move in moves:
            if not self.is_move_along_pin(move):
                moves.remove(move)
        return moves
    
    def get_move_directions(self):
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
class Queen(ChessPiece):
    def __init__(self, color: bool, position: tuple[int, int]):
        super().__init__(color, position, "Queen")

    def get_moves(self, board: list[list[ChessPiece | None]]):
        moves = []
        # Combine Rook and Bishop moves
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                for step in range(1, 8):
                    new_x = self.position[0] + dx * step
                    new_y = self.position[1] + dy * step
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        target = board[new_x][new_y]
                        if target is None:
                            moves.append((new_x, new_y))
                        elif target.color != self.color:
                            moves.append((new_x, new_y))
                            break
                        else:
                            break
                    else:
                        break
        for move in moves:
            if not self.is_move_along_pin(move):
                moves.remove(move)
        return moves
    
    def get_move_directions(self):
        return [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
class King(ChessPiece):
    def __init__(self, color: bool, position: tuple[int, int]):
        super().__init__(color, position, "King")
        self.checks: list[tuple[int, int]] = []

    def get_moves(self, board: list[list[ChessPiece | None]]):
        moves = []
        # One square in any direction
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = self.position[0] + dx
                new_y = self.position[1] + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8 and (new_x, new_y) not in self.checks:
                    target = board[new_x][new_y]
                    if target is None or target.color != self.color:
                        moves.append((new_x, new_y))
        # Castling
        if self.can_castle_kingside(board):
            moves.append((self.position[0], 6))
        if self.can_castle_queenside(board):
            moves.append((self.position[0], 2))
        return moves

    def get_move_directions(self):
        return None
    
    def add_check(self, position: tuple[int, int]):
        if position not in self.checks:
            self.checks.append(position)

    def is_checked(self):
        return self.position in self.checks
    
    def clear_checks(self):
        self.checks = []

    def can_castle_kingside(self, board):
        if self.has_moved or self.is_checked():
            return False
        rook = board[self.position[0]][7]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False
        if board[self.position[0]][5] is not None or board[self.position[0]][6] is not None:
            return False
        if (self.position[0], 5) in self.checks or (self.position[0], 6) in self.checks:
            return False
        return True
    
    def can_castle_queenside(self, board):
        if self.has_moved or self.is_checked():
            return False
        rook = board[self.position[0]][0]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False
        if board[self.position[0]][1] is not None or board[self.position[0]][2] is not None or board[self.position[0]][3] is not None:
            return False
        if (self.position[0], 1) in self.checks or (self.position[0], 2) in self.checks or (self.position[0], 3) in self.checks:
            return False
        return True