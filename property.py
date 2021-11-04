
import mglobals

class BaseProperty(object):
    '''
    Class managing common functionalities related to property.

    >>> # Initialization
    >>> import mglobals
    >>> import ui
    >>> from player import Player
    >>> mglobals.init()

    >>> # Tests for can_purchase()
    >>> mglobals.MSG_SCR = ui.MsgDisplayUI()
    >>> testplayer = Player(mglobals.PLAYER_ONE)
    >>> b = BaseProperty()
    >>> b.cost = mglobals.CASH_INITIAL - 1000; b.owner_name = mglobals.BANK
    >>> b.can_purchase(testplayer.player_name, testplayer.cash)
    True
    >>> b.cost = mglobals.CASH_INITIAL + 1000
    >>> b.can_purchase(testplayer.player_name, testplayer.cash)
    False
    >>> b.cost = mglobals.CASH_INITIAL; b.owner_name = mglobals.PLAYER_TWO
    >>> b.property_name = 'Mayfair'
    >>> b.can_purchase(testplayer.player_name, testplayer.cash)
    False

    >>> # Tests for purchase()
    >>> b.cost = mglobals.CASH_INITIAL - 1000; b.owner_name = mglobals.BANK
    >>> b.purchase(testplayer.player_name, testplayer.cash)
    True
    >>> b.cost = mglobals.CASH_INITIAL + 1000; b.owner_name = mglobals.BANK
    >>> b.purchase(testplayer.player_name, testplayer.cash)
    False
    >>> b.owner_name = mglobals.PLAYER_TWO
    >>> b.purchase(testplayer.player_name, testplayer.cash)
    False

    >>> # Tests for can_mortgage()
    >>> b.can_mortgage(testplayer.player_name)
    False
    >>> b.mortgaged = True; b.owner_name = mglobals.PLAYER_ONE
    >>> b.can_mortgage(testplayer.player_name)
    False
    >>> b.mortgaged = False
    >>> b.can_mortgage(testplayer.player_name)
    True

    >>> # Tests for mortgage()
    >>> b.mortgage_val = mglobals.CASH_INITIAL - 1200
    >>> ret = b.mortgage(testplayer.player_name)
    >>> ret == b.mortgage_val
    True
    >>> b.mortgage(testplayer.player_name)
    0
    >>> b.owner_name = mglobals.BANK
    >>> b.mortgage(testplayer.player_name)
    0

    >>> # Tests for can_unmortgage()
    >>> b.can_unmortgage(testplayer.player_name, testplayer.cash)
    False
    >>> b.mortgaged = False; b.owner_name = mglobals.PLAYER_ONE
    >>> b.can_unmortgage(testplayer.player_name, testplayer.cash)
    False
    >>> b.mortgaged = True; b.mortgage_val = mglobals.CASH_INITIAL
    >>> b.can_unmortgage(testplayer.player_name, testplayer.cash)
    False
    >>> b.mortgage_val = mglobals.CASH_INITIAL - 1200
    >>> b.can_unmortgage(testplayer.player_name, testplayer.cash)
    True

    >>> # Tests for unmortgage()
    >>> ret = b.unmortgage(testplayer.player_name, testplayer.cash)
    >>> ret == b.mortgage_val * 1.1
    True
    >>> b.owner_name = mglobals.BANK
    >>> b.unmortgage(testplayer.player_name, testplayer.cash)
    0
    >>> b.owner_name = mglobals.PLAYER_ONE; b.mortgaged = False
    >>> b.unmortgage(testplayer.player_name, testplayer.cash)
    0
    >>> b.mortgaged = True; b.mortgage_val = mglobals.CASH_INITIAL
    >>> b.unmortgage(testplayer.player_name, testplayer.cash)
    0

    >>> # Tests for can_sell()
    >>> b.can_sell()
    False
    >>> b.mortgaged = False
    >>> b.can_sell()
    True

    >>> # Tests for sell()
    >>> ret = b.sell()
    >>> ret == b.cost and b.owner_name == mglobals.BANK
    True
    >>> b.mortgaged = True
    >>> b.sell()
    0
   '''

    def __init__(self):
        pass

    def can_purchase(self, currentplayer, cash):
        if self.owner_name == mglobals.BANK:
            if cash >= self.cost:
                return True
            else:
                mglobals.MSG_SCR.display('%s does not have enough cash to buy!' \
                                          % (currentplayer))
                return False
        mglobals.MSG_SCR.display('%s is already purchased!' % (self.property_name))
        return False

    def purchase(self, currentplayer, cash):
        val = self.can_purchase(currentplayer, cash)
        if val:
            self.owner_name = currentplayer
            return True
        return val

    def can_mortgage(self, currentplayer):
        if self.owner_name != currentplayer:
            mglobals.MSG_SCR.display('%s does not own %s!' \
                                      % (currentplayer, self.property_name))
            return False
        if self.mortgaged:
            mglobals.MSG_SCR.display('%s is already mortgaged!' \
                                      % (self.property_name))
            return False
        return True

    def mortgage(self, currentplayer):
        if self.can_mortgage(currentplayer):
            self.mortgaged = True
            return self.mortgage_val
        return 0

    def can_unmortgage(self, currentplayer, cash):
        if self.owner_name != currentplayer:
            mglobals.MSG_SCR.display('%s does not own %s!' \
                                      % (currentplayer, self.property_name))
            return False
        if not self.mortgaged:
            mglobals.MSG_SCR.display('%s is not mortgaged!' %(self.property_name))
            return False
        if cash < self.mortgage_val * 1.1:
            mglobals.MSG_SCR.display('%s does not have enough cash to unmortgage %s!' \
                                      % (self.owner_name, self.property_name))
            return False
        return True

    def unmortgage(self, currentplayer, cash):
        if self.can_unmortgage(currentplayer, cash):
            self.mortgaged = False
            return int(self.mortgage_val * 1.1)
        return 0

    def can_sell(self):
        if self.mortgaged:
            mglobals.MSG_SCR.display('Unmortgage %s before selling!' \
                                                 % (self.property_name))
            return False
        return True

    def sell(self):
        if self.can_sell():
            self.owner_name = mglobals.BANK
            return self.cost
        return 0

