from random import randint
import copy
import math
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class TreeNode():
    # class for TreeNode object
        # keeps track of all basic attributes that a tree node should has
    def __init__(self, color, move=None):
        self.color = color
        self.move = move
        self.value = None
        self.children = []

class Tree():
    # class for Tree object
    # -> main purpose is create and print and possibly update
        def __init__(self, root, board, depth=5):
            self.root = root# intialize tree from root
            self.board = board
            self.depth = depth
            self.create_tree(root, 0)

        def create_tree(self, node, depth):
            # create tree up to specified depth to pick next path ---> simulate step?

            # select and expand nodes
            if (self.depth == depth):
                return
            for c in self.board.get_all_possible_moves(self.root.color):
                self.root.children.append(create_tree(treeNode, depth + 1))
            

        def print_tree(self, node, level):
            print(" " * level, node.value, "->", node.move)
            if len(node.children) != 0:  # as long as node has children --> recurse for printing
                for c in node.children:
                    self.print_tree(c, node + 1)

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p   # rows containing pieces
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    
    def heuristic(self, c):
        if self.color == 1:
            color = 'B'
        else:
            color = 'W'
        
        if color == 'B':
            return c.black_count - c.white_count
        else:
            return c.white_count - c.black_count

    def evaluation(self, moves):
        move_list = []
        prev = 0
        move = moves[0][0]
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                c = copy.deepcopy(self.board)
                c.make_move(moves[i][j], self.color)
                eval = self.heuristic(c)
                if eval > prev:
                    move = moves[i][j]
                    prev = eval
        return move
    
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        
        moves = self.board.get_all_possible_moves(self.color)
        move = self.evaluation(moves)
        
        self.board.make_move(move,self.color)

        root = TreeNode(self.opponent[self.color])
        
        tree = Tree(root, self.board)
        

        return move

#     def minimax_search(self, game, state): #game - moves? state- board?
#         self.color = #self.board.
#         value, move = self.maxValue(game, state)
        
#         return move
    
#     def maxValue(self, game, state):
#         if (0==k): #k - depth
#             return evaluation(moves)
#         v = math.inf
#         for a in self.board.get_all_possible_moves(self.color):
#             v2, a2 = self.minValue(game, game.result(state, a))
#             if v2 > v:
#                 v, move = v2, a
#         return v, move
    
#     def minValue(game, state)
#         if (0==k):
#             return evaluation(moves)
#         v = - math.inf
#         for i in self.board.get_all_possible_moves(self.color):
#             v2, a2 = self.maxValue(game, game.result(state, a))
#             if v2 < v:
#                 v, move = v2, a
#         return v, move
    
