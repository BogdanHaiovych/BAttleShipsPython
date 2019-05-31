import pygame


# класс поле.
class Field:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.side = 10              # кол-ство клеток по диагонале и горизонтале
        self.data = []              # здесь хранятся клетки
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.side * 50, self.side * 50)

    def draw_field(self,screen):
        for i in self.data:
            for j in i:
                j.draw()
        '''
        for i in self.data:
            for j in i:
                if j.ship_is_here and j.ship_start[0]:
                    j.ship_start[1].draw(screen)
        '''

# класс клетка поля
class Cell:
    def __init__(self,screen,x,y):
        self.screen = screen

        self.pos = (x+2, y+2)
        self.side = 48
        self.btn_color = (0, 51, 102)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.side, self.side)
        self.rect.bottomleft = (self.pos[0], self.pos[1] + 50)

        #Показывает, обстреляна ли клетка
        #Если сюда уже стреляли - False
        self.alive = True

        #Показывает, есть ли здесь корабль
        self.ship_is_here = False
        self.ship_start = [False, None]

    def draw(self):
        #Рисует клетку
        if not self.alive and self.ship_is_here:
            pygame.draw.rect(self.screen, (196, 30, 58), self.rect, 1)
        elif not self.alive:
            pygame.draw.rect(self.screen, (0, 255, 255), self.rect, 1)
        elif self.alive:
            pygame.draw.rect(self.screen, self.btn_color, self.rect, 1)

