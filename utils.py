import pygame


def setScreen():
    screen = pygame.display.set_mode((600, 300))
    return screen


def loadBaseImages():
    bg_img = pygame.image.load('images/backMenu.jpg')
    #bg_img = pygame.image.load('images/backMenu.jpg')

    walk_left = [
        pygame.image.load('images/player/character_left1.png'),
        pygame.image.load('images/player/character_left2.png'),
        pygame.image.load('images/player/character_left3.png'),
        pygame.image.load('images/player/character_left4.png')
    ]

    walk_right = [
        pygame.image.load('images/player/character_right1.png'),
        pygame.image.load('images/player/character_right2.png'),
        pygame.image.load('images/player/character_right3.png'),
        pygame.image.load('images/player/character_right4.png')
    ]

    return bg_img, walk_left, walk_right


def loadEnemiesImages():
    ghost_img = pygame.image.load('images/ghost.png')
    ghost_img = pygame.transform.scale(ghost_img, (40, 40))

    return ghost_img

def initVals():
    player_anim = 0
    bg_x = 0

    player_speed = 6
    player_x = 70
    player_y = 200

    is_jump = False
    jump_count = 8
    ghost_list_in_game=[]

    return player_anim,bg_x,player_speed,player_x,player_y,is_jump,jump_count,ghost_list_in_game

def loadSounds():
    #bg_sound = pygame.mixer.Sound('sounds/Hitman(chosic.com).mp3')
    bg_sound = pygame.mixer.Sound('sounds/mulberry.mp3')
    return bg_sound


def setTimer():
    ghost_timer = pygame.USEREVENT
    pygame.time.set_timer(ghost_timer, 2500)
    reload_timer = pygame.USEREVENT + 2

    return ghost_timer,reload_timer


def setText():
    menu_font = pygame.font.SysFont(None, 36)
    label = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
    lose_lable = label.render('YOU LOST!', False, (193, 196, 199))
    begin_label = label.render('Start The Game', False, (115, 132, 148))
    begin_label_rect = begin_label.get_rect(topleft=(20, 10))
    menu_label = label.render('Menu', False, (115, 132, 148))
    menu_label_rect = menu_label.get_rect(topright=(557, 40))
    controls_label = label.render('Controls', False, (115, 132, 148))
    controls_label_rect = controls_label.get_rect(topleft=(20, 70))
    quit_label = label.render('Quit', False, (115, 132, 148))
    quit_label_rect = quit_label.get_rect(topleft=(20, 130))
    restart_lable = label.render('TRY AGAIN!', False, (115, 132, 148))
    restart_lable_rect = restart_lable.get_rect(topleft=(190, 180))
    kill_count_font = pygame.font.Font('fonts/Roboto-Black.ttf', 24)
    reload_font = pygame.font.Font('fonts/Roboto-Black.ttf', 18)

    return label,lose_lable,restart_lable_rect,restart_lable,kill_count_font,reload_font,menu_font,begin_label,begin_label_rect, controls_label,controls_label_rect,menu_label,menu_label_rect,quit_label,quit_label_rect

def setBullet():
    bullet_img = pygame.image.load('images/bullet.png')
    bullet_img = pygame.transform.scale(bullet_img, (32, 32))

    return  bullet_img


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def setColors():
    menuBack = (0, 0, 0)
    white = (255, 255, 255)
    grey = (100, 100, 100)

    return menuBack,white,grey