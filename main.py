import pygame, sys, time
from pygame.locals import *

def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    
    screen = pygame.display.set_mode((0,0), FULLSCREEN)
    screen_size = screen.get_size()
    
    clock = pygame.time.Clock()
    fps = 60
    
    mode, cube_size, start_point, chars_surf = init(screen_size)
    current_time = get_current_time()

    black_screen = pygame.Surface(screen_size)
    black_screen.fill((0,0,0))
    onchange = False
    fadein = 1
    alpha = 0
    
    while True:

        current_time = get_current_time()

        if onchange:
            alpha += 5 * fadein
            black_screen.set_alpha(alpha)
            if alpha >= 255 and fadein == 1:
                fadein = -1
                mode, cube_size, start_point, chars_surf = init(screen_size, not mode)
            if alpha <= 0 and fadein == -1:
                onchange = False
                fadein = 1
        
        if mode:
            current_time = ' ' + current_time

        screen.fill((0,0,0))
        
        current_point = start_point[::]
        for i, char in enumerate(current_time):
            surf = chars_surf[char]
            screen.blit(surf, current_point)
            if (i+1)%3 == 0 and mode:
                current_point[0] = start_point[0]
                current_point[1] += surf.get_height() + cube_size * 2
            else:
                current_point[0] += surf.get_width() + cube_size
        
        if onchange:
            screen.blit(black_screen, (0,0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    onchange = True
        
        pygame.display.flip()
        clock.tick(fps)

def init(screen_size, mode=None):
    if mode is None and mode not in [0, 1]:
        mode = 1 if screen_size[0] <= screen_size[1] else 0

    if mode:
        cube_size = min([screen_size[0]//15,screen_size[1]//27])
        start_point = [(screen_size[0]-cube_size*13)//2,(screen_size[1]-cube_size*25)//2]
    else:
        cube_size = min([screen_size[0]//41,screen_size[1]//9])
        start_point = [(screen_size[0]-cube_size*39)//2,(screen_size[1]-cube_size*7)//2]
    
    chars_surf = get_chars_surf(cube_size=cube_size,border=cube_size//10)
    
    return mode, cube_size, start_point, chars_surf
    
def get_current_time():
    return time.strftime('%H:%M:%S')

def get_chars_surf(cube_size=30,color=(255,255,255),border=1):
    chars = {
        '0': ['01110','10001','10001','10001','10001','10001','01110'],
        '1': ['00100','01100','10100','00100','00100','00100','11111'],
        '2': ['01110','10001','00001','00010','00100','01000','11111'],
        '3': ['01110','10001','00001','01110','00001','10001','01110'],
        '4': ['00010','00110','01010','10010','11111','00010','00010'],
        '5': ['11111','10000','10000','11111','00001','10001','01110'],
        '6': ['01110','10001','10000','11110','10001','10001','01110'],
        '7': ['11111','10001','00001','00010','00100','00100','00100'],
        '8': ['01110','10001','10001','01110','10001','10001','01110'],
        '9': ['01110','10001','10001','01111','00001','10001','01110'],
        ':': ['1','0','0','0','1','0','0'],
        ' ': ['0','0','0','0','0','0','0']
    }
    chars_surf = {}

    for key, char in chars.items():
        surf = pygame.Surface((len(char[0])*cube_size,len(char)*cube_size)).convert()
        for i, row in enumerate(char):
            for j, col in enumerate(row):
                if not int(col):
                    continue
                pygame.draw.rect(surf, color, (j*cube_size, i*cube_size, cube_size, cube_size))
                pygame.draw.rect(surf, (0,0,0), (j*cube_size, i*cube_size, cube_size, cube_size), border)
        surf.set_colorkey((0,0,0))
        chars_surf[key] = surf
    
    return chars_surf

if __name__ == '__main__':
    main()