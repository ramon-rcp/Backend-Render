import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from chessPieces import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King
from chessGame import Game


def make_empty_game():
    """Return a Game with an empty board and kings manually set."""
    game = Game.__new__(Game)
    game.board = [[]]
    for _ in range(8):
        game.board.append([[None] * 8])
    game.white_king = None
    game.black_king = None
    game.white_turn = True
    game.checkmate = False
    game.stalemate = False
    game.opponent_moves = {}
    game.player_moves = {}
    return game


def place_kings(game, white_pos=(0, 4), black_pos=(7, 4)):
    """Place kings on the board and assign them to game."""
    white_king = King(True, white_pos)
    black_king = King(False, black_pos)
    game.board[white_pos[0]][white_pos[1]] = white_king
    game.board[black_pos[0]][black_pos[1]] = black_king
    game.white_king = white_king
    game.black_king = black_king
    return white_king, black_king


# ---------------------------------------------------------------------------
# Game.__init__
# ---------------------------------------------------------------------------

class TestGameInit:
    def test_white_turn_on_start(self):
        game = Game()
        assert game.white_turn is True

    def test_checkmate_false_on_start(self):
        game = Game()
        assert game.checkmate is False

    def test_stalemate_false_on_start(self):
        game = Game()
        assert game.stalemate is False

    def test_board_is_8x8(self):
        game = Game()
        assert len(game.board) == 8
        for row in game.board:
            assert len(row) == 8

    def test_opponent_moves_is_dict(self):
        game = Game()
        assert isinstance(game.opponent_moves, dict)

    def test_player_moves_is_dict(self):
        game = Game()
        assert isinstance(game.player_moves, dict)


# ---------------------------------------------------------------------------
# Game.initialize_board
# ---------------------------------------------------------------------------

class TestInitializeBoard:
    def test_white_pawns_on_row_1(self):
        board, _, _ = Game.initialize_board()
        for col in range(8):
            assert isinstance(board[1][col], Pawn), f"Expected Pawn at (1, {col})"
            assert board[1][col].color is True

    def test_black_pawns_on_row_6(self):
        board, _, _ = Game.initialize_board()
        for col in range(8):
            assert isinstance(board[6][col], Pawn), f"Expected Pawn at (6, {col})"
            assert board[6][col].color is False

    def test_rooks_on_corners_row_0(self):
        board, _, _ = Game.initialize_board()
        assert isinstance(board[0][0], Rook)
        assert isinstance(board[0][7], Rook)

    def test_rooks_on_corners_row_7(self):
        board, _, _ = Game.initialize_board()
        assert isinstance(board[7][0], Rook)
        assert isinstance(board[7][7], Rook)

    def test_white_pieces_on_row_0(self):
        board, _, _ = Game.initialize_board()
        for col in range(8):
            piece = board[0][col]
            if piece is not None:
                assert piece.color is True

    def test_black_pieces_on_row_7(self):
        board, _, _ = Game.initialize_board()
        for col in range(8):
            piece = board[7][col]
            if piece is not None:
                assert piece.color is False

    def test_middle_rows_are_empty(self):
        board, _, _ = Game.initialize_board()
        for row in range(2, 6):
            for col in range(8):
                assert board[row][col] is None

    def test_queens_on_column_3(self):
        board, _, _ = Game.initialize_board()
        assert isinstance(board[0][3], Queen)
        assert isinstance(board[7][3], Queen)

    def test_bishops_on_columns_2_and_5(self):
        board, _, _ = Game.initialize_board()
        assert isinstance(board[0][2], Bishop)
        assert isinstance(board[0][5], Bishop)
        assert isinstance(board[7][2], Bishop)
        assert isinstance(board[7][5], Bishop)

    def test_pawn_positions_match_board_index(self):
        board, _, _ = Game.initialize_board()
        for col in range(8):
            assert board[1][col].position == (1, col)
            assert board[6][col].position == (6, col)


# ---------------------------------------------------------------------------
# Game.make_move — basic moves
# ---------------------------------------------------------------------------

