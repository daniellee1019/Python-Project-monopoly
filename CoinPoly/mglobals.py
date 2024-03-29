import pygame
import collections
import os
from PIL import Image

current_path = os.path.dirname(__file__) # 현재파일의 위치 반환 ,그러면 지금 파일의 위치를 반환 해주는거다.
image_path = os.path.join(current_path , "pics") # images 폴더 위치 반환 curren_path에 폴더의 path를 더해준다. 그러면 images 폴더 위치가 할당이됨.
Player1_Animation_path = os.path.join(current_path , "Player1_ani_pic")
Player2_Animation_path = os.path.join(current_path , "Player2_ani_pic")

walkRight =[pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (1).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (2).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (3).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (4).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (5).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (6).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (7).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (8).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (9).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (10).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (11).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (12).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (13).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (14).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(Player1_Animation_path + '/Run (15).png'),-5,0.35),
            ]

DISPLAY_W, DISPLAY_H = 1200, 800
BOARD_WIDTH = 800

BOARD_SQUARES = 40

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BROWN = (165, 42, 42)
PURPLE = (128,0,128)
LITEBLUE = (153, 204, 255)
DEEPBLUE = (24, 53, 131)
BLUE = (0, 0, 255)
SKY_BLUE = (576, 226, 255)
DEEP_SKY_BLUE = (0, 191, 255)
DARK_BLUE = (0, 0, 139)
ROYAL_BLUE = (65, 105, 225)
PINK = (255, 0, 255)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (231,138,9)
DARKER_YELLOW = (200, 160, 30)
GREEN = (0, 255, 0)
SEA_GREEN = (46, 139, 87)
GRAY = (169,169,169)

PLAYER_ONE = '모노'
PLAYER_TWO = '폴리'

PLAYER_ONE_COLOR = 'orange' #플레이어 색 변동
PLAYER_TWO_COLOR = 'yellow'

PLAYER_AI  = 'Player AI'
BANK       = 'BANK'

color_map = {
        'purple': PURPLE,
        'black': BLACK,
        'brown': BROWN,
        'sky blue': DEEP_SKY_BLUE,
        'pink': PINK,
        'orange': ORANGE,
        'red': RED,
        'yellow': DARKER_YELLOW,
        'gold' : GOLD,
        'green': GREEN,
        'blue': BLUE,
        'liteblue' : LITEBLUE,
        'sea_green': SEA_GREEN,
        'royal_blue': ROYAL_BLUE,
        'white': WHITE,
        'gray': GRAY,
};

fontsize_map = { #각 폰트 사이즈 변경
        'big': 50,
        'mid': 25,
        'small_p': 16,
        'small_m' : 14,
        'small': 12,
};

GD = None
CLK = None
BACK_IMG = None
P1_IMG = None
P2_IMG = None
PvAI = False
P_INFO_CLRSCR = None
MSG_CLRSCR = None
MSG_SCR = None

CASH_INITIAL = 1500 # 게임 시작 시 플레이들에게 주어지는 돈
CASH_INSUFF = False
CHANCE_CHEST_VALUE = 0
JAIL_MSG = None

PLAYER_OBJ = {}
PLAYER_NAME_SPRITE = {}
CURRENTPLAYER_IMG = {}
PLAYER_NAME_DISPLAY = pygame.sprite.Group()

DICEOBJ = None
DICE_NUMBER_MAP = {}
DICE_DISPLAY = pygame.sprite.Group()

PROPERTY_NAME_SPRITE_MAP = {}
PROPERTY_DISPLAYS = pygame.sprite.Group()
CENTRE_DISPLAYS = pygame.sprite.Group()
POBJECT_MAP = {}
PNAME_OBJ_MAP = {}
PROP_COLOR_INDEX = collections.defaultdict(list)

INDEX_PROPPIC_MAP = {}
HOUSE_COUNT_DISPLAYS = pygame.sprite.Group()
INDEX_HOUSE_COUNT_MAP = collections.defaultdict(dict)

CHANCE_MAP = {}
CHEST_MAP = {}
CHESTCHANCE_DISPLAYS = pygame.sprite.Group()
PLAYER_JAIL_CARD = collections.defaultdict(dict)
JAILCARD_DISPLAY = pygame.sprite.Group()


def load_imgs():
    i = 1
    global BACK_IMG, P1_IMG, P2_IMG, P_INFO_CLRSCR, MSG_CLRSCR
    BACK_IMG = pygame.image.load(os.path.join(image_path , "coinboard2.png"))
    
    # Player1 이미지 Player2 이미지 로드후 blit
    P1_IMG = pygame.image.load(os.path.join(image_path , "run1.png"))
    P2_IMG = pygame.image.load(os.path.join(image_path , "run2.png"))
    BACK_IMG = pygame.transform.scale(BACK_IMG, (DISPLAY_W - 400, DISPLAY_H))
    P_INFO_CLRSCR = pygame.Surface([375, 375])
    MSG_CLRSCR = pygame.Surface([389, 23])

def init_pygame():
    global GD, CLK
    pygame.init()
    GD = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    pygame.display.set_caption('Monopoly')
    CLK = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

def init():
    init_pygame()
    load_imgs()
