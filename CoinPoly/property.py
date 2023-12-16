import mglobals
import sound

#기본적인 property 틀
class BaseProperty(object):

    def __init__(self):
        pass

    def can_purchase(self, currentplayer, cash): #지역을 살 수 있는지 없는지 판단여부
        if self.owner_name == mglobals.BANK:
            if cash >= self.cost: #내가 가지고 있는 돈이 그 지역의 값보다 크거나 같은 경우 true 반환
                sound.p_buy()
                return True
            else: #내가 가지고 있는 돈이 그 지역의 값보다 작은 경우
                mglobals.MSG_SCR.display('%s는 코인을 사기위한 돈이 부족합니다!' \
                                        % (currentplayer))
                return False
        sound.np_buy()
        mglobals.MSG_SCR.display('%s의 소유자가 이미 있습니다!' % (self.property_name)) #지역의 소유자가 있는 경우
        return False


    def purchase(self, currentplayer, cash): #지역을 구매하기 위한 기본적인 함수(건들지 않아도 될 것 같음)
        val = self.can_purchase(currentplayer, cash)
        if val:
            self.owner_name = currentplayer
            return True
        return val

    def can_mortgage(self, currentplayer): #내가 가지고 있는 지역의 저당을 잡을 수 있는지 판단 여부 
                                        #저당은 부동산 담보 대출을 말하며 해제를 원할 경우
                                        #모기지 가치와 10%의 이자를 더해서 지불을 해야된다.
                                        
        if self.owner_name != currentplayer: #지역의 소유자 이름과 현재 플레이어의 이름이 같지 않을 경우
            mglobals.MSG_SCR.display('%s는 %s을/를소유하고 있지 않습니다!' \
                                    % (currentplayer, self.property_name))
            return False
        if self.mortgaged: #지역이 이미 저당이 잡혀있는 경우
            mglobals.MSG_SCR.display('%s에 대한 저당이 이미 잡혀있습니다!' \
                                    % (self.property_name))
            return False
        return True

    def mortgage(self, currentplayer): # 저당을 잡기 위한 기본적 함수(건들지 않아도 됨)
        if self.can_mortgage(currentplayer):
            self.mortgaged = True
            return self.mortgage_val
        return 0

    def can_unmortgage(self, currentplayer, cash): #저당을 해제할 수 있는지 판단 여부
        if self.owner_name != currentplayer: #지역의 소유자이름과 현재 플레이어가 같지 않을 경우
            mglobals.MSG_SCR.display('%s는 %s을/를소유하고 있지 않습니다!' \
                                    % (currentplayer, self.property_name))
            return False
        if not self.mortgaged: #지역이 저당이 잡혀있지 않은 경우
            mglobals.MSG_SCR.display('%s에 대한 저당이 잡혀있지 않습니다!' %(self.property_name))
            return False
        if cash < self.mortgage_val * 1.1: #현재 가진 돈보다 모기지 가치와 이자10프로를 더한 값이 더 큰 경우 저당을 해제할 수 없다.
            mglobals.MSG_SCR.display('%s에 잡혀있는 저당을 해제하기 위한 돈이 부족합니다! %s!' \
                                    % (self.owner_name, self.property_name))
            return False
        return True

    def unmortgage(self, currentplayer, cash): #저당을 해제하기 위한 기본적 함수(164줄에 이자율 부분빼고 건들지 않아도 됨)
        if self.can_unmortgage(currentplayer, cash):
            self.mortgaged = False
            return int(self.mortgage_val * 1.1) # 이자율 표시
        return 0

    def can_sell(self): # 지역을 팔 수 있는지 없는지 판단 여부
        if self.mortgaged: #지역이 저당에 잡혀있는 경우 저당해제 후 팔 수 있다는 표시가 뜸
            mglobals.MSG_SCR.display('%s에 대한 저당해제 후 팔 수 있습니다!' \
                                                % (self.property_name))
            return False
        return True

    def sell(self): #지역을 팔기위한 기본적 함수 (건들지 않아도 됨)
        if self.can_sell():
            self.owner_name = mglobals.BANK
            return self.cost
        return 0

