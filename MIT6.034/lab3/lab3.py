# 6.034 Fall 2010 Lab 3: Games
# Name: Xin Lin
# Email: linxin025@gmail.com

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    if board.is_game_over():
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        
        for chain in board.chain_cells(board.get_current_player_id()):
            score += 2**(len(chain) - 1)
        
        for chain in board.chain_cells(board.get_other_player_id()):
            score -= 2**(len(chain) - 1)

    return score

## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.

def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves, is_terminal_fn=is_terminal):
    best_val = None

    for move, new_board in get_next_moves_fn(board):
        val = -1 * alpha_beta_search_helper(new_board, depth - 1, eval_fn, NEG_INFINITY, INFINITY, get_next_moves_fn, is_terminal_fn)
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)

    return best_val[1]

def alpha_beta_search_helper(board, depth, eval_fn, alpha, beta, get_next_moves_fn=get_all_next_moves, is_terminal_fn=is_terminal):
    if is_terminal_fn(depth, board):
        return eval_fn(board)
    
    best_val = NEG_INFINITY
    
    for move, new_board in get_next_moves_fn(board):
        best_val = max(best_val, -1 * alpha_beta_search_helper(new_board, depth - 1, eval_fn, -1 * beta, -1 * alpha, get_next_moves_fn, is_terminal_fn))
        alpha = max(alpha, best_val)
        if beta <= alpha:
            break

    return best_val

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.
def is_column_chain(chain):
    col_pos = None
    for pos in chain:
        if col_pos == None:
            col_pos = pos[1]
        else:
            if col_pos != pos[1]:
                return False
    return True

# From Left to Right
def is_row_left(chain):
    row_pos = None
    col_pos = None
    for pos in chain:
        if row_pos == None and col_pos == None:
            row_pos = pos[0]
            col_pos = pos[1]
        else:
            col_diff = pos[1] - col_pos
            if row_pos == pos[0] and col_diff == 1:
                row_pos = pos[0]
                col_pos = pos[1]
            else:
                return False
    return True

# From Right to Left
def is_row_right(chain):
    row_pos = None
    col_pos = None
    for pos in chain:
        if row_pos == None and col_pos == None:
            row_pos = pos[0]
            col_pos = pos[1]
        else:
            col_diff = pos[1] - col_pos
            if row_pos == pos[0] and col_diff == -1:
                row_pos = pos[0]
                col_pos = pos[1]
            else:
                return False
    return True

# From Bottom Left to Upper Right
def is_diagonal_left_up(chain):
    row_pos = None
    col_pos = None
    for pos in chain:
        if row_pos == None and col_pos == None:
            row_pos = pos[0]
            col_pos = pos[1]
        else:
            row_diff = pos[0] - row_pos
            col_diff = pos[1] - col_pos
            if row_diff == -1 and col_diff == 1:
                row_pos = pos[0]
                col_pos = pos[1]
            else:
                return False
    return True

# From Upper Left to Bottom Right
def is_diagonal_left_down(chain):
    row_pos = None
    col_pos = None
    for pos in chain:
        if row_pos == None and col_pos == None:
            row_pos = pos[0]
            col_pos = pos[1]
        else:
            row_diff = pos[0] - row_pos
            col_diff = pos[1] - col_pos
            if row_diff == 1 and col_diff == 1:
                row_pos = pos[0]
                col_pos = pos[1]
            else:
                return False
    return True

# From Bottom Right to Upper Left
def is_diagonal_right_up(chain):
    row_pos = None
    col_pos = None
    for pos in chain:
        if row_pos == None and col_pos == None:
            row_pos = pos[0]
            col_pos = pos[1]
        else:
            row_diff = pos[0] - row_pos
            col_diff = pos[1] - col_pos
            if row_diff == -1 and col_diff == -1:
                row_pos = pos[0]
                col_pos = pos[1]
            else:
                return False
    return True

# From Upper Right to Bottom Left
def is_diagonal_right_down(chain):
    row_pos = None
    col_pos = None
    for pos in chain:
        if row_pos == None and col_pos == None:
            row_pos = pos[0]
            col_pos = pos[1]
        else:
            row_diff = pos[0] - row_pos
            col_diff = pos[1] - col_pos
            if row_diff == 1 and col_diff == -1:
                row_pos = pos[0]
                col_pos = pos[1]
            else:
                return False
    return True

