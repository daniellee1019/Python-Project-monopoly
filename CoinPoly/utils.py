import pygame

import mglobals

def text_objects(msg, fontobj, color='black'):
    color = mglobals.color_map[color]
    text_surf = fontobj.render(msg, True, color)
    return text_surf, text_surf.get_rect()

def message_display(msg, x=mglobals.DISPLAY_W/2, y=mglobals.DISPLAY_H/2, clear_color=None,
                    color='black', fntsize='big', center_coord=True):
    if clear_color:
        mglobals.GD.fill(mglobals.color_map[clear_color])

    textfont = pygame.font.SysFont('AppleGothic', mglobals.fontsize_map[fntsize])
        
    if textfont != True:
        textfont = pygame.font.SysFont('malgungothic', mglobals.fontsize_map[fntsize])
    else:
        return textfont
    
    text_surf, text_rect = text_objects(msg, textfont, color)
    if center_coord:
        text_rect.center = (x, y)
    else:
        text_rect.x, text_rect.y = x, y
    mglobals.GD.blit(text_surf, text_rect)
    pygame.display.update()

def message_display_lines(lines, x=mglobals.DISPLAY_W/2, y=mglobals.DISPLAY_H/2,
                          y_inc=50, color='black', fntsize='big'):
    for line in lines:
        message_display(line, x, y, color=color, fntsize=fntsize)
        y += y_inc

def draw_board():
    mglobals.GD.blit(mglobals.BACK_IMG, (-2, 0)) # 플레이어 선택시 테두리 위치

def clear_info(player):
    if player == mglobals.PLAYER_ONE:
        clear_p1_info()
    else:
        clear_p2_info()

def clear_p1_info():
    mglobals.P_INFO_CLRSCR.fill(mglobals.color_map['liteblue'])
    mglobals.GD.blit(mglobals.P_INFO_CLRSCR, (808, 0))

def clear_p2_info():
    mglobals.P_INFO_CLRSCR.fill(mglobals.color_map['liteblue'])
    mglobals.GD.blit(mglobals.P_INFO_CLRSCR, (808, 385))

def clear_msg_info():
    mglobals.MSG_CLRSCR.fill(mglobals.color_map['white'])
    mglobals.GD.blit(mglobals.MSG_CLRSCR, (808, 770))

def draw_player_menu(ocolor1): #초기 화면 위치변경 함
    mglobals.GD.fill(mglobals.LITEBLUE)
    message_display("Coinpoly !!!" ,x=(mglobals.DISPLAY_W/2),
                                    y=(mglobals.DISPLAY_H/2)-100,
                                    color=ocolor1)
    message_display("PvP", x=(mglobals.DISPLAY_W/2),
                           y=(mglobals.DISPLAY_H/2)+50,
                           color=ocolor1)