#BaseProperty를 이용해서 게임 안의 여러가지 값들을 지정하는 class
class Property(BaseProperty):

    #여러가지 값들의 매개변수를 지정해준다.
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

    def can_mortgage(self, currentplayer): #BaseProperty와 동일
        if self.owner_name != currentplayer:
            mglobals.MSG_SCR.display('%s는 %s을/를소유하고 있지 않습니다!' \
                                    % (currentplayer, self.property_name))
            return False
        if self.mortgaged:
            mglobals.MSG_SCR.display('%s에 대한 저당이 이미 잡혀있습니다!' % (self.property_name))
            return False
        if self.house_count != 0: #저당을 해제하기 위한 규칙이 한 가지 더 있다. 
                                #그 지역에 집이나 호텔이 있으면 저당을 받을 수 없다. 
            mglobals.MSG_SCR.display('%s의 갯수가 1개 이상이므로 저당을 잡을 수 없습니다!' \
                                    % (self.property_name))
            return False
        return True

    def compute_rent(self, currentplayer): # 잘 모르겠는데 그냥 자동화되는 부분인듯 
        if currentplayer == self.owner_name or \
           self.owner_name == mglobals.BANK or self.mortgaged:
            return 0
        if self.house_count == 0 and self.color_all:
            return self.rent_details[self.house_count] * self.color_cost
        return self.rent_details[self.house_count]

    def can_build_house(self, currentplayer, cash): #집을 지을 수 있는지 판단 여부
        if self.owner_name != currentplayer: #소유하고 있지 않을 경우
            mglobals.MSG_SCR.display('%s는 %s을/를소유하고 있지 않습니다!' \
                                      % (currentplayer, self.property_name))
            return False
        if not self.color_all: # 같은 색의 지역을 모두 다 가지고 있지 않는 경우
            mglobals.MSG_SCR.display('먼저 %s와/과 같은 색의 코인을 전부 구매하셔야 됩니다!' % (self.color))
            return False
        if self.mortgaged: # 지역이 저당이 잡혀있는 경우
            mglobals.MSG_SCR.display('%s은/는 저당이 있으므로, 집을 지을 수 없습니다!' % (self.property_name))
            return False
        if cash < self.house_hotel_cost: # 플레이어가 가지고 있는 돈보다 호텔을 지을 수 있는 비용이 클 경우
            mglobals.MSG_SCR.display('%s는 코인을 추가로 구매하기 위한 돈이 부족합니다!' \
                                      % (self.owner_name))
            return False
        if self.house_count == 5: #그 지역에 집이 5개를 지을 경우
                                  #(모노폴리 게임 룰에서는 집을 최대 4개까지 지을 수 있고, 추가로 1개의 호텔을 지을 수 있다.)
            mglobals.MSG_SCR.display('더 이상 %s의 코인을 구매하실 수 없습니다!' \
                                                     % (self.property_name))
            return False
        h_count = []
        for each_index in mglobals.PROP_COLOR_INDEX[self.color]: #공평하게 건축을 해야된다. 즉 한 지역에 1개의 집을 지었으면
                                                                 #같은 색깔을 가진 모든 지역에 1개의 집을 지을 때까지 추가적인 건설을 못 한다.
            h_count.append(mglobals.POBJECT_MAP[each_index].house_count)
        if not(self.house_count < max(h_count)) and len(set(h_count)) != 1:
            mglobals.MSG_SCR.display('같은 색의 코인에는 균일한 코인의 갯수를 구매하셔야 됩니다!')
            return False
        return True

    def build(self, currentplayer, cash):#집을 지을 때 쓰는 기본적 함수(건들지 않아도 됨)
        if self.can_build_house(currentplayer, cash):
            self.house_count += 1
            return self.house_hotel_cost
        return 0

    def can_sell(self, h_count):#BaseProperty와 동일
        if self.mortgaged:
            mglobals.MSG_SCR.display('%s에 대한 저당해제 후 팔 수 있습니다.' %(self.property_name))
            return False
        if set(h_count) != 1 and self.house_count != max(h_count): #집을 건설하기 위한 규칙처럼 팔때도 동일한 규칙이 적용된다.
                                                                #즉, 부지마다 공평하게 집이 남아있게 판매되어야 한다.
             mglobals.MSG_SCR.display('%s 색의 코인에는 균일한 코인의 갯수로 팔 수 있습니다!' \
                                                                        % (self.color))
             return False
        return True

    def sell(self): #집을 팔기위한 기본적 함수(건들이지 않아도 됨)
        h_count = []
        for each_index in mglobals.PROP_COLOR_INDEX[self.color]:
            h_count.append(mglobals.POBJECT_MAP[each_index].house_count)
        if self.can_sell(h_count):
            sound.sell()
            if max(h_count) == 0:
                self.owner_name = mglobals.BANK
                return self.cost
            else:
                self.house_count -= 1
                return self.house_hotel_cost
        return 0

