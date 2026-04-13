# import pytest
from chessPieces import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King


class TestChessPiece:
    def test_init(self):
        piece = ChessPiece(True, (0, 0), "Test")
        assert piece.color is True
        assert piece.position == (0, 0)
        assert piece.name == "Test"
        assert piece.pinned == [(0, 0)]
        assert piece.has_moved is False
        print("ChessPiece initialized correctly")


    def test_set_pinned(self):
        piece = ChessPiece(True, (4, 4), "Test")
        piece.set_pinned((1, 0))
        assert piece.pinned == [(1, 0)]
        print("Pinned state set correctly")

    def test_move(self):
        piece = ChessPiece(True, (0, 0), "Test")
        piece.move((1, 1))
        assert piece.position == (1, 1)
        assert piece.has_moved is True
        print("Piece moved correctly")

    def test_is_move_along_pin_no_pin(self):
        piece = ChessPiece(True, (4, 4), "Test")
        assert piece.is_move_along_pin((5, 5)) is True
        print("Move along pin correctly identified for no pin")

    def test_is_move_along_pin_horizontal(self):
        piece = ChessPiece(True, (4, 4), "Test")
        piece.set_pinned((1, 0))
        assert piece.is_move_along_pin((4, 5)) is False
        assert piece.is_move_along_pin((7, 4)) is True
        assert piece.is_move_along_pin((3, 4)) is True
        print("Move along pin correctly identified for horizontal pin")

    def test_is_move_along_pin_diagonal(self):
        piece = ChessPiece(True, (4, 4), "Test")
        piece.set_pinned((1, 1))
        assert piece.is_move_along_pin((5, 5)) is True
        assert piece.is_move_along_pin((2, 2)) is True
        assert piece.is_move_along_pin((5, 4)) is False
        print("Move along pin correctly identified for diagonal pin")



