# use math library if needed
import math
import sys
from collections import defaultdict


def get_child_boards(player, board):
    """
    Generate a list of succesor boards obtained by placing a disc 
    at the given board for a given player
   
    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that will place a disc on the board
    board: the current board instance

    Returns
    -------
    a list of (col, new_board) tuples,
    where col is the column in which a new disc is placed (left column has a 0 index), 
    and new_board is the resulting board instance
    """
    res = []
    for c in range(board.cols):
        if board.placeable(c):
            tmp_board = board.clone()
            tmp_board.place(player, c)
            res.append((c, tmp_board))
    return res


def evaluate(player, board):
    """
    This is a function to evaluate the advantage of the specific player at the
    given game board.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the specific player
    board: the board instance

    Returns
    -------
    score: float
        a scalar to evaluate the advantage of the specific player at the given
        game board
    """
    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    # Initialize the value of scores
    # [s0, s1, s2, s3, --s4--]
    # s0 for the case where all slots are empty in a 4-slot segment
    # s1 for the case where the player occupies one slot in a 4-slot line, the rest are empty
    # s2 for two slots occupied
    # s3 for three
    # s4 for four
    score = [0] * 5
    adv_score = [0] * 5

    # Initialize the weights
    # [w0, w1, w2, w3, --w4--]
    # w0 for s0, w1 for s1, w2 for s2, w3 for s3
    # w4 for s4
    weights = [0, 1, 4, 16, 1000]

    # Obtain all 4-slot segments on the board
    seg = []
    invalid_slot = -1
    left_revolved = [
        [invalid_slot] * r + board.row(r) + \
        [invalid_slot] * (board.rows - 1 - r) for r in range(board.rows)
    ]
    right_revolved = [
        [invalid_slot] * (board.rows - 1 - r) + board.row(r) + \
        [invalid_slot] * r for r in range(board.rows)
    ]
    for r in range(board.rows):
        # row
        row = board.row(r)
        for c in range(board.cols - 3):
            seg.append(row[c:c + 4])
    for c in range(board.cols):
        # col
        col = board.col(c)
        for r in range(board.rows - 3):
            seg.append(col[r:r + 4])
    for c in zip(*left_revolved):
        # slash
        for r in range(board.rows - 3):
            seg.append(c[r:r + 4])
    for c in zip(*right_revolved):
        # backslash
        for r in range(board.rows - 3):
            seg.append(c[r:r + 4])
    # compute score
    for s in seg:
        if invalid_slot in s:
            continue
        if adversary not in s:
            score[s.count(player)] += 1
        if player not in s:
            adv_score[s.count(adversary)] += 1
    reward = sum([s * w for s, w in zip(score, weights)])
    penalty = sum([s * w for s, w in zip(adv_score, weights)])
    return reward - penalty


