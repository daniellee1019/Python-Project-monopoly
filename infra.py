# -*- coding: utf-8 -*-

import random

import mglobals
import property as _property

CHANCE_INDEXLIST = [7, 22, 36]
CHEST_INDEXLIST = [2, 17, 33]

class Jail(object):
    '''
    Class managing functionalities related to Jail

    >>> # Initialization
    >>> import mglobals
    >>> import ui
    >>> from player import Player
    >>> mglobals.init()
    >>> ui.init_printui()
    >>> mglobals.MSG_SCR = ui.MsgDisplayUI()

    >>> # Tests for use_cash()
    >>> testplayer = Player(mglobals.PLAYER_ONE)
    >>> mglobals.PLAYER_OBJ[mglobals.PLAYER_ONE] = testplayer
    >>> cash = testplayer.cash
    >>> testplayer.jail.use_cash()
    >>> (testplayer.jail.in_jail == False) and (cash == testplayer.cash)
    True
    >>> testplayer.jail.in_jail = True
    >>> testplayer.jail.use_cash()
    >>> (testplayer.jail.in_jail == False) and (cash - 50 == testplayer.cash)
    True

    >>> # Tests for use_jail_pass()
    >>> testplayer.jail.in_jail = True
    >>> testplayer.jail.use_jail_pass()
    >>> testplayer.jail.in_jail == True
    True
    >>> testplayer.jail.free_jail_pass = 1
    >>> testplayer.jail.use_jail_pass()
    >>> testplayer.jail.in_jail == False and testplayer.jail.free_jail_pass == 0
    True

    '''
    def __init__(self, player_name):
        self.player_name = player_name
        self.free_jail_pass = 0
        self.in_jail = False

    def _clear_jail(self):
        self.in_jail = False
        mglobals.JAIL_MSG.unset_x_y()
        mglobals.MSG_SCR.display()

    def use_cash(self):
        if self.in_jail:
            mglobals.PLAYER_OBJ[self.player_name].take_player_cash(50)
            self._clear_jail()

    def use_jail_pass(self):
        if self.in_jail and self.free_jail_pass:
            self.free_jail_pass -= 1
            mglobals.PLAYER_OBJ[self.player_name].piu.jail_card_display(False)
            self._clear_jail()