class TestPawn:
    def test_pawn_init(self):
        pawn = Pawn(True, (1, 0))
        assert pawn.color is True
        assert pawn.position == (1, 0)
        assert pawn.name == "Pawn"
        print("Pawn initialized correctly")

    def test_pawn_move_forward_white(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        pawn = Pawn(True, (1, 0))
        moves = pawn.get_moves(board)
        assert (2, 0) in moves
        print("Pawn moves forward correctly")

    def test_pawn_move_two_squares_first_move(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        pawn = Pawn(True, (1, 0))
        moves = pawn.get_moves(board)
        assert (3, 0) in moves
        print("Pawn moves two squares on first move correctly")

    def test_pawn_cannot_move_two_squares_after_first_move(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        pawn = Pawn(True, (1, 0))
        pawn.move((2, 0))
        moves = pawn.get_moves(board)
        assert (4, 0) not in moves
        print("Pawn cannot move two squares after first move")

    def test_pawn_blocked(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        blocking_piece = Pawn(False, (2, 0))
        board[2][0] = blocking_piece
        pawn = Pawn(True, (1, 0))
        moves = pawn.get_moves(board)
        assert (2, 0) not in moves
        print("Pawn blocked correctly")

    def test_pawn_capture_diagonal(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        enemy = Pawn(False, (2, 1))
        board[2][1] = enemy
        pawn = Pawn(True, (1, 0))
        moves = pawn.get_moves(board)
        assert (2, 1) in moves
        print("Pawn captures diagonally correctly")

    def test_pawn_cannot_capture_own_piece(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        ally = Pawn(True, (2, 1))
        board[2][1] = ally
        pawn = Pawn(True, (1, 0))
        moves = pawn.get_moves(board)
        assert (2, 1) not in moves
        print("Pawn cannot capture own piece")

    def test_pawn_pinned_horizontal(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        pawn = Pawn(True, (4, 4))
        pawn.set_pinned((1, 0))
        moves = pawn.get_moves(board)
        # Pawn moves vertically, but pinned horizontally, so no moves
        assert len(moves) == 0
        print("Pawn pinned horizontally correctly")


class TestRook:
    def test_rook_horizontal_movement(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        rook = Rook(True, (4, 4))
        moves = rook.get_moves(board)
        assert (4, 0) in moves
        assert (4, 7) in moves
        assert (4, 5) in moves
        print("Rook horizontal movement works correctly")

    def test_rook_vertical_movement(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        rook = Rook(True, (4, 4))
        moves = rook.get_moves(board)
        assert (0, 4) in moves
        assert (7, 4) in moves
        assert (5, 4) in moves
        print("Rook vertical movement works correctly")

    def test_rook_blocked_by_piece(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        blocking = Rook(True, (4, 6))
        board[4][6] = blocking
        rook = Rook(True, (4, 4))
        moves = rook.get_moves(board)
        assert (4, 6) not in moves
        assert (4, 5) in moves
        print("Rook correctly blocked by piece")

    def test_rook_captures_enemy(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        enemy = Rook(False, (4, 6))
        board[4][6] = enemy
        rook = Rook(True, (4, 4))
        moves = rook.get_moves(board)
        assert (4, 6) in moves
        print("Rook captures enemy correctly")

    def test_rook_pinned(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        rook = Rook(True, (4, 4))
        rook.set_pinned((1, 0))
        moves = rook.get_moves(board)
        # Should only be able to move horizontally
        assert (4, 5) in moves
        assert (5, 4) not in moves
        print("Rook pinned correctly")


class TestKnight:
    def test_knight_l_shaped_moves(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        knight = Knight(True, (4, 4))
        moves = knight.get_moves(board)
        expected = [(6, 5), (6, 3), (2, 5), (2, 3), (5, 6), (5, 2), (3, 6), (3, 2)]
        for move in expected:
            assert move in moves
        print("Knight L-shaped moves work correctly")

    def test_knight_edge_boundaries(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        knight = Knight(True, (0, 0))
        moves = knight.get_moves(board)
        assert (2, 1) in moves
        assert (1, 2) in moves
        assert (-1, 2) not in moves
        print("Knight edge boundaries handled correctly")

    def test_knight_pinned(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        knight = Knight(True, (4, 4))
        knight.set_pinned((1, 0))
        moves = knight.get_moves(board)
        # Knights can't move while pinned (no L-shaped moves along pin)
        assert len(moves) == 0
        print("Knight pinned correctly")


class TestBishop:
    def test_bishop_diagonal_moves(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        bishop = Bishop(True, (4, 4))
        moves = bishop.get_moves(board)
        assert (5, 5) in moves
        assert (3, 3) in moves
        assert (5, 3) in moves
        assert (3, 5) in moves
        print("Bishop diagonal moves work correctly")

    def test_bishop_blocked(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        blocking = Bishop(True, (5, 5))
        board[5][5] = blocking
        bishop = Bishop(True, (4, 4))
        moves = bishop.get_moves(board)
        assert (5, 5) not in moves
        assert (6, 6) not in moves
        print("Bishop correctly blocked")

    def test_bishop_captures_enemy(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        enemy = Bishop(False, (6, 6))
        board[6][6] = enemy
        bishop = Bishop(True, (4, 4))
        moves = bishop.get_moves(board)
        assert (6, 6) in moves
        print("Bishop captures enemy correctly")

    def test_bishop_pinned_diagonal(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        bishop = Bishop(True, (4, 4))
        bishop.set_pinned((1, 1))
        moves = bishop.get_moves(board)
        # Should only move along diagonal
        assert (5, 5) in moves
        assert (3, 3) in moves
        assert (5, 3) not in moves
        print("Bishop pinned diagonally correctly")


class TestQueen:
    def test_queen_all_directions(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        queen = Queen(True, (4, 4))
        moves = queen.get_moves(board)
        # Horizontal
        assert (4, 5) in moves
        # Vertical
        assert (5, 4) in moves
        # Diagonal
        assert (5, 5) in moves
        print("Queen moves in all directions correctly")

    def test_queen_blocked(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        blocking = Queen(True, (4, 6))
        board[4][6] = blocking
        queen = Queen(True, (4, 4))
        moves = queen.get_moves(board)
        assert (4, 6) not in moves
        assert (4, 5) in moves
        print("Queen correctly blocked")


class TestKing:
    def test_king_one_square_all_directions(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (4, 4))
        moves = king.get_moves(board)
        assert len(moves) == 8
        assert (5, 5) in moves
        assert (3, 3) in moves
        print("King moves one square in all directions correctly")

    def test_king_boundary(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (0, 0))
        moves = king.get_moves(board)
        assert (1, 1) in moves
        assert (-1, -1) not in moves
        print("King boundary handling works correctly")

    def test_king_castling_kingside(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (0, 4))
        rook = Rook(True, (0, 7))
        board[0][4] = king
        board[0][7] = rook
        moves = king.get_moves(board)
        assert (0, 6) in moves
        print("King kingside castling works correctly")

    def test_king_no_castling_after_move(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (0, 4))
        king.move((0, 5))
        rook = Rook(True, (0, 7))
        board[0][4] = None
        board[0][5] = king
        board[0][7] = rook
        moves = king.get_moves(board)
        assert (0, 6) not in moves
        print("King cannot castle after moving correctly")

    def test_king_castling_queenside(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (0, 4))
        rook = Rook(True, (0, 0))
        board[0][4] = king
        board[0][0] = rook
        moves = king.get_moves(board)
        assert (0, 2) in moves
        print("King queenside castling works correctly")

    def test_king_no_castling_when_checked(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (0, 4))
        king.add_check((0, 4))
        rook = Rook(True, (0, 7))
        board[0][4] = king
        board[0][7] = rook
        moves = king.get_moves(board)
        assert (0, 6) not in moves
        print("King cannot castle when in check")

    def test_king_no_castling_when_path_attacked(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (0, 4))
        king.add_check((0, 6))
        rook = Rook(True, (0, 7))
        board[0][4] = king
        board[0][7] = rook
        moves = king.get_moves(board)
        assert (0, 6) not in moves
        print("King cannot castle through attacked square")

    def test_king_no_castling_when_rook_moved(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (0, 4))
        rook = Rook(True, (0, 7))
        rook.has_moved = True
        board[0][4] = king
        board[0][7] = rook
        moves = king.get_moves(board)
        assert (0, 6) not in moves
        print("King cannot castle when rook has moved")

    def test_king_no_castling_when_pieces_between(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (0, 4))
        rook = Rook(True, (0, 7))
        blocking = Knight(True, (0, 6))
        board[0][4] = king
        board[0][7] = rook
        board[0][6] = blocking
        moves = king.get_moves(board)
        assert (0, 6) not in moves
        print("King cannot castle when pieces are between")

    def test_king_cannot_move_to_checked_square(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        king = King(True, (4, 4))
        king.add_check((5, 5))
        king.add_check((5, 4))
        moves = king.get_moves(board)
        assert (5, 5) not in moves
        assert (5, 4) not in moves
        print("King cannot move to attacked squares")

    def test_king_add_check(self):
        king = King(True, (4, 4))
        king.add_check((4, 5))
        assert (4, 5) in king.checks
        print("add_check works correctly")

    def test_king_add_check_no_duplicates(self):
        king = King(True, (4, 4))
        king.add_check((4, 5))
        king.add_check((4, 5))
        assert king.checks.count((4, 5)) == 1
        print("add_check does not add duplicate squares")

    def test_king_is_checked(self):
        king = King(True, (4, 4))
        assert king.is_checked() is False
        king.add_check((4, 4))
        assert king.is_checked() is True
        print("is_checked works correctly")

    def test_king_clear_checks(self):
        king = King(True, (4, 4))
        king.add_check((4, 4))
        king.add_check((3, 4))
        king.clear_checks()
        assert king.checks == []
        print("clear_checks works correctly")


class TestChessPieceCopy:
    def test_copy_preserves_all_fields(self):
        piece = ChessPiece(True, (3, 3), "Test")
        piece.set_pinned((1, 0))
        piece.move((4, 4))
        copy = ChessPiece.copy_ChessPiece(piece)
        assert copy.color == piece.color
        assert copy.position == piece.position
        assert copy.name == piece.name
        assert copy.pinned == piece.pinned
        assert copy.has_moved == piece.has_moved
        print("copy_ChessPiece preserves all fields")

    def test_copy_is_independent(self):
        piece = ChessPiece(True, (3, 3), "Test")
        copy = ChessPiece.copy_ChessPiece(piece)
        copy.move((5, 5))
        assert piece.position == (3, 3)
        print("copy_ChessPiece creates an independent object")

    def test_copy_raises_for_non_chess_piece(self):
        raised = False
        try:
            ChessPiece.copy_ChessPiece("not a piece")
        except ValueError:
            raised = True
        assert raised
        print("copy_ChessPiece raises ValueError for non-ChessPiece")


class TestClearPin:
    def test_clear_pin_resets_to_zero(self):
        piece = ChessPiece(True, (4, 4), "Test")
        piece.set_pinned((1, 0))
        piece.clear_pin()
        assert piece.pinned == (0, 0)
        print("clear_pin resets pin to (0, 0)")


class TestPawnEnPassant:
    def test_pawn_en_passant_capture(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        pawn = Pawn(True, (4, 4))
        enemy_pawn = Pawn(False, (4, 5))
        enemy_pawn.en_passant_target = True
        board[4][5] = enemy_pawn
        moves = pawn.get_moves(board)
        assert (5, 5) in moves
        print("Pawn en passant capture works correctly")

    def test_pawn_no_en_passant_without_target(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        pawn = Pawn(True, (4, 4))
        enemy_pawn = Pawn(False, (4, 5))
        enemy_pawn.en_passant_target = False
        board[4][5] = enemy_pawn
        moves = pawn.get_moves(board)
        assert (5, 5) not in moves
        print("Pawn en passant not available when target flag is False")

    def test_pawn_no_en_passant_against_ally(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        pawn = Pawn(True, (4, 4))
        ally_pawn = Pawn(True, (4, 5))
        ally_pawn.en_passant_target = True
        board[4][5] = ally_pawn
        moves = pawn.get_moves(board)
        assert (5, 5) not in moves
        print("Pawn cannot en passant capture own piece")


class TestGetMoveDirections:
    def test_rook_move_directions(self):
        rook = Rook(True, (0, 0))
        dirs = rook.get_move_directions()
        assert (1, 0) in dirs
        assert (-1, 0) in dirs
        assert (0, 1) in dirs
        assert (0, -1) in dirs
        assert len(dirs) == 4
        print("Rook get_move_directions correct")

    def test_bishop_move_directions(self):
        bishop = Bishop(True, (0, 0))
        dirs = bishop.get_move_directions()
        assert (-1, -1) in dirs
        assert (-1, 1) in dirs
        assert (1, -1) in dirs
        assert (1, 1) in dirs
        assert len(dirs) == 4
        print("Bishop get_move_directions correct")

    def test_queen_move_directions(self):
        queen = Queen(True, (0, 0))
        dirs = queen.get_move_directions()
        assert len(dirs) == 8
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                assert (dx, dy) in dirs
        print("Queen get_move_directions correct")

    def test_pawn_move_directions_is_none(self):
        pawn = Pawn(True, (1, 0))
        assert pawn.get_move_directions() is None
        print("Pawn get_move_directions returns None")

    def test_knight_move_directions_is_none(self):
        knight = Knight(True, (0, 0))
        assert knight.get_move_directions() is None
        print("Knight get_move_directions returns None")


class TestQueenExtra:
    def test_queen_captures_enemy(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        enemy = Queen(False, (4, 7))
        board[4][7] = enemy
        queen = Queen(True, (4, 4))
        moves = queen.get_moves(board)
        assert (4, 7) in moves
        print("Queen captures enemy correctly")

    def test_queen_pinned_horizontal(self):
        board: list[list[ChessPiece | None]] = [[None] * 8 for _ in range(8)]
        queen = Queen(True, (4, 4))
        queen.set_pinned((0, 1))
        moves = queen.get_moves(board)
        assert (4, 5) in moves
        assert (4, 3) in moves
        assert (5, 4) not in moves
        assert (5, 5) not in moves
        print("Queen pinned horizontally moves only along pin")