
import pygame
import collections

import mglobals
import utils
import infra
import property as _property

from ui import PlayerInfoUI

class PlayerMovement(object):
    RECT_WIDTH = 65
    RECT_HEIGHT = 106
    SQ_HEIGHT_WIDTH = 106
    PIMG_WIDTH = 60
    PIMG_HEIGHT = 40

    def __init__(self, player_name, player_img, position=0):
        self.position = position
        self.player_name = player_name
        self.player_img = player_img
        self.x, self.y = 720, 730

    def find_rent_amount(self, count):
        for player, obj in mglobals.PLAYER_OBJ.items():
            if player == self.player_name:
                currentplayer = obj
            else:
                otherplayer = obj
        p_object = mglobals.POBJECT_MAP.get(self.position, None)
        if not p_object:
            return
        if p_object in _property.PROPERTIES:
            val = p_object.compute_rent(self.player_name)
        elif p_object in _property.RAILWAYS:
            val = p_object.compute_rent(self.player_name, \
                                        len(otherplayer.properties.get(p_object.color, [])))
        else:
            val = p_object.compute_rent(self.player_name, \
                                        len(otherplayer.properties.get(p_object.color, [])), \
                                        count)
        currentplayer.take_player_cash(val)
        otherplayer.give_player_cash(val)

    def advance(self, count):
        currentplayer = mglobals.PLAYER_OBJ[self.player_name]
        prev_pos = self.position
        self.position = (self.position + count) % mglobals.BOARD_SQUARES
        self.find_rent_amount(count)
        if self.position == 0 or (prev_pos > self.position and \
                                  not currentplayer.jail.in_jail):
            currentplayer.give_player_cash(200)
        if self.position in infra.CHANCE_INDEXLIST + infra.CHEST_INDEXLIST:
            infra.ChanceChest().chance_chest(self.player_name)
        # Income Tax deduction
        if self.position == 4:
            currentplayer.take_player_cash(200)
        # Super Tax deduction
        elif self.position == 38:
            currentplayer.take_player_cash(100)
        # Go to jail
        elif self.position == 30:
            self.position = 10
            currentplayer.jail.in_jail = True
        self.reposition()
        self.render()

    def goback(self, count):
        self.position = (self.position - count) % mglobals.BOARD_SQUARES
        self.reposition()
        self.find_rent_amount(count)
        self.render()

    def reposition(self):
        # If the position corresponds to a square
        if self.position % 10 == 0:
            if self.position in [0, 10]:
                self.y = mglobals.DISPLAY_H - PlayerMovement.PIMG_HEIGHT - 33
                self.x = 720 if self.position == 0 \
                           else 25
            else:
                self.y = 33
                self.x = 720 if self.position == 30 \
                           else 25

        # If the position corresponds to a vertical rectangle
        elif (self.position > 0 and self.position < 10) or \
             (self.position > 20 and self.position < 30):
            if self.position > 0 and self.position < 10:
                self.y = 730
                self.x = mglobals.BOARD_WIDTH - PlayerMovement.SQ_HEIGHT_WIDTH \
                         - PlayerMovement.PIMG_WIDTH  - 3 \
                         - ((self.position - 1) * PlayerMovement.RECT_WIDTH)
            else:
                self.y = 33
                self.x = PlayerMovement.SQ_HEIGHT_WIDTH + 3 \
                         + (((self.position % 10) - 1) * PlayerMovement.RECT_WIDTH)

        # If the position corresponds to a horizontal rectangle
        else:
            if self.position > 10 and self.position < 20:
                self.x = 25
                self.y = mglobals.DISPLAY_H - PlayerMovement.SQ_HEIGHT_WIDTH \
                         - PlayerMovement.PIMG_HEIGHT - 12 \
                         - (((self.position % 10) - 1) * PlayerMovement.RECT_WIDTH)
            else:
                self.x = 720
                self.y = PlayerMovement.SQ_HEIGHT_WIDTH + 12 \
                         + (((self.position % 10) - 1) * PlayerMovement.RECT_WIDTH)

    def render(self):
        mglobals.GD.blit(self.player_img, (self.x, self.y))

