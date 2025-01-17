import copy


class piece:

    def __init__(self, color, number, index=-1):
        self.color = color
        self.number = number
        self.index = index

    def copy(self):
        return piece(self.color, self.number, copy.deepcopy(self.index))