class TestMakeMoveBasic:
    def test_valid_pawn_move_returns_true(self):
        game = make_empty_game()
        place_kings(game)
        pawn = Pawn(True, (1, 0))
        game.board[1][0] = pawn
        game.update_opponent_moves()
        assert game.make_move((1, 0), (2, 0)) is True

    def test_piece_lands_on_destination(self):
        game = make_empty_game()
        place_kings(game)
        pawn = Pawn(True, (1, 3))
        game.board[1][3] = pawn
        game.update_opponent_moves()
        game.make_move((1, 3), (2, 3))
        assert game.board[2][3] is pawn
        assert game.board[1][3] is None

    def test_piece_position_updated(self):
        game = make_empty_game()
        place_kings(game)
        pawn = Pawn(True, (1, 3))
        game.board[1][3] = pawn
        game.update_opponent_moves()
        game.make_move((1, 3), (2, 3))
        assert pawn.position == (2, 3)
        assert pawn.has_moved is True

    def test_turn_switches_after_valid_move(self):
        game = make_empty_game()
        place_kings(game)
        pawn = Pawn(True, (1, 0))
        game.board[1][0] = pawn
        game.update_opponent_moves()
        game.make_move((1, 0), (2, 0))
        assert game.white_turn is False

    def test_two_successive_moves_switch_turns(self):
        game = make_empty_game()
        white_king, black_king = place_kings(game)
        white_pawn = Pawn(True, (1, 0))
        black_pawn = Pawn(False, (6, 0))
        game.board[1][0] = white_pawn
        game.board[6][0] = black_pawn
        game.update_opponent_moves()
        game.make_move((1, 0), (2, 0))
        game.make_move((6, 0), (5, 0))
        assert game.white_turn is True


# ---------------------------------------------------------------------------
# Game.make_move — invalid moves
# ---------------------------------------------------------------------------

class TestMakeMoveInvalid:
    def test_empty_square_returns_false(self):
        game = make_empty_game()
        place_kings(game)
        game.update_opponent_moves()
        assert game.make_move((3, 3), (4, 3)) is False

    def test_wrong_color_returns_false(self):
        game = make_empty_game()
        place_kings(game)
        black_pawn = Pawn(False, (6, 0))
        game.board[6][0] = black_pawn
        game.update_opponent_moves()
        assert game.make_move((6, 0), (5, 0)) is False  # White's turn

    def test_illegal_destination_returns_false(self):
        game = make_empty_game()
        place_kings(game)
        pawn = Pawn(True, (1, 0))
        game.board[1][0] = pawn
        game.update_opponent_moves()
        assert game.make_move((1, 0), (5, 0)) is False  # Pawn can't jump 4 squares

    def test_turn_not_changed_on_invalid_move(self):
        game = make_empty_game()
        place_kings(game)
        game.update_opponent_moves()
        game.make_move((3, 3), (4, 3))
        assert game.white_turn is True


# ---------------------------------------------------------------------------
# Game.make_move — captures
# ---------------------------------------------------------------------------

class TestMakeMoveCapture:
    def test_capture_enemy_piece(self):
        game = make_empty_game()
        place_kings(game)
        white_rook = Rook(True, (4, 0))
        black_pawn = Pawn(False, (4, 5))
        game.board[4][0] = white_rook
        game.board[4][5] = black_pawn
        game.update_opponent_moves()
        result = game.make_move((4, 0), (4, 5))
        assert result is True
        assert game.board[4][5] is white_rook
        assert game.board[4][0] is None

    def test_cannot_capture_own_piece(self):
        game = make_empty_game()
        place_kings(game)
        white_rook = Rook(True, (4, 0))
        white_pawn = Pawn(True, (4, 5))
        game.board[4][0] = white_rook
        game.board[4][5] = white_pawn
        game.update_opponent_moves()
        assert game.make_move((4, 0), (4, 5)) is False


# ---------------------------------------------------------------------------
# Game.update_opponent_moves
# ---------------------------------------------------------------------------

