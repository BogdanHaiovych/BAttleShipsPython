import math
import sys
from Ship import Ship
from Buttons import *
import random
import time


# все события
def Events(screen, game_set, play_btn, myfield, enemyfield, addship_btns, myfleet, enemyfleet, start_btn, ai, info):
    #
    if game_set.game_started and not game_set.my_turn:
        pygame.mouse.set_visible(False)
        time.sleep(1)
        fireee(screen, 0, 0, myfield, enemyfield, game_set, myfleet, enemyfleet, ai, addship_btns, start_btn, info)
        time.sleep(1)
        draw_screen(screen, game_set, myfield, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, info)
    else:
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # нажатие на крестик
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP: # что делать, когда отпускаем кнопку мыши
                if event.button == 1:   # левая кнопка мыши
                    # считываем координаты мыши
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # проверяем, нажали ли мы кнопку Плей
                    check_play(screen, game_set, play_btn, mouse_x, mouse_y,
                               myfield, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, info)

                    # проверяет, нажали ди мы кнопку добавления кораблей на поле
                    check_addships(screen, game_set, mouse_x, mouse_y, addship_btns, myfleet, start_btn)

                    # проверяет, нажали ли мы кнопку Старт Баттл
                    check_start(screen, game_set, mouse_x, mouse_y, myfield, enemyfield,
                                addship_btns, start_btn, myfleet, enemyfleet, ai, info)

                    # Проверяет, есть ли еще не поставленный корабль (он висит над полем)
                    for ship in myfleet:
                        if ship.move: # параметр, определяющий, что мы двигаем корабль

                            # разместить корабль в указанной клетке
                            locate_ship(screen, game_set, myfield, enemyfield, addship_btns, mouse_x, mouse_y, ship, myfleet, start_btn, enemyfleet, info)

                    # если битва началась и моя очередь ходить, то . . .
                    if game_set.game_started and game_set.my_turn:
                        # и если я попал по полю противника . . .
                        if enemyfield.rect.collidepoint(mouse_x, mouse_y):
                            # "огооонь!!1!"
                            fireee(screen, mouse_x, mouse_y, myfield, enemyfield, game_set, myfleet, enemyfleet, ai, addship_btns, start_btn, info)
                            draw_screen(screen, game_set, myfield, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, info)

                # если мы нажали правую кнопку мыши
                if event.button == 3:
                    for ship in myfleet:
                        # если есть корабль, который мы двигаем
                        if ship.move:
                            # поменять направление
                            ship.change_dir()
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            # передвинуть корабль к указателю мыши
                            move_ship(screen, game_set, myfield, enemyfield, addship_btns, mouse_x, mouse_y, ship, start_btn, myfleet, enemyfleet, info)

            for ship in myfleet:
                # если есть корабль, который мы двигаем . . .
                if ship.move:
                    # если мышка двигалась . . .
                    if event.type == pygame.MOUSEMOTION:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # передвинуть корабль к указателю мыши
                        move_ship(screen, game_set, myfield, enemyfield, addship_btns, mouse_x, mouse_y, ship, start_btn, myfleet, enemyfleet, info)


# ф-ция перерисовки экрана
def draw_screen(screen, game_set, the_field, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, info):
    if game_set.game_started:
        print('draw screen')
    gamebg = game_set.bg  # Фон (звёзды)
    screen.blit(gamebg, (0, 0))
    info.message()
    # Рисует клетки
    the_field.draw_field(screen)
    enemyfield.draw_field(screen)

    # кол-ство уничтоженных кораблей противника(en_dest) и моих(my_dest)
    my_dest = 0
    en_dest = 0
    # рисует корабли
    for ship in myfleet:
        ship.draw(screen)
        if ship.destroyed:
            my_dest +=1
    # корабли противника рисуем только те, что уже уничтожены
    for ship in enemyfleet:
        if ship.destroyed:
            ship.draw(screen)
            en_dest += 1


    # если расставили еще не все корабли
    for ship_btn in addship_btns:
        if ship_btn.active:
            # рисуем кнопку для расстановки соотв. корабля
            ship_btn.csb_draw()

    # если еще не нарисована кнопка Старт Баттл
    if not start_btn.active:
        # если все кнопки расстановки кораблей не активны (мы всес уже поставили) . . .
        if addship_btns[0].ships_left == 0 and addship_btns[1].ships_left == 0 and addship_btns[2].ships_left == 0 and addship_btns[3].ships_left == 0 \
                and not myfleet[len(myfleet)-1].move and not game_set.game_started:
            # активируем кнопку Старт Баттл и рисуем ее
            start_btn.active = True
            start_btn.startbuttondraw()
        else:
            info.show()
    else:
        # если кнопка уже активна - рисуем
        start_btn.startbuttondraw()

    if len(myfleet) != 0 and len(enemyfleet) != 0:
        if my_dest == len(myfleet) :
            info.msg = '. . .Defeat. . .'
            info.message()
            info.show()
            time.sleep(10)

        elif en_dest == len(enemyfleet):
            info.msg = 'Victory!'
            info.message()
            info.show()
            time.sleep(10)

