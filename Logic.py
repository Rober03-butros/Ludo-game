import random
from os import remove

from six import moves
from statsmodels.graphics.tukeyplot import results


class logic:

    def __init__(self, state, turns_order, current_player_index=0):
        self.state = state
        self.turns_order = turns_order
        self.current_player_index = current_player_index

    def next_player(self):
        self.state.playerTurn = self.turns_order[self.current_player_index]
        self.current_player_index = (self.current_player_index + 1) % len(self.turns_order)

    def start_game(self):
        # # DON'T TOUCH
        # print('_____________________________________________________')
        # actions = state.get_possible_actions()
        # print('POSSIBLE ACTIONS : ' + str(len(actions)))
        # for action in actions:
        #     for move in action:
        #         print('piece color : ' + str(move[0].color) + '  |  piece index : ' + str(move[0].index) + '  |  piece number : ' + str(move[0].number) + '  |  number : ' +  str(move[1]))
        #     print('BOOOOOOOOOOORDEEEEEEEEEEEEEEEEER')
        # print('_____________________________________________________')

        # print('Start game')
        # print()
        self.print_state()
        turn = 2
        while (True):

            if self.state.is_final():
                break

            self.next_player()

            current_player = None

            for player in self.state.players:
                if player.color == self.state.playerTurn:
                    current_player = player

            input('inter anythings to throw the dice')
            dice_number = self.throw_the_dice()
            print(f'dice number is: {dice_number}')

            print('current player color is : ' + str(current_player.color))
            if current_player.ishuman:
                removed = self.human_play(current_player, dice_number)
            else:
                removed = self.computer_play(dice_number, turn)

            if (dice_number == 6 or removed) and turn:
                self.current_player_index -= 1
                turn -= 1
            else:
                turn = 2

            self.print_state()

        '''
        while game not finished 
        allow current player to play
        change the turn 
        '''

    def human_play(self, current_player, dice_number):
        # print(f'dice number is: {dice_number}')
        pieceNum = int(input('enter number the piece'))
        piece = current_player.pieces[pieceNum]
        removed = False

        if not self.state.can_move(current_player, piece, dice_number):
            print('GGs')
        else:
            returned = self.state.apply_single_move(piece, dice_number)
            removed = returned[1]
            print('The movement was completed successfully')

        return removed

    def computer_play(self, dice_number, turn=3):
        # actions = self.state.get_possible_actions(dice_number, 3)
        # print('_____________________________________________________')
        # print('POSSIBLE ACTIONS : ' + str(len(actions)))
        # for action in actions:
        #     print('action : ' + str(action))
        #     # for move in action:
        #     #     print('piece color : ' + str(move[0].color) + '  |  piece index : ' + str(move[0].index) + '  |  piece number : ' + str(move[0].number) + '  |  number : ' +  str(move[1]))
        #     # print('BOOOOOOOOOOORDEEEEEEEEEEEEEEEEER')
        # print('_____________________________________________________')
        removed = False

        # if actions == []:
        #     print('you can not move')
        # else:
        # if dice_number != 6:
        #     fix_action = []
        #     for action in actions:
        #         fix_action.append([action])
        #     actions = fix_action

        best_move = [0, 0]
        best_cost = -1
        result = self.Expectiminimax(self.state, 3, 'min', 'chance', dice_number, turn)
        best_cost = result[0]
        best_move = result[1]

        print('best move : ' + str(best_move))

        print('_____________________________________________________')
        # actions = state.get_possible_actions()
        print('best move : ')
        for move in best_move:
            print('piece color : ' + str(move[0].color) + '  |  piece index : ' + str(
                move[0].index) + '  |  piece number : ' + str(move[0].number) + '  |  number : ' + str(move[1]))
        print('_____________________________________________________')

        print('computer move')
        print(F"best cost:{best_cost}")
        print(f"piece number:{best_move[0][0].number}     dice number:{best_move[0][1]}")
        print()
        # print(f"piece number:{best_move[0].number}     dice number:{best_move[1]}")
        returned = self.state.apply_single_move(best_move[0][0], best_move[0][1])
        removed = returned[1]
        return removed

    def throw_the_dice(self):
        return random.randint(1, 6)

    def print_state(self):
        for player in self.state.players:
            print(f"player color {player.color}:")
            for piece in player.pieces:
                print(f'number :{piece.number}                 index:{piece.index}     real{player.get_index(piece)}')
        print()

    def Expectiminimax(self, state, depth, lastNode, node, dice_number=0, turn=3):
        if depth == 0 or state.is_final():
            return state.cost, state.action

        if node == 'max':
            # print(node)
            best_value = float('-inf')
            newState = state.copy()
            for number in range(1, 7):
                result = self.Expectiminimax(newState, depth - 1, node, 'chance', number, turn)
                value = result[0]
                move = result[1]
                best_value = max(value, best_value)
                if value == best_value:  # we got a better value (a better move)
                    best_move = move
            return best_value, best_move

        elif node == 'min':

            best_value = float('inf')
            newState = state.copy()
            for number in range(1, 7):
                result = self.Expectiminimax(newState, depth - 1, node, 'chance', number, turn)
                value = result[0]
                move = result[1]
                best_value = min(value, best_value)
                if value == best_value:  # we got a better value (a better move)
                    best_move = move
            return best_value, best_move

        else:

            value = 0
            best_value = float('-inf')
            if lastNode == 'min':
                # state.playerTurn = 'G'
                nextNode = 'max'
            else:
                # state.playerTurn = 'R'
                nextNode = 'min'

            # print('dice number here : ' + str(dice_number))
            states = state.generate_next_states(dice_number, turn)
            # print('states count : ' + str(len(states)))
            # if not states:
            #     raise Exception('no satasetftsef')
            for newState in states:
                # value += self.Expectiminimax(newState,depth-1,node,nextNode)*self.calculate_probability(action[1])
                result = self.Expectiminimax(newState, depth - 1, node, nextNode)
                value += result[0] * (1 / 6)
                if result[0] > best_value:
                    best_value = result[0] * (1 / 6)
                    best_move = newState.action
            return value, best_move