class TestUpdateOpponentMoves:
    def test_opponent_moves_keyed_by_position(self):
        game = make_empty_game()
        place_kings(game)
        black_pawn = Pawn(False, (6, 3))
        game.board[6][3] = black_pawn
        game.update_opponent_moves()
        assert (6, 3) in game.opponent_moves

    def test_player_pieces_not_in_opponent_moves(self):
        game = make_empty_game()
        white_king, _ = place_kings(game)
        white_pawn = Pawn(True, (1, 3))
        game.board[1][3] = white_pawn
        game.update_opponent_moves()
        assert (1, 3) not in game.opponent_moves

    def test_opponent_moves_cleared_on_each_call(self):
        game = make_empty_game()
        place_kings(game)
        game.opponent_moves = {(0, 0): [(1, 0)]}
        game.update_opponent_moves()
        assert (0, 0) not in game.opponent_moves

    def test_opponent_moves_values_are_lists(self):
        game = make_empty_game()
        place_kings(game)
        black_pawn = Pawn(False, (6, 3))
        game.board[6][3] = black_pawn
        game.update_opponent_moves()
        assert isinstance(game.opponent_moves[(6, 3)], list)

    def test_returns_early_when_king_is_none(self):
        game = make_empty_game()
        # No kings placed; white_king is None
        game.update_opponent_moves()
        assert game.opponent_moves == {}


# ---------------------------------------------------------------------------
# Game.update_player_moves
# ---------------------------------------------------------------------------

class TestUpdatePlayerMoves:
    def test_player_moves_keyed_by_position(self):
        game = make_empty_game()
        place_kings(game)
        white_pawn = Pawn(True, (1, 3))
        game.board[1][3] = white_pawn
        game.update_opponent_moves()
        game.update_player_moves()
        assert (1, 3) in game.player_moves

    def test_opponent_pieces_not_in_player_moves(self):
        game = make_empty_game()
        place_kings(game)
        black_pawn = Pawn(False, (6, 3))
        game.board[6][3] = black_pawn
        game.update_opponent_moves()
        game.update_player_moves()
        assert (6, 3) not in game.player_moves

    def test_player_moves_values_are_lists(self):
        game = make_empty_game()
        place_kings(game)
        white_pawn = Pawn(True, (1, 3))
        game.board[1][3] = white_pawn
        game.update_opponent_moves()
        game.update_player_moves()
        assert isinstance(game.player_moves[(1, 3)], list)


# ---------------------------------------------------------------------------
# Game.check_pins
# ---------------------------------------------------------------------------

class TestCheckPins:
    def test_rook_pin_along_column(self):
        game = make_empty_game()
        white_king = King(True, (0, 4))
        black_rook = Rook(False, (7, 4))
        white_rook = Rook(True, (4, 4))  # Pinned between king and black rook
        game.board[0][4] = white_king
        game.board[7][4] = black_rook
        game.board[4][4] = white_rook
        game.white_king = white_king
        game.update_opponent_moves()
        assert white_rook.pinned != (0, 0)

    def test_pin_direction_is_toward_king(self):
        game = make_empty_game()
        white_king = King(True, (0, 4))
        black_rook = Rook(False, (7, 4))
        white_rook = Rook(True, (4, 4))
        game.board[0][4] = white_king
        game.board[7][4] = black_rook
        game.board[4][4] = white_rook
        game.white_king = white_king
        game.update_opponent_moves()
        # Pin direction should be along column (row axis)
        assert white_rook.pinned[1] == 0  # No column component

    def test_no_pin_when_two_pieces_between(self):
        game = make_empty_game()
        white_king = King(True, (0, 4))
        black_rook = Rook(False, (7, 4))
        white_rook1 = Rook(True, (3, 4))
        white_rook2 = Rook(True, (5, 4))
        game.board[0][4] = white_king
        game.board[7][4] = black_rook
        game.board[3][4] = white_rook1
        game.board[5][4] = white_rook2
        game.white_king = white_king
        game.update_opponent_moves()
        assert white_rook1.pinned == (0, 0)
        assert white_rook2.pinned == (0, 0)

    def test_no_pin_when_not_aligned(self):
        game = make_empty_game()
        white_king = King(True, (0, 4))
        black_rook = Rook(False, (7, 4))
        white_pawn = Pawn(True, (3, 0))  # Not in rook's line of attack
        game.board[0][4] = white_king
        game.board[7][4] = black_rook
        game.board[3][0] = white_pawn
        game.white_king = white_king
        game.update_opponent_moves()
        assert white_pawn.pinned == (0, 0)


