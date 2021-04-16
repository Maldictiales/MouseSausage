# импорт нужных библиотек
import os
import sys
import webbrowser

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
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                animation(self, storage.mouse_images, 35, True)
                self.speedx = -1 * self.move_speed
                self.is_right = False
            elif keystate[pygame.K_RIGHT]:
                animation(self, storage.mouse_images, 35, True)
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
        self.image = storage.cheese_images[random.randint(0, 2)]
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
        if self.is_alive:
            self.angle += 2
            self.rotate()
            self.rect.y += self.speedy
            if is_collided_with(self, mouse):
                self.speedy = 0
                sound_mixer_.sounds["cheese_sound"].play(0)
                scores_.scores += 1
                self.is_alive = False
            if self.rect.bottom > HEIGHT:
                mouse.take_damage()
                self.speedy = 0
                self.is_alive = False
        else:
            animation(self, storage.cheese_pieses_images, 60, False)

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)


class Scores:
    def __init__(self):
        self.scores = 0

    def update(self):
        print_text("SCORES: " + str(self.scores), storage.font25, WHITE, 50, 50)


class Button:
    def __init__(self, name, func, width=250, height=125):
        try:
            self.image_normal = self.load_button_image(name, width, height)
        except:
            self.image_normal = storage.font25.render(name, True, WHITE)
        self.image_in_focus = pygame.transform.scale(self.image_normal, (width + 5, height + 5))
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.func = func

    def draw(self):
        if mouse_in_rect(self.rect):
            self.image = self.image_in_focus
        else:
            self.image = self.image_normal
        screen.blit(self.image, self.rect)

    def is_clicked(self):
        if mouse_in_rect(self.rect):
            sound_mixer_.sounds["cheese_sound"].play(0)
            self.func()

    def load_button_image(self, name, scaleX, scaleY):
        return pygame.transform.scale(
            pygame.image.load(
                resource_path(os.path.join("venv\\Sprites\\" + name + ".png"))).convert_alpha(), (scaleX, scaleY))

class Radio_button:
    def __init__(self, boolean, x, y):
        self.image = storage.radio_button_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.on = boolean

    def draw(self):
        if self.on:
            self.image = storage.radio_button_images[1]
        else:
            self.image = storage.radio_button_images[0]
        screen.blit(self.image, self.rect)

    def is_clicked(self):
        if mouse_in_rect(self.rect):
            sound_mixer_.sounds["cheese_sound"].play(0)
            self.on = not self.on

class Menu:
    def __init__(self):
        self.local_x = 455
        self.local_y = 800
        self.move_up = False
        self.in_menu = True
        self.in_settings = False
        self.move_down = False
        self.button_add_volume = Button("button_soundplus", sound_mixer_.add_volume, width=120, height=80)
        self.button_minus_volume = Button("button_soundminus", sound_mixer_.decrease_volume, width=120, height=80)
        self.button_to_menu = Button("button_quit", self.to_menu)
        self.button_music_onoff = Radio_button(sound_mixer_.play_music, self.local_x, self.local_y)
        self.buttons = [Button("button_start", self.start),
                        Button("button_credits", about_us.about_us_button),
                        Button("button_settings", self.settings),
                        Button("button_quit", self.quit)]

    def update(self):
        if self.move_down:
            self.moving_down()
        if self.move_up:
            self.moving_up()
        if self.in_menu:
            self.move_up = True
            self.move_down = False
            screen.blit(storage.fade_image, storage.fade_image.get_rect())
            if not self.in_settings:
                for i in range(len(self.buttons)):
                    self.buttons[i].rect.x = self.local_x
                    self.buttons[i].rect.y = self.local_y + i * 125
                    self.buttons[i].draw()
            else:
                self.button_music_onoff.rect.y = self.local_y
                print_text("Disable music", storage.font25, WHITE, self.local_x + 100, self.local_y + 10)
                self.button_music_onoff.draw()
                sound_mixer_.play_music = self.button_music_onoff.on

                self.button_add_volume.rect.x = self.local_x - 10
                self.button_add_volume.rect.y = self.local_y + 100
                self.button_add_volume.draw()

                print_text("Volume", storage.font25, WHITE, self.local_x + 100, self.local_y + 110)

                self.button_minus_volume.rect.x = self.local_x + 210
                self.button_minus_volume.rect.y = self.local_y + 100
                self.button_minus_volume.draw()

                self.button_to_menu.rect.x = self.local_x
                self.button_to_menu.rect.y = self.local_y + 200
                self.button_to_menu.draw()


        if not self.in_menu:
            self.move_down = True
            self.move_up = False
            for i in range(len(self.buttons)):
                self.buttons[i].rect.x = self.local_x
                self.buttons[i].rect.y = self.local_y + i * 125
                self.buttons[i].draw()

    def buttons_is_pressed(self):
        for button in self.buttons:
            button.is_clicked()

    def moving_up(self):
        if self.local_y < 100:
            self.move_up = False
        if self.move_up:
            self.local_y -= 15

    def moving_down(self):
        if self.local_y > 800:
            self.move_down = False
        if self.move_down:
            self.local_y += 15

    def settings(self):
        self.in_settings = True

    def start(self):
        self.in_menu = False

    def to_menu(self):
        self.in_settings = False
        self.in_menu = True

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