class PlayerSelection(object):
    BOX_THICKNESS = 5
    RECT_WIDTH = 65
    RECT_HEIGHT = 106
    SQ_HEIGHT_WIDTH = 106

    def __init__(self, color, position=0):
        self.position = position
        self.color = color
        self.x, self.y = 0, 0
        self.cw, self.ch = 0, 0
        self.reposition()
        self.render()

    def reposition(self):
        # If the position corresponds to a square
        if self.position % 10 == 0:
            if self.position in [0, 10]:
                self.y = mglobals.DISPLAY_H - PlayerSelection.SQ_HEIGHT_WIDTH
                self.x = 0 if self.position == 10 \
                           else mglobals.BOARD_WIDTH - PlayerSelection.SQ_HEIGHT_WIDTH
            else:
                self.y = 0
                self.x = 0 if self.position == 20 \
                           else mglobals.BOARD_WIDTH - PlayerSelection.SQ_HEIGHT_WIDTH
            self.cw, self.ch = PlayerSelection.SQ_HEIGHT_WIDTH, PlayerSelection.SQ_HEIGHT_WIDTH

        # If the position corresponds to a vertical rectangle
        elif (self.position > 0 and self.position < 10) or \
             (self.position > 20 and self.position < 30):
            if self.position > 0 and self.position < 10:
                self.y = (mglobals.DISPLAY_H - PlayerSelection.RECT_HEIGHT)
                self.x = mglobals.BOARD_WIDTH \
                         - PlayerSelection.SQ_HEIGHT_WIDTH \
                         - (PlayerSelection.RECT_WIDTH * self.position)
            else:
                self.y = 0
                self.x = PlayerSelection.SQ_HEIGHT_WIDTH \
                         + (PlayerSelection.RECT_WIDTH * ((self.position % 10) - 1))
            self.cw, self.ch = PlayerSelection.RECT_WIDTH, PlayerSelection.RECT_HEIGHT

        # If the position corresponds to a horizontal rectangle
        else:
            if self.position > 10 and self.position < 20:
                self.x = 0
                self.y = mglobals.DISPLAY_H \
                         - PlayerSelection.SQ_HEIGHT_WIDTH \
                         - (PlayerSelection.RECT_WIDTH * (self.position % 10))
            else:
                self.x = mglobals.BOARD_WIDTH - PlayerSelection.SQ_HEIGHT_WIDTH
                self.y = PlayerSelection.SQ_HEIGHT_WIDTH \
                         + (PlayerSelection.RECT_WIDTH * ((self.position % 10) -1))
            self.ch, self.cw = PlayerSelection.RECT_WIDTH, PlayerSelection.RECT_HEIGHT


    def advance(self):
        self.position += 1
        if self.position >= mglobals.BOARD_SQUARES:
            self.position %= mglobals.BOARD_SQUARES
        self.reposition()
        self.render()

    def goback(self):
        self.position -= 1
        if self.position < 0:
            self.position %= mglobals.BOARD_SQUARES
        self.reposition()
        self.render()

    def render(self):
        pygame.draw.rect(mglobals.GD, mglobals.color_map[self.color],
                         [self.x, self.y, self.cw, self.ch],
                         PlayerSelection.BOX_THICKNESS)
    def show(self):
        psprite = mglobals.INDEX_PROPPIC_MAP.get(self.position, None)
        if not psprite:
            return
        psprite.set_x_y()

    def hide(self):
        psprite = mglobals.INDEX_PROPPIC_MAP.get(self.position, None)
        if not psprite:
            return
        psprite.unset_x_y()