class Property(BaseProperty):
    '''
    Class managing functionalities for properties

    >>> # Initialization
    >>> import mglobals
    >>> from player import Player
    >>> import ui
    >>> mglobals.init()

    >>> init_pobject_map()

    >>> # Tests for can_mortgage()
    >>> mglobals.MSG_SCR = ui.MsgDisplayUI()
    >>> testplayer = Player(mglobals.PLAYER_ONE)
    >>> p = mglobals.POBJECT_MAP[37]
    >>> p.can_mortgage(testplayer.player_name)
    False
    >>> p.mortgaged = True; p.owner_name = mglobals.PLAYER_ONE
    >>> p.can_mortgage(testplayer.player_name)
    False
    >>> p.mortgaged = False; p.color_all=True; p.house_count = 1
    >>> p.can_mortgage(testplayer.player_name)
    False
    >>> p.color_all = False; p.house_count = 0
    >>> p.can_mortgage(testplayer.player_name)
    True

    >>> # Tests for compute_rent()
    >>> p.compute_rent(testplayer.player_name)
    0
    >>> p.owner_name = mglobals.BANK
    >>> p.compute_rent(testplayer.player_name)
    0
    >>> p.owner_name = mglobals.PLAYER_TWO; p.mortgaged = True
    >>> p.compute_rent(testplayer.player_name)
    0
    >>> p.mortgaged = False
    >>> ret = p.compute_rent(testplayer.player_name)
    >>> ret == p.rent_details[0]
    True
    >>> p.color_all = True
    >>> ret = p.compute_rent(testplayer.player_name)
    >>> ret == p.rent_details[0] * p.color_cost
    True
    >>> p.house_count = 1
    >>> ret = p.compute_rent(testplayer.player_name)
    >>> ret == p.rent_details[p.house_count]
    True
    >>> p.house_count = 5
    >>> ret = p.compute_rent(testplayer.player_name)
    >>> ret == p.rent_details[p.house_count]
    True

    >>> #Tests for can_build_house()
    >>> p.house_count = 0
    >>> p.can_build_house(testplayer.player_name, testplayer.cash)
    False
    >>> p.owner_name = mglobals.PLAYER_ONE; p.color_all = False
    >>> p.can_build_house(testplayer.player_name, testplayer.cash)
    False
    >>> p.color_all = True; p.mortgaged = True
    >>> p.can_build_house(testplayer.player_name, testplayer.cash)
    False
    >>> p.mortgaged = False; p.house_hotel_cost += mglobals.CASH_INITIAL
    >>> p.can_build_house(testplayer.player_name, testplayer.cash)
    False
    >>> p.house_hotel_cost -= mglobals.CASH_INITIAL; p.house_count = 5
    >>> p.can_build_house(testplayer.player_name, testplayer.cash)
    False
    >>> p1 = mglobals.POBJECT_MAP[39]
    >>> p1.owner_name = mglobals.PLAYER_ONE; p1.color_all = True
    >>> p.house_count = 1
    >>> p.can_build_house(testplayer.player_name, testplayer.cash)
    False
    >>> p1.house_count = 1
    >>> p.can_build_house(testplayer.player_name, testplayer.cash)
    True

    >>> # Tests for build()
    >>> p.house_count =0; p1.house_count = 0
    >>> ret = p.build(testplayer.player_name, testplayer.cash)
    >>> ret == p.house_hotel_cost
    True
    >>> p.owner_name = mglobals.BANK; p.color_all = False; p.house_count = 0
    >>> p1.color_all = False; p1.house_count = 0
    >>> p.build(testplayer.player_name, testplayer.cash)
    0
    >>> p1.build(testplayer.player_name, testplayer.cash)
    0
    >>> p.owner_name = mglobals.PLAYER_ONE; p.color_all = True; p1.color_all = True
    >>> p.mortgaged = True
    >>> p.build(testplayer.player_name, testplayer.cash)
    0
    >>> p.mortgaged = False; p.house_hotel_cost += mglobals.CASH_INITIAL
    >>> p.build(testplayer.player_name, testplayer.cash)
    0
    >>> p.house_hotel_cost -= mglobals.CASH_INITIAL; p.house_count = 5
    >>> p.build(testplayer.player_name, testplayer.cash)
    0
    >>> p.house_count = 1
    >>> p.build(testplayer.player_name, testplayer.cash)
    0

    >>> # Tests for can_sell()
    >>> h_count = []; h_count.extend([p.house_count, p1.house_count])
    >>> p.mortgaged = True
    >>> p.can_sell(h_count)
    False
    >>> p.mortgaged = False; p1.house_count = 2
    >>> h_count = []; h_count.extend([p.house_count, p1.house_count])
    >>> p.can_sell(h_count)
    False
    >>> p.house_count = 2
    >>> h_count = []; h_count.extend([p.house_count, p1.house_count])
    >>> p.can_sell(h_count)
    True

    >>> # Tests for sell()
    >>> ret = p.sell()
    >>> ret == p.house_hotel_cost
    True
    >>> p.sell()
    0
    >>> p.house_count = 0; p1.house_count = 0; p.mortgaged = True
    >>> p.sell()
    0
    >>> p.mortgaged = False
    >>> ret = p.sell()
    >>> ret == p.cost
    True
    '''

    def __init__(self, index, property_name, cost, color, rent_details, mortgage_val,
                 house_hotel_cost, color_cost, color_all=False, owner_name=mglobals.BANK):
        super(Property, self).__init__()
        self.index = index
        self.property_name = property_name
        self.cost = cost
        self.color = color
        self.rent_details = rent_details
        self.mortgage_val = mortgage_val
        self.house_hotel_cost = house_hotel_cost
        self.color_cost = color_cost
        self.color_all = color_all
        self.owner_name = owner_name

        self.house_count = 0
        self.mortgaged = False

    def can_mortgage(self, currentplayer):
        if self.owner_name != currentplayer:
            mglobals.MSG_SCR.display('%s does not own %s!' \
                                      % (currentplayer, self.property_name))
            return False
        if self.mortgaged:
            mglobals.MSG_SCR.display('%s is already mortgaged!' % (self.property_name))
            return False
        if self.house_count != 0:
            mglobals.MSG_SCR.display('%s has houses, so cannot mortgage!' \
                                      % (self.property_name))
            return False
        return True

    def compute_rent(self, currentplayer):
        if currentplayer == self.owner_name or \
           self.owner_name == mglobals.BANK or self.mortgaged:
            return 0
        if self.house_count == 0 and self.color_all:
            return self.rent_details[self.house_count] * self.color_cost
        return self.rent_details[self.house_count]

    def can_build_house(self, currentplayer, cash):
        if self.owner_name != currentplayer:
            mglobals.MSG_SCR.display('%s does not own %s!' \
                                      % (currentplayer, self.property_name))
            return False
        if not self.color_all:
            mglobals.MSG_SCR.display('Buy all properties of %s color FIRST!!' % (self.color))
            return False
        if self.mortgaged:
            mglobals.MSG_SCR.display('%s is mortgaged, cannot build!' % (self.property_name))
            return False
        if cash < self.house_hotel_cost:
            mglobals.MSG_SCR.display('%s does not have enough cash to build!' \
                                      % (self.owner_name))
            return False
        if self.house_count == 5:
            mglobals.MSG_SCR.display('Cannot build more houses/hotel on %s!' \
                                                     % (self.property_name))
            return False
        h_count = []
        for each_index in mglobals.PROP_COLOR_INDEX[self.color]:
            h_count.append(mglobals.POBJECT_MAP[each_index].house_count)
        if not(self.house_count < max(h_count)) and len(set(h_count)) != 1:
            mglobals.MSG_SCR.display('Build equal number of houses in a color!')
            return False
        return True

    def build(self, currentplayer, cash):
        if self.can_build_house(currentplayer, cash):
            self.house_count += 1
            return self.house_hotel_cost
        return 0

    def can_sell(self, h_count):
        if self.mortgaged:
            mglobals.MSG_SCR.display('Unmortgage %s before selling.' %(self.property_name))
            return False
        if set(h_count) != 1 and self.house_count != max(h_count):
             mglobals.MSG_SCR.display('Sell houses evenly in properties of %s color.' \
                                                                          % (self.color))
             return False
        return True

    def sell(self):
        h_count = []
        for each_index in mglobals.PROP_COLOR_INDEX[self.color]:
            h_count.append(mglobals.POBJECT_MAP[each_index].house_count)
        if self.can_sell(h_count):
            if max(h_count) == 0:
                self.owner_name = mglobals.BANK
                return self.cost
            else:
                self.house_count -= 1
                return self.house_hotel_cost
        return 0