class ChanceChest(object):
    '''
    Class managing functionalities related to Chance and CommunityChest

    >>> # Initialization
    >>> import mglobals
    >>> import ui
    >>> from player import Player
    >>> import property as _property
    >>> mglobals.init()
    >>> ui.init_printui()
    >>> ui.init_property_displays()
    >>> _property.init_pobject_map()

    >>> testplayer = Player(mglobals.PLAYER_ONE)
    >>> mglobals.PLAYER_OBJ[mglobals.PLAYER_ONE] = testplayer
    >>> mglobals.PLAYER_OBJ[mglobals.PLAYER_TWO] = Player(mglobals.PLAYER_TWO)

    >>> # Tests for deduct_house_hotel_repair()
    >>> testplayer.buy_property(1); testplayer.buy_property(39)
    >>> t = testplayer.mortgage_property(1)
    >>> mglobals.POBJECT_MAP[39].house_count = 3
    >>> ret = ChanceChest().deduct_house_hotel_repair(testplayer, 10, 100)
    >>> ret == mglobals.POBJECT_MAP[39].house_count * 10
    True

    >>> # Tests for chance()
    >>> ChanceChest().chance(testplayer, 0)
    >>> testplayer.pm.position == 0
    True
    >>> ChanceChest().chance(testplayer, 1)
    >>> (testplayer.pm.position == 10) and (testplayer.jail.in_jail == True)
    True
    >>> testplayer.jail.in_jail = False
    >>> ChanceChest().chance(testplayer, 2)
    >>> testplayer.pm.position == 11
    True
    >>> ChanceChest().chance(testplayer, 3)
    >>> testplayer.pm.position == 15
    True
    >>> ChanceChest().chance(testplayer, 4)
    >>> testplayer.pm.position == 24
    True
    >>> ChanceChest().chance(testplayer, 5)
    >>> testplayer.pm.position == 39
    True
    >>> cur = testplayer.pm.position
    >>> ChanceChest().chance(testplayer, 6)
    >>> testplayer.pm.position == (cur - 3) % mglobals.BOARD_SQUARES
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chance(testplayer, 7)
    >>> testplayer.cash == cash - mglobals.POBJECT_MAP[39].house_count * 25
    True
    >>> cash = testplayer.cash; mglobals.POBJECT_MAP[39].house_count = 5
    >>> ChanceChest().chance(testplayer, 8)
    >>> testplayer.cash == cash - 115
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chance(testplayer, 9)
    >>> testplayer.cash == cash - 150
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chance(testplayer, 10)
    >>> testplayer.cash == cash - 20
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chance(testplayer, 11)
    >>> testplayer.cash == cash - 15
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chance(testplayer, 12)
    >>> testplayer.cash == cash + 150
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chance(testplayer, 13)
    >>> testplayer.cash == cash + 100
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chance(testplayer, 14)
    >>> testplayer.cash == cash + 50
    True
    >>> ChanceChest().chance(testplayer, 15)
    >>> testplayer.jail.free_jail_pass == 1
    True

    >>> # Tests for chest
    >>> ChanceChest().chest(testplayer, 0)
    >>> testplayer.pm.position == 0
    True
    >>> ChanceChest().chest(testplayer, 1)
    >>> testplayer.pm.position == 1
    True
    >>> ChanceChest().chest(testplayer, 2)
    >>> testplayer.pm.position == 10 and testplayer.jail.in_jail == True
    True
    >>> testplayer.jail.in_jail = False; cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 3)
    >>> testplayer.cash == cash - 100
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 4)
    >>> testplayer.cash == cash - 50
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 5)
    >>> testplayer.cash == cash - 50
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 6)
    >>> testplayer.cash == cash + 200
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 7)
    >>> testplayer.cash == cash + 100
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 8)
    >>> testplayer.cash == cash + 100
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 9)
    >>> testplayer.cash == cash + 50
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 10)
    >>> testplayer.cash == cash + 25
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 11)
    >>> testplayer.cash == cash + 20
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 12)
    >>> testplayer.cash == cash + 10
    True
    >>> cash1  = mglobals.PLAYER_OBJ[mglobals.PLAYER_ONE].cash
    >>> cash2  = mglobals.PLAYER_OBJ[mglobals.PLAYER_TWO].cash
    >>> ChanceChest().chest(testplayer, 13)
    >>> testplayer.cash == cash1 + 10 and mglobals.PLAYER_OBJ[mglobals.PLAYER_TWO].cash == cash2 - 10
    True
    >>> ChanceChest().chest(testplayer, 14)
    >>> testplayer.jail.free_jail_pass == 2
    True
    >>> cash = testplayer.cash
    >>> ChanceChest().chest(testplayer, 15)
    >>> testplayer.cash == cash - 10
    True

    '''
    def __init__(self):
        pass

    def chance_chest(self, player_name):
        player_obj = mglobals.PLAYER_OBJ[player_name]
        mglobals.CHANCE_CHEST_VALUE = random.randrange(16)
        if player_obj.pm.position in CHANCE_INDEXLIST:
            mglobals.CHANCE_MAP[mglobals.CHANCE_CHEST_VALUE].set_x_y()
            self.chance(player_obj, mglobals.CHANCE_CHEST_VALUE)
        else:
            mglobals.CHEST_MAP[mglobals.CHANCE_CHEST_VALUE].set_x_y()
            self.chest(player_obj, mglobals.CHANCE_CHEST_VALUE)

    def deduct_house_hotel_repair(self, player_obj, house_cost, hotel_cost):
        repair_amt = 0
        for color in player_obj.properties:
            for pname in player_obj.properties[color]:
                if '_' in pname:
                    continue
                prop = mglobals.PNAME_OBJ_MAP[pname]
                if prop in _property.PROPERTIES:
                    if prop.house_count > 4:
                        repair_amt += hotel_cost
                    else:
                        repair_amt += prop.house_count * house_cost
        return repair_amt

    def chance(self, player_obj, value):
        if value in range(6):
            m = {0:0, 1:10, 2:11, 3:15, 4:24, 5:39}
            if value == 1:
                player_obj.jail.in_jail = True
            player_obj.pm.advance(mglobals.BOARD_SQUARES + m[value] - player_obj.pm.position)

        elif value == 6:
            player_obj.pm.goback(3)

        elif value in [7, 8]:
            m = {7: (25, 100), 8: (40, 115)}
            house_cost, hotel_cost = m[value]
            amt = self.deduct_house_hotel_repair(player_obj, house_cost, hotel_cost)
            player_obj.take_player_cash(amt)

        elif value in [9, 10, 11]:
            m = {9:150, 10:20, 11:15}
            player_obj.take_player_cash(m[value])

        elif value in [12, 13, 14]:
            m = {12:150, 13:100, 14:50}
            player_obj.give_player_cash(m[value])

        elif value == 15:
            player_obj.jail.free_jail_pass += 1
            player_obj.piu.jail_card_display()

    def chest(self, player_obj, value):
        if value in range(3):
            m = {0:0, 1:1, 2:10}
            if value == 2:
                player_obj.jail.in_jail = True
            player_obj.pm.advance(mglobals.BOARD_SQUARES + m[value] - player_obj.pm.position)

        elif value in [3, 4, 5]:
            m = {3:100, 4:50, 5:50}
            player_obj.take_player_cash(m[value])

        elif value in range(6,13):
            m = {6:200, 7:100, 8:100, 9:50, 10:25, 11:20, 12:10}
            player_obj.give_player_cash(m[value])

        elif value == 13:
            for player, obj in mglobals.PLAYER_OBJ.iteritems():
                if not(player == player_obj.player_name):
                    obj.take_player_cash(10)
            player_obj.give_player_cash(10)

        elif value == 14:
            player_obj.jail.free_jail_pass += 1
            player_obj.piu.jail_card_display()

        elif value == 15:
            player_obj.take_player_cash(10)

