# импорт нужных модулей
import pygame
import os
import sys
import main
import play


def show_end_game(lvl, points, new_record, check_stop_music_menu):
    '''
    функция отображения окна окончания игры
    '''
    # создание холста окончания игры
    size_window = width, height = 1100, 600
    ending_screen = pygame.display.set_mode(size_window)
    ending_screen.fill(pygame.Color('black'))
    pygame.display.flip()

    # добавление звука окончания игры(когда новый рекорд)
    sound_victory = pygame.mixer.Sound('data/music/sound_victory.wav')
    sound_victory.set_volume(0.2)

    # добавление звука окончания игры(когда не новый рекорд)
    sound_game_over = pygame.mixer.Sound('data/music/sound_game_over.wav')
    sound_game_over.set_volume(0.2)

    # добавление заднего фона окна окончания игры
    fon_ending_group = pygame.sprite.Group()
    fon_ending_window = pygame.sprite.Sprite(fon_ending_group)
    fon_ending_window.image = pygame.transform.scale(load_image('ending_window_sprites/fon_ending_window.jpg'),
                                                     (width, height))
    fon_ending_window.rect = fon_ending_window.image.get_rect()

    # добавление кнопки выхода из приложения
    exit_image = pygame.sprite.Sprite(fon_ending_group)
    exit_image.image = pygame.transform.scale(load_image('ending_window_sprites\exit_image.png'), (40, 40))
    exit_image.rect = exit_image.image.get_rect()
    exit_image.rect.x = 10
    exit_image.rect.y = 10

    # добавление кнопки выхода меню игры
    home_button_image = pygame.sprite.Sprite(fon_ending_group)
    home_button_image.image = pygame.transform.scale(load_image('ending_window_sprites\home_button_image.png'),
                                                     (190, 190))
    home_button_image.rect = home_button_image.image.get_rect()
    home_button_image.rect.center = (300, 395)

    # добавление кнопки для начала игры заново
    reset_button_image = pygame.sprite.Sprite(fon_ending_group)
    reset_button_image.image = pygame.transform.scale(load_image('pause_window_sprites/reset_button_image.png'),
                                                      (150, 160))
    reset_button_image.rect = reset_button_image.image.get_rect()
    reset_button_image.rect.center = (807, 405)

    # добавление спрайта "новый рекорд"(звёздочка) в зависимости от того был ли поставлен новый рекорд
    if new_record:
        new_record_group = pygame.sprite.Group()
        star = pygame.sprite.Sprite(new_record_group)
        star.image = pygame.transform.scale(load_image('ending_window_sprites/star.png'), (170, 170))
        star.rect = star.image.get_rect()
        star.rect.x = 800
        star.rect.y = 60

    # создание нужных шрифтов
    font_100 = pygame.font.Font('data/font/Graffiti_font.ttf', 100)
    font_36 = pygame.font.Font('data/font/Graffiti_font.ttf', 36)
    font_20 = pygame.font.Font('data/font/Graffiti_font.ttf', 20)

    # добавление звука клика курсора
    sound_click = pygame.mixer.Sound("data/music/click_cursor.ogg")
    sound_click.set_volume(0.2)

    # включение нужной мелодии в зависимости от того был ли поставлен новый рекорд
    if new_record:
        sound_victory.play()
    else:
        sound_game_over.play()

    # добавление ограничителя кадров в секунду
    clock = pygame.time.Clock()
    fps = 60

    # игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sound_click.play()
                mouse_pos = event.pos
                if 732 <= mouse_pos[0] <= 882 and 325 <= mouse_pos[1] <= 485:
                    sound_victory.stop()
                    sound_game_over.stop()
                    play.show_play(lvl, check_stop_music_menu)
                elif 205 <= mouse_pos[0] <= 395 and 300 <= mouse_pos[1] <= 490:
                    sound_victory.stop()
                    sound_game_over.stop()
                    main.show_menu(lvl, check_stop_music_menu)
                elif 10 <= mouse_pos[0] <= 50 and 10 <= mouse_pos[1] <= 50:
                    terminate()
        fon_ending_group.draw(ending_screen)
        draw_game_over(ending_screen, font_100)
        if new_record:
            new_record_group.draw(ending_screen)
            draw_new_record(ending_screen, font_20)
            draw_information(ending_screen, lvl, points, (255, 0, 190), font_36)
        else:
            draw_information(ending_screen, lvl, points, (220, 220, 220), font_36)
        pygame.display.flip()
        clock.tick(fps)
    terminate()


def draw_information(ending_screen, lvl, points, color, font_36):
    '''
    функция для отображение текущего уроня и очков пользователя в игре
    '''
    lvl = font_36.render(f"Lvl: {lvl}", True, color)
    points = font_36.render(f"Points: {points}", True, color)
    ending_screen.blit(lvl, (230, 165))
    ending_screen.blit(points, (230, 205))


def draw_new_record(ending_screen, font_20):
    '''
    функция для отоображения надписи новый рекорд внутри звёздочки
    '''
    new_record = font_20.render("New record", True, (255, 0, 190))
    ending_screen.blit(new_record, (833, 130))


def draw_game_over(ending_screen, font_100):
    '''
    функция для отображения надписи "Game over"
    '''
    game_over = font_100.render("Game over", True, (0, 0, 0))
    game_over_x = 1100 // 2 - game_over.get_width() // 2
    ending_screen.blit(game_over, (game_over_x, 50))


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