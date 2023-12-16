# -*- coding: utf-8 -*-

import random

import mglobals
import property as _property

CHANCE_INDEXLIST = [7, 22, 36]
CHEST_INDEXLIST = [2, 17, 33]

# Test Push

class Jail(object):
    
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
            m = {6:200, 7:150, 8:100, 9:50, 10:50, 11:20, 12:30}
            player_obj.give_player_cash(m[value])

        elif value == 13:
            for player, obj in mglobals.PLAYER_OBJ.items():
                if not(player == player_obj.player_name):
                    obj.take_player_cash(10)
            player_obj.give_player_cash(10)

        elif value == 14:
            player_obj.jail.free_jail_pass += 1
            player_obj.piu.jail_card_display()

        elif value == 15:
            player_obj.take_player_cash(10)

CHANCE = {
        0: '시작지점으로 가세요',
        1: '화성으로 직행(시작지점 통과X)',
        2: '시작지점 통과 후(200원 Plus) 스텔라루웬으로 가세요',
        3: '그래픽카드 업그레이드 찬스! 시작지점 통과 후 아수스로 가세요',
        4: '시작지점 통과 후(200원 Plus) 유니스왑으로 가세요',
        5: '비트코인으로 가세요(시작지점 통과X)',
        6: '3칸 뒤로 이동하세요',
        7: '소유한 추가코인 1~4/개당 25원 5개부터/ 100원의 수수료 발생',
        8: '소유한 추가코인 1~4/개당 40원 5개부터/ 115원의 수수료 발생',
        9: '거래소에 150원을 기부하세요',
        10: '거래소에 20원을 기부하세요',
        11: '거래소에 15원을 기부하세요',
        12: '우수 고객으로 선정되었습니다! 150원을 받으세요',
        13: '장기 고객으로 선정되었습니다! 100원을 받으세요',
        14: '길에서 50원을 주웠습니다',
        15: '화성에서 탈출할 수 있는 찬스카드',
}

COMMUNITYCHEST={
        0: '시작지점으로 가세요',
        1: '파일코인으로 돌아가세요(시작지점 통과X)',
        2: '화성으로 직행(시작지점 통과X)',
        3: '컴퓨터가 고장났습니다 - 수리비용:100원',
        4: "컴퓨터 부품을 교체하세요 - 교체비용:50원",
        5: '목 디스크가 왔습니다 - 진료 비용:50원',
        6: '서버 네트워크 오류로 거래소에서 200원을 보냈습니다',
        7: '우수 고객으로 선정되었습니다! 150원을 받으세요',
        8: '장기 고객으로 선정되었습니다! 100원을 받으세요',
        9: '길에서 50원을 주웠습니다',
        10: '코인 투자 대회에서 우승하셨습니다 - 우승상금:50원',
        11: '수수료에 대한 세금이 일부 반환됐습니다 - 20원',
        12: '코인 투자 대회에서 2등하셨습니다 - 상금:30원',
        13: '거래소에서 모든 플레이어에게 20원을 보냈습니다',
        14: '화성에서 탈출할 수 있는 찬스카드',
        #TODO Take Chance
        15: '세금을 내세요 - 10원',
}

if __name__ == '__main__':
    import doctest
    doctest.testmod()
