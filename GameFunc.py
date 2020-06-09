import math
import sys
from Ship import Ship
from Buttons import *
import random
import time
import pygame


# screen, game_set, play_btn, myfield, enemyfield,
# addship_btns, myfleet, enemyfleet, start_btn, info
# все события
def Events(self, gd):
    self._gd = gd
    if gd.game_set.game_started and not gd.game_set.my_turn:
        pygame.mouse.set_visible(False)
        # time.sleep(1)
        # fireee(gd, 0, 0)
        # time.sleep(1)
        draw_screen(gd)
        
    else:
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # нажатие на крестик
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:  # что делать, когда отпускаем кнопку мыши
                if event.button == 1:   # левая кнопка мыши
                    # считываем координаты мыши
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # проверяем, нажали ли мы кнопку Плей
                    check_play(gd, mouse_x, mouse_y)

                    # проверяет, нажали ди мы кнопку добавления кораблей на поле
                    check_addships(gd, mouse_x, mouse_y)

                    # проверяет, нажали ли мы кнопку Старт Баттл
                    check_start(self, gd, mouse_x, mouse_y)

                    # Проверяет, есть ли еще не поставленный корабль (он висит над полем)
                    for ship in gd.myfleet:
                        if ship.move:  # параметр, определяющий, что мы двигаем корабль

                            # разместить корабль в указанной клетке
                            locate_ship(gd, mouse_x, mouse_y, ship)

                    # если битва началась и моя очередь ходить, то . . .
                    if gd.game_set.game_started and gd.game_set.my_turn:
                        # и если я попал по полю противника . . .
                        if gd.enemyfield.rect.collidepoint(mouse_x, mouse_y):
                            # "огооонь!!1!"
                            fireee(gd, mouse_x, mouse_y)
                            draw_screen(gd)

                # если мы нажали правую кнопку мыши
                if event.button == 3:
                    for ship in gd.myfleet:
                        # если есть корабль, который мы двигаем
                        if ship.move:
                            # поменять направление
                            ship.change_dir()
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            # передвинуть корабль к указателю мыши
                            move_ship(gd, mouse_x, mouse_y, ship)

            for ship in gd.myfleet:
                # если есть корабль, который мы двигаем . . .
                if ship.move:
                    # если мышка двигалась . . .
                    if event.type == pygame.MOUSEMOTION:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # передвинуть корабль к указателю мыши
                        move_ship(gd, mouse_x, mouse_y, ship)


def turnCommand(self):
    """Команда /turn (зробити хід)."""
    self.myturn = True


def hitCommand(self, arg):
    pos = arg[:2]
    xy = [int(pos[0]), int(pos[1])]
    arg = arg[2:]



def fireCommand(self, pos):
    xy = [int(pos[0]), int(pos[1])]
    if self._gd.myfield.data[xy[0]][xy[1]].ship_is_here:
        self.sendMessage('/hit {}True'.format(pos))
    else:
        self.sendMessage('/hit {}False'.format(pos))


# ф-ция перерисовки экрана
def draw_screen(gd):
    if gd.game_set.game_started:
        print('draw screen')
    gamebg = gd.game_set.bg  # Фон (звёзды)
    gd.screen.blit(gamebg, (0, 0))
    gd.info.message()
    # Рисует клетки
    gd.myfield.draw_field(gd.screen)
    gd.enemyfield.draw_field(gd.screen)

    # кол-ство уничтоженных кораблей противника(en_dest) и моих(my_dest)
    my_dest = 0
    en_dest = 0
    # рисует корабли
    for ship in gd.myfleet:
        ship.draw(gd.screen)
        if ship.destroyed:
            my_dest += 1
    # корабли противника рисуем только те, что уже уничтожены
    for ship in gd.enemyfleet:
        if ship.destroyed:
            ship.draw(gd.screen)
            en_dest += 1

    # если расставили еще не все корабли
    for ship_btn in gd.addship_btns:
        if ship_btn.active:
            # рисуем кнопку для расстановки соотв. корабля
            ship_btn.csb_draw()

    # если еще не нарисована кнопка Старт Баттл
    if not gd.start_btn.active:
        # если все кнопки расстановки кораблей не активны (мы всес уже поставили) . . .
        if gd.addship_btns[0].ships_left == 0 \
           and gd.addship_btns[1].ships_left == 0 \
           and gd.addship_btns[2].ships_left == 0 \
           and gd.addship_btns[3].ships_left == 0 \
           and not gd.myfleet[len(gd.myfleet)-1].move and not gd.game_set.game_started:
            # активируем кнопку Старт Баттл и рисуем ее
            gd.start_btn.active = True
            gd.start_btn.startbuttondraw()
        else:
            gd.info.show()
    else:
        # если кнопка уже активна - рисуем
        gd.start_btn.startbuttondraw()

    if len(gd.myfleet) != 0 and len(gd.enemyfleet) != 0:
        if my_dest == len(gd.myfleet):
            gd.info.msg = '. . .Defeat. . .'
            gd.info.message()
            gd.info.show()
            time.sleep(10)

        elif en_dest == len(gd.enemyfleet):
            gd.info.msg = 'Victory!'
            gd.info.message()
            gd.info.show()
            time.sleep(10)


