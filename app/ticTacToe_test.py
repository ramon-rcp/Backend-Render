from ticTacToe import TicTacToe

def test_ai_wins_when_possible():
    game = TicTacToe(ai_player="X", opponent_player="O", starting_player="X")
    # X | X | 
    # O | O | 
    #   |   | 
    game.board = ["X", "X", "", "O", "O", "", "", "", ""]
    game.current_player = "X"
    score, move = game.minimax(game.board[:], 9, True, "X", "O")
    assert move == 2, f"AI should win at position 2, got {move}"

def test_ai_blocks_opponent():
    game = TicTacToe(ai_player="O", opponent_player="X", starting_player="O")
    # X | X | 
    # O |   | 
    #   |   | 
    game.board = ["X", "X", "", "O", "", "", "", "", ""]
    game.current_player = "O"
    score, move = game.minimax(game.board[:], 9, True, "O", "X")
    assert move == 2, f"AI should block at position 2, got {move}"

def test_draw_scenario():
    game = TicTacToe(ai_player="X", opponent_player="O", starting_player="X")
    # X | O | X
    # X | O | O
    # O | X | 
    game.board = ["X", "O", "X", "X", "O", "O", "O", "X", ""]
    game.current_player = "X"
    score, move = game.minimax(game.board[:], 9, True, "X", "O")
    assert move == 8, f"AI should play last move at position 8, got {move}"

def run_tests():
    test_ai_wins_when_possible()
    print("test_ai_wins_when_possible passed.")
    test_ai_blocks_opponent()
    print("test_ai_blocks_opponent passed.")
    test_draw_scenario()
    print("test_draw_scenario passed.")

def main():
    print("Welcome to Tic Tac Toe Test!")
    game = TicTacToe()
    game.make_move(0)
    game.make_move(1)
    game.make_move(2)
    #########
    # x o x #
    # - - - #
    # - - - #
    #########
    print("Score for X after 3 moves:", game.evaluate("X", "O", game.board))
    game.make_move(3)
    game.make_move(4)
    #########
    # x o x #
    # o x - #
    # - - - #
    #########
    print("Score for X after 5 moves:", game.evaluate("X", "O", game.board))
    game.reset()
    game.make_move(1)
    game.make_move(0)
    game.make_move(2)
    game.make_move(3)
    game.make_move(4)
    #########
    # o x x #
    # o x - #
    # - - - #
    #########
    print("Score for X after 5 moves:", game.evaluate("X", "O", game.board))


if __name__ == "__main__":
    main()
    run_tests()
    print("All tests passed!")