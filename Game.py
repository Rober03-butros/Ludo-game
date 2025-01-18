from Logic import logic
from State import state
from Player import player
import random

p1 = player('R', isHuman=True)
p2 = player('G', isHuman=False)

p2.pieces[0].index=0
# p2.pieces[1].index=0
# p2.pieces[2].index=0
# p2.pieces[3].index=0

players = [p1, p2]
s = state(players, 'R')

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
