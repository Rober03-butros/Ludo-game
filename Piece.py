import copy


class piece:

    def __init__(self, color, number, index=-1):
        self.color = color
        self.number = number
        self.index = index

    def __hash__(self):
        return hash((self.color, self.index))

    def __eq__(self, other):
        if not isinstance(other, piece):
            return False
        return self.color == other.color and self.index == other.index

    def copy(self):
        return piece(self.color, self.number, copy.deepcopy(self.index))
