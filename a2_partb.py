# Main Author: Mahdi Zanganeh

# This function duplicates and returns the board. You may find this useful
import time 


def copy_board(board):
    current_board = []
    height = len(board)
    for i in range(height):
        current_board.append(board[i].copy())
    return current_board


# this function is your evaluation function for the board
def evaluate_board(board, player):
    """
    Evaluates the board

    Args:
    Board: the grid of the game that needs evaluation.
    player (int, 1 or -1): Indicates if its player1(1) or player(2)

    Returns:
    Score (int): Score of the corresponding player
    """
    p1_score = sum(cell for row in board for cell in row if cell > 0)
    p2_score = sum(abs(cell) for row in board for cell in row if cell < 0)
    if p1_score and p2_score:
        return 0
    elif player > 0:
        return 1000 if p1_score > p2_score else (-1000 if p1_score < p2_score else p1_score)
    else:
        return 1000 if p2_score > p1_score else (-1000 if p2_score < p1_score else p2_score)


class GameTree:
    """Represents a game tree for a turn-based game."""

    class Node:
        """Represents a node in the game tree."""

        def __init__(self, board, depth, player, tree_height=4, move=None):
            """
            Initializes a node in the game tree.

            Args:
                board (list of list): The game board state.
                depth (int): The depth of the node in the tree.
                player (int): The player to make the next move.
                tree_height (int): The maximum height of the tree.
                move (tuple): The move that led to this node.
            """
            self.board = board
            self.depth = depth
            self.player = player
            self.tree_height = tree_height
            self.children = []
            self.move = move

            if depth < tree_height and not self.is_terminal_state():
                self.generate_children()

        def is_terminal_state(self):
            """
            Checks if the current state is a terminal state.

            Returns:
                bool: True if the state is terminal, False otherwise.
            """
            if all((cell >= 0 if self.player == 1 else cell <= 0) for row in self.board for cell in row if cell != 0):
                return True
            if all((cell <= 0 if self.player == 1 else cell >= 0) for row in self.board for cell in row if cell != 0):
                return True
            return False

        def generate_children(self):
            """Generates child nodes for possible moves."""
            next_player = -self.player

            for row_index, row in enumerate(self.board):
                for col_index, cell in enumerate(row):
                    if cell == 0 or cell * self.player > 0:
                        new_board = copy_board(self.board)
                        new_board[row_index][col_index] += self.player
                        new_child = GameTree.Node(new_board, self.depth + 1, next_player, self.tree_height,
                                                  move=(row_index, col_index))
                        self.children.append(new_child)

    def __init__(self, board, player, tree_height=4):
        """
        Initializes the game tree.

        Args:
            board (list of list): The initial game board state.
            player (int): The player to make the first move.
            tree_height (int): The maximum height of the tree.
        """
        self.root = GameTree.Node(copy_board(board), 0, player, tree_height)
        self.player = player
        self.move_history = []
        self.high_scores = []  # List to store high scores #Mehrnoosh added
        self.start_time = None  # Initialize start time #Mehrnoosh added
        self.end_time = None  # Initialize end time #Mehrnoosh added

    def minimax(self, node, depth, maximizingPlayer):
        """
        Performs the minimax algorithm to find the best move.

        Args:
            node (Node): The current node in the game tree.
            depth (int): The depth of the node in the tree.
            maximizingPlayer (bool): Indicates if the current player is maximizing.

        Returns:
            int: The evaluated score of the best move.
        """
        if depth == 0 or node.is_terminal_state():
            return evaluate_board(node.board, self.player)

        if maximizingPlayer:
            best_value = float('-inf')
            for child in node.children:
                value = self.minimax(child, depth - 1, False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for child in node.children:
                value = self.minimax(child, depth - 1, True)
                best_value = min(best_value, value)
            return best_value

    def get_move(self):
        """
        Gets the best move using the minimax algorithm.

        Returns:
            tuple: The best move coordinates.
        """
        best_score = float('-inf')
        best_move = None

        for child in self.root.children:
            score = self.minimax(child, self.root.tree_height - 1, False)
            if score > best_score:
                best_score = score
                best_move = child.move

        if best_move is not None:
            return (best_move[0], best_move[1] + 1)

        for row in range(len(self.root.board)):
            for col in range(len(self.root.board[row])):
                if self.is_valid_move(row, col):
                    return (row, col + 1)

        raise Exception("No valid moves available")

    def clear_tree(self):
        """Clears the entire game tree."""
        def clear_node(node):
            for child in node.children:
                clear_node(child)
            node.children = []

        clear_node(self.root)
        self.root = None
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        # Added by Mehrnoosh ( Part C )

    def undo_last_move(self):  # UndoLastMove Feature ( reverts the game to a state before that human player's last move )
        """
        Undo the last move made by a human player.
        """
        if self.move_history:
            last_move = self.move_history.pop()
            row, col = last_move
            self.root.board[row][col] = 0
        else:
            raise Exception("No moves to undo")

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def update_high_scores(self, score):  # HighScore Feature  ( Keep track of the highest scores achieved by players and display them in a high score table. )
        """Update the high scores list with a new score."""
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)  # Sort the high scores in descending order

    def display_high_scores(self):
        """Display the high scores in a formatted table."""
        print("High Scores:")
        print("Rank\tScore")
        for i, score in enumerate(self.high_scores, start=1):
            print(f"{i}\t{score}")

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def start_timer(self):  # Timer Feature ( Players must match gems within a certain time limit to progress or earn bonus points.)
        """Start the timer."""
        self.start_time = time.time()

    def stop_timer(self):
        """Stop the timer."""
        self.end_time = time.time()

    def get_elapsed_time(self):
        """Get the elapsed time in seconds."""
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        else:
            return 0
