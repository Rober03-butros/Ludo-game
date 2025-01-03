from Player import player

class state :

    def __init__(self,players,playerTurn,parent=None,action=None,cost=0,depth=0):

        #player is a list of objects (player).
        self.players = players
        self.playerTurn = playerTurn
        self.parent = parent
        #action is a number on dice and the piece we want to move it
        self.action = action
        self.depth = depth
        self.cost = cost

    '''
    cost:
        put a piece in the end point = 15
        release a piece = 8
        kill pieces = 5+2*n
        build a wall = 5-2(n-2)
        put a piece in safe place = 4
        move a piece Normally = 2
    '''

    def get_possible_actions(self):
        return action

    def generate_next_states(self):
        return states

    def apply_move(self,piece,number):
        return state

    def can_move(self,piece,number):
        return True

    def is_final(self):
        return True
    
    def is_win(self,player):
        #return if this player win or not
        return True