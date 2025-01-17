
# sorting players by color
def sort_players(players):
    players.sort(key=lambda player: player.color)

class state:
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
    safe = [8, 21, 34, 47]

    current_player_index = 0

    def next_player(self):
        global current_player_index
        self.playerTurn = self.players[current_player_index]
        current_player_index = (current_player_index + 1) % len(self.players)
        # return current_player

    def __init__(self, players, playerTurn, parent=None, action=None, cost=0, depth=0):

        # player is a list of objects (player).
        self.players = players
        self.playerTurn = playerTurn
        self.parent = parent
        # action is a number on dice and the piece we want to move it
        self.action = action
        self.depth = depth
        self.cost = cost
        self.grid = [' _ ' for i in range(52)]

    def __hash__(self):
        players_hashes = tuple(hash(player) for player in self.players)
        return hash(players_hashes)

    def __eq__(self, other):

        if not isinstance(other, state):
            return False

        sort_players(self.players)
        sort_players(other.players)
        for player1, player2 in zip(self.players, other.players):
            if not player1 == player2:
                return False

        return True


    '''
    cost:
        put a piece in the end point = 15
        release a piece = 8
        kill pieces = 5+2*n
        build a wall = 5-2(n-2)
        put a piece in safe place = 4
        move a piece Normally = 2
    '''

    def get_possible_actions(self,dice_number=0):

        possible_actions = []

        # playerTurn is containing the color of the current player
        player = next(
            (player for player in self.players if player.color == self.playerTurn), None)

        # if playerTurn changed to containing the player object
        # player = self.playerTurn

        for piece in player.pieces:
            for number in range(1, 7):
                if dice_number == number or dice_number == 0:
                    action = []

                    if not self.can_move(player, piece, number):
                        continue

                    if not number == 6:
                        action = [(piece, number)]
                        possible_actions.append(action)
                    else:
                        state_copy = self.copy()

                        matching_player = next(
                            (player for player in state_copy.players if player.color == piece.color), None)

                        matching_piece = next(
                            (p for p in matching_player.pieces if p.number == piece.number), None)

                        returned = state_copy.apply_single_move(matching_piece, number)
                        new_state = returned[0]
                        removed = returned[1]
                        if removed:
                            action = [(matching_piece, 6)]
                            possible_actions.append(action)
                        else:
                            for piece1 in matching_player.pieces:
                                for number1 in range(1, 7):
                                    action = [(matching_piece, 6)]

                                    player1 = None
                                    for p in new_state.players:
                                        if p.color == player.color:
                                            player1 = p
                                            break

                                    if not new_state.can_move(player1, piece1, number1):
                                        continue

                                    if not number1 == 6:
                                        # action = [(piece,6),(piece1,number1)]
                                        action.append((piece1, number1))
                                        possible_actions.append(action)
                                    else:
                                        state_copy1 = new_state.copy()

                                        matching_player1 = next(
                                            (player for player in state_copy1.players if player.color == piece1.color),
                                            None)

                                        matching_piece1 = next(
                                            (p for p in matching_player1.pieces if p.number == piece1.number), None)

                                        returned = state_copy1.apply_single_move(matching_piece1, number1)
                                        new_state1 = returned[0]
                                        removed1 = returned[1]
                                        if removed1:
                                            # action = [(piece, 6),(piece, 6)]
                                            action.append((matching_piece1, 6))
                                            possible_actions.append(action)
                                        else:
                                            for piece2 in matching_player1.pieces:
                                                for number2 in range(1, 7):
                                                    action = [(piece, 6), (matching_piece1, 6)]

                                                    player2 = None
                                                    for p in new_state1.players:
                                                        if p.color == player.color:
                                                            player2 = p
                                                            break

                                                    if not new_state1.can_move(player2, piece2, number2):
                                                        continue
                                                    # action = [(piece,6),(piece1,6),(piece2,number2)]
                                                    action.append((piece2, number2))
                                                    possible_actions.append(action)
                                                    action = []

                                possible_actions.append(action)
                                action = []

        return possible_actions

    def generate_next_states(self):
        next_states = set()

        for action in self.get_possible_actions():
            state_copy = self.copy()
            next_states.add(state_copy.apply_move(action))
        return next_states

    def apply_move(self, action):

        if not action in self.get_possible_actions():
            # throw an exception !!!?
            return self, False

        check = False
        current_state = self

        for move in action:
            returned = current_state.apply_single_move(move[0], move[1])
            new_state = returned[0]
            removed = returned[1]
            current_state = new_state
            if removed:
                break

        return current_state, check

    def apply_single_move(self, piece, number):

        currentPlayer = None
        for player in self.players:
            if player.color == piece.color:
                currentPlayer = player
                break

        # if the piece is out of the board, Enter it
        newIndex = 0
        # if the piece is already in the board, move it
        if piece.index != -1:
            newIndex = piece.index + number

        piece.index = newIndex

        # if it reach to the end, Change the endpoint for this player
        if newIndex == currentPlayer.endPoint:
            currentPlayer.change_endpoint()
            return self, False
        # there are opponents here, remove them
        if self.remove_opponent(piece, currentPlayer):
            return self, True

        return self, False

    def can_move(self, player, piece, number):

        # move piece from start point
        if piece.index == -1:
            return number == 6

        # check if the piece will reach the end point or not
        if piece.index + number > 50:
            return piece.index + number == player.endPoint

        # check if there is a wall
        for step in range(number):
            if self.there_are_wall((player.get_index(piece) + step) % 52, piece.color):
                return False

        return True

    def is_final(self):
        for player in self.players:
            if (self.is_win(player)):
                print(f'player with color {player.color} win')
                return True
        return False

    def is_win(self, player):
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

    def there_are_wall(self, index, color):
        # count number of pieces that not same as my color in this index
        for player in self.players:
            if player.color == color:
                continue
            count = 0
            for piece in player.pieces:
                count += (index == player.get_index(piece))
            # if the count > 1 then there are a wall
            if count > 1:
                return True
        return False

    def remove_opponent(self, piece, player):

        # if safe point do not do anything

        removed = False  # indicates if we have removed opponent pieces or not
        if player.get_index(piece) in self.safe:
            return removed

        for opponent in self.players:
            if player == opponent:
                continue
            for opponent_piece in opponent.pieces:
                if player.get_index(piece) == opponent.get_index(opponent_piece):
                    opponent_piece.index = -1
                    removed = True
        return removed

    def copy(self):
        return state([player.copy() for player in self.players], self.playerTurn)