class Sound_mixer:
    def __init__(self):
        self.volume = 0.1
        self.sounds = {"cheese_sound": self.load_sound("cheese_sound")}
        self.play_music = True

    def load_sound(self, name):
        path = resource_path(os.path.join("venv\\Sounds\\", name + ".wav"))
        return pygame.mixer.Sound(path)

    def update(self):
        mixer.music.set_volume(self.volume)
        for sound in self.sounds.keys():
            self.sounds[sound].set_volume(self.volume)

    def add_volume(self):
        self.volume += 0.03

    def decrease_volume(self):
        self.volume -= 0.03



# класс для загрузки всех спрайтов
class Storage:
    def __init__(self):
        self.mouse_images = load_images("mouse", 23, int(530 / 3), int(180 / 3))
        self.cheese_images = load_images("falling_cheese", 3, 80, 80)
        self.cheese_pieses_images = load_images("cheesepiece", 5, 100, 100)
        self.authors_images = load_images("chibi", 3, 300, 300)
        self.background_credits = pygame.image.load(
            resource_path(os.path.join("venv\\Sprites\\background_credits.png"))).convert_alpha()
        self.background_images = load_images("background", 9, 0, 0)
        self.radio_button_images = load_images("radio_button", 2, 80, 60)
        self.button_volume_add_image = pygame.image.load(
                resource_path(os.path.join("venv\\Sprites\\button_soundplus.png"))).convert_alpha()
        self.button_volume_minus_image = pygame.image.load(
            resource_path(os.path.join("venv\\Sprites\\button_soundminus.png"))).convert_alpha()
        self.fade_image = pygame.transform.scale(
            pygame.image.load(
                resource_path(os.path.join("venv\\Sprites\\fade.png"))).convert_alpha(), (WIDTH, HEIGHT))
        self.fade_image.set_alpha(125)
        self.floor_image = pygame.transform.scale(
            pygame.image.load(
                resource_path(os.path.join("venv\\Sprites\\floor.png"))).convert_alpha(), (WIDTH, 400))
        self.floor_rect = self.floor_image.get_rect()
        self.floor_rect.y += 300
        self.foreground_image = pygame.image.load(
            resource_path(os.path.join("venv\\Sprites\\foreground.png"))).convert_alpha()
        self.foreground_rect = self.foreground_image.get_rect()
        font_path = resource_path(os.path.join("venv\\Fonts\\", "main_font.ttf"))
        self.font10 = pygame.font.Font(font_path, 10)
        self.font16 = pygame.font.Font(font_path, 16)
        self.font25 = pygame.font.Font(font_path, 25)
        self.font50 = pygame.font.Font(font_path, 50)


class Lives:
    def __init__(self):
        pass

    def draw(self):
        print_text(f"LIVES: {mouse.lives}", storage.font25, WHITE, 50, 85)


class Spawner:
    def __init__(self):
        self.speed = 1400
        self.last_update = pygame.time.get_ticks()
        self.difficulty = 1
        self.i = 0

    def update(self):
        now = pygame.time.get_ticks()
        mouse.move_speed = scores_.scores / 10 + 5
        if now - self.last_update > self.speed - scores_.scores * 5:
            self.last_update = now
            cheese = Cheese(random.randint(100, 1000), 2 + scores_.scores / 20)
            cheeses.add(cheese)
            self.i += 1
            self.difficulty += self.difficulty / self.i


class About_us:
    def __init__(self):
        self.in_view = False
        self.exit_button = Button("BACK", self.about_us_button)
        self.exit_button.rect.y = 600
        self.exit_button.rect.x = 1000
        self.authors = [Info_node(x=500, y=50, header="Kira Beznik",
                                  main=["telegram", "github"],
                                  links=["https://web.telegram.org/#/im?p=@Maldictiales",
                                         "https://github.com/Maldictiales"]),
                        Info_node(x=500, y=300, header="RusKom",
                                  main=["telegram", "github"],
                                  links=["https://web.telegram.org/#/im?p=@RusK0m", "https://github.com/RusKom27"]),
                        Info_node(x=500, y=500, header="Miracyber",
                                  main=["telegram", "github"],
                                  links=["https://web.telegram.org/#/im?p=@Bruuh228", "https://github.com/Kekwait777"])]

        self.images = [[storage.background_credits, storage.background_credits.get_rect()],
                       [storage.authors_images[0], (700, 20, 200, 200)],
                       [storage.authors_images[1], (100, 220, 200, 200)],
                       [storage.authors_images[2], (700, 320, 200, 200)]]

    def about_us_button(self):
        self.in_view = not self.in_view

    def draw(self):
        for image in self.images:
            screen.blit(image[0], image[1])
        for author in self.authors:
            author.draw()
        screen.blit(self.exit_button.image, self.exit_button.rect)


