from Logic import logic
from State import state
from Player import player
import random 


p1 = player('R',True)
p2 = player('G',True)


players = [p1,p2]
s = state(players,0)

# # print(s.is_final())
# print(p1.endPoint)
# s.print()
# print()
# s.apply_move(p1.pieces[1],6)
# print(p1.endPoint)
# s.print()

l = logic()
l.start_game(s)