from Piece import piece
import copy


# sorting pieces by index
def sort_pieces(pieces):
    pieces.sort(key=lambda piece: piece.number)


class player:

    def __init__(self, color, pieces=None, isHuman=False):
        colorMap = {
            'R': 0,
            'Y': 1,
            'B': 2,
            'G': 3
        }

        if pieces is None:
            self.pieces = [piece(color, i) for i in range(4)]
        else:
            self.pieces = pieces
        self.shift = 13 * colorMap[color]
        self.color = color
        self.endPoint = 55
        self.ishuman = isHuman

    def __hash__(self):
        pieces_hashes = tuple(hash(piece) for piece in self.pieces)
        return hash(pieces_hashes)

    def __eq__(self, other):

        if not isinstance(other, player):
            return False

        sort_pieces(self.pieces)
        sort_pieces(other.pieces)
        for piece1 ,piece2 in zip(self.pieces, other.pieces):
            if not piece1 == piece2:
                return False

        return True


    def change_endpoint(self):
        self.endPoint -= 1

    def get_index(self, piece):
        if piece.index == -1 or piece.index > 51:
            return piece.index
        return (piece.index + self.shift) % 52

    def copy(self):
        return player(self.color, [piece.copy() for piece in self.pieces], self.ishuman)
