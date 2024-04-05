import pygame
import random
image_pass = ''
clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Kartashov_RunningMan")
icon =pygame.image.load(image_pass + 'images/1778592.png')
pygame.display.set_icon(icon)


bg = pygame.image.load(image_pass + 'images/fon-3.jpg').convert()
walk_right = [
    pygame.image.load(image_pass + 'images/sh-r1.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-r2.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-r3.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-r4.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-r5.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-r6.png').convert_alpha(),
]
walk_left = [
    pygame.image.load(image_pass + 'images/sh-l1.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-l2.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-l3.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-l4.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-l5.png').convert_alpha(),
    pygame.image.load(image_pass + 'images/sh-l6.png').convert_alpha(),
]

ghost = pygame.image.load(image_pass + 'images/ghost.png').convert_alpha()
ghost_list_in_game = []

target = pygame.image.load(image_pass + 'images/target.png').convert_alpha()
target_list_in_game = []

bullet = pygame.image.load(image_pass + 'images/bullet1.png').convert_alpha()
bullets_left = 10
bullets = []

ammo = pygame.image.load(image_pass + 'images/ammo.png').convert_alpha()
ammo_list_in_game = []



player_anim_count =0
bg_x = 0

player_speed =5
player_x =640
player_y =500

is_jump = False
jump_count = 12


bg_sound1 = pygame.mixer.Sound(image_pass + 'sounds/music.mp3')
bg_sound1.play()


ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, random.randint(1000,3000))

target_timer = pygame.USEREVENT + 2
pygame.time.set_timer(target_timer, random.randint(1000,3000))

ammo_timer = pygame.USEREVENT + 3
pygame.time.set_timer(ammo_timer, random.randint(1000,10000))




label = pygame.font.Font(image_pass + 'fonts/Art-Victorian.ttf', 40)
lose_label = label.render('Вы проиграли!', False, (193, 196, 199))
restart_label = label.render('Начать заново', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(500, 300))
bullets_label = label.render(f'Осталось пуль: {bullets_left}', False, (193, 196, 199))



gameplay =True

running = True
while running:
# тело цикла-----------------------------------------------------------------------


    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x+1280, 0))

    screen.blit(bullets_label, (500, 50))


    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False


        if target_list_in_game:
            for (i, el) in enumerate(target_list_in_game):
                screen.blit(target, el)
                el.x -= 10

                if el.x < -10:
                    target_list_in_game.pop(i)


        if ammo_list_in_game:
            for (i, el) in enumerate(ammo_list_in_game):
                screen.blit(ammo, el)
                el.x -= 10

                if el.x < -10:
                    ammo_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    bullets_left += 10
                    ammo_list_in_game.pop(i)
#                    break





        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 340:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 940:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -12:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 12

        if player_anim_count == 5:
            player_anim_count = 0
        else:
            player_anim_count += 1

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

                if target_list_in_game:
                    for (index, target_el) in enumerate(target_list_in_game):
                        if el.colliderect(target_el):
                            target_list_in_game.pop(index)
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

    bullets_label = label.render(f'Осталось пуль: {bullets_left}', False, (193, 196, 199))
    screen.blit(bullets_label, (500, 50))

    # тело цикла-----------------------------------------------------------------------
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        rnd = random.randint(0, 2)
        if rnd == 0:
            if event.type == ghost_timer:
                ghost_list_in_game.append(ghost.get_rect(topleft=(1300, 500)))
        elif rnd == 1:
            if event.type == target_timer:
                target_list_in_game.append(target.get_rect(topleft=(1300, random.randint(200, 400))))
        elif rnd == 2:
            if event.type == ammo_timer:
                ammo_list_in_game.append(ammo.get_rect(topleft=(1300, 600)))



        if gameplay and event.type == pygame.MOUSEBUTTONUP and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 60)))
            bullets_left -= 1

    clock.tick(10)






