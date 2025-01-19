from Logic import logic
from State import state
from Player import player
import random

p1 = player('R', isHuman=True)
p2 = player('G', isHuman=False)

# p2.pieces[0].index=0
# p2.pieces[1].index=1
# p2.pieces[3].index=2
# p2.pieces[2].index=3

# p1.pieces[3].index=0
# p1.pieces[1].index=1
# p1.pieces[0].index=2
# p1.pieces[2].index=3


players = [p1, p2]
s = state(players, 'R')
# print(len(s.generate_next_states(4)))
# print(len(s.get_possible_actions()))
# for i in [s.get_possible_actions(2,1)]:
#     print(i)
#     print()

# for i in s.get_possible_actions(turn=3):
    # print(i)

# states = s.generate_next_states()
# for state in states:
#     print(state.cost)
# s.apply_move([(p1.pieces[1],6),(p1.pieces[1],5)])

# s2 = s.copy()
# print('State equality check : ' + str(s == s2))
# s.apply_single_move(p1.pieces[1],6)
# print('State equality check : ' + str(s == s2))

# # print(s.is_final())
# print(p1.endPoint)
# s.print()
# print()
# s.apply_move(p1.pieces[1],6)
# print(p1.endPoint)
# s.print()

l = logic()
l.start_game(s)