# ---------------------------------------------------------------------------
# Game.add_checks
# ---------------------------------------------------------------------------

class TestAddChecks:
    def test_king_in_check_when_attacked(self):
        game = make_empty_game()
        white_king = King(True, (4, 4))
        black_rook = Rook(False, (4, 7))
        game.board[4][4] = white_king
        game.board[4][7] = black_rook
        game.white_king = white_king
        game.black_king = King(False, (7, 0))
        game.board[7][0] = game.black_king
        game.update_opponent_moves()
        assert white_king.is_checked()

    def test_king_not_in_check_when_clear(self):
        game = make_empty_game()
        white_king, _ = place_kings(game)
        game.update_opponent_moves()
        assert not white_king.is_checked()

    def test_checks_cleared_on_update(self):
        game = make_empty_game()
        white_king = King(True, (4, 4))
        white_king.add_check((4, 4))  # Manually set in check
        game.board[4][4] = white_king
        game.white_king = white_king
        black_king = King(False, (7, 0))
        game.board[7][0] = black_king
        game.black_king = black_king
        game.update_opponent_moves()
        assert not white_king.is_checked()


# ---------------------------------------------------------------------------
# Checkmate and stalemate detection
# ---------------------------------------------------------------------------

class TestCheckmateStalemate:
    def test_checkmate_flag_set(self):
        # Back-rank mate: black king at (7,0), white rooks control all escape squares
        game = make_empty_game()
        white_king = King(True, (0, 4))
        black_king = King(False, (7, 0))
        white_rook_a = Rook(True, (7, 1))  # Covers (7,1..7) and attacks king
        white_rook_b = Rook(True, (6, 7))  # Covers row 6
        game.board[0][4] = white_king
        game.board[7][0] = black_king
        game.board[7][1] = white_rook_a
        game.board[6][7] = white_rook_b
        game.white_king = white_king
        game.black_king = black_king
        # Simulate state after white's last move: black to move
        game.white_turn = False
        game.update_opponent_moves()
        game.update_player_moves()
        assert black_king.is_checked()
        assert game.player_moves.get(black_king.position, []) == []

    def test_stalemate_king_has_no_moves_and_not_in_check(self):
        # Stalemate: black king at (7,0), white queen covers all adjacent squares
        # without giving check
        game = make_empty_game()
        white_king = King(True, (0, 4))
        black_king = King(False, (7, 0))
        # Queen at (5,2) covers (6,1), (6,0), (7,1) blocking all escape
        white_queen = Queen(True, (5, 2))
        game.board[0][4] = white_king
        game.board[7][0] = black_king
        game.board[5][2] = white_queen
        game.white_king = white_king
        game.black_king = black_king
        game.white_turn = False
        game.update_opponent_moves()
        game.update_player_moves()
        assert not black_king.is_checked()
        assert game.player_moves.get(black_king.position, []) == []

    def test_make_move_sets_checkmate(self):
        # Construct a position where white's move delivers checkmate
        # Black king at (7,0), white rook at (7,1) attacks it, white rook at (5,7)
        # White plays rook from (5,7) to (6,7), sealing escape — checkmate
        game = make_empty_game()
        white_king = King(True, (0, 4))
        black_king = King(False, (7, 0))
        white_rook_a = Rook(True, (7, 1))  # Attacks black king on row 7
        white_rook_b = Rook(True, (5, 7))  # Will cover row 6
        game.board[0][4] = white_king
        game.board[7][0] = black_king
        game.board[7][1] = white_rook_a
        game.board[5][7] = white_rook_b
        game.white_king = white_king
        game.black_king = black_king
        game.update_opponent_moves()
        game.make_move((5, 7), (6, 7))
        assert game.checkmate is True

    def test_checkmate_false_when_king_can_escape(self):
        game = make_empty_game()
        place_kings(game)
        game.update_opponent_moves()
        game.update_player_moves()
        assert game.checkmate is False
        assert game.stalemate is False
