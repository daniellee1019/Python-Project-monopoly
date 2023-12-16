# 게임 사운드 만드는 부분
import pygame
import collections
import os

current_path = os.path.dirname(__file__) 
sound_path = os.path.join(current_path, "sound") # sound 폴더 위치 반환
jail_sound_list = []

def load_bgm():
    test_sound = pygame.mixer.Sound(sound_path + "/" + "Ooh.mp3")
    test_sound.set_volume(0.3)
    test_sound.play(-1)
    
def dice_effect():
    test_dice_sound = pygame.mixer.Sound(sound_path + "/" + "dice_sound.mp3")
    ## ~~sound.play() 하면 한번만 실행을 한다.
    test_dice_sound.play()
    
def p_buy():
    p_buy = pygame.mixer.Sound(sound_path + "/" + "p_buy.mp3")
    p_buy.play()
    
def np_buy():
    np_buy = pygame.mixer.Sound(sound_path + "/" + "np_buy.mp3")
    np_buy.play()
    
def sell():
    sell_sound = pygame.mixer.Sound(sound_path + "/" + "sell_sound.mp3")
    sell_sound.play()
    
def no_money():
    np_buy = pygame.mixer.Sound(sound_path + "/" + "no_money.mp3")
    np_buy.play()
    
def jail_sound():
    jail_sound = pygame.mixer.Sound(sound_path + "/" + "jail_sound.mp3")
    jail_sound.play()
    
def jail_pick_sound1():
    jail_pick_sound1 = pygame.mixer.Sound(sound_path + "/" + "jail_pick_sound1.mp3")
    jail_pick_sound1.play()
    
def jail_pick_sound2():
    jail_pick_sound2 = pygame.mixer.Sound(sound_path + "/" + "jail_pick_sound2.mp3")
    jail_pick_sound2.play()
    
def jail_pick_sound3():
    jail_pick_sound3 = pygame.mixer.Sound(sound_path + "/" + "jail_pick_sound3.mp3")
    jail_pick_sound3.play()
    
def q_sound():
    q_sound = pygame.mixer.Sound(sound_path + "/" + "q_sound.mp3")
    q_sound.play()
    
def keyboard_move_sound():
    keyboard_move = pygame.mixer.Sound(sound_path + "/" + "keyboard_move_sound.mp3")
    keyboard_move.play()
    
def turn_end():
    turn = pygame.mixer.Sound(sound_path + "/" + "turn_end.mp3")
    turn.play()
    
def double_sound():
    double = pygame.mixer.Sound(sound_path + "/" + "double_sound.mp3")
    double.play()
    
