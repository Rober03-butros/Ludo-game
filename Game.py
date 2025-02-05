from Logic import logic
from State import state
from Player import player

p1 = player('R', isHuman=False)
p2 = player('G', isHuman=False)
p3 = player('Y', isHuman=False)
p4 = player('B', isHuman=False)

p2.pieces[0].index = 0
p2.pieces[1].index = 1
p2.pieces[3].index = 2
p2.pieces[2].index = 2

p1.pieces[3].index = 35
p1.pieces[1].index = 34
p1.pieces[0].index = 38
p1.pieces[2].index = 42

players = [p1, p2, p3, p4]
order = [p1.color, p2.color, p3.color, p4.color]

while True:
    num_players = int(input("Enter the number of players (2 to 4): "))

    if num_players < 2 or num_players > 4:
        print("Invalid number of players. Please enter a number between 2 and 4.")
    else:
        players = players[:num_players]
        order = order[:num_players]
        break

s = state(players, 'R', order)
l = logic(s)
l.start_game()