def minimax(player, board, depth_limit):
    """
    Minimax algorithm with limited search depth.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1

    # ## Please finish the code below ##############################################
    # ##############################################################################
    # ## Sub-Function ##############################################################

    # ******************************************************************************
    # value*************************************************************************

    def value(player, board, depth_limit):
        """
        acting as a highway function for the minmax algorithm, the board game hasn't ended
        or the depth_limit is not 0 then run the max_value and min_value
        :param player: is the current player turn in the given game
        :param board: is the current board in which the player exist
        :param depth_limit: is the level in which we traversed in the tree
        :return the best possible placement in the current board
        """
        if depth_limit == 0 or board.terminal():
            if board.terminal():
                if board.who_wins() == max_player:
                    # if the board is in a terminal states and the max player
                    # has won then return an evaluation
                    return None, evaluate(max_player, board)
                elif board.who_wins() == next_player:
                    # if the board is in a terminal states and the other player
                    # has won then return an evaluation
                    return None, evaluate(max_player, board)
                else:  # if the board is terminal and there is no winner return 0 as there is no possible states
                    return None, evaluate(max_player, board)
            else:  # at depth 0 and the board is not in terminal state then return the score
                return None, evaluate(max_player, board)

        if max_player == player:  # if the current player is max_player
            return max_value(player, board, depth_limit)
        else:
            return min_value(player, board, depth_limit)

    # ******************************************************************************
    # Max value*********************************************************************
    def max_value(player, board, depth_limit):
        """
        find the maximum possible placement, score value of the given board

        :param player: the max player on the given call
        :param board: the current board state
        :param depth_limit: the depth in which player is on the tree
        :return: the maximum possible placement on the board and score
        """
        placement = None
        local_max = -sys.maxsize  # assign the local max to smallest number
        for i, move in get_child_boards(player, board):  # loop through all the child boards
            score = value(next_player, move, depth_limit - 1)[1]

            if score > local_max:  # if the current score is greater the local max
                placement = i  # set the placement to the column
                local_max = score  # set the local max to the current score

        return placement, local_max

    # *****************************************************************************
    # Min value********************************************************************
    def min_value(player, board, depth_limit):
        """
        find the minimum possible placement, score value of the given board

        :param player: the min player on the given call
        :param board: the current board state
        :param depth_limit: the depth in which player is on the tree
        :return: the minimum possible placement on the board and score
        """
        placement = None
        local_min = sys.maxsize
        for i, move in get_child_boards(player, board):
            score = value(max_player, move, depth_limit - 1)[1]

            if score < local_min:  # if the current score is less the local min
                placement = i  # set the placement to the column
                local_min = score  # set the local min to the current score

        return placement, local_min

    ###############################################################################
    ###############################################################################

    return value(player, board, depth_limit)[0]


def alphabeta(player, board, depth_limit):
    """
    Minimax algorithm with alpha-beta pruning.

     Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    alpha: float
    beta: float
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1

    # ## Please finish the code below ##############################################
    # ##############################################################################
    # ## Sub-Function ##############################################################

    # ******************************************************************************
    # value*************************************************************************
    def value(player, board, depth, alpha, beta):
        """
        acting as a highway function for the expected-max algorithm, the board game hasn't ended
        or the depth_limit is not 0 then run the max_value and min_value
        :param player: is the current player turn in the given game
        :param board: is the current board in which the player exist
        :param depth: is the level in which we traversed in the tree
        :param alpha: Initially, alpha is negative infinity as we transcend through max_value we will update
                      and we will prune nodes given we have a alpha >= beta
        :param beta:  Initially, positive infinity as we transcend through min_value we will update
                      and we will prune nodes given we have a alpha >= beta
        :return: the maximum possible placement on the board
        """

        if depth == 0 or board.terminal():
            if board.terminal():

                if board.who_wins() == next_player:
                    # if the board is in a terminal states and the other player
                    # has won then return an evaluation
                    return None, evaluate(max_player, board)

                elif board.who_wins() == max_player:
                    return None, evaluate(max_player, board)

                else:  # if the boarqd is terminal and there is no winner return 0 as there is no possible states
                    return None, evaluate(max_player, board)
            else:  # at depth 0 and the board is not in terminal state then return the score
                return None, evaluate(max_player, board)

        else:
            if max_player == player:
                return max_value(player, board, depth, alpha, beta)
            else:
                return min_value(player, board, depth, alpha, beta)

    # ******************************************************************************
    # Max value*********************************************************************
    def max_value(player_max, board_max, depth, alpha, beta):
        """
        find the maximum possible placement, score value of the given board

        :param player_max: the max player on the given call
        :param board_max: the current board state
        :param depth: the depth in which player is on the tree
        :param alpha: Initially, alpha is negative infinity as we transcend through max_value we will update
                      and we will prune nodes given we have a alpha >= beta
        :param beta:  Initially, positive infinity as we transcend through min_value we will update
                      and we will prune nodes given we have a alpha >= beta
        :return: the maximum possible placement on the board
        """
        local_max = -sys.maxsize
        placement = None
        # dict = defaultdict(list)  # --TEST--
        for i, move in get_child_boards(player_max, board_max):
            score = value(next_player, move, depth - 1, alpha, beta)[1]

            # **********************************
            # TESTING***************************
            # dict[str(score)].append(i)
            # **********************************

            if score > local_max:  # if the current score is greater the local max
                placement = i  # set the placement to the column
                local_max = score  # set the local max to the current score

            alpha = max(alpha, score)
            if alpha >= beta:  # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
                break  # coped from the wiki page Alpha–beta pruning

        # print("max:", dict)  # TESTING
        return placement, local_max

    # *****************************************************************************
    # Min value********************************************************************
    def min_value(min_player, board_min, depth, alpha, beta):
        """
        find the minimum possible placement, score value of the given board

        :param beta:
        :param alpha:
        :param min_player: the min player on the given call
        :param board_min: the current board state
        :param depth: the depth in which player is on the tree
        :return: the minimum possible placement on the board
        """

        placement = None
        local_min = sys.maxsize
        # list_min = [] --TEST--
        for i, move in get_child_boards(min_player, board_min):
            score = value(max_player, move, depth - 1, alpha, beta)[1]

            # **********************************
            # TESTING***************************
            # list_min.append(score) --TEST--
            # **********************************

            if score < local_min:  # if the current score is less the local min
                placement = i  # set the placement to the column
                local_min = score  # set the local min to the current score

            beta = min(beta, score)
            if beta <= alpha:  # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
                break  # coped from the wiki page Alpha–beta pruning

        # print("min: ", list_min) # --TEST--
        return placement, local_min

    ###############################################################################
    ###############################################################################

    return value(player, board, depth_limit, -sys.maxsize, sys.maxsize)[0]


