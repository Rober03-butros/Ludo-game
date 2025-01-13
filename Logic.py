import random
from State import state

class logic:
    
    def start_game(self,state):
        print('start game')

        while(True):
            # state.print()
            print()
            for player in state.players:
                print(f"player color {player.color}:")
                for piece in player.pieces:
                    print(f'number :{piece.number}                 index:{piece.index}     real{player.get_index(piece)}')
            print()
            if state.is_final():
                break
            print('player one turn')
            piece,number = self.human_play(state,'R')
            state.apply_move(piece,number)
            # state.print()
            print()
            for player in state.players:
                print(f"player color {player.color}:")
                for piece in player.pieces:
                    print(f'number :{piece.number}                 index:{piece.index}     real{player.get_index(piece)}')
            print()
            if state.is_final():
                break
            print('Player two turn ')
            piece,number = self.human_play(state,'G')
            state.apply_move(piece,number)
            print()
            for player in state.players:
                print(f"player color {player.color}:")
                for piece in player.pieces:
                    print(f'number :{piece.number}                 index:{piece.index}     real{player.get_index(piece)}')
            print()
            if state.is_final():
                break
        '''
        while game not finished 
        allow current player to play
        change the turn 
        '''

    def human_play(self,state,color):
        number = input('inter anythings to throw the dice')
        number = self.throw_the_dice()
        print(f'dice number is: {number}')
        pieceNum = int(input('enter number the piece'))
        for player in state.players :
            if player.color == color:
                piece = player.pieces[pieceNum]
        return piece,number
        print('human play')

    def computer_play(self):
        print('computer play')

    def throw_the_dice(self):
        return random.randint(1,6)

    def Expectiminimax(self):
        print('Expectiminimax')