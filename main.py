import pygame
import sys
import utils as u
import random

clock = pygame.time.Clock()

pygame.init()

screen = u.setScreen()

pygame.display.set_caption('Suncake game')

#load images

bg_img,walk_left,walk_right = u.loadBaseImages()


#Enemy
ghost_img = u.loadEnemiesImages()


player_anim,bg_x,player_speed,player_x, player_y ,is_jump,jump_count,ghost_list_in_game = u.initVals()

#load sound
bg_sound = u.loadSounds()


ghost_timer,reload_timer = u.setTimer()

#text
label, lose_lable, restart_lable_rect, restart_lable, kill_count_font, reload_font, menu_font, begin_label, begin_label_rect, controls_label, controls_label_rect, menu_label, menu_label_rect, quit_label, quit_label_rect= u.setText()

#bullet image
bullet_img = u.setBullet()
bullets = []

# Kill counter
kill_count = 0


# Переменные для стрельбы и перезарядки
shots_fired = 0
reloading = False
reload_color = (220, 220, 220)

to_remove_bullets = []
to_remove_ghosts = []


menuBack,white,grey = u.setColors()





def main_menu(bg_img,bg_sound,screen):
    menu = True
    while menu:

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if begin_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                bg_img = pygame.image.load('images/background.jpg')
                bg_sound.stop()
                bg_sound = pygame.mixer.Sound('sounds/Hitman(chosic.com).mp3')
                bg_sound.play()
                startGame(screen, bg_img, walk_left, walk_right, ghost_img, player_anim, bg_x, player_speed,
                          player_x, player_y, is_jump, jump_count, ghost_list_in_game, ghost_timer, reload_timer,
                          label, lose_lable, restart_lable_rect, restart_lable, kill_count_font, reload_font,
                          bullet_img, bullets, kill_count, shots_fired, reloading, reload_color, to_remove_bullets,
                          to_remove_ghosts,bg_sound)

            if controls_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                show_controls(bg_img)

            if quit_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



        screen.blit(bg_img, [0, 0])
        screen.blit(begin_label, begin_label.get_rect(topleft=(20, 10)))
        screen.blit(controls_label, controls_label.get_rect(topleft=(20, 70)))
        screen.blit(quit_label, controls_label.get_rect(topleft=(20, 130)))

        pygame.display.update()




def show_controls(bg_img):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.blit(bg_img, [0, 0])
        u.draw_text('Controls', menu_font, grey, screen, 20, 20)
        u.draw_text('Move with UP, RIGHT,LEFT.Shoot with SPACE', menu_font, grey, screen, 20, 100)
        u.draw_text('Press ESC to return', menu_font, grey, screen, 20, 180)
        pygame.display.update()



def startGame(screen,bg_img,walk_left,walk_right,ghost_img,player_anim,bg_x,player_speed,player_x, player_y ,is_jump,jump_count,ghost_list_in_game,ghost_timer,reload_timer,label,lose_lable,restart_lable_rect,restart_lable,kill_count_font,reload_font,bullet_img,bullets,kill_count,shots_fired,reloading,reload_color,to_remove_bullets,to_remove_ghosts,bg_sound  ):
    gameplay = True

    run = True
    while run:

        screen.blit(bg_img, (bg_x, 0))
        screen.blit(bg_img, (bg_x + 600, 0))

        if gameplay:

            screen.blit(walk_right[player_anim], (player_x, player_y))
            screen.blit(menu_label, menu_label.get_rect(topright=(557, 40)))

            mouse = pygame.mouse.get_pos()
            if menu_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                bg_sound.stop()
                bg_sound = pygame.mixer.Sound('sounds/mulberry.mp3')
                bg_sound.play()
                bg_img = pygame.image.load('images/backMenu.jpg')
                main_menu(bg_img,bg_sound,screen)

            #contact with enemies
            player_rect = walk_left[0].get_rect(topleft = (player_x, player_y))

            #creating multiple ghosts and their movement
            if ghost_list_in_game:
                for (i, el) in enumerate(ghost_list_in_game):
                    screen.blit(ghost_img, el)

                    el.x -= 8+(kill_count*0.50)

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

                ghost_level = 2
                if(kill_count >= 14 and kill_count <=20):
                    ghost_level = 3
                elif(kill_count >=20 and kill_count <= 25):
                    ghost_level = 4
                elif(kill_count >=25):
                    ghost_level = 5

                for i in range(0,random.randint(1,ghost_level)):
                    ghost_list_in_game.append(new_ghost_rect)
            #Setting reload
            if event.type == reload_timer:
                reloading = False
                shots_fired = 0
                pygame.time.set_timer(reload_timer, 0)  # Отключаем таймер перезарядки
            #Сделать так, чтобы только при отпуска клавиши выпускалась пуля
            if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
               if not reloading and shots_fired < 5:
                new_bullet_rect = bullet_img.get_rect(topleft=(player_x + 15, player_y + 8))
                bullets.append(new_bullet_rect)
                shots_fired += 1
                if shots_fired == 5:
                    reloading = True
                    pygame.time.set_timer(reload_timer, 2500)  # Запускаем таймер перезарядки на 2 секунды

    pygame.quit()



if __name__ == '__main__':
    bg_sound.play()
    main_menu(bg_img,bg_sound,screen)