#전기세 수도세 property = 각 거래소로 변환
class UtilityProperty(BaseProperty):

    def __init__(self, index, property_name, cost, mortgage_val, owner_name=mglobals.BANK):
        super(UtilityProperty, self).__init__()
        self.index = index
        self.property_name = property_name
        self.cost = cost
        self.mortgage_val = mortgage_val
        self.owner_name = owner_name
        self.color = 'purple'
        self.rent_details = {1: 4, 2: 10} #전기세 4달러 수도세 10달러

        self.mortgaged = False
    # 두개의 거래소중 하나만 소유하고 있다면 주사위 수 * 4의 통행료
    # 두개의 거래소 모두 소유하고 있다면 주사위 수 * 10의 통행료
    def compute_rent(self, currentplayer, util_count, dice_val):
        if currentplayer == self.owner_name or \
           self.owner_name == mglobals.BANK or self.mortgaged:
            return 0
        return self.rent_details[util_count] * dice_val

#4개의 기차역 property = 그래픽카드로 변환
class RailwayProperty(BaseProperty):

    def __init__(self, index, property_name, cost, mortgage_val, owner_name=mglobals.BANK):
        super(RailwayProperty, self).__init__()
        self.index = index
        self.property_name = property_name
        self.cost = cost
        self.mortgage_val = mortgage_val
        self.owner_name = owner_name
        self.color = 'black'
        self.rent_details = {1: 25, 2: 50, 3: 100, 4: 200} #모노폴리 규칙에는 기차역의 소유개수에 따라 임대료가 달라진다.
                                                           #1개 25달러 2개 50달러 3개 100달러 4개 200달라

        self.mortgaged = False

    def compute_rent(self, currentplayer, rail_count):
        if currentplayer == self.owner_name or \
           self.owner_name == mglobals.BANK or self.mortgaged:
            return 0
        return self.rent_details[rail_count]

