# импорт нужных модулей
import pygame
import os
import sys
import play
import main


def show_pause_window(lvl, points, check_stop_music_menu):
    '''
    функция отображения окна паузы в игре
    '''
    # создание холста паузы
    size_window = width, height = 1100, 600
    pause_screen = pygame.display.set_mode(size_window)
    pause_screen.fill(pygame.Color('black'))
    pygame.display.flip()

    # добавление заднего фона окна паузы
    fon_pause_group = pygame.sprite.Group()
    fon_pause_window = pygame.sprite.Sprite(fon_pause_group)
    fon_pause_window.image = pygame.transform.scale(load_image('pause_window_sprites/fon_pause_window.jpg'),
                                                    (width, height))
    fon_pause_window.rect = fon_pause_window.image.get_rect()

    # добавление кнопки выхода из приложения
    exit_image = pygame.sprite.Sprite(fon_pause_group)
    exit_image.image = pygame.transform.scale(load_image('pause_window_sprites\exit_image.png'), (40, 40))
    exit_image.rect = exit_image.image.get_rect()
    exit_image.rect.x = 10
    exit_image.rect.y = 10

    # добавление кнопки выхода в меню игры
    home_button_image = pygame.sprite.Sprite(fon_pause_group)
    home_button_image.image = pygame.transform.scale(load_image('pause_window_sprites\home_button_image.png'),
                                                     (190, 190))
    home_button_image.rect = home_button_image.image.get_rect()
    home_button_image.rect.center = (300, 395)

    # добавление кнопки продолжения игры
    continue_button_image = pygame.sprite.Sprite(fon_pause_group)
    continue_button_image.image = pygame.transform.scale(load_image('pause_window_sprites\continue_button_image.png'),
                                                     (195, 195))
    continue_button_image.rect = continue_button_image.image.get_rect()
    continue_button_image.rect.center = (550, 400)

    # добавление кнопки для начала игры заново
    reset_button_image = pygame.sprite.Sprite(fon_pause_group)
    reset_button_image.image = pygame.transform.scale(load_image('pause_window_sprites/reset_button_image.png'),
                                                         (150, 160))
    reset_button_image.rect = reset_button_image.image.get_rect()
    reset_button_image.rect.center = (807, 405)

    # создание нужных шрифтов
    font_100 = pygame.font.Font('data/font/Graffiti_font.ttf', 100)
    font_36 = pygame.font.Font('data/font/Graffiti_font.ttf', 36)

    # добавление звука клика курсора
    sound_click = pygame.mixer.Sound("data/music/click_cursor.ogg")
    sound_click.set_volume(0.2)

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
                if 453 <= mouse_pos[0] <= 647 and 303 <= mouse_pos[1] <= 497:
                    pygame.mixer.music.unpause()
                    return True
                elif 732 <= mouse_pos[0] <= 882 and 325 <= mouse_pos[1] <= 485:
                    play.show_play(lvl, check_stop_music_menu)
                elif 205 <= mouse_pos[0] <= 395 and 300 <= mouse_pos[1] <= 490:
                    main.show_menu(lvl, check_stop_music_menu)
                elif 10 <= mouse_pos[0] <= 50 and 10 <= mouse_pos[1] <= 50:
                    terminate()
        fon_pause_group.draw(pause_screen)
        draw_pause(pause_screen, font_100)
        draw_information(pause_screen, lvl, points, font_36)
        pygame.display.flip()
        clock.tick(fps)
    terminate()


def draw_information(pause_screen, lvl, points, font_36):
    '''
    функция для отображение текущего уроня и очков пользователя в игре
    '''
    lvl = font_36.render(f"Lvl: {lvl}", True, (220, 220, 220))
    points = font_36.render(f"Points: {points}", True, (220, 220, 220))
    pause_screen.blit(lvl, (330, 150))
    pause_screen.blit(points, (330, 190))


def draw_pause(pause_screen, font_100):
    '''
    функция для отрисовки названия игры в меню
    '''
    title = font_100.render("Pause", True, (0, 0, 0))
    title_x = 1100 // 2 - title.get_width() // 2
    pause_screen.blit(title, (title_x, 50))


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