class UtilityProperty(BaseProperty):
    '''
    Class managing functionalities related to Utilities

    >>> # Initialization
    >>> import mglobals
    >>> import random
    >>> from player import Player
    >>> mglobals.init()

    >>> init_pobject_map()

    >>> # Tests for compute_rent()
    >>> testplayer = Player(mglobals.PLAYER_ONE)
    >>> u = mglobals.POBJECT_MAP[12]
    >>> d = random.randrange(2,12); count = 0
    >>> u.compute_rent(testplayer.player_name, count, d)
    0
    >>> u.owner_name = mglobals.PLAYER_ONE
    >>> u.compute_rent(testplayer.player_name, count, d)
    0
    >>> u.owner_name = mglobals.PLAYER_TWO; u.mortgaged = True
    >>> count = 1
    >>> u.compute_rent(testplayer.player_name, count, d)
    0
    >>> u.mortgaged = False
    >>> ret = u.compute_rent(testplayer.player_name, count, d)
    >>> ret == u.rent_details[count] * d
    True
    '''

    def __init__(self, index, property_name, cost, mortgage_val, owner_name=mglobals.BANK):
        super(UtilityProperty, self).__init__()
        self.index = index
        self.property_name = property_name
        self.cost = cost
        self.mortgage_val = mortgage_val
        self.owner_name = owner_name
        self.color = 'purple'
        self.rent_details = {1: 4, 2: 10}

        self.mortgaged = False

    def compute_rent(self, currentplayer, util_count, dice_val):
        if currentplayer == self.owner_name or \
           self.owner_name == mglobals.BANK or self.mortgaged:
            return 0
        return self.rent_details[util_count] * dice_val


