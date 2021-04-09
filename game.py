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

class Mouse:
    def __init__(self):
        self.move_speed = 6
        self.image = storage.mouse_images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 - 180
        self.rect.bottom = HEIGHT - 120
        self.speedx = 0
        self.last_sprite_update = pygame.time.get_ticks()
        self.i = 0
        self.lives = 3
        self.is_right = True

    def update(self):
        if self.lives > 0:
            animation(self, storage.mouse_images, 35, True)
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -1 * self.move_speed
                self.is_right = False
            elif keystate[pygame.K_RIGHT]:
                self.speedx = self.move_speed
                self.is_right = True
            self.rect.x += self.speedx
            if self.rect.left > 1100:
                self.rect.left = 1100
            if self.rect.left < 0:
                self.rect.left = 0
        else:
            menu.in_menu = True
            self.lives = 3
            scores_.scores = 0
            cheeses.empty()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.is_right, False), self.rect)

    def take_damage(self):
        self.lives -= 1

class Cheese(pygame.sprite.Sprite):
    def __init__(self, x, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = storage.cheese_images[random.randint(0,2)]
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 700
        self.rect.centerx = x
        self.speedy = speed
        self.last_sprite_update = pygame.time.get_ticks()
        self.orig_image = self.image
        self.i = 0
        self.angle = 0
        self.is_alive = True

    def update(self):
        self.angle += 2
        self.rotate()
        self.rect.y += self.speedy
        if self.is_alive:
            if is_collided_with(self, mouse):
                self.speedy = 0
                sound_mixer.sounds["cheese_sound"].play(0)
                scores_.scores += 1
                self.is_alive = False
            if self.rect.bottom > HEIGHT:
                mouse.take_damage()
                self.speedy = 0
                self.is_alive = False
        else:
            cheeses.remove(self)

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

class Scores:
    def __init__(self):
        self.scores = 0

    def update(self):
        print_text("SCORES: " + str(self.scores), 30, WHITE, 50, 50)

class Button:
    def __init__(self, name, func):
        self.image_normal = self.load_button_image(name, 250, 125)
        self.image_in_focus = pygame.transform.scale(self.image_normal, (255, 130))
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.func = func

    def draw(self):
        if mouse_in_rect(self):
            self.image = self.image_in_focus
        else:
            self.image = self.image_normal
        screen.blit(self.image,self.rect)

    def is_clicked(self):
        if mouse_in_rect(self):
            sound_mixer.sounds["cheese_sound"].play(0)
            self.func()

    def load_button_image(self, name, scaleX, scaleY):
        return pygame.transform.scale(
            pygame.image.load(
                resource_path(os.path.join("venv\\Sprites\\" + name + ".png"))).convert_alpha(), (scaleX, scaleY))

class Menu:
    def __init__(self):
        self.local_x = 455
        self.local_y = 800
        self.buttons = [Button("button_start", self.start),
                        Button("button_quit", self.quit)]
        self.move_up = False
        self.in_menu = True
        self.move_down = False

    def update(self):
        if self.move_down:
            self.moving_down()
        if self.move_up:
            self.moving_up()

        if self.in_menu:
            self.move_up = True
            self.move_down = False
            screen.blit(storage.fade_image, storage.fade_image.get_rect())
            for i in range(len(self.buttons)):
                self.buttons[i].rect.x = self.local_x
                self.buttons[i].rect.y = self.local_y + i * 100
                self.buttons[i].draw()

        if not self.in_menu:
            self.move_down = True
            self.move_up = False
            for i in range(len(self.buttons)):
                self.buttons[i].rect.x = self.local_x
                self.buttons[i].rect.y = self.local_y + i * 100
                self.buttons[i].draw()

    def buttons_is_pressed(self):
        for button in self.buttons:
            button.is_clicked()

    def moving_up(self):
        if self.local_y < 200:
            self.move_up = False
        if self.move_up:
            self.local_y -= 15

    def moving_down(self):
        if self.local_y > 800:
            self.move_down = False
        if self.move_down:
            self.local_y += 15


    def start(self):
        self.in_menu = False

    def quit(self):
        sys.exit()

class Background:
    def __init__(self):
        self.image = storage.background_images[0]
        self.rect = self.image.get_rect()
        self.last_sprite_update = pygame.time.get_ticks()
        self.i = 0

    def update(self):
        animation(self, storage.background_images, 600, True)

    def draw(self):
        screen.blit(self.image, self.rect)

class Sound_mixer():
    def __init__(self):
        self.volume = 0.1
        self.sounds = {"cheese_sound": self.load_sound("cheese_sound")}

    def load_sound(self, name):
        path = resource_path(os.path.join("venv\\Sounds\\", name + ".wav"))
        return pygame.mixer.Sound(path)

    def update(self):
        mixer.music.set_volume(self.volume)
        for sound in self.sounds.keys():
            self.sounds[sound].set_volume(self.volume)

# класс для загрузки всех спрайтов
class Storage:
    def __init__(self):
        self.mouse_images = load_images("mouse", 23, int(530 / 3), int(180 / 3))
        self.cheese_images = load_images("falling_cheese", 3, 80, 80)
        self.cheese_pieses_images = load_images("cheesepiece", 5, 100, 100)
        self.background_images = load_images("background", 9, 0, 0)
        self.fade_image = pygame.transform.scale(
            pygame.image.load(
                resource_path(os.path.join("venv\\Sprites\\fade.png"))).convert_alpha(), (WIDTH,HEIGHT))
        self.fade_image.set_alpha(125)
        self.floor_image = pygame.transform.scale(
            pygame.image.load(
                resource_path(os.path.join("venv\\Sprites\\floor.png"))).convert_alpha(), (WIDTH,400))
        self.floor_rect = self.floor_image.get_rect()
        self.floor_rect.y += 300
        self.foreground_image = pygame.image.load(
            resource_path(os.path.join("venv\\Sprites\\foreground.png"))).convert_alpha()
        self.foreground_rect = self.foreground_image.get_rect()

class Lives:
    def __init__(self):
        pass

    def drow(self):
        print_text(f"LIVES: {mouse.lives}",30, WHITE, 50, 85)

class Spawner:
    def __init__(self):
        self.speed = 1400
        self.last_update = pygame.time.get_ticks()
        self.difficulty = 1
        self.i = 0

    def update(self):
        now = pygame.time.get_ticks()
        mouse.move_speed = scores_.scores/10 + 5
        if now - self.last_update > self.speed - scores_.scores*5:
            self.last_update = now
            cheese = Cheese(random.randint(100, 1000), 2 + scores_.scores/20)
            cheeses.add(cheese)
            self.i += 1
            self.difficulty += self.difficulty / self.i

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

def mouse_in_rect(Entity):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return Entity.rect.left < mouse_x < Entity.rect.left + Entity.rect.width and Entity.rect.top < mouse_y < Entity.rect.top + Entity.rect.height

# метод для загрузки нескольких спрайтов в массив
def load_images(name, count, scaleX,scaleY):
    array = []
    if scaleX == 0 and scaleY == 0:
        for i in range(count):
            try:
                array.append(pygame.image.load(resource_path(os.path.join("venv\\Sprites\\", str(name) + str(i + 1) + ".png"))).convert_alpha())
            except Warning:
                print(Warning)
    else:
        for i in range(count):
            try:
                array.append(pygame.transform.scale(
                    pygame.image.load(resource_path(os.path.join("venv\\Sprites\\", str(name) + str(i + 1) + ".png"))).convert_alpha(), (scaleX, scaleY)))
            except Warning:
                print(Warning)

    return array

# метод для отображения текста на экране
def print_text(text, size, color, x, y):
    font = pygame.font.Font(resource_path(os.path.join("venv\\Fonts\\", "main_font.ttf")), size)
    screen.blit(font.render(text, True, color), (x, y))

storage = Storage()
cheeses = pygame.sprite.Group()
cheeses.add(Cheese(100, 3))
background = Background()
mouse = Mouse()
scores_ = Scores()
spawner = Spawner()
menu = Menu()
lives = Lives()
sound_mixer = Sound_mixer()

# переменная от которой зависит цикл игры
running = True
GAME_OVER = False
GAME_STARTED = False

mixer.music.load(resource_path(os.path.join("venv\\Sounds\\","MOUSE_SAUSAGE.mp3")))
mixer.music.set_volume(0.2)
mixer.music.play(-1)

while running:
    # установка определенное колличество кадров в секунду (в нашем случае 60)
    clock.tick(FPS)
    PAUSED = menu.in_menu
    # цикл для прослушивания всех событий в игре
    for event in pygame.event.get():
        # если игрок закрывает окно, то прекратить цикл
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            menu.buttons_is_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                PAUSED = not PAUSED
                menu.in_menu = not menu.in_menu
    if not PAUSED:
        background.update()
        spawner.update()
        mouse.update()
        cheeses.update()

    background.draw()
    cheeses.draw(screen)
    mouse.draw()
    screen.blit(storage.floor_image, storage.floor_rect)
    menu.update()
    screen.blit(storage.foreground_image,storage.foreground_rect)
    lives.drow()
    scores_.update()
    print_text(str(int(clock.get_fps())), 10, WHITE, 5, 5)
    pygame.display.flip()
sys.exit()