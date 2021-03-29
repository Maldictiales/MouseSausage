# импорт нужных библиотек
import os
import sys

import pygame
import random
from pygame import mixer

# переменные для конфигурации игры
WIDTH = 1200
HEIGHT = 700
FPS = 60

# переменные цветовых кодов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# метод для безопасной загрузки в системе
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

# инициализация элементов движка
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MouseSausage")
clock = pygame.time.Clock()
PAUSED = False
GAME_OVER = False
GAME_STARTED = False
start_ticks = 0

class Background:
    def __init__(self):
        self.image = storage.background_images[0]
        self.rect = self.image.get_rect()
        self.last_sprite_update = pygame.time.get_ticks()
        self.i = 0

    def update(self):
        animation(self, storage.background_images, 600, True)
        screen.blit(self.image,self.rect)
# класс для загрузки всех спрайтов
class Storage:
    def __init__(self):
        self.mouse_image = load_images("mouse", 23, 0)
        self.background_images = load_images("background", 9, 0)
        self.floor_image = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("venv\\Sprites\\floor.png"))).convert_alpha(), (WIDTH,400))
        self.floor_rect = self.floor_image.get_rect()
        self.floor_rect.y += 300
        self.foreground_image = pygame.image.load(resource_path(os.path.join("venv\\Sprites\\foreground.png"))).convert_alpha()

# метод для проигрывания анимации
def animation(Entity, images, speed, endless):
    now = pygame.time.get_ticks()
    is_alive = True
    if now - Entity.last_sprite_update > speed:
        Entity.i += 1
        if Entity.i > len(images) - 1:
            if endless:
                Entity.i = 0
            else:
                Entity.i = 0
                try:
                    Entity.kill()
                except Exception:
                    pass
                is_alive = False
                return is_alive
        if is_alive:
            Entity.last_sprite_update = now
            new_image = images[Entity.i]
            Entity.image = new_image


def is_collided_with(self, sprite):
    return self.rect.colliderect(sprite.rect)

def is_pressed_by_mouse(Entity):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return Entity.rect.left < mouse_x < Entity.rect.left + Entity.rect.width and Entity.rect.top < mouse_y < Entity.rect.top + Entity.rect.height

# метод для загрузки нескольких спрайтов в массив
def load_images(name, count, scale):
    array = []
    if scale == 0:
        for i in range(count):
            try:
                array.append(pygame.image.load(resource_path(os.path.join("venv\\Sprites\\", str(name) + str(i + 1) + ".png"))).convert_alpha())
            except Warning:
                print(Warning)
    else:
        for i in range(count):
            try:
                array.append(pygame.transform.scale(
                    pygame.image.load(resource_path(os.path.join("venv\\Sprites\\", str(name) + str(i + 1) + ".png"))).convert_alpha(), (scale, scale)))
            except Warning:
                print(Warning)

    return array

# метод для отображения текста на экране
def print_text(text, size, color, x, y):
    font = pygame.font.Font(resource_path(os.path.join("venv\\Fonts\\","MinecraftFont.ttf")), size)
    screen.blit(font.render(text, True, color), (x, y))


storage = Storage()
background = Background()
# переменная от которой зависит цикл игры
running = True

while running:
    # установка определенное колличество кадров в секунду (в нашем случае 60)
    clock.tick(FPS)
    # цикл для прослушивания всех событий в игре
    for event in pygame.event.get():
        # если игрок закрывает окно, то прекратить цикл
        if event.type == pygame.QUIT:
            running = False

    background.update()
    screen.blit(storage.floor_image, storage.floor_rect)
    screen.blit(storage.foreground_image,storage.foreground_image.get_rect())
    pygame.display.flip()
sys.exit()