class RailwayProperty(BaseProperty):
    '''
    Class managing functionalities related to Railways

    >>> # Initialization
    >>> import mglobals
    >>> from player import Player
    >>> mglobals.init()

    >>> init_pobject_map()

    >>> # Tests for compute_rent()
    >>> testplayer = Player(mglobals.PLAYER_ONE)
    >>> r = mglobals.POBJECT_MAP[15]
    >>> count = 3
    >>> r.compute_rent(testplayer.player_name, count)
    0
    >>> r.owner_name = mglobals.PLAYER_ONE
    >>> r.compute_rent(testplayer.player_name, count)
    0
    >>> r.owner_name = mglobals.PLAYER_TWO; r.mortgaged = True
    >>> r.compute_rent(testplayer.player_name, count)
    0
    >>> r.mortgaged = False
    >>> ret = r.compute_rent(testplayer.player_name, count)
    >>> ret == r.rent_details[count]
    True

    '''

    def __init__(self, index, property_name, cost, mortgage_val, owner_name=mglobals.BANK):
        super(RailwayProperty, self).__init__()
        self.index = index
        self.property_name = property_name
        self.cost = cost
        self.mortgage_val = mortgage_val
        self.owner_name = owner_name
        self.color = 'black'
        self.rent_details = {1: 25, 2: 50, 3: 100, 4: 200}

        self.mortgaged = False

    def compute_rent(self, currentplayer, rail_count):
        if currentplayer == self.owner_name or \
           self.owner_name == mglobals.BANK or self.mortgaged:
            return 0
        return self.rent_details[rail_count]


