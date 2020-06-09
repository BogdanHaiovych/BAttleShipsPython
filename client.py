import socket
import sys
import pygame
from Settings import Settings
import GameFunc as gf
from Cell import Cell, Field
from Buttons import *
from Ship import Ship
from Data import Data


class ServerError(Exception):
    "Виключення у разі отримання неправильних даних від сервера."
    pass


class PlayerClient:
    """Клас клієнта гри у відгадування слів."""

    def __init__(self, host, port, name):
        """Встановити з'єднання з сервером."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        # створити файлоподібні об'єкти для обміну даними
        self.input = self.socket.makefile('rb', 0)
        self.output = self.socket.makefile('wb', 0)
        self.my_turn = False
        # game data
        self._gd = None
        self.sendMessage(name)          # надіслати ім'я на сервер.
        # self.run()                      # вести гру
        self.play()

    def play(self):
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
        gameData = Data(screen, game_set, play_btn, myfield, enemyfield,
                        addship_btns, myfleet, enemyfleet, start_btn, info)
        self._gd = gameData
        while True:
            # доступ к событиям (нажатие кнопки, перемещение мыши)
            """Веде гру, приймає та відправляє дані."""
            done = False
            # Вести гру
            while not done:
                try:
                    done = self.processInput()  # обробити отримані дані
                except ServerError as error:
                    print(error)
                    done = self.quitCommand()
                except socket.error as e:
                    print(e)
                    done = self.quitCommand()

                gf.Events(self, gameData)
                self._gd = gameData

                # стандартная функция при работе игры
                pygame.display.flip()

    # def run(self):
    #     """Веде гру, приймає та відправляє дані."""
    #     done = False
    #     # Вести гру
    #     while not done:
    #         try:
    #             done = self.processInput()  # обробити отримані дані
    #         except ServerError as error:
    #             print(error)
    #             done = self.quitCommand()
    #         except socket.error as e:
    #             print(e)
    #             done = self.quitCommand()

    def sendMessage(self, message):
        """Відправити повідомлення серверу."""
        print('send "%s"' % message)
        self.output.write(bytes(message + '\r\n', encoding='utf-8'))

    def processInput(self):
        """Читає рядок тексту від сервера та обробляє отриману команду.

           Якщо рядок не є командою, - показує його.
        """
        done = False
        line = self._readline()
        # отримати команду та аргументи
        command, arg = self._parseCommand(line)
        if command:
            # викликати метод для виконання команди
            # та передати параметри, якщо є
            if arg:
                done = command(arg)
            else:
                done = command()
        else:   # якщо не команда, - просто показати рядок
            print(line)
        return done

    # def turnCommand(self):
    #     """Команда /turn (зробити хід)."""
    #     self.myturn = True
    #
    # def hitCommand(self, arg):
    #     pass
    #
    # def fireCommand(self, pos):

    def quitCommand(self):
        """Команда /quit (завершити роботу)."""
        self.socket.shutdown(2)     # закрити "файли"
        self.socket.close()         # закрити з'єднання
        return True

    def _parseCommand(self, inp):
        """Намагається розібрати рядок як команду клієнту.

           Якщо цю команду реалізовано, викликає відповідний метод.
           Якщо рядок не є командою, - показує його.
        """
        commandMethod, arg = None, None
        # якщо рядок непорожній та починається з '/'
        if inp and inp[0] == '/':
            if len(inp) < 2:
                raise ServerError('Недопустима команда: "{}"'.format(inp))
            # список з 2 (або 1) значень: команда та її аргументи (якщо є)
            commandAndArg = inp[1:].split(' ', 1)
            if len(commandAndArg) == 2:  # є аргументи
                command, arg = commandAndArg
            else:
                command, = commandAndArg  # немає аргументів
            # Чи реалізовано у класі метод, який починається
            # ім'ям команди та завершується 'Command'
            commandMethod = getattr(gf, command + 'Command', None)
            if not commandMethod:
                raise ServerError('Немає такої команди: "{}"'.format(command))
        return commandMethod, arg

    def _readline(self):
        """Читає з мережі рядок, видаляє пропуски з початку та кінця."""
        line = str(self.input.readline().strip(), encoding='utf-8')
#        print(line)
        return line


if __name__ == '__main__':

    HOST = '192.168.1.8'    # Комп'ютер для з'єднання з сервером
    PORT = 30003          # Порт для з'єднання з сервером

    if len(sys.argv) < 4:              # якщо не вистачає параметрів, ввести
        host = HOST
        port = PORT
        name = input("Введіть ім'я:")
    else:
        host = sys.argv[1]     # 1 параметр
        port = sys.argv[2]     # 2 параметр
        name = sys.argv[3]     # 3 параметр

    player = PlayerClient(host, port, name)
