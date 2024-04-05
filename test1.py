# import pygame
#
# #image_pass = '/data/data/org.test.myapp/files/app/'
# image_pass = ''
#
# clock = pygame.time.Clock()
#
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# pygame.display.set_caption("Kartashov_Game")
# icon =pygame.image.load(image_pass + 'images/1778592.png')
# pygame.display.set_icon(icon)
#
#
# bg =pygame.image.load(image_pass + 'images/fon-3.jpg').convert()
# walk_right = [
#     pygame.image.load(image_pass + 'images/player/sh-r1.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-r2.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-r3.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-r4.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-r5.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-r6.png').convert_alpha(),
# ]
# walk_left = [
#     pygame.image.load(image_pass + 'images/player/sh-l1.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-l2.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-l3.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-l4.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-l5.png').convert_alpha(),
#     pygame.image.load(image_pass + 'images/player/sh-l6.png').convert_alpha(),
# ]
#
# ghost =pygame.image.load(image_pass + 'images/ghost.png').convert_alpha()
# ghost_list_in_game = []
#
# player_anim_count =0
# bg_x = 0
#
# player_speed =5
# player_x =640
# player_y =500
#
# is_jump = False
# jump_count = 12
#
# bg_sound = pygame.mixer.Sound(image_pass + 'sounds/music.mp3')
# #bg_sound.play()
#
# ghost_timer = pygame.USEREVENT + 1
# pygame.time.set_timer(ghost_timer, 3000)
#
# label =pygame.font.Font(image_pass + 'fonts/Art-Victorian.ttf', 40)
# lose_label = label.render('Вы проиграли!', False, (193, 196, 199))
# restart_label = label.render('Начать заново', False, (115, 132, 148))
# restart_label_rect = restart_label.get_rect(topleft=(500, 300))
#
# bullets_left =5
# bullet = pygame.image.load(image_pass + 'images/bullet1.png').convert_alpha()
# bullets = []
#
# gameplay =True
#
# running = True
# while running:
# тело цикла-----------------------------------------------------------------------

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x+1280, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate( ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x >340:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x <940:
            player_x +=player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -12:
                if jump_count >0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 12

        if player_anim_count ==5:
            player_anim_count =0
        else:
            player_anim_count +=1

        bg_x -= 5
        if bg_x == -1280:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 10

                if el.x > 1300:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (500, 250))
        screen.blit(restart_label, (restart_label_rect))

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 640
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    # тело цикла-----------------------------------------------------------------------
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(1300, 500)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x+30, player_y+60)))
            bullets_left -= 1

    clock.tick(10)