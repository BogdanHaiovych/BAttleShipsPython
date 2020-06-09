import pygame.font
import pygame


class Button():     # абстрактный класс для всех кнопок
    def __init__(self, screen, pos, color, width, height):
        # атрибуты кнопки
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # размер и свойства
        self.color = color
        self.pos = pos
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)


class Play(Button):     # Кнопка "Играть"
    def __init__(self, screen, msg):
        Button.__init__(self, screen, (0, 0), (0, 51, 102), 240, 240)
        # размер и свойства
        self.radius = 120
        self.text_color = (224, 255, 255)
        self.font = pygame.font.SysFont(None, 55, True)
        self.active = True

        # выравнивание по центру
        self.rect.center = self.screen_rect.center

        # одиночное создание конпки

        self.message(msg)

    def message(self, msg):
        # формирование и выравнивание текста
        self.msg = self.font.render(msg, True, self.text_color, self.color)
        self.msg_rect = self.msg.get_rect()
        self.msg_rect.center = self.screen_rect.center

    # отрисовка кнопки

    def play_draw(self):
        gamebg = pygame.image.load('gallery/bg.jpg')  # Фон (звёзды)
        self.screen.blit(gamebg, (0, 0))
        pygame.draw.circle(self.screen, self.color, self.screen_rect.center, self.radius)
        pygame.draw.circle(self.screen, self.text_color, self.screen_rect.center, self.radius - 10, 4)
        self.screen.blit(self.msg, self.msg_rect)


class StartGame(Button):      # кнопка Старт Баттл
    def __init__(self, screen, msg):
        Button.__init__(self, screen, (0, 0), (164, 198, 57), 300, 70)
        # если нажимабельна - тру, нет - фолс
        self.active = False
        self.rect.center = (self.screen_rect.center[0], self.screen_rect.center[1] + 275)

        self.text_color = (224, 255, 255)
        self.font = pygame.font.SysFont(None, 55, True)

        self.message(msg)

    # пишет сообщение на кнопке
    def message(self, msg):
        # формирование и выравнивание текста
        self.msg = self.font.render(msg, True, self.text_color, self.color)
        self.msg_rect = self.msg.get_rect()
        self.msg_rect.center = (self.screen_rect.center[0], self.screen_rect.center[1] + 275)

    # рисует кнопку
    def startbuttondraw(self):
        pygame.draw.rect(self.screen, (224, 255, 255), [self.rect[0] + 6, self.rect[1] + 6, self.width, self.height], 4)
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msg, self.msg_rect)


class ChooseShipButton(Button):         # Кнопки выбора кораблей
    def __init__(self, screen, pos, width, sleft):
        Button.__init__(self, screen, pos, (224, 255, 255), width, 50)

        self.active = True
        self.ships_left = sleft

        self.image = pygame.image.load('gallery/mass_%sr.png'%str(round(self.width / 50)))

    def csb_draw(self):
        for i in range(int(self.width/50)):
            self.screen.blit(self.image, self.pos)


class Destroyer(ChooseShipButton):      # Выбрать корабль на 1 клетку
    def __init__(self, screen, pos):
        ChooseShipButton.__init__(self, screen, pos, 50, 4)


class Cruiser(ChooseShipButton):        # Выбрать корабль на 2 клетки
    def __init__(self, screen, pos):
        ChooseShipButton.__init__(self, screen, pos, 100, 3)


class Battleship(ChooseShipButton):     # выбрать корабль на 3 клетки
    def __init__(self, screen, pos):
        ChooseShipButton.__init__(self, screen, pos, 150, 2)


class Aircraft(ChooseShipButton):       # Выбрать корабль на 4 клетки
    def __init__(self, screen, pos):
        ChooseShipButton.__init__(self, screen, pos, 200, 1)


class Information:
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.msg = msg
        self.text_color = (224, 255, 255)
        self.font = pygame.font.SysFont(None, 45, True)

        self.message()

    def message(self):
        self.py_msg = self.font.render(self.msg, True, self.text_color)
        self.py_msg_rect = self.py_msg.get_rect()
        self.py_msg_rect.center = (self.screen_rect.center[0], self.screen_rect.center[1] + 250)

    def show(self):
        self.screen.blit(self.py_msg, self.py_msg_rect)
