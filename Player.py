from Piece import piece

class player :
    
    def __init__(self,color):
        colorMap = {
            'R' : 0,
            'Y' : 1,
            'B' : 2,
            'G' : 3
        }

        self.pieces = [piece(color,i) for i in range(4)]
        self.shift = 13*colorMap[color]
        self.color = color
        self.endPoint = 55