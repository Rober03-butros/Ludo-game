from Player import player

class state :

    # Probability of rolling a specific number(1 to 5)
    #     1 / 6
    # Probability of rolling a 6 followed by another roll
    #     1 / 6 * 5 / 6 = 5 / 36
    # Probability of rolling two consecutive 6s followed by another roll
    #     (1 / 6) * (1 / 6) * (5 / 6) = 5 / 216
    # Probability of rolling three consecutive 6s
    #     (1 / 6) * (1 / 6) * (1 / 6) = 1 / 216

    # end = [['G','G','G','G','G'],['B','B','B','B','B'],['Y','Y','Y','Y','Y'],['R','R','R','R','R']]
    # colorMap = {
    #         'R' : 3,
    #         'Y' : 2,
    #         'B' : 1,
    #         'G' : 0
    #     }

    # safe place is in index  8+i*13  where i is [0,1,2,3]
    safe = [8,21,34,47]

    current_player_index = 0

    def next_player(this):
        global current_player_index
        this.playerTurn = this.players[current_player_index]
        current_player_index = (current_player_index + 1) % len(this.players)
        # return current_player

    def __init__(self,players,playerTurn,parent=None,action=None,cost=0,depth=0):

        #player is a list of objects (player).
        self.players = players
        self.playerTurn = playerTurn
        self.parent = parent
        #action is a number on dice and the piece we want to move it
        self.action = action
        self.depth = depth
        self.cost = cost
        self.grid = [' _ ' for i in range(52)] 

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

    # (self, action)
    def apply_move(self,piece,number):
        
        for player in self.players:
            if player.color == piece.color:
                currentPlayer = player
                break 

        if not self.can_move(currentPlayer,piece,number):
            return state

        # if the piece is out of the board, Enter it 
        newIndex = 0
        # if the piece is already in the board, move it
        if piece.index != -1:
            newIndex = piece.index + number

        piece.index = newIndex

        # if it reach to the end, Change the endpoint for this player
        if newIndex == currentPlayer.endPoint:
            currentPlayer.change_endpoint()
            return self
        # there are opponents here, remove them
        self.remove_opponent(piece,currentPlayer)

        return self

    def can_move(self,player,piece,number):

        #move piece from start point
        if piece.index == -1 :
            return number == 6

        #check if the piece will reach the end point or not
        if piece.index+number > 50:
            return piece.index+number == player.endPoint

        #check if there is a wall 
        for step in range(number):
            if self.there_are_wall((player.get_index(piece)+step)%52,piece.color) :
                return False

        return True

    def is_final(self):
        for player in self.players:
            if(self.is_win(player)):
                print(f'player with color {player.color} win')
                return True
        return False
    
    def is_win(self,player):
        return player.endPoint <= 51

    # def print(self):
        
        # for i in range(5):
        #     for j in range(4):
        #         print(f"                                  {str(self.end[j][i])}    ",end='')
        #     print()

        # grid = [' _ ' for i in range(52)]

        # for player in self.players:
        #     for piece in player.pieces:
        #         if piece.index >= 0 and piece.index < player.endPoint:
        #             grid[(piece.index-player.shift)%52] = ' '+piece.color+str(piece.number)

        # for i in range(52):
        #     print(grid[i],end='')
        # print()
    
    def there_are_wall(self,index,color):
        # count number of pieces that not same as my color in this index
        for player in self.players:
            if player.color == color:
                continue
            count = 0
            for piece in player.pieces:
                count += (index == player.get_index(piece))
            # if the count > 1 then there are a wall
            if count>1:
                return True
        return False

    def remove_opponent(self,piece,player):
        #if safe point do not do anythings
        if player.get_index(piece) in self.safe:
            return

        for opponent in self.players:
            if player == opponent:
                continue
            for opponent_piece in opponent.pieces:
                if player.get_index(piece) == opponent.get_index(opponent_piece):
                    opponent_piece.index=-1
             