class TicTacToe:
    def __init__(self, ai_player="X", opponent_player="O", starting_player="X"):
        self.ai_player = ai_player
        self.opponent_player = opponent_player
        self.board = [""] * 9  # 3x3 board
        self.current_player = starting_player # Starting player, options are "X" or "O"
        self.winner = None
        self.moves = 0 # Total moves made
        self.wins = [
            [0,1,2], [3,4,5], [6,7,8],  # rows
            [0,3,6], [1,4,7], [2,5,8],  # cols
            [0,4,8], [2,4,6]            # diags
        ]

    def get_state(self):
        return {
            "board": self.board,
            "current_player": self.current_player,
            "winner": self.winner,
            "moves": self.moves
        }

    # Make a move on the board and update gamestate
    # Returns True if the move was successful, False if it was invalid
    def make_move(self, position):
        if self.winner or self.board[position] != "":
            return False  # Invalid move

        self.board[position] = self.current_player # place the current player's piece
        self.moves += 1 # a move was made
        if self.check_winner():
            self.winner = self.current_player # update the winner if this move wins the game
        elif self.moves == 9:
            self.winner = "Draw" # if all squares are full adn there's no winner it's a draw
        else: # switch players
            self.current_player = "O" if self.current_player == "X" else "X"
        return True

    # Check if one of the players won
    def check_winner(self):
        for a, b, c in self.wins:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return True
        return False
    
    def reset(self):
        self.__init__()

    # Evaluate the game state for AI purposes
    def evaluate(self, player, opponent, newBoard):
        score = 0
        for a, b, c in self.wins:
            # check if player won
            if player == self.board[a] == self.board[b] == self.board[c]:
                return 10
            # check if opponent won
            if opponent == self.board[a] == self.board[b] == self.board[c]:
                return -10
            
            # check how many player and opponent pieces are in the line
            pcount = sum(1 for i in [self.board[a], self.board[b], self.board[c]] if i == player)
            ocount = sum(1 for i in [self.board[a], self.board[b], self.board[c]] if i == opponent)
            if pcount == 2 and ocount == 0: #almost a win for player
                score += 1
            elif ocount == 2 and pcount == 0: # almost a win for opponent
                score -= 1
        return score
    
    # Minimax algorithm for AI move selection
    def minimax(self, board, depth, is_maximizing, player, opponent):
        score = self.evaluate(player, opponent, board)
        if score == 10 or score == -10 or depth == 0 or "" not in board:
            return score, None

        if is_maximizing:
            best = -float('inf')
            best_move = -1
            for i in range(9):
                if board[i] == "":
                    board[i] = player
                    value, move = self.minimax(board, depth - 1, False, player, opponent)
                    board[i] = ""
                    if value > best:
                        best = value
                        best_move = i
            return (best, best_move)
        else:
            best = float('inf')
            best_move = -1
            for i in range(9):
                if board[i] == "":
                    board[i] = opponent
                    value, move = self.minimax(board, depth - 1, True, player, opponent)
                    board[i] = ""
                    if value < best:
                        best = value
                        best_move = i
            return (best, best_move)
        
    def ai_move(self):
        best_score, best_move = self.minimax(self.board, 9, True, self.ai_player, self.opponent_player)
        if best_move != -1:
            self.make_move(best_move)
        return best_move
    
        
            