#각 거래소 위치 지정
UTILITIES = [
        UtilityProperty(12, '업비트', 150, 75),
        UtilityProperty(28, '코인원', 150, 75),
]
#그래픽카드 위치 지정
RAILWAYS = [
        RailwayProperty(5, '엔비디아', 200, 100),
        RailwayProperty(15, '아수스', 200, 100),
        RailwayProperty(25, '기가바이트', 200, 100),
        RailwayProperty(35, '조택', 200, 100),
]
#각 코인 위치 지정 및 가격설정
# Property(코인위치, 코인이름, 땅가격,코인색,추가코인갯수당 임대료 가격,저당가격,추가코인구매가격
PROPERTIES = [
        # Brown
        Property(1, '파일코인', 60, 'brown', {0: 2, 1: 10, 2: 30, 3: 90, 4: 160, 5: 250}, 50, 30, 2, False),
        Property(3, '트론', 60, 'brown', {0: 4, 1: 20, 2: 60, 3: 180, 4: 360, 5: 450}, 50, 30, 2, False),

        # Sky Blue
        Property(6, '쎄타토큰', 100, 'sky blue', {0: 6, 1: 30, 2: 90, 3: 270, 4: 400, 5: 550}, 50, 50, 2, False),
        Property(8, '크립토닷컴', 100, 'sky blue', {0: 6, 1: 30, 2: 90, 3: 270, 4: 400, 5: 550}, 50, 50, 2, False),
        Property(9, '코스모스', 120, 'sky blue', {0: 8, 1: 40, 2: 100, 3: 300, 4: 450, 5: 600}, 60, 50, 2, False),

        # Pink
        Property(11, '스텔라루멘', 140, 'pink', {0: 10, 1: 50, 2: 150, 3: 450, 4: 625, 5: 750}, 70, 100, 2, False),
        Property(13, '엑시인피니티', 140, 'pink', {0: 10, 1: 50, 2: 150, 3: 450, 4: 625, 5: 750}, 70, 100, 2, False),
        Property(14, '비체인', 160, 'pink', {0: 12, 1: 60, 2: 180, 3: 500, 4: 700, 5: 900}, 80, 80, 2, False),

        # Orange
        Property(16, '비트코인캐시', 180, 'orange', {0: 14, 1: 70, 2: 200, 3: 550, 4: 750, 5: 950}, 90, 100, 2, False),
        Property(18, '알고랜드', 180, 'orange', {0: 14, 1: 70, 2: 200, 3: 550, 4: 750, 5: 950}, 90, 100, 2, False),
        Property(19, '폴리곤', 200, 'orange', {0: 16, 1: 80, 2: 220, 3: 600, 4: 800, 5: 1000}, 100, 100, 2, False),

        # Red
        Property(21, '라이트코인', 220, 'red', {0: 18, 1: 90, 2: 250, 3: 700, 4: 875, 5: 1050}, 110, 150, 2, False),
        Property(23, '체인링크', 220, 'red', {0: 18, 1: 90, 2: 250, 3: 700, 4: 875, 5: 1050}, 110, 150, 2, False),
        Property(24, '유니스왑', 240, 'red', {0: 20, 1: 100, 2: 300, 3: 750, 4: 925, 5: 1100}, 120, 150, 2, False),

        # Yellow
        Property(26, '루나', 260, 'yellow', {0: 22, 1: 110, 2: 330, 3: 800, 4: 975, 5: 1150}, 150, 150, 2, False),
        Property(27, '도지코인', 260, 'yellow', {0: 22, 1: 110, 2: 330, 3: 800, 4: 975, 5: 1150}, 150, 150, 2, False),
        Property(29, '폴카닷', 280, 'yellow', {0: 22, 1: 120, 2: 360, 3: 850, 4: 1025, 5: 1200}, 150, 140, 2, False),

        # Green
        Property(31, '리플', 300, 'green', {0: 26, 1: 130, 2: 390, 3: 900, 4: 1100, 5: 1275}, 200, 150, 2, False),
        Property(32, '에이다', 300, 'green', {0: 26, 1: 130, 2: 390, 3: 900, 4: 1100, 5: 1275}, 200, 150, 2, False),
        Property(34, '솔라나', 320, 'green', {0: 28, 1: 150, 2: 450, 3: 1000, 4: 1200, 5: 1400}, 200, 160, 2, False),

        # Blue
        Property(37, '이더리움', 350, 'blue', {0: 35, 1: 175, 2: 500, 3: 1100, 4: 1300, 5: 1500}, 175, 200, 2, False),
        Property(39, '비트코인', 400, 'blue', {0: 50, 1: 200, 2: 600, 3: 1400, 4: 1700, 5: 2000}, 200, 200, 2, False),
]


def init_pobject_map(): #위에서 지정한 class와 property값을 하나로 합침
    for obj in PROPERTIES + RAILWAYS + UTILITIES:
        mglobals.POBJECT_MAP[obj.index] = obj
        mglobals.PROP_COLOR_INDEX[obj.color].append(obj.index)
        mglobals.PNAME_OBJ_MAP[obj.property_name] = obj

if __name__ == '__main__':
    import doctest
    doctest.testmod()
