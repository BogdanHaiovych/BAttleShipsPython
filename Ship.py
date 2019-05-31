import pygame

# класс корабль
class Ship:
    def __init__(self, size, pos, direction, move):
        self.size = size
        self.pos = pos
        self.rect = None
        # направление корабля - right / down
        self.direction = direction
        self.rect_by_pos()
        # кол-ство попаданий по кораблю
        self.hit = 0
        self.destroyed = False

        # загрузка модели корабля
        if self.direction == 'right':
            self.model = pygame.image.load('gallery/mass_%sr.png'%str(self.size))
        else:
            self.model = pygame.image.load('gallery/mass_%s.png'%str(self.size))

        self.model_rect = self.model.get_rect()
        self.move = move

    # рисовать корабль
    def draw(self, screen):
        part = pygame.Surface((48,48))
        part.fill((138, 243, 226))
        self.pos = self.rect[0] + 2, self.rect[1] + 2
        screen.blit(self.model, self.pos)

    # повернуть корабль (нажатие ПКМ)
    def change_dir(self):
        if self.direction == 'right':
            self.direction = 'down'
            self.rect = pygame.Rect(self.rect[0], self.rect[1], 50, self.size * 50)
            self.model = pygame.image.load('gallery/mass_%s.png'%str(self.size))
        else:
            self.direction = 'right'
            self.rect = pygame.Rect(self.rect[0], self.rect[1], self.size * 50, 50)
            self.model = pygame.image.load('gallery/mass_%sr.png' % str(self.size))

    # посчитать self.rect , по данным self.pos
    def rect_by_pos(self):
        if self.direction == "right":
            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size * 50, 50)
        elif self.direction == 'down':
            self.rect = pygame.Rect(self.pos[0], self.pos[1], 50, self.size * 50)