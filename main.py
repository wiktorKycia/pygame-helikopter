import pygame
import os
import random

pygame.init()

width = 1000
height = 800

screen = pygame.display.set_mode((width, height))


def write(text, x, y, font_size, is_centered=False ,font_style="Comic Sans"):
    font = pygame.font.SysFont(font_style, font_size)
    rend = font.render(text, True, (255, 100, 100))
    if is_centered is True:
        x = (width - rend.get_rect().width)/2
        y = (height - rend.get_rect().height)/2
    screen.blit(rend, (x, y))


class Przeszkoda():
    def __init__(self, x, szerokosc):
        self.x = x
        self.szerokosc = szerokosc
        self.y_gora = 0
        self.wys_gora = random.randint(225, 350)
        self.odstep = 200
        self.y_dol = self.wys_gora + self.odstep
        self.wys_dol = height - self.y_dol
        self.kolor = (160, 140, 190)
        self.ksztalt_gora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
        self.ksztalt_dol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)

    def rysuj(self):
        pygame.draw.rect(screen, self.kolor, self.ksztalt_gora)
        pygame.draw.rect(screen, self.kolor, self.ksztalt_dol)

    def ruch(self, v):
        self.x = self.x - v
        self.ksztalt_gora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
        self.ksztalt_dol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)

    def kolizja(self, player):
        if self.ksztalt_gora.colliderect(player) or self.ksztalt_dol.colliderect(player):
            return True
        else: return False

class Helikopter():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.szerokosc = 50
        self.wysokosc = 50
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
        self.grafika = pygame.image.load(os.path.join('zielony_helikopter.png'))

    def rysuj(self):
        screen.blit(self.grafika, (self.x, self.y))
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)

    def ruch(self):
        speed = 2
        if pygame.key.get_pressed()[pygame.K_w]:
            self.y -= speed
        if pygame.key.get_pressed()[pygame.K_s]:
            self.y += speed


keys = pygame.key.get_pressed()
gracz = Helikopter(250, 350)
grafika = pygame.image.load(os.path.join('zielony_helikopter.png'))
copokazuje = "menu"
przeszkody = []

clock = 0

for i in range(26):
    przeszkody.append(Przeszkoda(i*width/25, width/25))

while True:
    clock += pygame.time.Clock().tick(1000)/1000
    pygame.time.Clock().tick(1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not copokazuje == "rozgrywka":
                    copokazuje = "rozgrywka"
                    gracz = Helikopter(250, 350)
    screen.fill((0, 0, 0))
    match copokazuje:
        case "menu":
            write("Hello in my game", 10, 10, 50, True)
            screen.blit(grafika, (100, 100))
        case "rozgrywka":
            for p in przeszkody:
                p.rysuj()
                p.ruch(1)
                if p.kolizja(gracz.ksztalt):
                    copokazuje = "koniec"
                if p.x <= -p.szerokosc:
                    przeszkody.remove(p)
                    przeszkody.append((Przeszkoda(width, width/25)))
            gracz.rysuj()
            gracz.ruch()
        case "koniec":
            write("Niestety przegrywasz", 50, 450, 25)
            write("Naciśnij spację, by zagrać jescze raz", 50, 500, 25)
        case _:
            pygame.quit()
            quit()

    pygame.display.update()
