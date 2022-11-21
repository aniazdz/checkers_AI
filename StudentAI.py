from random import randint
from BoardClasses import Move
from BoardClasses import Board
from time import time
from copy import deepcopy
from math import sqrt, log
from operator import attrgetter
#from collections import defaultdict

opponent = {1:2, 2:1}

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
        if move is not None:
            self.board.make_move(move, opponent[self.color])
        self.expansion()

    def expansion(self):  
        self.children = dict()
        if self.board.is_win(opponent[self.color]) == 0:
            moves_list = self.board.get_all_possible_moves(self.color)
            for i in range(len(moves_list)):
                for j in range(len(moves_list[i])):
                    self.children[moves_list[i][j]] = None
 
    def backpropogate(self, win_for_parent):
        self.visit_count += 1
        
        if self.parent:
            self.parent.backpropogate(-win_for_parent)
                        
            if win_for_parent > 0:
                self.wins += win_for_parent 
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
        start_time = time()
        
        if len(move) != 0:
            self.board.make_move(move, opponent[self.color])
            self.update_tree(move, opponent[self.color])
        else:
            self.color = 1
            self.mcts.root = TreeNode(self.board, self.color, None, None)
            moves = self.board.get_all_possible_moves(self.color)
            move = random_index(moves)
            self.board.make_move(move, self.color)
            self.update_tree(move, self.color)
            return move
        
        moves = self.board.get_all_possible_moves(self.color)
        if len(moves) == 1 and len(moves[0]) == 1:
            move = moves[0][0]
            self.board.make_move(move, self.color)
            self.update_tree(move, self.color)
            return move
        
        time_limit = self.total_time_remaining / self.time_divisor

        move = self.mcts.search(time_limit)
        self.board.make_move(move, self.color)
        self.update_tree(move, self.color)
        
        self.time_divisor -= 0.5 - 1/self.timed_move_count
        self.timed_move_count += 1
        self.total_time_remaining -= time() - start_time
        return move
    
    def update_tree(self, move, color):
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
        try:
            sorted_moves = sorted(self.root.children.items(), key=lambda x: x[1].visit_count, reverse=True)
            return sorted_moves[0][0]
        except:
            return random_index(self.root.children.items())

    def search(self, time_limit):
        timeout = time() + time_limit
                
        while time() < timeout:
            node = self.selection(self.root)
            board_copy = deepcopy(node.board)
            color_copy = node.color
            self.simulation(board, color)
            
        return self.best_child()
    
    def simulation(self, board, color):
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
            node.backpropogate(wins)

    
    def selection(self, node):
        if len(node.children) == 0:
            return node
        if None not in node.children.values():
            sorted_children = sorted(node.children.values(), key=attrgetter('ucb_value'), reverse=True)
            return self.selection(sorted_children[0])
        for move, child in node.children.items():
            if child is None:
                node.children[move] = TreeNode(node.board, opponent[node.color], move, node)
                return node.children[move]
    
    
