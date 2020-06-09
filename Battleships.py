import pygame
from Settings import Settings
import GameFunc as gf
from Cell import Cell, Field
from Buttons import *
from Ship import Ship
from copy import deepcopy


def play():
    pygame.init()
    pygame.display.set_caption('Battleships')
    game_set = Settings()  # Настройки игры
    screen = pygame.display.set_mode((game_set.screen_w, game_set.screen_h))  # Рабочее окно

    # Создает мое поле и поле противника
    myfield = Field(50, 50)
    enemyfield = Field(650, 50)

    # Добавляет в мое поле и в поле противника клетки
    myfleet = []
    enemyfleet = []
    for j in range(10):
        my = []
        enemy = []
        for k in range(10):
            block = Cell(screen, k * 50 + myfield.pos[0], j * 50 + myfield.pos[1])
            my.append(block)
            block = Cell(screen, k * 50 + enemyfield.pos[0], j * 50 + enemyfield.pos[1])
            enemy.append(block)
        myfield.data.append(my)
        enemyfield.data.append(enemy)

    # Создает 4 кнопки выбора кораблей (Если игра не началась - их не показывает)

    addship_btns = []  # Массив этих кнопок
    ship = Aircraft(screen, (75, 625))
    addship_btns.append(ship)
    ship = Battleship(screen, (425, 625))
    addship_btns.append(ship)
    ship = Cruiser(screen, (725, 625))
    addship_btns.append(ship)
    ship = Destroyer(screen, (975, 625))
    addship_btns.append(ship)

    # Создает фон
    gamebg = game_set.bg  # Фон (звёзды)
    screen.blit(gamebg, (0, 0))

    # Создает кнопки Плей и Старт Баттл
    play_btn = Play(screen, 'Play')
    play_btn.play_draw()
    start_btn = StartGame(screen, 'Start battle')
    info = Information(screen, 'Choose a ship and place it')
    while True:
        # доступ к событиям (нажатие кнопки, перемещение мыши)
        gf.Events(
                    screen, game_set, play_btn, myfield, enemyfield,
                    addship_btns, myfleet, enemyfleet, start_btn, info)
        # стандартная функция при работе игры
        pygame.display.flip()


play()