UTILITIES = [
        UtilityProperty(12, 'Electric Company', 150, 75),
        UtilityProperty(28, 'Water Works', 150, 75),
]

RAILWAYS = [
        RailwayProperty(5, 'Kings Cross Station', 200, 100),
        RailwayProperty(15, 'Marylebone Station', 200, 100),
        RailwayProperty(25, 'Fenchurch St. Station', 200, 100),
        RailwayProperty(35, 'Liverpool Street Station', 200, 100),
]

PROPERTIES = [
        # Brown
        Property(1, 'Old Kent Road', 60, 'brown', {0: 2, 1: 10, 2: 30, 3: 90, 4: 160, 5: 250}, 50, 30, 2, False),
        Property(3, 'Whitechapel Road', 60, 'brown', {0: 4, 1: 20, 2: 60, 3: 180, 4: 360, 5: 450}, 50, 30, 2, False),

        # Sky Blue
        Property(6, 'The Angel Islington', 100, 'sky blue', {0: 6, 1: 30, 2: 90, 3: 270, 4: 400, 5: 550}, 50, 50, 2, False),
        Property(8, 'Euston Road', 100, 'sky blue', {0: 6, 1: 30, 2: 90, 3: 270, 4: 400, 5: 550}, 50, 50, 2, False),
        Property(9, 'Pentonville Road', 120, 'sky blue', {0: 8, 1: 40, 2: 100, 3: 300, 4: 450, 5: 600}, 60, 50, 2, False),

        # Pink
        Property(11, 'Pall Mall', 140, 'pink', {0: 10, 1: 50, 2: 150, 3: 450, 4: 625, 5: 750}, 70, 100, 2, False),
        Property(13, 'Whitehall', 140, 'pink', {0: 10, 1: 50, 2: 150, 3: 450, 4: 625, 5: 750}, 70, 100, 2, False),
        Property(14, 'Northumberland Avenue', 160, 'pink', {0: 12, 1: 60, 2: 180, 3: 500, 4: 700, 5: 900}, 80, 80, 2, False),

        # Orange
        Property(16, 'Bow Street', 180, 'orange', {0: 14, 1: 70, 2: 200, 3: 550, 4: 750, 5: 950}, 90, 100, 2, False),
        Property(18, 'Marlborough Street', 180, 'orange', {0: 14, 1: 70, 2: 200, 3: 550, 4: 750, 5: 950}, 90, 100, 2, False),
        Property(19, 'Vine Street', 200, 'orange', {0: 16, 1: 80, 2: 220, 3: 600, 4: 800, 5: 1000}, 100, 100, 2, False),

        # Red
        Property(21, 'Strand', 220, 'red', {0: 18, 1: 90, 2: 250, 3: 700, 4: 875, 5: 1050}, 110, 150, 2, False),
        Property(23, 'Fleet Street', 220, 'red', {0: 18, 1: 90, 2: 250, 3: 700, 4: 875, 5: 1050}, 110, 150, 2, False),
        Property(24, 'Trafalgar Square', 240, 'red', {0: 20, 1: 100, 2: 300, 3: 750, 4: 925, 5: 1100}, 120, 150, 2, False),

        # Yellow
        Property(26, 'Leicester Square', 260, 'yellow', {0: 22, 1: 110, 2: 330, 3: 800, 4: 975, 5: 1150}, 150, 150, 2, False),
        Property(27, 'Coventry Street', 260, 'yellow', {0: 22, 1: 110, 2: 330, 3: 800, 4: 975, 5: 1150}, 150, 150, 2, False),
        Property(29, 'Piccadilly', 280, 'yellow', {0: 22, 1: 120, 2: 360, 3: 850, 4: 1025, 5: 1200}, 150, 140, 2, False),

        # Green
        Property(31, 'Regent Street', 300, 'green', {0: 26, 1: 130, 2: 390, 3: 900, 4: 1100, 5: 1275}, 200, 150, 2, False),
        Property(32, 'Oxford Street', 300, 'green', {0: 26, 1: 130, 2: 390, 3: 900, 4: 1100, 5: 1275}, 200, 150, 2, False),
        Property(34, 'Bond Street', 320, 'green', {0: 28, 1: 150, 2: 450, 3: 1000, 4: 1200, 5: 1400}, 200, 160, 2, False),

        # Blue
        Property(37, 'Park Lane', 350, 'blue', {0: 35, 1: 175, 2: 500, 3: 1100, 4: 1300, 5: 1500}, 175, 200, 2, False),
        Property(39, 'Mayfair', 400, 'blue', {0: 50, 1: 200, 2: 600, 3: 1400, 4: 1700, 5: 2000}, 200, 200, 2, False),
]

def init_pobject_map():
    for obj in PROPERTIES + RAILWAYS + UTILITIES:
        mglobals.POBJECT_MAP[obj.index] = obj
        mglobals.PROP_COLOR_INDEX[obj.color].append(obj.index)
        mglobals.PNAME_OBJ_MAP[obj.property_name] = obj

if __name__ == '__main__':
    import doctest
    doctest.testmod()

