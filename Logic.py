import random


class logic:

    def start_game(self, state):
        # # DON'T TOUCH
        # print('_____________________________________________________')
        # print('POSSIBLE ACTIONS : ')
        # actions = state.get_possible_actions()
        # for action in actions:
        #     for move in action:
        #         print('piece color : ' + str(move[0].color) + '  |  piece index : ' + str(move[0].index) + '  |  piece number : ' + str(move[0].number) + '  |  number : ' +  str(move[1]))
        #     print('BOOOOOOOOOOORDEEEEEEEEEEEEEEEEER')
        # print('_____________________________________________________')

        # print('Start game')
        # print()
        self.print_state(state)
        while (True):
            if state.is_final():
                break
            for player in state.players:
                if player.ishuman:
                    print(f'Your turn ({player.color} player)')
                    self.human_play(state, player.color)
                    state.playerTurn = 'G'
                else:
                    print(f'Computer turn ({player.color} player)')
                    self.computer_play(state)
                    state.playerTurn = 'R'

                # test baby
                # print('_____________________________________________________')
                # print('POSSIBLE ACTIONS : ')
                # actions = state.get_possible_actions()
                # for action in actions:
                #     for move in action:
                #         print('piece color : ' + str(move[0].color) + '  |  piece index : ' + str(
                #             move[0].index) + '  |  piece number : ' + str(move[0].number) + '  |  number : ' + str(
                #             move[1]))
                #     print('BOOOOOOOOOOORDEEEEEEEEEEEEEEEEER')
                # print('_____________________________________________________')

                self.print_state(state)

        '''
        while game not finished 
        allow current player to play
        change the turn 
        '''

    def human_play(self, state, color):
        input('inter anythings to throw the dice')
        number = self.throw_the_dice()
        print(f'dice number is: {number}')
        pieceNum = int(input('enter number the piece'))
        piece = None
        curr_player = None
        for player in state.players:
            if player.color == color:
                curr_player = player
                piece = player.pieces[pieceNum]
                break

        if not state.can_move(curr_player, piece, number):
            print('GGs')
        else:
            state.apply_single_move(piece, number)
            print('The movement was completed successfully')
        # for action in state.get_possible_actions():
        #     if piece==action.piece and number==action.number:
        #      state.apply_move(piece,number)
        #      print('The movement was completed successfully')

        #     print('The movement is not correct')

    def computer_play(self,state):
        number = self.throw_the_dice()

        actions = state.get_possible_actions(number)
        
        best_move = [0,0]
        best_cost = -1
        print(actions)
        for action in actions:
            copyState = state.copy()
            copyState.apply_move(action)
            expect = self.Expectiminimax(copyState,3,'chance','max')
            # # print(cost[0])
            if best_cost < expect:
                best_cost = expect
                best_move = action

        state.apply_move(best_move) 
        print()
        print(f'dice number is: {number}')

    def throw_the_dice(self):
        return random.randint(1, 6)

    def print_state(self, state):
        for player in state.players:
            print(f"player color {player.color}:")
            for piece in player.pieces:
                print(f'number :{piece.number}                 index:{piece.index}     real{player.get_index(piece)}')
        print()

    def Expectiminimax(self,state,depth, lastNode,node):
        # print(depth)
        if depth == 0 or state.is_final():
            return state.cost

        if node == 'max':
            best_value = float('-inf')
            states = state.generate_next_states()
            for newState in states:
                value = self.Expectiminimax(newState,depth-1,node,'chance')
                best_value = max(value,best_value)
            return best_value

        elif node == 'min':
            best_value = float('inf')
            states = state.generate_next_states()
            for newState in states:
                value = self.Expectiminimax(newState,depth-1,node,'chance')
                best_value = min(value,best_value)
            return best_value

        else:
            value = 0
            if lastNode == 'min':
                nextNode = 'max'
            else:
                nextNode = 'min'
            states = state.generate_next_states()

            for newState in states:
                # value += self.Expectiminimax(newState,depth-1,node,nextNode)*self.calculate_probability(action[1])
                value += self.Expectiminimax(newState,depth-1,node,nextNode)*(1/6)
            return value


# expectiminimax frame test
class Expectiminimax:
    def __init__(self, state):
        self.state = state

    def expectiminimax(self, depth, player):
        if depth == 0 or self.state.is_terminal():
            return self.state.get_utility()

        if player == 'max':
            value = float('-inf')
            for action in self.state.get_possible_actions():
                new_state = self.state.apply_action(action)
                value = max(value, self.expectiminimax(depth - 1, 'chance'))
            return value
        elif player == 'chance':
            value = 0
            actions = self.state.get_possible_actions()
            for action in actions:
                new_state = self.state.apply_action(action)
                value += self.calculate_probability(action) * self.expectiminimax(depth - 1, 'min')
            return value
        else:  # player == 'min'
            value = float('inf')
            for action in self.state.get_possible_actions():
                new_state = self.state.apply_action(action)
                value = min(value, self.expectiminimax(depth - 1, 'max'))
            return value

    def calculate_probability(self, action):
        # Calculate the probability of the chance node based on the action
        # Customize this method based on the specific probabilities in your game
        if action == "1 to 5":
            return 1 / 6
        elif action == "6 and then 1 to 5":
            return 1 / 6 * 1 / 5
        elif action == "two consecutive 6s and then 1 to 6":
            return 1 / 6 * 1 / 6 * 1 / 6
        else:
            return 0  # Default case for unknown action

    def get_best_action(self, depth):
        best_value = float('-inf')
        best_action = None
        for action in self.state.get_possible_actions():
            new_state = self.state.apply_action(action)
            value = self.expectiminimax(depth, 'chance')
            if value > best_value:
                best_value = value
                best_action = action
        return best_action