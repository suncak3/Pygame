import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Suncake game')

#load images
bg_img = pygame.image.load('images/background.jpg')

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

#Enemy
ghost_img = pygame.image.load('images/ghost.png')
ghost_img = pygame.transform.scale(ghost_img, (40, 40))
ghost_list_in_game = []

player_anim = 0
bg_x = 0

player_speed = 6
player_x = 70
player_y = 200

is_jump = False
jump_count = 8

#load sound
bg_sound = pygame.mixer.Sound('sounds/Hitman(chosic.com).mp3')
bg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

#text
label = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
lose_lable = label.render('YOU LOST!', False, (193, 196, 199))
restart_lable = label.render('TRY AGAIN!', False, (115, 132, 148))
restart_lable_rect = restart_lable.get_rect(topleft = (190, 180))

#bullet image
bullet_img = pygame.image.load('images/bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (32, 32))
bullets = []

# Kill counter
kill_count = 0
kill_count_font = pygame.font.Font('fonts/Roboto-Black.ttf', 24)

# Переменные для стрельбы и перезарядки
shots_fired = 0
reloading = False
reload_timer = pygame.USEREVENT + 2
reload_font = pygame.font.Font('fonts/Roboto-Black.ttf', 18)
reload_color = (220, 220, 220)

to_remove_bullets = []
to_remove_ghosts = []


gameplay = True

run = True
while run:

    screen.blit(bg_img, (bg_x, 0))
    screen.blit(bg_img, (bg_x + 600, 0))

    if gameplay:

        screen.blit(walk_right[player_anim], (player_x, player_y))

        #contact with enemies
        player_rect = walk_left[0].get_rect(topleft = (player_x, player_y))
        
        #creating multiple ghosts and their movement  
        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost_img, el)
                el.x -= 8

                #remove ghosts
                if el.x < 8:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        #movement of player
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim], (player_x, player_y))
        elif keys[pygame.K_RIGHT]:
            screen.blit(walk_right[player_anim], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 20:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 120:
            player_x += player_speed
        
        
        #jump
        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8
        
        
        #player animation
        if player_anim == 3:
            player_anim = 0
        else:
            player_anim += 1


        #transition of background
        bg_x -= 2
        if bg_x == -600:
            bg_x = 0

        
        #contact of bullets with ghosts
        if bullets:
            for bullet in bullets:
                bullet_moved = False # Флаг, чтобы перемещать пулю только один раз
                for ghost_el in ghost_list_in_game:
                    if bullet.colliderect(ghost_el):
                        if ghost_el not in to_remove_ghosts:
                            to_remove_ghosts.append(ghost_el)
                        if bullet not in to_remove_bullets:
                            to_remove_bullets.append(bullet)
                        bullet_moved = True
                        kill_count += 1
                        break # Выход после первого столкновения
                if not bullet_moved:
                    screen.blit(bullet_img, (bullet.x, bullet.y))
                    bullet.x += 4
                    if bullet.x > 620 and bullet not in to_remove_bullets:
                        to_remove_bullets.append(bullet)
        
        # Display kill counter
        kill_counter_text = kill_count_font.render(f'Kills: {kill_count}', True, (255, 255, 255))
        screen.blit(kill_counter_text, (480, 10))

# Удаление пуль и призраков после обработки всех столкновений
        for bullet in to_remove_bullets:
            bullets.remove(bullet)
        for ghost in to_remove_ghosts:
            ghost_list_in_game.remove(ghost)

        to_remove_bullets.clear()
        to_remove_ghosts.clear()

        #Вывод надписи перезарядки на экран
        if reloading:
            reload_text = reload_font.render('Reloading...', True, reload_color)
            screen.blit(reload_text, (10, 10))
    #text when you lost
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_lable, (200, 90))
        screen.blit(restart_lable, restart_lable_rect)

        #restart game
        mouse = pygame.mouse.get_pos()
        if restart_lable_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 70
            ghost_list_in_game.clear()
            bullets.clear()
            kill_count = 0


    pygame.display.update()

    #fps
    clock.tick(20)

    for event in pygame.event.get():
        #quit from the game
        if event.type == pygame.QUIT:
            run = False
        if event.type == ghost_timer:
            new_ghost_rect = ghost_img.get_rect(topleft=(602, 200))
            ghost_list_in_game.append(new_ghost_rect)
        #Setting reload
        if event.type == reload_timer:
            reloading = False
            shots_fired = 0
            pygame.time.set_timer(reload_timer, 0)  # Отключаем таймер перезарядки
        #Сделать так, чтобы только при отпуска клавиши выпускалась пуля
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
           if not reloading and shots_fired < 3:
            new_bullet_rect = bullet_img.get_rect(topleft=(player_x + 15, player_y + 8))
            bullets.append(new_bullet_rect)
            shots_fired += 1
            if shots_fired == 3:
                reloading = True
                pygame.time.set_timer(reload_timer, 2500)  # Запускаем таймер перезарядки на 2 секунды
               
pygame.quit()