class Info_node:
    def __init__(self, header="HEADER", main=None, links=None, x=100, y=100):
        if main is None:
            main = ["youtube", "second"]
        if links is None:
            links = ["https://www.youtube.com", ""]
        self.rect = pygame.Rect(x, y, 100, 100)
        self.header = header
        self.main = main.copy()
        self.main_rects = []
        for _ in main:
            self.main_rects.append(pygame.Rect)
        self.links = links

    def draw(self):
        print_text(self.header, storage.font25, WHITE, self.rect.x, self.rect.y)
        for info in range(len(self.main)):
            self.main_rects[info] = print_text(self.main[info], storage.font16, WHITE, self.rect.x,
                                               (self.rect.y + 40) + 25 * info)
            self.main_rects[info].x = self.rect.x
            self.main_rects[info].y = (self.rect.y + 40) + 25 * info
            self.is_focused(self.main_rects[info].copy())

    def is_focused(self, rect):
        if mouse_in_rect(rect):
            rect.height = 3
            rect.y += 25
            rect.x -= 1
            pygame.draw.rect(screen, BLACK, rect, 2)
            rect.x += 1
            rect.y -= 1
            pygame.draw.rect(screen, WHITE, rect, 2)

    def click(self):
        for rect in range(len(self.main_rects)):
            if type(self.main_rects[rect]) == type(self.rect):
                if mouse_in_rect(self.main_rects[rect]):
                    sound_mixer_.sounds["tv_sound_buttons"].play(0)
                    if not self.links[rect] == "":
                        webbrowser.open_new_tab(self.links[rect])

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


def mouse_in_rect(rect):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return rect.left < mouse_x < rect.left + rect.width and rect.top < mouse_y < rect.top + rect.height


# метод для загрузки нескольких спрайтов в массив
def load_images(name, count, scaleX, scaleY):
    array = []
    if scaleX == 0 and scaleY == 0:
        for i in range(count):
            try:
                array.append(pygame.image.load(
                    resource_path(os.path.join("venv\\Sprites\\", str(name) + str(i + 1) + ".png"))).convert_alpha())
            except Warning:
                print(Warning)
    else:
        for i in range(count):
            try:
                array.append(pygame.transform.scale(
                    pygame.image.load(resource_path(
                        os.path.join("venv\\Sprites\\", str(name) + str(i + 1) + ".png"))).convert_alpha(),
                    (scaleX, scaleY)))
            except Warning:
                print(Warning)

    return array


# метод для отображения текста на экране
def print_text(text, font, color, x, y):
    screen.blit(font.render(text, True, BLACK), (x - 1, y + 1))
    screen.blit(font.render(text, True, color), (x, y))
    return font.render(text, True, color).get_rect()


storage = Storage()
cheeses = pygame.sprite.Group()
background = Background()
mouse = Mouse()
scores_ = Scores()
spawner = Spawner()
about_us = About_us()
sound_mixer_ = Sound_mixer()
menu = Menu()
lives = Lives()


# переменная от которой зависит цикл игры
running = True
GAME_OVER = False
GAME_STARTED = False

while running:
    if sound_mixer_.play_music:
        mixer.music.load(resource_path(os.path.join("venv\\Sounds\\", "MOUSE_SAUSAGE.mp3")))
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)
    # установка определенное колличество кадров в секунду (в нашем случае 60)
    clock.tick(FPS)
    PAUSED = menu.in_menu
    # цикл для прослушивания всех событий в игре
    for event in pygame.event.get():
        # если игрок закрывает окно, то прекратить цикл
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            print(about_us.in_view, menu.in_menu, menu.in_settings)
            if not about_us.in_view and not menu.in_settings:
                menu.buttons_is_pressed()
            elif about_us.in_view:
                about_us.exit_button.is_clicked()
            elif menu.in_settings:
                menu.button_to_menu.is_clicked()
                menu.button_add_volume.is_clicked()
                menu.button_minus_volume.is_clicked()
                menu.button_music_onoff.is_clicked()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not about_us.in_view:
                    PAUSED = not PAUSED
                    menu.in_menu = not menu.in_menu
                    menu.in_settings = False
                else:
                    about_us.in_view = not about_us.in_view
    if not PAUSED:
        background.update()
        spawner.update()
        mouse.update()
        cheeses.update()
    background.draw()
    cheeses.draw(screen)
    mouse.draw()
    sound_mixer_.update()
    screen.blit(storage.floor_image, storage.floor_rect)
    menu.update()
    screen.blit(storage.foreground_image, storage.foreground_rect)
    if about_us.in_view:
        about_us.draw()
    if not PAUSED:
        lives.draw()
        scores_.update()
    print_text(str(int(clock.get_fps())), storage.font10, WHITE, 5, 5)
    pygame.display.flip()
sys.exit()
