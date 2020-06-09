import pygame


# настройки игры
class Settings:
    def __init__(self):
        # фон и экран
        self.screen_w = 1200
        self.screen_h = 700
        self.bg = pygame.image.load('gallery/bg.jpg')
        # процесс битвы
        self.game_started = False   # если битва началась - True
        self.my_turn = False
