
import pygame
import time
import collections

import ui
import mglobals
import utils
import infra
import sound
import property as _property

from player import Player, PlayerSelection, PlayerMovement

def player_menu_loop():
    one, two = 'white', 'gold'
    utils.draw_player_menu(one)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    one, two = two, one
                    utils.draw_player_menu(one)

                elif event.key == pygame.K_RETURN:
                    if (one) == ('gold'):
                        PvAI = True
                        return
        pygame.display.update()
        mglobals.CLK.tick(30)

def game_loop():
    utils.draw_board()

    mglobals.MSG_SCR = ui.MsgDisplayUI()

    P1 = Player(mglobals.PLAYER_ONE)
    P2 = Player(mglobals.PLAYER_TWO)

    mglobals.PLAYER_OBJ[mglobals.PLAYER_ONE] = P1
    mglobals.PLAYER_OBJ[mglobals.PLAYER_TWO] = P2

    P1.pm.render()
    P2.pm.render()

    currentplayer, otherplayer = P1, P2
    mglobals.PLAYER_NAME_SPRITE[currentplayer.player_name].set_x_y(350, 120)
    mglobals.CURRENTPLAYER_IMG[currentplayer.player_name].set_x_y(480, 115)

    double_count = 0
    roll, double = True, False
    

    while True:
        for event in pygame.event.get():
    
            if currentplayer.jail.in_jail:
                mglobals.JAIL_MSG.set_x_y(120, 630)
                if roll:
                    mglobals.MSG_SCR.display('화성탈출: 1번 50원으로 탈출 , 2번 찬스카드 사용, 3번 차례 넘기기')
                    
            else:
                mglobals.JAIL_MSG.unset_x_y()

            mglobals.CASH_INSUFF = False if currentplayer.cash >= 0 \
                                        else True
            if not mglobals.CASH_INSUFF and mglobals.MSG_SCR.cash_insuff_msg:
                    mglobals.MSG_SCR.display()
                    mglobals.MSG_SCR.cash_insuff_msg = False

            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                # if(event.key == pygame.K_d):
                #     sound.dice_effect()
                    
                if event.key == pygame.K_q:
                    mglobals.MSG_SCR.display("%s declares bankrupcy!" \
                                            % (currentplayer.player_name))
                    return

                # Options 1, 2 & 3 to get out of jail
                if currentplayer.pm.position == 10 and roll:
                    if event.key == pygame.K_1:
                        sound.jail_pick_sound1()
                        utils.draw_board()
                        currentplayer.pm.render()
                        otherplayer.pm.render()
                        currentplayer.jail.use_cash()

                    elif event.key == pygame.K_2:
                        sound.jail_pick_sound2()
                        utils.draw_board()
                        currentplayer.pm.render()
                        otherplayer.pm.render()
                        currentplayer.jail.use_jail_pass()

                    elif event.key == pygame.K_3:
                        sound.jail_pick_sound3()
                        utils.draw_board()
                        currentplayer.pm.render()
                        otherplayer.pm.render()
                        roll = False
                
                # Dice roll
                if event.key == pygame.K_d and roll and not(currentplayer.jail.in_jail)\
                                        and not mglobals.CASH_INSUFF:
                    utils.draw_board()
                    mglobals.CHANCE_MAP[mglobals.CHANCE_CHEST_VALUE].unset_x_y()
                    mglobals.CHEST_MAP[mglobals.CHANCE_CHEST_VALUE].unset_x_y()
                    mglobals.DICEOBJ.hide()
                    currentplayer.ps.hide()
                    val, double = mglobals.DICEOBJ.roll()
                    currentplayer.pm.advance(val)
                    otherplayer.pm.render()
                    
                    ## dice_effect ##
                    sound.dice_effect()
                    ## 이까지가 dice소리 중복 안나게 하는부분  ##
                    
                    if double:
                        double_count += 1
                        if(double_count >= 1):
                            sound.double_sound()
                        
                        if double_count == 3:
                            infra.ChanceChest().chance(currentplayer, 1)
                            double_count = 0
                            roll = False
                    else:
                        double_count = 0
                        roll = False

                # Buy property
                elif event.key == pygame.K_b and (not(roll) or double):
                    utils.draw_board()
                    currentplayer.pm.render()
                    otherplayer.pm.render()
                    currentplayer.buy_property(currentplayer.pm.position)

                if event.key == pygame.K_LEFT:
                    sound.keyboard_move_sound()
                    utils.draw_board()
                    currentplayer.ps.hide()
                    currentplayer.ps.advance()
                    currentplayer.ps.show()
                    currentplayer.pm.render()
                    otherplayer.pm.render()

                elif event.key == pygame.K_RIGHT:
                    sound.keyboard_move_sound()
                    utils.draw_board()
                    currentplayer.ps.hide()
                    currentplayer.ps.goback()
                    currentplayer.ps.show()
                    currentplayer.pm.render()
                    otherplayer.pm.render()

                # Mortgage property
                elif event.key == pygame.K_m:
                    utils.draw_board()
                    currentplayer.pm.render()
                    otherplayer.pm.render()
                    currentplayer.ps.show()
                    currentplayer.mortgage_property(currentplayer.ps.position)

                # Unmortgage property
                elif event.key == pygame.K_u:
                    utils.draw_board()
                    currentplayer.pm.render()
                    otherplayer.pm.render()
                    currentplayer.ps.show()
                    currentplayer.unmortgage_property(currentplayer.ps.position)

                # Build house/hotel
                elif event.key == pygame.K_h:
                    utils.draw_board()
                    currentplayer.pm.render()
                    otherplayer.pm.render()
                    currentplayer.ps.show()
                    currentplayer.build_house(currentplayer.ps.position)

                # Sell property
                elif event.key == pygame.K_s:
                    
                    utils.draw_board()
                    currentplayer.pm.render()
                    otherplayer.pm.render()
                    currentplayer.ps.show()
                    currentplayer.sell_property(currentplayer.ps.position)

                elif event.key == pygame.K_n:

                    utils.draw_board()
                    currentplayer.pm.render()
                    otherplayer.pm.render()
                    sound.turn_end()
                    if roll or mglobals.CASH_INSUFF:
                        pass
                    else:
                        roll = True
                        currentplayer, otherplayer = otherplayer, currentplayer

                        mglobals.CHANCE_MAP[mglobals.CHANCE_CHEST_VALUE].unset_x_y()
                        mglobals.CHEST_MAP[mglobals.CHANCE_CHEST_VALUE].unset_x_y()
                        mglobals.JAIL_MSG.unset_x_y()
                        mglobals.DICEOBJ.hide()
                        mglobals.PLAYER_NAME_SPRITE[currentplayer.player_name].set_x_y(350, 120)
                        mglobals.PLAYER_NAME_SPRITE[otherplayer.player_name].unset_x_y()
                        mglobals.CURRENTPLAYER_IMG[currentplayer.player_name].set_x_y(480, 115)
                        mglobals.CURRENTPLAYER_IMG[otherplayer.player_name].unset_x_y()
                        mglobals.MSG_SCR.draw_rect()
                        currentplayer.ps.hide()
                        otherplayer.ps.hide()

        mglobals.DICE_DISPLAY.update()
        mglobals.DICE_DISPLAY.draw(mglobals.GD)
        mglobals.CENTRE_DISPLAYS.update()
        mglobals.CENTRE_DISPLAYS.draw(mglobals.GD)
        mglobals.PROPERTY_DISPLAYS.update()
        mglobals.PROPERTY_DISPLAYS.draw(mglobals.GD)
        mglobals.HOUSE_COUNT_DISPLAYS.update()
        mglobals.HOUSE_COUNT_DISPLAYS.draw(mglobals.GD)
        mglobals.CHESTCHANCE_DISPLAYS.update()
        mglobals.CHESTCHANCE_DISPLAYS.draw(mglobals.GD)
        mglobals.JAILCARD_DISPLAY.update()
        mglobals.JAILCARD_DISPLAY.draw(mglobals.GD)
        mglobals.PLAYER_NAME_DISPLAY.update()
        mglobals.PLAYER_NAME_DISPLAY.draw(mglobals.GD)

        pygame.display.update()
        mglobals.CLK.tick(30)

def main():
    mglobals.init()
    sound.load_bgm()
    player_menu_loop()
    ui.init_dice()
    ui.init_printui()
    ui.init_centre_displays()
    ui.init_property_displays()
    ui.init_house_count_displays()
    _property.init_pobject_map()
    game_loop()
    pygame.quit()
    
    # mglobals BGM stop하는 부분
    # mglobals.load_BGM.stop()
    quit()

if __name__ == '__main__':
    main()



