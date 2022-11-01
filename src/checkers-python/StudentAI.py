from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class TreeNode():
    # class for TreeNode object
        # keeps track of all basic attributes that a tree node should has
    def __init__(self):
        # self.color = color
        # self.move = move
        self.value = None
        self.children = []

class Tree():
    # class for Tree object
    # -> main purpose is create and print and possibly update
        def __init__(self, root):
            self.root = root# intialize tree from root
            #self.level

        def create_tree(self, treeNode: TreeNode):
            # create tree up to specified depth to pick next path ---> simulate step?

            # select and expand nodes
            pass

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
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)

        # root = TreeNode()
        #
        # tree = Tree(root)

        return move

    # do heuristics as functions of studentAI class
