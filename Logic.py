import random


class logic:

    def __init__(self, state):
        self.state = state
        self.show_information = False

    def question_to_show_information(self):
        answer = input('Do you want to show information?(Y/N)')
        if answer == 'y' or answer == 'Y':
            return True
        elif answer == 'n' or answer == 'N':
            return False
        else:
            print("Invalid input, please enter 'Y' or 'N'.")
            return self.question_to_show_information()

    def start_game(self):
        self.show_information = self.question_to_show_information()
        if self.show_information == True or self.show_information == False:
            self.state.print()
            turn = 2
            while (True):

                if self.state.is_final():
                    break

                self.state.next_player()

                current_player = None

                for player in self.state.players:
                    if player.color == self.state.playerTurn:
                        current_player = player

                input('inter anythings to throw the dice')
                dice_number = self.throw_the_dice()
                print(f'dice number is: {dice_number}')
                print('Current player color is : ' + str(self.state.playerTurn))

                if current_player.ishuman:
                    removed = self.human_play(current_player, dice_number)
                else:
                    removed = self.computer_play(dice_number, turn + 1)

                if (dice_number == 6 or removed) and turn:
                    self.state.current_player_index -= 1
                    turn -= 1
                else:
                    turn = 2

                self.state.print()

            '''
            while game not finished 
            allow current player to play
            change the turn 
            '''

    def human_play(self, current_player, dice_number):
        removed = False
        possible_actions = self.state.get_possible_actions(dice_number)

        while (True):
            if len(possible_actions) > 0:
                pieceNum = int(input('enter number the piece'))
                piece = current_player.pieces[pieceNum]
                if not self.state.can_move(current_player, piece, dice_number):
                    print('this move not possible , you have another one.')
                else:
                    returned = self.state.apply_single_move(piece, dice_number)
                    removed = returned[1]
                    print('The movement was completed successfully')
                    break
            else:
                print('You don\'t have any possible moves.')
                break

        return removed

    def computer_play(self, dice_number, turn=3):

        removed = False
        best_move = [0, 0]
        best_cost = -1
        result = self.Expectiminimax(self.state, 4, 0, 'chance', dice_number, turn)
        best_cost = result[0]
        best_move = result[1]

        if best_move:
            if self.show_information:
                print(f'The number of visited nodes: {result[2]}')
                print(F"Best cost for computer player(Max player) :{best_cost}")
                print(f"Best action : piece number:{best_move[0][0].number}     dice number:{best_move[0][1]}")

            returned = self.state.apply_single_move(best_move[0][0], best_move[0][1])
            removed = returned[1]
        else:
            if self.show_information:
                print(f'The number of visited nodes: {result[2]}')
                print(F"Best cost for computer player(Max player) :{best_cost}")
                print(f"Best action : there is no action to be done.")

            print('GGs')

        return removed

    def throw_the_dice(self):
        return random.randint(1, 6)

    def Expectiminimax(self, state, depth,turn_iteration, node, dice_number=0, turn=3):
        if depth == 0 or state.is_final():
            return state.cost, state.action, 1

        if node == 'max':
            best_value = float('-inf')
            best_move = None
            newState = state.copy()
            nodes_count = 0
            for number in range(1, 7):
                result = self.Expectiminimax(newState, depth -1 ,turn_iteration, 'chance', number, turn)
                value = result[0]
                move = result[1]
                nodes_count += result[2]
                best_value = max(value, best_value)
                if value == best_value:  # we got a better value (a better move)
                    best_move = move
            return best_value, best_move, nodes_count + 1

        elif node == 'min':

            best_value = float('inf')
            best_move = None
            newState = state.copy()
            nodes_count = 0

            for number in range(1, 7):
                result = self.Expectiminimax(newState, depth-1,turn_iteration, 'chance', number, turn)
                value = result[0]
                move = result[1]
                nodes_count += result[2]
                best_value = min(value, best_value)
                if value == best_value:  # we got a better value (a better move)
                    best_move = move
            return best_value, best_move, nodes_count + 1

        else:

            value = 0
            best_value = float('-inf')
            best_move = None
            nodes_count = 0

            states = state.generate_next_states(dice_number, turn)
            next_player = self.next_player(turn_iteration)
            for newState in states:
                result = self.Expectiminimax(newState, depth - 1, turn_iteration+1,next_player)
                value += result[0] * (1 / 6) ** len(newState.action)
                nodes_count += result[2]
                if result[0] * (1 / 6) ** len(newState.action) > best_value:
                    best_value = result[0]
                    best_move = newState.action
            return value, best_move, nodes_count + 1

    def next_player(self,turn_iteration):
        if turn_iteration % len(self.state.turns_order) == 0 :
            return 'max'
        else:
            return 'min'
