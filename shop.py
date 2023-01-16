# импорт нужных модулей
import pygame
import os
import sys
import main


def show_shop(lvl, check_stop_music_menu):
    '''
    функция для отображения магазина скинов игры
    '''
    # создание холста магазина
    size_window = width, height = 1100, 600
    shop_screen = pygame.display.set_mode(size_window)
    shop_screen.fill(pygame.Color('black'))
    pygame.display.flip()

    # добавление заднего фона окна
    fon_shop_group = pygame.sprite.Group()
    fon_shop_image = pygame.sprite.Sprite(fon_shop_group)
    fon_shop_image.image = pygame.transform.scale(load_image('shop_window_sprites/fon_shop_image.jpg'),
                                                  (width, height))
    fon_shop_image.rect = fon_shop_image.image.get_rect()

    # добавление кнопки выхода в меню игры
    home_button_image = pygame.sprite.Sprite(fon_shop_group)
    home_button_image.image = pygame.transform.scale(load_image('shop_window_sprites\home_button_image.png'),
                                                     (150, 150))
    home_button_image.rect = home_button_image.image.get_rect()
    home_button_image.rect.x = 55
    home_button_image.rect.y = 445

    # список со всеми данными из файла
    with open('for_skins_and_all_points.txt', 'r') as f:
        all_iformation = f.readlines()

    # список с координатами квадратиков, для выбора скина
    coords_rect = [(57, 115), (57, 226), (57, 337), (727, 115), (727, 226), (727, 337), (397, 453)]

    # группа спрайтов для отображения галочки, показывающей какой выбран скин
    mark_group = pygame.sprite.Group()

    # добавление скинов и расстановка их по полочкам
    colors = ['red', 'yellow', 'purpule', 'blue', 'brown', 'green', 'white']
    coords_skin = [(90, 50), (90, 161), (90, 272), (760, 50), (760, 161), (760, 272), (430, 388)]
    for i in range(len(colors)):
        skin = colors[i]
        ninja = pygame.sprite.Sprite(fon_shop_group)
        ninja.image = pygame.transform.scale(load_image(f'shop_window_sprites/run_ninja_3_{skin}.png'), (70, 100))
        ninja.rect = ninja.image.get_rect()
        ninja.rect.x = coords_skin[i][0]
        ninja.rect.y = coords_skin[i][1]

        # добавление галочки, показывающей какой выбран скин
        if all_iformation[0][0:-1] == skin:
            mark = pygame.sprite.Sprite(mark_group)
            mark.image = pygame.transform.scale(load_image('shop_window_sprites\check_mark_image.png'), (40, 40))
            mark.rect = mark.image.get_rect()
            mark.rect.x = coords_rect[i][0]
            mark.rect.y = coords_rect[i][1] - 10

    # добавление переменной с общими очками пользователя
    with open('for_skins_and_all_points.txt', 'r') as f:
        all_points = f.readlines()[1][0:-1]

    # список с индексами купленных скинов
    with open('for_skins_and_all_points.txt', 'r') as f:
        index = [int(i) for i in f.readlines()[2].split()]

    # список с ценами скинов
    prices = [0, 10000, 50000, 130000, 270000, 420000, 1000000]

    # список с координатами для отображения цены
    coord_prices = [(210, 50), (210, 161), (210, 272), (870, 50), (870, 161), (870, 272), (540, 388)]

    # список с координатами кнопки купить
    coords_buy = [(210, 100), (210, 211), (210, 322), (870, 100), (870, 211), (870, 322), (540, 438)]

    # добавление кнопки купить
    buy_group = pygame.sprite.Group()
    if 7 not in index:
        for i in range(len(index)):
            buy = pygame.sprite.Sprite(buy_group)
            buy.image = pygame.transform.scale(load_image('shop_window_sprites\_buy_image.png'), (100, 35))
            buy.rect = buy.image.get_rect()
            buy.rect.x = coords_buy[index[i]][0]
            buy.rect.y = coords_buy[index[i]][1]

    # переменная для музыки в меню
    check_stop_music_menu += 1

    # добавление чека(флага) для перезаписи данных в файле
    check_for_write_f = False

    # добавление чека(флага) и переменной для отображения надписи, что пользователю не хватает очков на покупку скина
    check_no_points = False
    time_for_show_no_points_tekst = 0

    # создание нужного шрифта
    font_36 = pygame.font.Font('data/font/Graffiti_font.ttf', 36)

    # добавление звука клика курсора
    sound_click = pygame.mixer.Sound("data/music/click_cursor.ogg")
    sound_click.set_volume(0.2)

    # добавление звука после покупки скина
    sound_drop_money = pygame.mixer.Sound("data/music/sound_drop_money.wav")
    sound_drop_money.set_volume(0.3)

    # добавление звука, когда не хватает очков для покупки скина
    sound_not_enough_points = pygame.mixer.Sound("data/music/sound_not_enough_points.wav")
    sound_not_enough_points.set_volume(0.3)

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
                if 55 <= mouse_pos[0] <= 205 and 445 <= mouse_pos[1] <= 595:
                    main.show_menu(lvl, check_stop_music_menu)
                for i in range(len(coords_rect)):
                    x = coords_rect[i][0]
                    y = coords_rect[i][1]
                    if x <= mouse_pos[0] <= x + 30 and y <= mouse_pos[1] <= y + 30 and i not in index:
                        mark.rect.x = x
                        mark.rect.y = y - 10
                        all_iformation[0] = colors[i] + '\n'
                        check_for_write_f = True
                    x = coords_buy[i][0]
                    y = coords_buy[i][1]
                    if x <= mouse_pos[0] <= x + 100 and y <= mouse_pos[1] <= y + 35 and i in index:
                        if int(all_iformation[1][0:-1]) >= prices[i]:
                            sound_drop_money.play()
                            check_for_write_f = True
                            all_iformation[1] = str(int(all_iformation[1][0:-1]) - prices[i]) + '\n'
                            if len(all_iformation[2]) > 1:
                                ind = all_iformation[2].index(f'{i}')
                                if i != max(index):
                                    s = all_iformation[2][:ind] + all_iformation[2][ind + 2:len(all_iformation[2]) + 1]
                                else:
                                    s = all_iformation[2][:-2]
                                all_iformation[2] = s
                            else:
                                all_iformation[2] = '7'
                        else:
                            sound_not_enough_points.play()
                            check_no_points = True
                            time_for_show_no_points_tekst = 0

        fon_shop_group.draw(shop_screen)
        draw_all_points(shop_screen, all_points, font_36)
        draw_rect_for_choice_skin(shop_screen, coords_rect, index)
        draw_prices(shop_screen, prices, index, coord_prices, font_36)
        mark_group.draw(shop_screen)
        buy_group.draw(shop_screen)
        if check_for_write_f:
            with open('for_skins_and_all_points.txt', 'w') as f:
                for st in all_iformation:
                    f.write(st)
            with open('for_skins_and_all_points.txt', 'r') as f:
                all_iformation = f.readlines()
                all_points = all_iformation[1][0:-1]
                index = [int(i) for i in all_iformation[2].split()]
            buy_group = pygame.sprite.Group()
            for i in range(len(index)):
                if 7 not in index:
                    buy = pygame.sprite.Sprite(buy_group)
                    buy.image = pygame.transform.scale(load_image('shop_window_sprites\_buy_image.png'), (100, 35))
                    buy.rect = buy.image.get_rect()
                    buy.rect.x = coords_buy[index[i]][0]
                    buy.rect.y = coords_buy[index[i]][1]
        if check_no_points:
            draw_not_enough_points(shop_screen, font_36)
            time_for_show_no_points_tekst += 1
            if time_for_show_no_points_tekst == 70:
                check_no_points = False
                time_for_show_no_points_tekst = 0
        check_for_write_f = False
        pygame.display.flip()
        clock.tick(fps)
    terminate()


