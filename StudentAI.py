from random import randint
from BoardClasses import Move
from BoardClasses import Board
from time import time
from copy import deepcopy
from math import sqrt, log
from operator import attrgetter
#from collections import defaultdict

opponent = {1:2, 2:1}

# def get_random_move(board, color):
#     '''
#     Given a board state and color, returns a random move.
#     '''
#     moves = board.get_all_possible_moves(color)
#     index = randint(0, len(moves) - 1)
#     inner_index = randint(0, len(moves[index]) - 1)
#     return moves[index][inner_index]

def random_index(container):
    index = randint(0, len(container) - 1)
    inner_index = randint(0, len(container[index]) - 1)
    return container[index][inner_index]

class TreeNode():
    def __init__(self, board, color, move, parent):
        self.board = deepcopy(board)
        self.color = color
        self.parent = parent
        self.visit_count = 1
        self.wins = 0
        self.ucb_value = 0
        self.children = None
        # Execute nodes' first move
        if move is not None:
            self.board.make_move(move, opponent[self.color])

        self.expansion()
        # Only create children if game is already over   

    def expansion(self):  
        self.children = dict()
        if self.board.is_win(opponent[self.color]) == 0:
            moves_list = self.board.get_all_possible_moves(self.color)
            for i in range(len(moves_list)):
                for j in range(len(moves_list[i])):
                    self.children[moves_list[i][j]] = None
 
    def backpropogate(self, win_for_parent):
        '''
        REcursively updates statistics for this node and all parents,
        given an outcome of the game.
        (1 is win for the parent, -1 is loss for the parent, 0 is tie,
        decimal values are based on heuristic)
        '''
        self.visit_count += 1
        
        if self.parent:
            self.parent.backpropogate(-win_for_parent)
                        
            if win_for_parent > 0:
                self.wins += win_for_parent
            # elif not win_for_parent:
            #     self.wins += 0.5
                     
            # calculate UCB value
            self.ucb_value = self.wins/self.visit_count + sqrt(2)*sqrt(log(self.parent.visit_count)/self.visit_count)
    
class StudentAI():
    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = 2
        self.mcts = MCTS(TreeNode(self.board, self.color, None, None))
        self.total_time_remaining = 89
        self.time_divisor = row * col * 0.5
        self.timed_move_count = 2
        
    def get_move(self, move) -> Move:
        '''
        prune tree with opponent move
        MCTS
        '''
        # Start timer
        start_time = time()
        
        # Check if opponent gave a turn and execute it
        if len(move) != 0:
            self.board.make_move(move, opponent[self.color])
            self.update_tree(move, opponent[self.color])
        # If first move of game, change self.color and make random move
        else:
            self.color = 1
            self.mcts.root = TreeNode(self.board, self.color, None, None)
            moves = self.board.get_all_possible_moves(self.color)
            move = random_index(moves)
            self.board.make_move(move, self.color)
            self.update_tree(move, self.color)
            return move
        
        # Check if only one move is possible
        moves = self.board.get_all_possible_moves(self.color)
        if len(moves) == 1 and len(moves[0]) == 1:
            move = moves[0][0]
            self.board.make_move(move, self.color)
            self.update_tree(move, self.color)
            
            return move
        
        # Set up time limit
        time_limit = self.total_time_remaining / self.time_divisor
        
        # MCTS
        move = self.mcts.search(time_limit)
        self.board.make_move(move, self.color)
        self.update_tree(move, self.color)
        
        
        # Change time divisor
        self.time_divisor -= 0.5 - 1/self.timed_move_count
        self.timed_move_count += 1
        
        # Decrement time remaining and return
        self.total_time_remaining -= time() - start_time
        return move
    
    def update_tree(self, move, color):
        """
        Updates tree root using Move given,
        either Move we just played or Move given by opponent.
        """
        for child in self.mcts.root.children.items():
            if str(move) == str(child[0]) and child[1] is not None:
                self.mcts.root = child[1]
                self.mcts.root.parent = None
                return

        self.mcts.root = TreeNode(self.board, opponent[color], None, None)
    
class MCTS():
    def __init__(self, root):
        self.root = root

    def best_child(self):
        '''
        Return the move with highest visit count.
        '''
        try:
            sorted_moves = sorted(self.root.children.items(), key=lambda x: x[1].visit_count, reverse=True)
            return sorted_moves[0][0]
        except:
            return random_index(sorted(self.root.children.items(), reverse=True))

    def search(self, time_limit):
        '''
        Performs Monte Carlo Tree Search until time runs out.
        Returns the best move.
        '''
        timeout = time() + time_limit
                
        while time() < timeout:
            # select node from the tree
            node = self.selection(self.root)
            
            # simulate outcome of the game
            board_copy = deepcopy(node.board)
            color_copy = node.color
            winner = board_copy.is_win(opponent[color_copy])
            
            while not winner:
                board_copy.make_move(random_index(board_copy.get_all_possible_moves(color_copy)), color_copy)
                winner = board_copy.is_win(color_copy)
                color_copy = opponent[color_copy]
    
            if winner == opponent[node.color]:
                wins = 1
            elif winner == node.color:
                wins = -1
            elif winner == -1:
                wins = 0
                
            # update values in tree
            node.backpropogate(wins)

        return self.best_child()
    
    def selection(self, node):
        '''
        Recursively traverses the tree to find a terminal node with the highest UCB value,
        then expands a new unexplored node.
        '''
        if len(node.children) == 0:
            return node
        if None not in node.children.values():
            sorted_children = sorted(node.children.values(), key=attrgetter('ucb_value'), reverse=True)
            return self.selection(sorted_children[0])
        for move, child in node.children.items():
            if child is None:
                node.children[move] = TreeNode(node.board, opponent[node.color], move, node)
                return node.children[move]
    
    