class Player(object):
    '''
    Class managing functionalities related to player

    >>> # Initialization
    >>> import mglobals
    >>> import ui
    >>> import property as _property
    >>> mglobals.init()
    >>> _property.init_pobject_map()
    >>> mglobals.MSG_SCR = ui.MsgDisplayUI()
    >>> ui.init_property_displays()

    >>> # Tests for give_player_cash()
    >>> testplayer = Player(mglobals.PLAYER_ONE)
    >>> cash = 150
    >>> testplayer.give_player_cash(cash)
    >>> testplayer.cash == mglobals.CASH_INITIAL + cash
    True

    >>> # Tests for take_player_cash()
    >>> testplayer.cash = mglobals.CASH_INITIAL
    >>> testplayer.take_player_cash(cash)
    >>> testplayer.cash == mglobals.CASH_INITIAL - cash
    True
    >>> testplayer.cash -= testplayer.cash
    >>> mglobals.CASH_INSUFF == False
    True
    >>> testplayer.take_player_cash(cash)
    >>> mglobals.CASH_INSUFF == True
    True
    >>> testplayer.take_player_cash(cash)
    False

    >>> # Tests for set_color_all()
    >>> pos = 39; testplayer.cash = mglobals.CASH_INITIAL
    >>> testplayer.set_color_all('blue')
    >>> mglobals.POBJECT_MAP[pos].color_all == True
    True
    >>> testplayer.set_color_all('blue', True)
    >>> mglobals.POBJECT_MAP[pos].color_all == False
    True

    >>> # Tests for buy_property()
    >>> pobj1 = mglobals.POBJECT_MAP[pos]
    >>> pobj1.property_name in testplayer.properties[pobj1.color]
    False
    >>> cash = testplayer.cash
    >>> testplayer.buy_property(pos)
    >>> testplayer.cash == cash - mglobals.POBJECT_MAP[pos].cost and \
                        pobj1.property_name in testplayer.properties[pobj1.color]
    True
    >>> cash = testplayer.cash
    >>> testplayer.buy_property(pos)
    >>> testplayer.cash == cash
    True
    >>> testplayer.cash -= testplayer.cash
    >>> pos = 37; pobj2 = mglobals.POBJECT_MAP[pos]
    >>> testplayer.buy_property(pos)
    >>> pobj2.property_name in testplayer.properties[pobj2.color]
    False
    >>> pobj1.color_all == False
    True
    >>> testplayer.cash = mglobals.CASH_INITIAL
    >>> testplayer.buy_property(pos)
    >>> pobj2.property_name in testplayer.properties[pobj2.color]
    True
    >>> pobj2.color_all == True and pobj1.color_all == True
    True

    >>> # Tests for mortgage_property()
    >>> testplayer.mortgage_property(pos)
    True
    >>> testplayer.mortgage_property(pos)
    False
    >>> testplayer.mortgage_property(38)

    >>> # Tests for unmortgage_property()
    >>> testplayer.unmortgage_property(pobj1.index)
    False
    >>> testplayer.unmortgage_property(pobj2.index)
    True
    >>> testplayer.unmortgage_property(38)

    >>> # Tests for sell_property()
    >>> ui.init_house_count_displays()
    >>> testplayer.sell_property(pobj2.index)
    >>> pobj2.owner_name == mglobals.BANK
    True
    >>> testplayer.sell_property(pobj2.index)
    >>> pobj1.house_count = 1
    >>> testplayer.sell_property(pobj1.index)
    >>> pobj1.owner_name == mglobals.PLAYER_ONE and pobj1.house_count == 0
    True
    >>> pobj1.mortgaged = True
    >>> testplayer.sell_property(pobj1.index)
    >>> pobj1.mortgaged = False

    >>> # Tests for build_house()
    >>> testplayer.build_house(38)
    >>> testplayer.build_house(15)
    False
    >>> testplayer.build_house(pobj1.index)
    False
    >>> testplayer.buy_property(pobj2.index)
    >>> testplayer.build_house(pobj1.index)
    >>> pobj1.house_count == 1
    True

    '''

    RECT_WIDTH = 65
    SQ_HEIGHT_WIDTH = 106

    def __init__(self, player_name):
        self.player_name = player_name
        self.color = mglobals.PLAYER_ONE_COLOR \
                            if self.player_name == mglobals.PLAYER_ONE \
                            else mglobals.PLAYER_TWO_COLOR
        self.properties = collections.defaultdict(list)
        self.cash = mglobals.CASH_INITIAL
        self.jail = infra.Jail(self.player_name)
        self.ps = PlayerSelection(self.color)
        self.piu = PlayerInfoUI(self.player_name, self.color)
        self.piu.render_name_cash()
        self.pm = PlayerMovement(self.player_name, mglobals.P1_IMG) \
                            if self.player_name == mglobals.PLAYER_ONE \
                            else PlayerMovement(self.player_name, mglobals.P2_IMG)

    def give_player_cash(self, cash):
        self.cash += cash
        self.piu.update_cash(self.cash)

    def take_player_cash(self, cash):
        if self.cash < 0:
            return False
        self.cash -= cash
        self.piu.update_cash(self.cash)
        if self.cash < 0:
            mglobals.CASH_INSUFF = True
            mglobals.MSG_SCR.cash_insuff_msg = True
            mglobals.MSG_SCR.display('%s owes money!' % (self.player_name))

    def set_color_all(self, color, unset=False):
        for each in mglobals.PROP_COLOR_INDEX[color]:
            p_object = mglobals.POBJECT_MAP[each]
            if unset:
                p_object.color_all = False
            else:
                p_object.color_all = True

    def buy_property(self, index):
        p_object = mglobals.POBJECT_MAP.get(index, None)
        if p_object and p_object.purchase(self.player_name, self.cash):
            prop_list = self.properties.get(p_object.color, None)
            if not prop_list or p_object.property_name not in prop_list:
                self.properties[p_object.color].append(p_object.property_name)
                self.take_player_cash(p_object.cost)
                self.piu.update_properties(self.properties)
                if len(self.properties[p_object.color]) == \
                   len(mglobals.PROP_COLOR_INDEX[p_object.color]) and \
                   (p_object in _property.PROPERTIES):
                    self.set_color_all(p_object.color)

    def mortgage_property(self, index):
        p_object = mglobals.POBJECT_MAP.get(index, None)
        if not p_object:
            return
        val = p_object.mortgage(self.player_name)
        if not val:
            return False
        self.give_player_cash(val)
        self.piu.replace_property(p_object.color, p_object.property_name, p_object.property_name+'_m')
        self.piu.update_properties(self.properties)
        return True

    def unmortgage_property(self, index):
        p_object = mglobals.POBJECT_MAP.get(index, None)
        if not p_object:
            return
        val = p_object.unmortgage(self.player_name, self.cash)
        if not val:
            return False
        self.take_player_cash(val)
        self.piu.replace_property(p_object.color, p_object.property_name+'_m', p_object.property_name)
        self.piu.update_properties(self.properties)
        return True

    def sell_property(self, index):
        p_object = mglobals.POBJECT_MAP.get(index, None)
        if p_object and p_object.owner_name == self.player_name:
            val = p_object.sell()
            if not val:
                return
            if val == p_object.cost:
                self.properties[p_object.color].remove(p_object.property_name)
                mglobals.PROPERTY_NAME_SPRITE_MAP[p_object.property_name].unset_x_y()
                if self.properties.get(p_object.color) == []:
                    self.properties.pop(p_object.color)
                if p_object in _property.PROPERTIES:
                    self.set_color_all(p_object.color, True)
                self.piu.update_properties(self.properties)
            elif val == p_object.house_hotel_cost:
                mglobals.INDEX_HOUSE_COUNT_MAP[index][p_object.house_count+1].unset_x_y()
                if p_object.house_count != 0:
                    hsprite = mglobals.INDEX_HOUSE_COUNT_MAP[index][p_object.house_count]
                    x, y = self.h_count_reposition(index)
                    hsprite.set_x_y(x, y)
            self.give_player_cash(val)

    def h_count_reposition(self, position):
        x, y = 900, 900
        # If the position corresponds to a vertical rectangle
        if position > 0 and position < 10:
            y = (mglobals.DISPLAY_H - Player.SQ_HEIGHT_WIDTH + 6)
            x = mglobals.BOARD_WIDTH - Player.SQ_HEIGHT_WIDTH \
                    - Player.RECT_WIDTH * (position - 0.5 )
        elif position > 10 and position < 20:
            y = mglobals.DISPLAY_H - Player.SQ_HEIGHT_WIDTH \
                    - Player.RECT_WIDTH * ((position % 10) - 0.5)
            x = Player.SQ_HEIGHT_WIDTH - 18
        # If the position corresponds to a horizontal rectangle
        elif position > 20 and position < 30:
            y = 87
            x = Player.SQ_HEIGHT_WIDTH + Player.RECT_WIDTH * ((position % 10) - 0.5)
        elif position > 30 and position < 40:
            y = Player.SQ_HEIGHT_WIDTH + Player.RECT_WIDTH * ((position % 10) - 0.5)
            x = mglobals.BOARD_WIDTH - 100
        return x, y

    def build_house(self, index):
        p_object = mglobals.POBJECT_MAP.get(index, None)
        if not p_object:
            return
        if index in [each.index for each in _property.UTILITIES + _property.RAILWAYS]:
            return False
        val = p_object.build(self.player_name, self.cash)
        if not val:
            return False
        prev_count = p_object.house_count - 1
        if not(prev_count == 0):
            mglobals.INDEX_HOUSE_COUNT_MAP[index][prev_count].unset_x_y()
        hsprite = mglobals.INDEX_HOUSE_COUNT_MAP[index][p_object.house_count]
        x, y = self.h_count_reposition(index)
        hsprite.set_x_y(x, y)
        self.take_player_cash(val)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

