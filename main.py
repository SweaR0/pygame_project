# импорт нужных модулей
import pygame
import os
import sys
import play
import shop


def show_menu(lvl, check_stop_music_menu):
    '''
    функция отображения главного меню игры
    '''
    # создание холста меню и инициализация pygame
    pygame.init()
    size_window = width, height = 1100, 600
    menu_screen = pygame.display.set_mode(size_window)
    pygame.display.set_caption('Ninja')
    menu_screen.fill(pygame.Color('black'))
    pygame.display.flip()

    # добавление заднего фона окна меню
    menu_group = pygame.sprite.Group()
    screensaver = pygame.sprite.Sprite(menu_group)
    screensaver.image = pygame.transform.scale(load_image('menu_window_sprites\screensaver.jpg'), (width, height))
    screensaver.rect = screensaver.image.get_rect()

    # добавление кнопки выхода из приложения
    exit_image = pygame.sprite.Sprite(menu_group)
    exit_image.image = pygame.transform.scale(load_image('menu_window_sprites\exit_image.png'), (40, 40))
    exit_image.rect = exit_image.image.get_rect()
    exit_image.rect.x = 10
    exit_image.rect.y = 10

    # добавление кнопки магазина
    shop_image = pygame.sprite.Sprite(menu_group)
    shop_image.image = pygame.transform.scale(load_image('menu_window_sprites\shop_image.png'), (70, 70))
    shop_image.rect = shop_image.image.get_rect()
    shop_image.rect.x = 1010
    shop_image.rect.y = 0

    # добавления списка с координатами уровней игры
    lvl_coords = [(100, 400, 216, 435), (100, 460, 221, 495), (100, 520, 224, 555)]

    # создание нужных шрифтов
    font_100 = pygame.font.Font('data/font/Graffiti_font.ttf', 100)
    font_36 = pygame.font.Font('data/font/Graffiti_font.ttf', 36)
    font_80 = pygame.font.Font('data/font/Graffiti_font.ttf', 80)

    # добавление звука клика курсора
    sound_click = pygame.mixer.Sound("data/music/click_cursor.ogg")
    sound_click.set_volume(0.2)

    # добавление фоновой музыки меню
    if check_stop_music_menu == 0:
        pygame.mixer.music.load("data/music/fon_menu_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.13)

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
                if 465 <= mouse_pos[0] <= 635 and 480 <= mouse_pos[1] <= 560:
                    pygame.mixer.music.pause()
                    play.show_play(lvl, check_stop_music_menu)
                for i in range(3):
                    coords = lvl_coords[i]
                    if coords[0] <= mouse_pos[0] <= coords[2] and coords[1] <= mouse_pos[1] <= coords[3]:
                        lvl = i + 1
                if 1010 <= mouse_pos[0] <= 1080 and 0 <= mouse_pos[1] <= 70:
                    shop.show_shop(lvl, check_stop_music_menu)
                elif 10 <= mouse_pos[0] <= 50 and 10 <= mouse_pos[1] <= 50:
                    terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.music.pause()
                play.show_play(lvl, check_stop_music_menu)
        menu_group.draw(menu_screen)
        draw_title(menu_screen, font_100)
        draw_records(menu_screen, font_36)
        draw_button_for_start_game(menu_screen, font_80)
        draw_level_selection(menu_screen, lvl, font_36)
        pygame.display.flip()
        clock.tick(fps)
    terminate()


def draw_title(menu_screen, font_100):
    '''
    функция для отрисовки названия игры в меню
    '''
    title = font_100.render("Ninja", True, (0, 0, 0))
    title_x = 1100 // 2 - title.get_width() // 2
    menu_screen.blit(title, (title_x, 50))


def draw_records(menu_screen, font_36):
    '''
    функция для отрисовки рекордов пользователя
    '''
    records = font_36.render("Records", True, (220, 220, 220))
    menu_screen.blit(records, (860, 350))
    level_1 = font_36.render("Level 1:", True, (220, 220, 220))
    menu_screen.blit(level_1, (770, 400))
    level_2 = font_36.render("Level 2:", True, (220, 220, 220))
    menu_screen.blit(level_2, (770, 460))
    level_3 = font_36.render("Level 3:", True, (220, 220, 220))
    menu_screen.blit(level_3, (770, 520))
    with open('records.txt', 'r') as f:
        list_records = f.readlines()
    record_for_level_1 = font_36.render(list_records[0][0:-1], True, (220, 220, 220))
    menu_screen.blit(record_for_level_1, (930, 400))
    record_for_level_2 = font_36.render(list_records[1][0:-1], True, (220, 220, 220))
    menu_screen.blit(record_for_level_2, (930, 460))
    record_for_level_3 = font_36.render(list_records[2], True, (220, 220, 220))
    menu_screen.blit(record_for_level_3, (930, 520))


def draw_button_for_start_game(menu_screen, font_80):
    '''
    функция для отрисовки кнопки запуска игры
    '''
    pygame.draw.rect(menu_screen, (220, 220, 220), ((465, 480), (170, 80)), 2)
    play = font_80.render("PLAY", True, (220, 220, 220))
    menu_screen.blit(play, (470, 482))


def draw_level_selection(menu_screen, lvl, font_36):
    '''
    функция для отрисовки выбора уровня игры
    '''
    green = (0, 200, 0)
    white = (220, 220, 220)
    level_selection = font_36.render("level selection", True, white)
    menu_screen.blit(level_selection, (30, 350))
    level_1 = font_36.render("Level 1", True, white)
    level_2 = font_36.render("Level 2", True, white)
    level_3 = font_36.render("Level 3", True, white)
    if lvl == 1:
        level_1 = font_36.render("Level 1", True, green)
    elif lvl == 2:
        level_2 = font_36.render("Level 2", True, green)
    elif lvl == 3:
        level_3 = font_36.render("Level 3", True, green)
    menu_screen.blit(level_1, (100, 400))
    menu_screen.blit(level_2, (100, 460))
    menu_screen.blit(level_3, (100, 520))


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


if __name__ == '__main__':
    show_menu(1, 0)