CHANCE = {
        0: 'Advance to GO',
        1: 'Go to jail. Move directly to jail. Do not pass GO.',
        2: 'Advance to Pall Mall. If you pass GO collect £200',
        3: 'Take a trip to Marylebone Station. If you pass GO collect £200',
        4: 'Advance to Trafalgar Square. If you pass "Go" collect £200',
        5: 'Advance to Mayfair',
        6: 'Go back three spaces',
        7: 'General repairs. Pay £25 per house, £100 per hotel.',
        8: 'Street repairs: Pay £40 per house, £115 per hotel.',
        9: 'Pay school fees of £150',
        10: '"Drunk in charge" fine £20',
        11: 'Speeding fine £15',
        12: 'Your building loan matures. Receive £150',
        13: 'You have won a crossword competition. Collect £100',
        14: 'Bank pays you dividend of £50',
        15: 'Get out of jail free.',
}

COMMUNITYCHEST={
        0: 'Advance to GO',
        1: 'Go back to Old Kent Road',
        2: 'Go to jail. Move directly to jail. Do not pass GO.',
        3: 'Pay hospital £100',
        4: "Doctor's fee. Pay £50",
        5: 'Pay your insurance premium £50',
        6: 'Bank error in your favour. Collect £200',
        7: 'Annuity matures. Collect £100',
        8: 'You inherit £100',
        9: 'From sale of stock you get £50',
        10: 'Receive interest on 7% preference shares: £25',
        11: 'Income tax refund. Collect £20',
        12: 'You have won second prize in a beauty contest. Collect £10',
        13: 'It is your birthday. Collect £10 from each player',
        14: 'Get out of jail free.',
        #TODO Take Chance
        15: 'Pay a £10 fine or take a "Chance"',
}

if __name__ == '__main__':
    import doctest
    doctest.testmod()
