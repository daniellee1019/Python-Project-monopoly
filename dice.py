
import random

import mglobals

class Dice(object):
    def __init__(self):
        self.number1 = 1
        self.number2 = 1
        self.dicemap = mglobals.DICE_NUMBER_MAP

    def roll(self):
        self.number1 = random.randrange(1, 7)
        self.number2 = random.randrange(1, 7)
        self.show()
        return (self.number1+self.number2), (self.number1==self.number2)

    def show(self):
        self.dicemap[(self.number1, self.number2)].set_x_y()

    def hide(self):
        self.dicemap[(self.number1, self.number2)].unset_x_y()

