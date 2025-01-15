import random
from State import state

class logic:
    def start_game(self,state):
        print('Start game')
        print()
        self.print_state(state)
        while(True):
            if state.is_final():
                break
            for player in state.players:
                if player.ishuman:
                     print(f'Your turn ({player.color} player)')
                     self.human_play(state,player.color)
                     
                
                else:
                    print(f'Computer turn ({player.color} player)')
                    self.computer_play()

                self.print_state(state)
            
        '''
        while game not finished 
        allow current player to play
        change the turn 
        '''

    def print_state(self, state):
        for player in state.players:
                print(f"player color {player.color}:")
                for piece in player.pieces:
                    print(f'number :{piece.number}                 index:{piece.index}     real{player.get_index(piece)}')
        print()


    def human_play(self,state,color):
        number = input('inter anythings to throw the dice')
        number = self.throw_the_dice()
        print(f'dice number is: {number}')
        pieceNum = int(input('enter number the piece'))
        for player in state.players :
            if player.color == color:
                piece = player.pieces[pieceNum]


        state.apply_move(piece,number)
        # for action in state.get_possible_actions():
        #     if piece==action.piece and number==action.number:
        #      state.apply_move(piece,number)
        #      print('The movement was completed successfully')
            
        #     print('The movement is not correct')



    def computer_play(self):
        print('computer play')

    def throw_the_dice(self):
        return random.randint(1,6)

    def Expectiminimax(self):
        print('Expectiminimax')
    
    