# проверяем, нажали ли мы кнопку Плей
def check_play(gd, mouse_x, mouse_y):
    if gd.play_btn.active:
        distance = math.sqrt((gd.play_btn.rect.center[0] - mouse_x) ** 2 + (gd.play_btn.rect.center[1] - mouse_y) ** 2)
        # поскольку она круглая, мы смотрим попали ли мы в радиус кнопки
        if distance <= gd.play_btn.radius:
            draw_screen(gd)
            gd.play_btn.active = False


# проверка нажатия кнопки Страт Баттл
def check_start(self, gd, mouse_x, mouse_y):
    # если попали . . .
    if gd.start_btn.rect.collidepoint(mouse_x, mouse_y):
        # и если она была активна. . .
        if gd.start_btn.active:
            # деактивируем,
            gd.start_btn.active = False
            # начинаем битву
            gd.game_set.game_started = True
            # отправляем серверу команду /start True, что значит, что мы готовы начать
            self.sendMessage('/start')
            self._field = gd.myfield
            # рисуем экран
            draw_screen(gd)


# проверка натиска кнопок выбора и перемещения кораблей
def check_addships(gd, mouse_x, mouse_y):
    for ship_btn in gd.addship_btns:
        if ship_btn.rect.collidepoint(mouse_x, mouse_y) and ship_btn.active:
            # создаем соотв. корабль в моем флоте
            size = int(ship_btn.width / 50)
            ship = Ship(size, ship_btn.pos, 'right', True)

            # все остальные корабли становятся недвигабельны (хз зачем, на всякий написал)
            for i in gd.myfleet:
                i.move = False
            '''
            for j in addship_btns:
                if not j.active:
                    j.ships_left += 1
            '''

            # добавляем корабль в список моего флота
            gd.myfleet.append(ship)
            # теперь эту кнопку можно нажать на 1 раз меньше
            ship_btn.ships_left -= 1

            # пока ставим, все кнопки выбора кораблей пропадают
            for item in gd.addship_btns:
                item.active = False


# двигаем корабль к курсору
def move_ship(gd, mouse_x, mouse_y, ship):
    ship.rect.center = (mouse_x, mouse_y)
    draw_screen(gd)
    ship.draw(gd.screen)


# ставим корабль в клетку
def locate_ship(gd, mouse_x, mouse_y, ship):
    # если попали в мое поле. . .
    if gd.myfield.rect.collidepoint(mouse_x, mouse_y):
        for i in range(gd.myfield.side):
            for j in range(gd.myfield.side):
                # смотрим в какую клетку попадает первый квадратик корабля
                if gd.myfield.data[i][j].rect.collidepoint(ship.pos[0]+25, ship.pos[1] + 25):
                    # если корабль повернут вправо и не выходит за правую грань
                    # или если корабль повернут вниз  и не выходит за нижнюю грань
                    if ((ship.direction == 'right' and (gd.myfield.side - j) >= ship.size) or (
                                    ship.direction == 'down' and (gd.myfield.side - i) >= ship.size)):

                        # проверяет, нет ли поблизоти других кораблей
                        if space_is_free((i, j), gd.myfield, ship):
                            # ставим корабль, в моем поле соотв. клетки помечаем как такие, в которых есть корабль
                            for k in range(ship.size):
                                if ship.direction == 'right':
                                    gd.myfield.data[i][j + k].ship_is_here = True
                                else:
                                    gd.myfield.data[i + k][j].ship_is_here = True

                            # записываем поз. первой клетки корабля как поз. корабля
                            ship.pos = (gd.myfield.data[i][j].pos[0] - 2, gd.myfield.data[i][j].pos[1] - 2)

                            ship.rect_by_pos()
                            # все, он не двигабельн
                            ship.move = False

                            #  если мы поставили дост. кораблей данного размера,
                            # соотв. кнопка выбора корабля стает неактивной и не рисуется
                            for item in gd.addship_btns:
                                if item.ships_left != 0:
                                    item.active = True
                                else:
                                    item.active = False

                            gd.myfield.data[i][j].ship_start = [True, ship]
                            draw_screen(gd)
                            break