# проверяем, нажали ли мы кнопку Плей
def check_play(screen, game_set, play, mouse_x, mouse_y, myfield, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, info):
    if play.active:
        distance = math.sqrt((play.rect.center[0] - mouse_x) ** 2 + (play.rect.center[1] - mouse_y) ** 2)
        # поскольку она круглая, мы смотрим попали ли мы в радиус кнопки
        if distance <= play.radius:
            draw_screen(screen, game_set, myfield, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, info)
            play.active = False


# проверка нажатия кнопки Страт Баттл
def check_start(screen, game_set, mouse_x, mouse_y, myfield, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, ai, info):
    # если попали . . .
    if start_btn.rect.collidepoint(mouse_x, mouse_y):
        # и если она была активна. . .
        if start_btn.active:
            # деактивируем,
            start_btn.active = False
            # начинаем битву
            game_set.game_started = True
            # рандомно определяем очередь
            game_set.my_turn = (random.choice([True, False]))

            # ИИ создает свой флот (рандомно)
            AI_create_fleet(enemyfield, enemyfleet, 4, screen)

            if game_set.my_turn:
                info.msg = 'Your Turn'
            else:
                info.msg = 'Enemy Turn'
            # рисуем экран
            draw_screen(screen, game_set, myfield, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, info)

            # если очередь ИИ - даем ему команду "огооонь!!1!"
            if not game_set.my_turn:
                fireee(screen, 0, 0, myfield, enemyfield, game_set, myfleet, enemyfleet, ai, addship_btns, start_btn, info)


# проверка натиска кнопок выбора и перемещения кораблей
def check_addships(screen, game_set, mouse_x, mouse_y, addship_btns, myfleet, start_btn):
    for ship_btn in addship_btns:
        if ship_btn.rect.collidepoint(mouse_x, mouse_y) and ship_btn.active:
            # создаем соотв. корабль в моем флоте
            size = int(ship_btn.width / 50)
            ship = Ship(size, ship_btn.pos, 'right', True)

            # все остальные корабли становятся недвигабельны (хз зачем, на всякий написал)
            for i in myfleet:
                i.move = False
            '''
            for j in addship_btns:
                if not j.active:
                    j.ships_left += 1
            '''

            # добавляем корабль в список моего флота
            myfleet.append(ship)
            # теперь эту кнопку можно нажать на 1 раз меньше
            ship_btn.ships_left -= 1

            # пока ставим, все кнопки выбора кораблей пропадают
            for item in addship_btns:
                item.active = False


# двигаем корабль к курсору
def move_ship(screen, game_set, myfield, enemyfield, addship_btns, mouse_x, mouse_y, ship, start_btn, myfleet, enemyfleet, info):
    ship.rect.center = (mouse_x, mouse_y)
    draw_screen(screen, game_set, myfield, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, info)
    ship.draw(screen)


# ставим корабль в клетку
def locate_ship(screen, game_set, myfield, enemyfield, addship_btns, mouse_x, mouse_y, ship, myfleet, start_btn, enemyfleet, info):
    # если попали в мое поле. . .
    if myfield.rect.collidepoint(mouse_x, mouse_y):
        for i in range(myfield.side):
            for j in range(myfield.side):
                # смотрим в какую клетку попадает первый квадратик корабля
                if myfield.data[i][j].rect.collidepoint(ship.pos[0]+25, ship.pos[1] + 25):
                    # если корабль повернут вправо и не выходит за правую грань
                    # или если корабль повернут вниз  и не выходит за нижнюю грань
                    if ((ship.direction == 'right' and (myfield.side - j) >= ship.size) or (
                                    ship.direction == 'down' and (myfield.side - i) >= ship.size)):

                        # проверяет, нет ли поблизоти других кораблей
                        if space_is_free((i, j), myfield, ship):
                            # ставим корабль, в моем поле соотв. клетки помечаем как такие, в которых есть корабль
                            for k in range(ship.size):
                                if ship.direction == 'right':
                                    myfield.data[i][j + k].ship_is_here = True
                                else:
                                    myfield.data[i + k][j].ship_is_here = True

                            # записываем поз. первой клетки корабля как поз. корабля
                            ship.pos = (myfield.data[i][j].pos[0] - 2, myfield.data[i][j].pos[1] - 2)

                            ship.rect_by_pos()
                            # все, он не двигабельн
                            ship.move = False

                            #  если мы поставили дост. кораблей данного размера,
                            # соотв. кнопка выбора корабля стает неактивной и не рисуется
                            for item in addship_btns:
                                if item.ships_left != 0:
                                    item.active = True
                                else:
                                    item.active = False

                            myfield.data[i][j].ship_start = [True, ship]
                            draw_screen(screen, game_set, myfield, enemyfield, addship_btns, start_btn, myfleet, enemyfleet, info)
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