def get_chain_score(board, chain):
    feature_4_score_board = [14, 17, 22, 30, 22, 17, 14]
    feature_3_score_board = [0, 10, 20, 25, 40, 55]
    
    count = len(chain)
    # Handle Feature 4
    if count == 1:
        return feature_4_score_board[chain[0][1]]

    if is_row_left(chain):
    # row left chain
        #print "row left chain: " + str(chain)[1:-1] 
        # Handle Feature 3
        if count == 3:
            is_front_available = False
            if chain[0][1] - 1 >= 0 and board.get_height_of_column(chain[0][1] - 1) == chain[0][0] - 1:
                is_front_available = True
            
            is_back_available = False
            if chain[-1][1] + 1 < board.board_width and board.get_height_of_column(chain[-1][1] + 1) == chain[-1][0] - 1:
                is_back_available = True
            
            if is_front_available and is_back_available:
                return 1000
            elif (not is_front_available and is_back_available) or (is_front_available and not is_back_available):
                return 600
            else:
                return 0
        # Handle Feature 2
        elif count == 2:
            local_count = 0
            col = chain[-1][1] + 1
            while col < board.board_width:
                if board.get_cell(chain[-1][0], col) == 0:
                    if chain[-1][0] == 5 or board.get_height_of_column(col) == chain[-1][0] - 1:
                        local_count += 1
                else:
                    break
                col += 1

            col = chain[0][1] - 1
            while col >= 0:
                if board.get_cell(chain[0][0], col) == 0:
                    if chain[0][0] == 5 or board.get_height_of_column(col) == chain[0][0] - 1:
                        local_count += 1
                else:
                    break
                col -= 1
            
            max_count = 0
            max_count = max(max_count, local_count)
            return feature_3_score_board[max_count]
        else:
        # Handle Exception Case
            return 0
    elif is_row_right(chain):
    # row right chain
        #print "row right chain: " + str(chain)[1:-1]
        if count == 3:
            is_front_available = False
            if chain[-1][1] - 1 >= 0 and board.get_height_of_column(chain[-1][1] - 1) == chain[-1][0] - 1:
                is_front_available = True
            
            is_back_available = False
            if chain[0][1] + 1 < board.board_width and board.get_height_of_column(chain[0][1] + 1) == chain[0][0] - 1:
                is_back_available = True
            
            if is_front_available and is_back_available:
                return 1000
            elif (not is_front_available and is_back_available) or (is_front_available and not is_back_available):
                return 600
            else:
                return 0
        elif count == 2:
            local_count = 0
            col = chain[0][1] + 1
            while col < board.board_width:
                if board.get_cell(chain[0][0], col) == 0:
                    if chain[0][0] == 5 or board.get_height_of_column(col) == chain[0][0] - 1:
                        local_count += 1
                else:
                    break
                col += 1

            col = chain[-1][1] - 1
            while col >= 0:
                if board.get_cell(chain[-1][0], col) == 0:
                    if chain[-1][0] == 5 or board.get_height_of_column(col) == chain[-1][0] - 1:
                        local_count += 1
                else:
                    break
                col -= 1
            
            max_count = 0
            max_count = max(max_count, local_count)
            return feature_3_score_board[max_count]
        else:
            return 0
    elif is_column_chain(chain):
    # column chain
        #print "column chain: " + str(chain)[1:-1] 
        if count == 3:
            if (chain[-1][0] + 1 < board.board_height and board.get_cell(chain[-1][0] + 1, chain[-1][1]) == 0) or (chain[-1][0] - 1 >= 0 and board.get_cell(chain[-1][0] - 1, chain[-1][1]) == 0):
                return 600
            else:
                return 0
        elif count == 2:
            row = chain[-1][0] - 1
            local_count = 0
            while row >= 0:
                if board.get_cell(row, chain[-1][1]) == 0:
                    local_count += 1
                else:
                    break
                row -= 1
            
            max_count = 0
            max_count = max(max_count, local_count)
            return feature_3_score_board[max_count]
        else:
            return 0
    else:
    # diagonal chain
        if is_diagonal_left_up(chain):
            #print "diagonal left chain UP: " + str(chain)[1:-1] 
            return 0
        elif is_diagonal_left_down(chain):
            #print "diagonal left chain DOWN: " + str(chain)[1:-1]
            return 0
        elif is_diagonal_right_up(chain):
            #print "diagonal right chain UP: " + str(chain)[1:-1]
            return 0
        elif is_diagonal_right_down(chain):
            #print "diagonal right chain DOWN: " + str(chain)[1:-1]
            return 0
        else:
            return 0

def better_evaluate(board):
    """
    Here, we are looking for 4 kinds of different features and grade each of them 
    separately. The grading rules is as following:
    
    Feature 1: (Four chessmen connected horizontally, vertically or diagonally)
            grade: 1000

    Feature 2: (Three chessmen connected horizontally, vertically or diagonally)
            grade:
                1. (1000) A move can be made on either immediately adjacent columns. 
                2. (600) A move can only be made on one of the immediately adjacent columns. 

    Feature 3: (Two chessmen connected horizontally, vertically or diagonally)
            grade:
                1. (250) A same chessman can be found a square away from two connected men.
                2. A move can only be made on one of the immediately adjacent columns. 
                  (The value depends on the number of available squares along the direction till an unavailable square is met.)
                   -- (55) 5
                   -- (40) 4
                   -- (25) 3
                   -- (20) 2
                   -- (10) 1

    Feature 4: (One chessmen connected horizontally, vertically or diagonally)
            grade:
                1. (30) In column 3
                2. (14)  In column 0 or 6
                3. (17)  In column 1 or 5
                4. (22) In column 2 or 4
    """
    if board.is_game_over():
        score = -1000
    else:
        score = 0
        
        # Handle Feature 1, which is absolute win
        if board.longest_chain(board.get_current_player_id()) >= 4:
            return 1000
        else:
            for chain in board.chain_cells(board.get_current_player_id()):
                score += get_chain_score(board, chain)

            for chain in board.chain_cells(board.get_other_player_id()):
                score -= get_chain_score(board, chain)
            
            score_board = [[3, 4,  5,  7,  5, 4, 3],
                           [4, 6,  9, 16,  9, 6, 4],
                           [5, 9, 21, 23, 21, 9, 5],
                           [5, 9, 21, 23, 21, 9, 5],
                           [4, 6,  9, 16,  9, 6, 4],
                           [3, 4,  5,  7,  5, 4, 3]]

            for row in range(6):
                for col in range(7):
                    if board.get_cell(row, col) == board.get_current_player_id():
                        score += score_board[row][col]
                    elif board.get_cell(row, col) == board.get_other_player_id():
                        score -= score_board[row][col]

    return score
    
# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
#better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)

## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = True

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "18"
WHAT_I_FOUND_INTERESTING = "Understanding the initial minimax function is quite challenging."
WHAT_I_FOUND_BORING = "Nothing"
NAME = "Xin Lin"
EMAIL = "linxin025@gmail.com"

