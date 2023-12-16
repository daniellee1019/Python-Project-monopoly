import pygame
import os

# Pygame 호출
pygame.init()

##### 화면 설정 #####
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "ani")

size = width, height = 800,600
win = pygame.display.set_mode(size)
######################

##### 정지할떄 사진 로드#####
char1 = pygame.transform.rotozoom(pygame.image.load(image_path + '/Idle (1).png'),0,0.35)
char2 = pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Idle (1).png'),True, False),0,0.35)
#########################

##### 프레임 #####

# 프레임을 위한 walkcount
walkcount = 0
# 프레임 setting
clock = pygame.time.Clock()
##################

##### 캐릭터 설정 #####

# 플레이어 크기
PlayerSize = char1.get_rect().size
# 플레이어 width, height 가져오기
PlayerWidth = PlayerSize[0]
PlayerHeight = PlayerSize[1]
# 플레이어 시작 위치
PlayerXPos = (800 / 2) - (PlayerWidth / 2)
PlayerYPos = (600 / 2) - PlayerHeight
# 플레이어 속도
PlayerSpeed = 0.1
# 플레이어 이동 speed
to_x = 0

# 행동에 관한 bool
left = False
right = False
stopd = True


# 정지할떄 사진 로드
char1 = pygame.transform.rotozoom(pygame.image.load(image_path + '/Idle (1).png'),0,0.35)
char2 = pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Idle (1).png'),True, False),0,0.35)


# Load an image
walkRight =[pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (1).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (2).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (3).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (4).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (5).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (6).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (7).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (8).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (9).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (10).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (11).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (12).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (13).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (14).png'),-5,0.35),
            pygame.transform.rotozoom(pygame.image.load(image_path + '/Run (15).png'),-5,0.35),
            ]

walkLeft = [pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (1).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (2).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (3).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (4).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (5).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (6).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (7).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (8).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (9).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (10).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (11).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (12).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (13).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (14).png'),True, False),1,0.35),
            pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(image_path + '/Run (15).png'),True, False),1,0.35)
            
            ]
print(walkLeft)

def redrawG():
    global walkcount

    if walkcount >= 60:
        walkcount = 0

    # walk right
    if right:
        win.blit(walkRight[walkcount//4],(PlayerXPos,PlayerYPos))
        print(walkcount//4)
        walkcount += 1
    #walk left
    elif left:
        win.blit(walkLeft[walkcount//4],(PlayerXPos,PlayerYPos))
        walkcount += 1

    elif stopd :
        win.blit(char1, (PlayerXPos, PlayerYPos))
        print("Right Direction")
    else:
        win.blit(char2, (PlayerXPos,PlayerYPos))
        print("Left Direction")
        pass
    pygame.display.update()

running = True

while running:
    
    # 프레임 60으로 설정
    df = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYUP:
            to_x = 0
            if right:
                right = False
                stopd = True
            if left:
                left = False
                stopd = False
            pass

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        to_x += PlayerSpeed
        right = True
        left = False
    if keys[pygame.K_a]:
        to_x -= PlayerSpeed
        right = False
        left = True
        
    PlayerXPos += to_x * df
    
    if PlayerXPos > width -100:
            PlayerXPos = width - 100
    if PlayerXPos < -150:
            PlayerXPos = -150
    
    redrawG()

pygame.quit()