import pygame


# класс ИИ - мозг противника
class AI():
    def __init__(self, screen, ai_view):
        self.scrren = screen
        # вид ИИ на мое поле
        self.ai_view = ai_view
        # массив координат клеток, в которых находится недобитый корабль
        self.correcting_fire = []

    # проверяет, есть ли в клетке моего поля корабль
    def check_cell(self, myfield, i, j, myfleet, info):
        print('check', i, j)
        self.ai_view.data[i][j].alive = False
        myfield.data[i][j].alive = False
        if myfield.data[i][j].ship_is_here:
            self.ai_view.data[i][j].ship_is_here = True
            for ship in myfleet:
                if ship.rect.collidepoint(myfield.data[i][j].rect.center):
                    ship.hit += 1
                    print('ship.hit', ship.hit)
                    self.correcting_fire.append((i, j))
                    if ship.hit == ship.size:
                        ship.destroyed = True
                        info.msg = 'Our ship destroyed!\nEnemyTurn'
                        info.message()
                        self.correcting_fire = []
                        print('cor_fire = ', self.correcting_fire)
                        if ship.direction == 'right':
                            dead_rect = pygame.Rect(ship.pos[0] - 50, ship.pos[1] - 50, ship.size + 100, 150)
                        else:
                            dead_rect = pygame.Rect(ship.pos[0] - 50, ship.pos[1] - 50, 150, ship.size + 100)
                        for line in self.ai_view.data:
                            for cell in line:
                                if dead_rect.collidepoint(cell.pos[0], cell.pos[1]):
                                    cell.alive = False
            return True
        else:
            return False

    # функция корректировки огня
            # если попали - в клетки по обе стороны от выбраной нет смысла стрелять,
            # только в направлении проверки
    def correct_fire(self, myfield, myfleet, info):
        for pos in self.correcting_fire:
            i, j = pos[0], pos[1]
            # проверяем на клетку ниже
            if (i+1 <= 9) and self.ai_view.data[i + 1][j].alive:
                if self.check_cell(myfield, i + 1, j, myfleet, info):
                    if j - 1 >= 0:
                        self.ai_view.data[i+1][j - 1].alive = False
                        self.ai_view.data[i][j - 1].alive = False
                    if j + 1 <=9:
                        self.ai_view.data[i+1][j + 1].alive = False
                        self.ai_view.data[i][j + 1].alive = False
                    return True
                else:
                    return False
            # проверяем на клетку вправо
            elif (j + 1 <= 9) and self.ai_view.data[i][j + 1].alive:
                if self.check_cell(myfield, i, j + 1, myfleet, info):
                    if i - 1 >= 0:
                        self.ai_view.data[i - 1][j + 1].alive = False
                        self.ai_view.data[i - 1][j].alive = False
                    if i + 1 <=9:
                        self.ai_view.data[i + 1][j + 1].alive = False
                        self.ai_view.data[i + 1][j].alive = False
                    return True
                else:
                    return False
            # проверяем на клетку выше
            elif (i - 1 >= 0) and self.ai_view.data[i - 1][j].alive:
                if self.check_cell(myfield, i - 1, j, myfleet, info):
                    if j - 1 >= 0:
                        self.ai_view.data[i - i][j - 1].alive = False
                        self.ai_view.data[i][j - 1].alive = False
                    if j + 1 <=9:
                        self.ai_view.data[i - 1][j + 1].alive = False
                        self.ai_view.data[i][j + 1].alive = False
                    return True
                else:
                    return False
            # проверяем на клетку влево
            elif (j - 1 >= 0) and self.ai_view.data[i][j - 1].alive:
                if self.check_cell(myfield, i, j - 1, myfleet, info):
                    if i - 1 >= 0:
                        self.ai_view.data[i - 1][j - 1].alive = False
                        self.ai_view.data[i - 1][j].alive = False
                    if i + 1 <=9:
                        self.ai_view.data[i + 1][j - 1].alive = False
                        self.ai_view.data[i + 1][j].alive = False
                    return True
                else:
                    return False

    def aim(self):
        targ = pygame.image.load('gallery/Aim.png')
        self.scrren.blit()
