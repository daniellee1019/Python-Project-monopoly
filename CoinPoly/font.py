import pygame,sys
from pygame.locals import QUIT

pygame.init()
SCREEN = pygame.display.set_mode((1408, 800))
pygame.display.set_caption('한글폰트 확인')

sysFont = pygame.font.SysFont(None,24)
txt = '한글'

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    for i, name in enumerate(pygame.font.get_fonts()):
        font = pygame.font.SysFont(name, 24)
        In = len(name) * 12
        
        imgName = sysFont.render('%s:' % name, True, (255,255,255))
        imgTxt = font.render(txt, True,(255,255,255))
        
        x = i % 2 * 300
        y = i //2 * 25
        
        SCREEN.blit(imgName, (x,y))
        SCREEN.blit(imgTxt, ((x + In, y)))
        
    pygame.display.update()