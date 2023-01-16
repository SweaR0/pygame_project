# импорт нужных модулей
import pygame
import sys
import os
from random import randint
import pause
import ending


def show_play(lvl, check_stop_music_menu):
    '''
    функция отображения самой игры
    '''
    # создание нужных шрифтов
    font_50 = pygame.font.Font('data/font/Graffiti_font.ttf', 50)
    font_36 = pygame.font.Font('data/font/Graffiti_font.ttf', 36)

    # создание холста игры
    size_window = width, height = 1100, 600
    play_screen = pygame.display.set_mode(size_window)
    play_screen.fill(pygame.Color('black'))
    draw_loading(play_screen, font_50)
    pygame.display.flip()

    # загрузка нужного скина персонажа
    with open('for_skins_and_all_points.txt', 'r') as f:
        skin = f.readlines()[0][0:-1]

    # создание 5 групп спрайтов для анимации бега персонажа игры
    group_run_ninja_1 = pygame.sprite.Group()
    run_ninja_1 = pygame.sprite.Sprite(group_run_ninja_1)
    run_ninja_1.image = pygame.transform.scale(load_image(f'play_window_sprites/run_ninja_1_{skin}.png'), (100, 150))
    run_ninja_1.rect = run_ninja_1.image.get_rect()
    run_ninja_1.rect.x = 130
    run_ninja_1.rect.y = 350

    group_run_ninja_2 = pygame.sprite.Group()
    run_ninja_2 = pygame.sprite.Sprite(group_run_ninja_2)
    run_ninja_2.image = pygame.transform.scale(load_image(f'play_window_sprites/run_ninja_2_{skin}.png'), (100, 150))
    run_ninja_2.rect = run_ninja_2.image.get_rect()
    run_ninja_2.rect.x = 130
    run_ninja_2.rect.y = 350

    group_run_ninja_3 = pygame.sprite.Group()
    run_ninja_3 = pygame.sprite.Sprite(group_run_ninja_3)
    run_ninja_3.image = pygame.transform.scale(load_image(f'play_window_sprites/run_ninja_3_{skin}.png'), (100, 150))
    run_ninja_3.rect = run_ninja_3.image.get_rect()
    run_ninja_3.rect.x = 130
    run_ninja_3.rect.y = 350

    group_run_ninja_4 = pygame.sprite.Group()
    run_ninja_4 = pygame.sprite.Sprite(group_run_ninja_4)
    run_ninja_4.image = pygame.transform.scale(load_image(f'play_window_sprites/run_ninja_4_{skin}.png'), (100, 150))
    run_ninja_4.rect = run_ninja_4.image.get_rect()
    run_ninja_4.rect.x = 130
    run_ninja_4.rect.y = 350

    group_run_ninja_5 = pygame.sprite.Group()
    run_ninja_5 = pygame.sprite.Sprite(group_run_ninja_5)
    run_ninja_5.image = pygame.transform.scale(load_image(f'play_window_sprites/run_ninja_5_{skin}.png'), (100, 150))
    run_ninja_5.rect = run_ninja_5.image.get_rect()
    run_ninja_5.rect.x = 130
    run_ninja_5.rect.y = 350

    # создание чеков для реализации анимации бега персонажа игры
    check_run_ninja = 0
    check_sprite_ninja = 1

    # добавление заднего фона окна игры
    fon_game_group = pygame.sprite.Group()
    screensaver = pygame.sprite.Sprite(fon_game_group)
    screensaver.image = pygame.transform.scale(load_image('play_window_sprites/fon_game_window.png'), (1100, height))
    screensaver.rect = screensaver.image.get_rect()
    screensaver.rect.x = 0
    screensaver.rect.y = 0

    fon_game_group_2 = pygame.sprite.Group()
    screensaver_2 = pygame.sprite.Sprite(fon_game_group_2)
    screensaver_2.image = pygame.transform.scale(load_image('play_window_sprites/fon_game_window.png'), (1100, height))
    screensaver_2.rect = screensaver_2.image.get_rect()
    screensaver_2.rect.x = 1100
    screensaver_2.rect.y = 0

    # добавление кнопки паузы
    pause_group = pygame.sprite.Group()
    pause_image = pygame.sprite.Sprite(pause_group)
    pause_image.image = pygame.transform.scale(load_image('play_window_sprites/pause_image.png'), (55, 55))
    pause_image.rect = pause_image.image.get_rect()
    pause_image.rect.x = 10
    pause_image.rect.y = 10

    # добавление группы спрайтов с камнями, которые надо будет перепрыгивать
    obstacle_group = pygame.sprite.Group()
    for i in range(6):
        if i == 0:
            stone = pygame.sprite.Sprite(obstacle_group)
            stone.image = pygame.transform.scale(load_image('play_window_sprites/stone.png'), (40, 40))
            stone.rect = stone.image.get_rect()
            stone.rect.x = 1120
            stone.rect.y = 460
            last_coords_stone = stone.rect.x
        else:
            stone = pygame.sprite.Sprite(obstacle_group)
            stone.image = pygame.transform.scale(load_image('play_window_sprites/stone.png'), (40, 40))
            stone.rect = stone.image.get_rect()
            stone.rect.x = last_coords_stone + randint(270, 600 - 50 * lvl)
            stone.rect.y = 460
            last_coords_stone = stone.rect.x

    # добавление подарков с дополнительными очками
    present_group = pygame.sprite.Group()
    present = pygame.sprite.Sprite(present_group)
    present.image = pygame.transform.scale(load_image('play_window_sprites/present.png'), (90, 90))
    present.rect = present.image.get_rect()
    present.rect.x = last_coords_stone + 150
    present.rect.y = 430

    # добавление чека(флага) для добавления подарка
    check_for_add_present = False

    # добавление счётчика очков в игре
    points = 0

    # добавление чека(флага) для включения анимации прыжка
    jump_check = False
    sign_to_jump = '-'

    # добавление списка для хранения координат летучей мыши, которую убил пользователь
    coords_of_deceased_bat = []

    # добавление чека(флага) для отрисовки доролнительных очков, полученных за подарок
    check_for_draw_dop_points_present = False
    timer_for_check_present = 0

    # добавление звука для поимки награды(убить летующую мышь)
    sound_for_catching_rewards = pygame.mixer.Sound("data/music/sound_for_catching_rewards.ogg")
    sound_for_catching_rewards.set_volume(0.17)

    # добавление звука прыжка
    sound_for_jump = pygame.mixer.Sound("data/music/sound_for_jump.wav")

    # добавление звука клика курсора
    sound_click = pygame.mixer.Sound("data/music/click_cursor.ogg")
    sound_click.set_volume(0.1)

    # добавление звука столкновения персонажа с камнем
    sound_falls = pygame.mixer.Sound('data/music/sound_falls.wav')

    # добавление переменной с прошлым рекордом на выбранном уровне, для проверки поставил ли пользователь новый рекорд
    with open('records.txt', 'r') as f:
        list_records = f.readlines()
    if lvl != 3:
        past_record = list_records[lvl - 1][0:-1]
    else:
        past_record = list_records[2]

    # создание группы спрайтов с летучими мышами
    enemy_bat_group = pygame.sprite.Group()
    size_bat = (130 - 10 * lvl, 130 - 10 * lvl)
    for _ in range(5):
        bat = pygame.sprite.Sprite(enemy_bat_group)
        bat.image = pygame.transform.scale(load_image('play_window_sprites/bat.png'), size_bat)
        bat.rect = bat.image.get_rect()
        bat.rect.x = randint(240, 980)
        bat.rect.y = randint(121, 220)

    # переменная для музыки в меню
    check_stop_music_menu = 0

    # добавление фоновой музыки игры
    pygame.mixer.music.load("data/music/fon_game_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    # добавление ограничителя кадров в секунду
    clock = pygame.time.Clock()
    fps = 60

    # игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jump_check = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sound_click.play()
                mouse_pos = event.pos
                for bat in enemy_bat_group:
                    x = bat.rect.x
                    y = bat.rect.y
                    if x <= mouse_pos[0] <= x + 120 and y <= mouse_pos[1] <= y + 120:
                        sound_for_catching_rewards.play()
                        coords_of_deceased_bat.append((x, y))
                        points += 10 * lvl
                        bat.remove(enemy_bat_group)
                if 15 <= mouse_pos[0] <= 60 and 15 <= mouse_pos[1] <= 60:
                    pygame.mixer.music.pause()
                    pause.show_pause_window(lvl, points, check_stop_music_menu)
        fon_game_group.draw(play_screen)
        fon_game_group_2.draw(play_screen)
        pause_group.draw(play_screen)
        draw_points(play_screen, points, font_36)
        enemy_bat_group.draw(play_screen)
        draw_plus_point(play_screen, coords_of_deceased_bat, lvl, font_36)
        obstacle_group.draw(play_screen)
        present_group.draw(play_screen)

        for stone in obstacle_group:
            if pygame.sprite.collide_rect(run_ninja_3, stone):
                pygame.mixer.music.pause()
                sound_falls.play()
                with open('for_skins_and_all_points.txt', 'r') as f:
                    inf = f.readlines()
                inf[1] = str(int(inf[1][0:-1]) + points) + '\n'
                with open('for_skins_and_all_points.txt', 'w') as f:
                    for el in inf:
                        f.write(el)
                if points > int(past_record):
                    if lvl != 3:
                        list_records[lvl - 1] = f'{points}' + '\n'
                    else:
                        list_records[2] = f'{points}'
                    with open('records.txt', 'w') as f:
                        for el in list_records:
                            f.write(el)
                    ending.show_end_game(lvl, points, True, check_stop_music_menu)
                else:
                    ending.show_end_game(lvl, points, False, check_stop_music_menu)

        if pygame.sprite.collide_rect(run_ninja_3, present) and check_for_add_present == False:
            sound_for_catching_rewards.play()
            points += 100 * lvl
            check_for_draw_dop_points_present = True
            check_for_add_present = True
            for present in present_group:
                present.remove(present_group)

        if not jump_check:
            if check_sprite_ninja == 1:
                group_run_ninja_1.draw(play_screen)
            elif check_sprite_ninja == 2:
                group_run_ninja_2.draw(play_screen)
            elif check_sprite_ninja == 3:
                group_run_ninja_1.draw(play_screen)
            elif check_sprite_ninja == 4:
                group_run_ninja_3.draw(play_screen)
            elif check_sprite_ninja == 5:
                group_run_ninja_4.draw(play_screen)
            elif check_sprite_ninja == 6:
                group_run_ninja_5.draw(play_screen)
            elif check_sprite_ninja == 7:
                group_run_ninja_4.draw(play_screen)
            elif check_sprite_ninja == 8:
                group_run_ninja_3.draw(play_screen)
        else:
            group_run_ninja_3.draw(play_screen)
        check_run_ninja += 1

        if check_run_ninja % (10 // lvl) == 0:
            points += 1
            check_sprite_ninja += 1
            if check_sprite_ninja > 8:
                check_sprite_ninja = 1
            if jump_check:
                if sign_to_jump == '-':
                    run_ninja_3.rect.y -= 20
                else:
                    run_ninja_3.rect.y += 20
                if run_ninja_3.rect.y == 130:
                    sign_to_jump = '+'
                elif run_ninja_3.rect.y == 350:
                    sound_for_jump.play()
                    sign_to_jump = '-'
                    jump_check = False
        if check_run_ninja % 20 == 0 and len(coords_of_deceased_bat) > 0:
            del coords_of_deceased_bat[0]

        screensaver.rect.x -= 1 * lvl
        screensaver_2.rect.x -= 1 * lvl
        if screensaver_2.rect.right <= 1103:
            screensaver.rect.x = 0
            screensaver_2.rect.x = 1100

        last_coords_stone -= 1 * lvl
        for obstacle in obstacle_group:
            obstacle.rect.x -= 1 * lvl
            if obstacle.rect.right < 0:
                obstacle.remove(obstacle_group)
                stone = pygame.sprite.Sprite(obstacle_group)
                stone.image = pygame.transform.scale(load_image('play_window_sprites/stone.png'), (40, 40))
                stone.rect = stone.image.get_rect()
                stone.rect.x = last_coords_stone + randint(270, 600 - 50 * lvl)
                stone.rect.y = 460
                last_coords_stone = stone.rect.x
                if check_for_add_present:
                    present_group = pygame.sprite.Group()
                    present = pygame.sprite.Sprite(present_group)
                    present.image = pygame.transform.scale(load_image('play_window_sprites/present.png'), (90, 90))
                    present.rect = present.image.get_rect()
                    present.rect.x = last_coords_stone + 150
                    present.rect.y = 430
                    check_for_add_present = False

        for bat in enemy_bat_group:
            bat.rect.x += randint(-3, 3)
            bat.rect.y += randint(-3, 3)
            if bat.rect.x > 980:
                bat.rect.x = 980
            elif bat.rect.x < 240:
                bat.rect.x = 240
            if bat.rect.y > 220:
                bat.rect.y = 220
            elif bat.rect.y < 121:
                bat.rect.y = 121

        if len(enemy_bat_group) == 0:
            size_bat = (130 - 10 * lvl, 130 - 10 * lvl)
            for _ in range(5):
                bat = pygame.sprite.Sprite(enemy_bat_group)
                bat.image = pygame.transform.scale(load_image('play_window_sprites/bat.png'), size_bat)
                bat.rect = bat.image.get_rect()
                bat.rect.x = randint(121, 980)
                bat.rect.y = randint(121, 220)

        present.rect.x -= 1 * lvl
        if present.rect.right <= 0:
            present.rect.x = 2500

        if check_for_draw_dop_points_present and timer_for_check_present <= 60:
            draw_points_for_the_present(play_screen, 100 * lvl, font_36)
            timer_for_check_present += 1
        else:
            timer_for_check_present = 0
            check_for_draw_dop_points_present = False

        pygame.display.flip()
        clock.tick(fps)
    terminate()


def draw_loading(play_screen, font_50):
    '''
    функция для отображения надписи "Loading..." перед запуском игры
    '''
    loading = font_50.render("Loading...", True, (220, 220, 220))
    loading_x = 1100 // 2 - loading.get_width() // 2
    loading_y = 600 // 2 - loading.get_height() // 2
    play_screen.blit(loading, (loading_x, loading_y))


def draw_points_for_the_present(play_screen, plus_points, font_36):
    '''
    функция для отображения дополнительных очков, полученных за поимку приза
    '''
    dop_point = font_36.render(f"+{plus_points}", True, (0, 200, 0))
    play_screen.blit(dop_point, (960, 60))


def draw_plus_point(play_screen, coords_of_deceased_bat, lvl, font_36):
    '''
    функция для отрисовки дополнительных очков на месте убитой летучей мыши
    '''
    for coo in coords_of_deceased_bat:
        dop_point = font_36.render(f"+{10 * lvl}", True, (220, 220, 220))
        play_screen.blit(dop_point, coo)


def draw_points(play_screen, points, font_36):
    '''
    фунция для отображения набранных очков пользователя
    '''
    count_points = font_36.render(f"Points: {points}", True, (220, 220, 220))
    play_screen.blit(count_points, (800, 20))


def load_image(name):
    '''
    функция для загрузки изображеия
    '''
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def terminate():
    '''
    функция выхода из приложения
    '''
    pygame.quit()
    sys.exit()