# ф-ция проверяет, нет ли поблизости еще кораблей
def space_is_free(pos, the_field, ship):
    if ship.direction == 'right':
        for i in range(pos[0] - 1, pos[0] + 2):
            for j in range(pos[1] - 1, pos[1] + 1 + ship.size):
                try:
                    if the_field.data[i][j].ship_is_here and i >= 0 and j >= 0:
                        return False
                except IndexError:
                    pass
    else:
        for i in range(pos[0] - 1, pos[0] + 1 + ship.size):
            for j in range(pos[1] - 1, pos[1] + 2):
                try:
                    if the_field.data[i][j].ship_is_here:
                        return False
                except IndexError:
                    pass
    return True


# "огооонь!!1!"
def fireee(gd, mouse_x, mouse_y):
    pass
    # # если моя очередь
    # if game_set.my_turn:
    #     print('My turn')
    #     game_set.my_turn = False
    #     info.msg = 'Enemy Turn'
    #     for i in enemyfield.data:
    #         # смотрим, куда попали
    #         for cell in i:
    #             if cell.rect.collidepoint(mouse_x, mouse_y) and cell.alive:
    #                 # клетка уже "бита"
    #                 cell.alive = False
    #                 # если здесь был корабль. . .
    #                 if cell.ship_is_here:
    #                     # ходим опять
    #                     game_set.my_turn = True
    #                     info.msg = 'Hit!'
    #                     # смотрим, какой корабль подбили
    #                     for ship in enemyfleet:
    #                         if ship.rect.collidepoint(mouse_x, mouse_y):
    #                             # убавляем ему жизни
    #                             ship.hit += 1
    #                             # если попаданий столько же, какой и размер корабля, он считается потопленным
    #                             if ship.hit == ship.size:
    #                                 ship.destroyed = True
    #                             if ship.destroyed:
    #                                 info.msg = 'Enemy Battleship Destroyed! Your Turn'
    #                 break
    #
    # # если не моя очередь
    # elif not game_set.my_turn:
    #
    #     # если ИИ в пред. раз попал, и не потопил, то ИИ исчет, где еще стоит этот корабль пока не потопит его
    #     if len(ai.correcting_fire) >= 1:
    #
    #         # ИИ корректикрует огонь
    #         if.correct_fire(myfield, myfleet, info):
    #             game_set.my_turn = False
    #         else:
    #             game_set.my_turn = True
    #             info.msg = 'Your Turn'
    #     # если нет раненых кораблей - выбираем клетку рандомно
    #     elif len(ai.correcting_fire) == 0:
    #         info.msg = 'Your Turn'
    #         targets = []
    #         for i in range(10):
    #             for j in range(10):
    #                 if.ai_view.data[i][j].alive:
    #                     targets.append([i, j])
    #         random_cell = random.choice(targets)
    #         i = int(random_cell[0])
    #         j = int(random_cell[1])
    #         target =.ai_view.data[i][j]
    #
    #         target.alive = False
    #         myfield.data[i][j].alive = False
    #
    #         game_set.my_turn = True
    #
    #         # ???????????????????????????????????
    #        m = pygame.image.load('gallery/Aim.png')
    #         screen.blit(Aim, myfield.data[i][j].pos)
    #         print('Aim')
    #         time.sleep(1)
    #
    #         # если ИИ попал в корабль. . .
    #         if myfield.data[i][j].ship_is_here:
    #             for ship in myfleet:
    #                 if ship.rect.collidepoint(myfield.data[i][j].rect.center):
    #                     ship.hit += 1
    #                     target.ship_is_here = True
    #                     game_set.my_turn = False
    #                     info.msg = 'Enemy Hit Our Ship!'
    #                    .correcting_fire.append((i, j))
    #                     # смотрим, убил ли корабль
    #                     if ship.hit == ship.size:
    #                         ship.destroyed = True
    #                        .correcting_fire = []
    #                         info.msg = 'Our Ship is Destroyed! Enemy Turn'
    #                         # dead_rect - прямоугольник на карте вокруг убитого корабля, в который ИИ стрелять не будет
    #                         if ship.direction == 'right':
    #                             dead_rect = pygame.Rect(ship.pos[0] - 50, ship.pos[1] - 50, ship.size + 100, 150)
    #                         else:
    #                             dead_rect = pygame.Rect(ship.pos[0] - 50, ship.pos[1] - 50, 150,  ship.size + 100)
    #                         for line in.ai_view.data:
    #                             for cell in line:
    #                                 if dead_rect.collidepoint(cell.pos[0], cell.pos[1]):
    #                                     cell.alive = False
    #                     break


def new_game():
    pass