def draw_not_enough_points(shop_screen, font_36):
    '''
    функция для отрисовки информации о том, что не хватает очков для покупки скина
    '''
    not_enough_points = font_36.render(f"Not enough points  =(", True, (220, 0, 0))
    not_enough_points_x = 1100 // 2 - not_enough_points.get_width() // 2
    shop_screen.blit(not_enough_points, (not_enough_points_x, 20))


def draw_prices(shop_screen, prices, index, coord_prices, font_36):
    '''
    функция для отрисоавки цен скинов
    '''
    if 7 not in index:
        for i in index:
            price = font_36.render(f"{prices[i]}", True, (220, 220, 220))
            shop_screen.blit(price, coord_prices[i])


def draw_rect_for_choice_skin(shop_screen, coords_rect, index):
    '''
    функция для отрисовки квадратиков, для выбора скина
    '''
    if 7 not in index:
        for i in range(7):
            if i not in index:
                pygame.draw.rect(shop_screen, (230, 230, 230), (coords_rect[i], (30, 30)), 2)
    else:
        for i in range(7):
            pygame.draw.rect(shop_screen, (230, 230, 230), (coords_rect[i], (30, 30)), 2)


def draw_all_points(shop_screen, all_points, font_36):
    '''
    функция для отрисовки общего количества очков пользователя
    '''
    points = font_36.render(f"All Points: {all_points}", True, (0, 200, 0))
    shop_screen.blit(points, (700, 550))


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