# ИИ создает свой флот
def AI_create_fleet(enemyfield, enemyfleet, size, screen):
    if size != 0:
        # создает для размера корабля:
        # 4 - 1 клетку
        # 3 - 2 клетки и тд
        for q in range(5 - size):
            # работает, пока не поставит корабль
            while True:
                # рандомное направение корабля
                rand_dir = random.randint(0, 1)
                if rand_dir == 0:
                    ship = Ship(size, (0, 0), 'right', False)
                else:
                    ship = Ship(size, (0, 0), 'down', False)

                # рандомная позиция
                i = random.randint(0, 9)
                j = random.randint(0, 9)

                # если здесь нет корабля и место свободно (функ. space_is_free)
                if not enemyfield.data[i][j].ship_is_here:
                    if ((ship.direction == 'right' and (enemyfield.side - j) >= ship.size) or (
                                    ship.direction == 'down' and (enemyfield.side - i) >= ship.size)):
                        if space_is_free((i, j), enemyfield, ship):
                            for k in range(ship.size):
                                if ship.direction == 'right':
                                    enemyfield.data[i][j + k].ship_is_here = True
                                else:
                                    enemyfield.data[i + k][j].ship_is_here = True

                            # ставим здесь корабль
                            ship.pos = (enemyfield.data[i][j].pos[0] - 2, enemyfield.data[i][j].pos[1] - 2)
                            ship.rect_by_pos()
                            enemyfleet.append(ship)
                            enemyfield.data[i][j].ship_start = [True, ship]
                            break
        # поставили все корабли этого размера - ставим след корабли, которые поменьше
        AI_create_fleet(enemyfield, enemyfleet, size - 1, screen)


# "огооонь!!1!"
def fireee(screen, mouse_x, mouse_y, myfield, enemyfield, game_set, myfleet, enemyfleet, ai, addship_btns, start_btn, info):
    # если моя очередь
    if game_set.my_turn:
        print('My turn')
        game_set.my_turn = False
        info.msg = 'Enemy Turn'
        for i in enemyfield.data:
            # смотрим, куда попали
            for cell in i:
                if cell.rect.collidepoint(mouse_x, mouse_y) and cell.alive:
                    # клетка уже "бита"
                    cell.alive = False
                    # если здесь был корабль. . .
                    if cell.ship_is_here:
                        # ходим опять
                        game_set.my_turn = True
                        info.msg = 'Hit!'
                        # смотрим, какой корабль подбили
                        for ship in enemyfleet:
                            if ship.rect.collidepoint(mouse_x, mouse_y):
                                # убавляем ему жизни
                                ship.hit += 1
                                # если попаданий столько же, какой и размер корабля, он считается потопленным
                                if ship.hit == ship.size:
                                    ship.destroyed = True
                                if ship.destroyed:
                                    info.msg = 'Enemy Battleship Destroyed! Your Turn'
                    break

    # если не моя очередь
    elif not game_set.my_turn:

        # если ИИ в пред. раз попал, и не потопил, то ИИ исчет, где еще стоит этот корабль пока не потопит его
        if len(ai.correcting_fire) >= 1:

            # ИИ корректикрует огонь
            if ai.correct_fire(myfield, myfleet, info):
                game_set.my_turn = False
            else:
                game_set.my_turn = True
                info.msg = 'Your Turn'
        # если нет раненых кораблей - выбираем клетку рандомно
        elif len(ai.correcting_fire) == 0:
            info.msg = 'Your Turn'
            targets = []
            for i in range(10):
                for j in range(10):
                    if ai.ai_view.data[i][j].alive:
                        targets.append([i, j])
            random_cell = random.choice(targets)
            i = int(random_cell[0])
            j = int(random_cell[1])
            target = ai.ai_view.data[i][j]

            target.alive = False
            myfield.data[i][j].alive = False

            game_set.my_turn = True

            # ???????????????????????????????????
            Aim = pygame.image.load('gallery/Aim.png')
            screen.blit(Aim, myfield.data[i][j].pos)
            print('Aim')
            time.sleep(1)

            # если ИИ попал в корабль. . .
            if myfield.data[i][j].ship_is_here:
                for ship in myfleet:
                    if ship.rect.collidepoint(myfield.data[i][j].rect.center):
                        ship.hit += 1
                        target.ship_is_here = True
                        game_set.my_turn = False
                        info.msg = 'Enemy Hit Our Ship!'
                        ai.correcting_fire.append((i, j))
                        # смотрим, убил ли корабль
                        if ship.hit == ship.size:
                            ship.destroyed = True
                            ai.correcting_fire = []
                            info.msg = 'Our Ship is Destroyed! Enemy Turn'
                            # dead_rect - прямоугольник на карте вокруг убитого корабля, в который ИИ стрелять не будет
                            if ship.direction == 'right':
                                dead_rect = pygame.Rect(ship.pos[0] - 50, ship.pos[1] - 50, ship.size + 100, 150)
                            else:
                                dead_rect = pygame.Rect(ship.pos[0] - 50, ship.pos[1] - 50, 150,  ship.size + 100)
                            for line in ai.ai_view.data:
                                for cell in line:
                                    if dead_rect.collidepoint(cell.pos[0], cell.pos[1]):
                                        cell.alive = False
                        break


def new_game():
    pass