def expectimax(player, board, depth_limit):
    """
    Expectimax algorithm.
    We assume that the adversary of the initial player chooses actions
    uniformly at random.
    Say that it is the turn for Player 1 when the function is called initially,
    then, during search, Player 2 is assumed to pick actions uniformly at
    random.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """

    max_player = player
    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1

    # ## Please finish the code below ##############################################
    # ##############################################################################
    # ## Sub-Function ##############################################################

    # *****************************************************************************
    # Value********************************************************************
    def value(player, board, depth_limit):
        """
        acting as a highway function for the expected-max algorithm, the board game hasn't ended
        or the depth_limit is not 0 then run the max_value and min_value
        :param player: is the current player turn in the given game
        :param board: is the current board in which the player exist
        :param depth_limit: is the level in which we traversed in the tree
        """
        if depth_limit == 0 or board.terminal():
            if board.terminal():
                if board.who_wins() == max_player:
                    return None, evaluate(max_player, board)
                elif board.who_wins() == next_player:
                    # if the board is in a terminal states and the other player
                    # has won then return an evaluation
                    return None, evaluate(max_player, board)
                else:  # if the board is terminal and there is no winner return 0 as there is no possible states
                    return None, evaluate(max_player, board)
            else:  # at depth 0 and the board is not in terminal state then return the score
                return None, evaluate(max_player, board)

        if max_player == player:
            return max_value(player, board, depth_limit)
        else:
            return min_value(player, board, depth_limit)

    # *****************************************************************************
    # Max value********************************************************************
    def max_value(player, board, depth_limit):
        """
        find the maximum possible placement, score value of the given board

        :param player: the max player on the given call
        :param board: the current board state
        :param depth_limit: the depth in which player is on the tree
        :return: the maximum possible placement on the board
        """
        local_max = -sys.maxsize
        placement = None
        for i, move in get_child_boards(player, board):
            score = value(next_player, move, depth_limit - 1)[1]

            if score > local_max:  # if the current score is greater the local max
                placement = i  # set the placement to the column
                local_max = score  # set the local max to the current score

        return placement, local_max

    # *****************************************************************************
    # Min value********************************************************************
    def min_value(player, board, depth_limit):
        """
        getting the expected value of the given distribution of given moves for the
        adversely agent

        :param player: the min player on the given call
        :param board: the current board state
        :param depth_limit: the depth in which player is on the tree
        :return: the minimum possible placement on the board
        """
        moves = get_child_boards(player, board)  # get the list of moves the adversely agent can make
        p = 1 / len(moves)  # the uniform probability of the moves
        expected_value = 0  # expected value of the given min
        for i, move in moves:
            expected_value += p * value(max_player, move, depth_limit - 1)[1] # summation of
            # E[x] = p(X=move_0) * score + ... + p(X=move_i) * score
        return None, expected_value

    ###############################################################################
    ###############################################################################

    return value(player, board, depth_limit)[0]


if __name__ == "__main__":
    from game_gui import GUI
    import tkinter

    algs = {
        "Minimax": minimax,
        "Alpha-beta pruning": alphabeta,
        "Expectimax": expectimax
    }

    root = tkinter.Tk()
    GUI(algs, root)
    root.mainloop()
