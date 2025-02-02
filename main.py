import math
import os
import random
import sys
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
LIGHT_RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
fps = 60

clock = pygame.time.Clock()
size = WIDTH, HEIGHT = 1920, 1080
button_width, button_height = 200, 50
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
weapons = pygame.sprite.Group()
protection = pygame.sprite.Group()
health = pygame.sprite.Group()
walls = pygame.sprite.Group()
iron_box = pygame.sprite.Group()
floor = pygame.sprite.Group()
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
screen_rect = (0, 0, WIDTH, HEIGHT)

sound_walking_iron = pygame.mixer.Sound('sounds\\walking_on_iron.wav')
sound_button = pygame.mixer.Sound('sounds\\button_sound.wav')

sound_heal = pygame.mixer.Sound('sounds\\heal_sound.wav')
sound_shoot = pygame.mixer.Sound('sounds\\shot_m4.wav')
sound_uzi = pygame.mixer.Sound('sounds\\uzi_sound.wav')
sound_sniper = pygame.mixer.Sound('sounds\\sniper_shoot.wav')
sound_pistol = pygame.mixer.Sound('sounds\\pistol_sound.wav')
sound_shotgun = pygame.mixer.Sound('sounds\\shotgun_sound.wav')
sound_change_weapon = pygame.mixer.Sound('sounds\\change_weapon.wav')
sound_no_ammo = pygame.mixer.Sound('sounds\\sound_no_ammo.wav')
sound_change_armor = pygame.mixer.Sound('sounds\\change_armor.wav')
sound_shoot_armor = pygame.mixer.Sound('sounds\\shoot_armor.wav')

sound_injury1 = pygame.mixer.Sound('sounds\\injury_people1.wav')
sound_injury2 = pygame.mixer.Sound('sounds\\injury_people2.wav')
sound_injury3 = pygame.mixer.Sound('sounds\\injury_people3.wav')
sound_injury4 = pygame.mixer.Sound('sounds\\injury_people4.wav')
sound_death = pygame.mixer.Sound('sounds\\death_people.wav')
sound_injury = [sound_injury1, sound_injury2, sound_injury3, sound_injury4]
all_sounds = [sound_walking_iron, sound_shoot, sound_change_weapon, sound_no_ammo, sound_change_armor,
              sound_shoot_armor,
              sound_injury1, sound_injury2, sound_injury3, sound_injury4, sound_death, sound_button, sound_heal,
              sound_uzi, sound_sniper, sound_pistol, sound_shotgun]
f1 = pygame.font.Font(None, 58)


def load_image(name, path='data', colorkey=None):
    fullname = os.path.join(path, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


font = pygame.font.Font('data\\main_font.otf', 30)
font_side = pygame.font.Font('data\\main_font.otf', 31)


def draw_button(surface, rect, color, hover_color, text, text_color):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    shadow_rect = rect.move(5, 5)
    pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=20)
    button_color = hover_color if is_hovered else color
    pygame.draw.rect(surface, button_color, rect, border_radius=20)
    draw_text(text, font, text_color, surface, rect.centerx, rect.centery)
    return is_hovered


def draw_text(text, font, color, surface, x, y, second=False):
    if second:
        text_obj = font_side.render(text, True, 'red')
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_slider(surface, rect, color, hover_color, value, is_dragging):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)

    # Изменение цвета слайдера при наведении
    slider_color = hover_color if is_hovered else color

    # слайдер
    pygame.draw.rect(surface, slider_color, rect, border_radius=10)

    # Положение ползунка
    indicator_x = rect.x + int(value * rect.width)
    indicator_y = rect.centery

    pygame.draw.line(surface, 'black', (1920 // 2 - 100, 280 + button_height // 2),
                     (1920 // 2 + 100, 280 + button_height // 2), 3)  # sound
    pygame.draw.line(surface, 'black', (1920 // 2 - 100, 380 + button_height // 2),
                     (1920 // 2 + 100, 380 + button_height // 2), 3)
    pygame.draw.circle(surface, 'black', (indicator_x, indicator_y), 14)
    pygame.draw.circle(surface, 'white', (indicator_x, indicator_y), 15, 1)

    if is_dragging:
        new_value = (mouse_pos[0] - rect.x) / rect.width
        new_value = max(0, min(1, new_value))
        return new_value
    return value


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.mixer.music.load('music\\main_menu.wav')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)

    start_button = pygame.Rect(1920 // 2 - button_width // 2, 400, button_width, button_height)
    settings_button = pygame.Rect(1920 // 2 - button_width // 2, 500, button_width, button_height)
    exit_button = pygame.Rect(1920 // 2 - button_width // 2, 600, button_width, button_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    sound_button.play()
                    pygame.mixer.music.stop()
                    return "start"
                elif settings_button.collidepoint(event.pos):
                    sound_button.play()
                    settings()
                elif exit_button.collidepoint(event.pos):
                    sound_button.play()
                    pygame.quit()
                    sys.exit()
        fon = pygame.transform.scale(load_image('main_menu_pic.jpg'), (1920, 1080))
        screen.blit(fon, (0, 0))
        draw_button(screen, start_button, (200, 0, 0), (255, 0, 0), "Начать игру", (0, 0, 0))
        draw_button(screen, settings_button, (200, 0, 0), (255, 0, 0), "Настройки", (0, 0, 0))
        draw_button(screen, exit_button, (200, 0, 0), (255, 0, 0), "Выход", (0, 0, 0))
        pygame.display.flip()
        clock.tick(fps)


def get_key_name(key_code):
    key_name = pygame.key.name(key_code)
    return f"{key_name.upper()}"


def settings():
    settings_data = load_settings()
    sound_value = settings_data["sound_value"]
    music_value = settings_data["music_value"]
    key_bindings = settings_data["key_bindings"]

    slider_sound = pygame.Rect(WIDTH // 2 - 100, 295, 200, 20)
    slider_music = pygame.Rect(WIDTH // 2 - 100, 395, 200, 20)

    buttons = {
        "back": pygame.Rect(WIDTH // 2 - 50, 900, 200, 50),
        "first_forward": pygame.Rect(WIDTH // 2 - 600, 575, 600, 30),
        "first_left": pygame.Rect(WIDTH // 2 - 600, 625, 600, 30),
        "first_back": pygame.Rect(WIDTH // 2 - 600, 675, 600, 30),
        "first_right": pygame.Rect(WIDTH // 2 - 600, 725, 600, 30),
        "first_action": pygame.Rect(WIDTH // 2 - 600, 775, 600, 30),
        "first_shoot": pygame.Rect(WIDTH // 2 - 600, 825, 600, 30),
        "second_forward": pygame.Rect(WIDTH // 2 + 50, 575, 600, 30),
        "second_left": pygame.Rect(WIDTH // 2 + 50, 625, 600, 30),
        "second_back": pygame.Rect(WIDTH // 2 + 50, 675, 600, 30),
        "second_right": pygame.Rect(WIDTH // 2 + 50, 725, 600, 30),
        "second_action": pygame.Rect(WIDTH // 2 + 50, 775, 600, 30),
        "second_shoot": pygame.Rect(WIDTH // 2 + 50, 825, 600, 30),
    }

    music_dragging = False
    sound_dragging = False

    active_button = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_sound.collidepoint(event.pos):
                    sound_dragging = True
                elif slider_music.collidepoint(event.pos):
                    music_dragging = True
                for button_name, button_rect in buttons.items():
                    if button_rect.collidepoint(event.pos) and button_name != "back":
                        active_button = button_name
                if buttons["back"].collidepoint(event.pos):
                    sound_button.play()
                    save_settings({
                        "sound_value": sound_value,
                        "music_value": music_value,
                        "key_bindings": key_bindings})
                    return key_bindings
            elif event.type == pygame.MOUSEBUTTONUP:
                music_dragging = False
                sound_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if music_dragging:
                    music_value = (event.pos[0] - slider_music.x) / slider_music.width
                    music_value = max(0, min(1, music_value))
                    pygame.mixer.music.set_volume(music_value)
                elif sound_dragging:
                    sound_value = (event.pos[0] - slider_sound.x) / slider_sound.width
                    sound_value = max(0, min(1, sound_value))
                    for sound in all_sounds:
                        sound.set_volume(sound_value)
            elif event.type == pygame.KEYDOWN and active_button:
                key_bindings[active_button] = event.key
                active_button = None

        fon = pygame.transform.scale(load_image('main_menu_pic.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        draw_slider(screen, slider_sound, RED, LIGHT_RED, sound_value, sound_dragging)
        draw_slider(screen, slider_music, RED, LIGHT_RED, music_value, music_dragging)

        draw_text('Звуки:', font, BLACK, screen, WIDTH // 2, 270, True)
        draw_text('Музыка:', font, BLACK, screen, WIDTH // 2, 370, True)
        draw_text('Управление', font, BLACK, screen, WIDTH // 2, 475, True)
        draw_text('Первый игрок', font, BLACK, screen, WIDTH // 2 - 300, 525, True)
        draw_text('Второй игрок', font, BLACK, screen, WIDTH // 2 + 300, 525, True)

        draw_button(screen, buttons["back"], RED, LIGHT_RED, "Назад", BLACK)

        draw_button(screen, buttons["first_forward"], RED, LIGHT_RED,
                    f"Вперед - {get_key_name(key_bindings['first_forward'])}", BLACK)
        draw_button(screen, buttons["first_left"], RED, LIGHT_RED,
                    f"Налево - {get_key_name(key_bindings['first_left'])}", BLACK)
        draw_button(screen, buttons["first_back"], RED, LIGHT_RED,
                    f"Назад - {get_key_name(key_bindings['first_back'])}", BLACK)
        draw_button(screen, buttons["first_right"], RED, LIGHT_RED,
                    f"Направо - {get_key_name(key_bindings['first_right'])}", BLACK)
        draw_button(screen, buttons["first_action"], RED, LIGHT_RED,
                    f"Действие - {get_key_name(key_bindings['first_action'])}", BLACK)
        draw_button(screen, buttons["first_shoot"], RED, LIGHT_RED,
                    f"Стрельба - {get_key_name(key_bindings['first_shoot'])}", BLACK)

        draw_button(screen, buttons["second_forward"], RED, LIGHT_RED,
                    f"Вперед - {get_key_name(key_bindings['second_forward'])}", BLACK)
        draw_button(screen, buttons["second_left"], RED, LIGHT_RED,
                    f"Налево - {get_key_name(key_bindings['second_left'])}", BLACK)
        draw_button(screen, buttons["second_back"], RED, LIGHT_RED,
                    f"Назад - {get_key_name(key_bindings['second_back'])}", BLACK)
        draw_button(screen, buttons["second_right"], RED, LIGHT_RED,
                    f"Направо - {get_key_name(key_bindings['second_right'])}", BLACK)
        draw_button(screen, buttons["second_action"], RED, LIGHT_RED,
                    f"Действие - {get_key_name(key_bindings['second_action'])}", BLACK)
        draw_button(screen, buttons["second_shoot"], RED, LIGHT_RED,
                    f"Стрельба - {get_key_name(key_bindings['second_shoot'])}", BLACK)

        if active_button:
            draw_text("Нажмите новую клавишу", font, BLACK, screen, WIDTH // 2, HEIGHT - 100, True)

        pygame.display.flip()


def load_settings():
    settings = {
        "sound_value": 1.0,
        "music_value": 1.0,
        "key_bindings": {
            "first_forward": pygame.K_w,
            "first_left": pygame.K_a,
            "first_back": pygame.K_s,
            "first_right": pygame.K_d,
            "first_action": pygame.K_e,
            "first_shoot": pygame.K_SPACE,
            "second_forward": pygame.K_UP,
            "second_left": pygame.K_LEFT,
            "second_back": pygame.K_DOWN,
            "second_right": pygame.K_RIGHT,
            "second_action": pygame.K_KP0,
            "second_shoot": pygame.K_RCTRL
        }
    }
    try:
        with open("settings.txt", "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                if key == "sound_value" or key == "music_value":
                    settings[key] = float(value)
                else:
                    key_binding, action = key.split(".")
                    settings["key_bindings"][key_binding] = int(value)
    except Exception:
        pass
    return settings


def save_settings(settings):
    with open("settings.txt", "w") as file:
        file.write(f"sound_value={settings['sound_value']}\n")
        file.write(f"music_value={settings['music_value']}\n")
        for key, value in settings["key_bindings"].items():
            file.write(f"{key}.key={value}\n")


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, owner):
        super().__init__(all_sprites)
        self.image = load_image("bullet.png", colorkey=-1)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.damage = 40
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.owner = owner
        self.v = 2000
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            self.velocity = [0, 0]
        else:
            self.angle_deviation = random.uniform(-0.1, 0.1)
            self.velocity = [
                (dx / distance) * self.v / fps + dy / distance * self.angle_deviation * self.v / fps,
                (dy / distance) * self.v / fps - dx / distance * self.angle_deviation * self.v / fps
            ]
            angle = math.degrees(math.atan2(dy, dx))
            self.image = pygame.transform.rotate(self.image, -angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, *args):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        box = pygame.sprite.spritecollideany(self, walls)
        if box is not None:
            box.hp -= self.damage
            create_particles((box.rect.centerx, box.rect.centery), box)
            if box.hp <= 0:
                box.kill()
            self.kill()

        iron = pygame.sprite.spritecollideany(self, iron_box)
        if iron is not None:
            create_particles((iron.rect.centerx, iron.rect.centery), iron)
            self.kill()

        for i in players:
            if i != self.owner:
                if i.armor is None:
                    if any(pygame.sprite.collide_mask(self, sprite) for sprite in players if
                           sprite != self and sprite != self.owner):
                        for i in players:
                            if i != self.owner:
                                i.hp -= self.damage
                                create_particles((i.rect.centerx, i.rect.centery), i)
                                if i.hp > 0:
                                    random.choice(sound_injury).play()
                        self.kill()
                else:
                    if pygame.sprite.collide_mask(self, i.armor):
                        i.armor.hp -= self.damage
                        if i.armor.hp <= 0:
                            i.hp += i.armor.hp
                        create_particles((i.rect.centerx, i.rect.centery), i.armor)
                        sound_shoot_armor.play()
                        self.kill()
                        break

        if not self.rect.colliderect(screen_rect):
            self.kill()


class Uzi_bullet(Bullet):
    def __init__(self, pos, target_pos, owner):
        super().__init__(pos, target_pos, owner)
        self.damage = 15
        self.angle_deviation = random.uniform(-0.05, 0.05)

        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            self.velocity = [
                (dx / distance) * self.v / fps + dy / distance * self.angle_deviation * self.v / fps,
                (dy / distance) * self.v / fps - dx / distance * self.angle_deviation * self.v / fps
            ]


class Sniper_bullet(Bullet):
    def __init__(self, pos, target_pos, owner):
        super().__init__(pos, target_pos, owner)
        self.damage = 500
        self.angle_deviation = random.uniform(-0.01, 0.01)
        self.v = 5000
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            self.velocity = [
                (dx / distance) * self.v / fps + dy / distance * self.angle_deviation * self.v / fps,
                (dy / distance) * self.v / fps - dx / distance * self.angle_deviation * self.v / fps
            ]


class Pistol_bullet(Bullet):
    def __init__(self, pos, target_pos, owner):
        super().__init__(pos, target_pos, owner)
        self.damage = 50
        self.angle_deviation = random.uniform(-0.05, 0.05)
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            self.velocity = [
                (dx / distance) * self.v / fps + dy / distance * self.angle_deviation * self.v / fps,
                (dy / distance) * self.v / fps - dx / distance * self.angle_deviation * self.v / fps
            ]


class Shotgun_bullet(Bullet):
    def __init__(self, pos, target_pos, owner):
        super().__init__(pos, target_pos, owner)
        self.damage = 50
        self.angle_deviation = random.uniform(-0.1, 0.1)
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            self.velocity = [
                (dx / distance) * self.v / fps + dy / distance * self.angle_deviation * self.v / fps,
                (dy / distance) * self.v / fps - dx / distance * self.angle_deviation * self.v / fps
            ]


class Player(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, player_folder):
        super().__init__(all_sprites, players)
        self.radius = radius
        self.last_step_time = 0
        self.player_folder = player_folder
        self.animations = {}
        self.load_animations()
        self.current_frame = 0
        self.animation_speed = 0.15
        self.current_animation = 'down'
        self.image = self.animations['down'][0]

        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 100
        self.weapon = None
        self.armor = None
        self.v = 500

    def load_animations(self):
        for direction in ['up', 'down', 'left', 'right']:
            path = os.path.join(self.player_folder, direction)
            if os.path.isdir(path):
                images = []
                for filename in sorted(os.listdir(path)):
                    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                        img = load_image(os.path.join(path, filename), '', -1)
                        img = pygame.transform.scale(img, (100, 100))
                        images.append(img)
                self.animations[direction] = images
            else:
                print('Папка не найдена')
                self.animations[direction] = [pygame.Surface((1, 1), pygame.SRCALPHA)]

    def update(self, bind):
        global victory
        flag = False
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if self == first_player:
            if keys[bind['first_forward']]:
                self.rect.y -= self.v / fps
                self.current_animation = 'up'
                if pygame.sprite.collide_mask(self, second_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.y += self.v / fps
            elif keys[bind['first_back']]:
                self.rect.y += self.v / fps
                self.current_animation = 'down'
                if pygame.sprite.collide_mask(self, second_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.y -= self.v / fps
            elif keys[bind['first_left']]:
                self.rect.x -= self.v / fps
                self.current_animation = 'left'
                if pygame.sprite.collide_mask(self, second_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.x += self.v / fps
            elif keys[bind['first_right']]:
                self.rect.x += self.v / fps
                self.current_animation = 'right'
                if pygame.sprite.collide_mask(self, second_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.x -= self.v / fps
            else:
                flag = True
        else:
            if keys[bind['second_forward']]:
                self.rect.y -= self.v / fps
                self.current_animation = 'up'
                if pygame.sprite.collide_mask(self, first_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.y += self.v / fps
            elif keys[bind['second_back']]:
                self.rect.y += self.v / fps
                self.current_animation = 'down'
                if pygame.sprite.collide_mask(self, first_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.y -= self.v / fps
            elif keys[bind['second_left']]:
                self.rect.x -= self.v / fps
                self.current_animation = 'left'
                if pygame.sprite.collide_mask(self, first_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.x += self.v / fps
            elif keys[bind['second_right']]:
                self.rect.x += self.v / fps
                self.current_animation = 'right'
                if pygame.sprite.collide_mask(self, first_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.x -= self.v / fps
            else:
                flag = True
        if not flag and current_time - self.last_step_time > 400:
            sound_walking_iron.play()

            self.last_step_time = current_time
        if self.hp <= 0:
            self.weapon = None
            self.kill()
            victory = True
            sound_death.play()

        if not flag:
            self.animate()
        else:
            self.image = self.animations['down'][0]

        if first_player.weapon:
            first_player.weapon.update(second_player)
        if second_player.weapon:
            second_player.weapon.update(first_player)
        if self.armor is not None:
            self.armor.update()

    def animate(self):
        animation = self.animations.get(self.current_animation, self.animations['down'])
        if animation:
            self.current_frame = (self.current_frame + self.animation_speed) % len(animation)
            self.image = animation[int(self.current_frame)]


class Weapon(pygame.sprite.Sprite):
    def __init__(self, image_path, owner):
        super().__init__(weapons)
        self.owner = owner
        self.ammo = 30
        self.original_image = load_image(image_path, colorkey=-1)
        self.original_image = pygame.transform.scale(self.original_image, (77, 26))
        self.image = self.original_image
        self.offset = pygame.math.Vector2(-10, 0)
        if self.owner is not None:
            self.rect = self.image.get_rect(center=owner.rect.center + self.offset)
        else:
            self.rect = self.image.get_rect(center=(10, 10))
        self.barrel_offset = pygame.math.Vector2(20, -5)
        self.flip_x = False
        self.angle_offset = 0
        self.fire_timer = 0

    def spawn_weapon(self):
        while True:
            self.rect.x = random.randrange(1920)
            self.rect.y = random.randrange(1080)
            if (not any(pygame.sprite.collide_rect(self, sprite) for sprite in weapons if
                        sprite != self) and not pygame.sprite.spritecollideany(self, walls)
                    and not pygame.sprite.spritecollideany(self, iron_box)):
                break

    def update(self, target):
        dx = target.rect.centerx - self.owner.rect.centerx
        dy = target.rect.centery - self.owner.rect.centery

        angle = math.degrees(math.atan2(dy, dx))

        if -270 < angle < -90 or 90 < angle < 270:
            if not self.flip_x:
                self.original_image = pygame.transform.flip(self.original_image, True, False)
                self.flip_x = True
                self.angle_offset = 180
            angle += self.angle_offset
        elif self.flip_x:
            self.original_image = pygame.transform.flip(self.original_image, True, False)
            self.flip_x = False
            self.angle_offset = 0

        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.owner.rect.center + self.offset)
        self.angle = angle
        if self.fire_timer > 0:
            self.fire_timer -= 1

    def get_barrel_position(self):
        barrel_offset = self.barrel_offset.copy()
        if self.flip_x:
            barrel_offset.x *= -1
        rotated_offset = barrel_offset.rotate(self.angle)
        return self.rect.center + rotated_offset

    def shoot(self):
        if self.fire_timer == 0 and self.ammo > 0:
            bullet_start_pos = self.get_barrel_position()
            target = second_player if self.owner == first_player else first_player
            bullet = Bullet(bullet_start_pos, target.rect.center, self.owner)
            bullets.add(bullet)
            sound_shoot.play()
            self.fire_timer = 10
            self.ammo -= 1
        if self.ammo == 0:
            sound_no_ammo.play()


class Uzi(Weapon):
    def __init__(self, image_path, owner):
        super().__init__(image_path, owner)
        self.ammo = 62
        self.original_image = load_image(image_path, colorkey=-1)
        self.original_image = pygame.transform.scale(self.original_image, (80, 45))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.fire_timer = 0
        self.fire_rate = 15

    def shoot(self):
        if self.fire_timer <= 0 and self.ammo > 0:
            bullet_start_pos = self.get_barrel_position()
            target = second_player if self.owner == first_player else first_player
            bullet = Uzi_bullet(bullet_start_pos, target.rect.center, self.owner)
            bullets.add(bullet)
            sound_uzi.play()
            self.fire_timer = self.fire_rate
            self.ammo -= 1

        if self.ammo == 0:
            sound_no_ammo.play()

    def update(self, target):
        super().update(target)
        if self.fire_timer > 0:
            self.fire_timer -= 1


class Sniper_rifle(Weapon):
    def __init__(self, image_path, owner):
        super().__init__(image_path, owner)
        self.ammo = 3
        self.original_image = load_image(image_path, colorkey=-1)
        self.original_image = pygame.transform.scale(self.original_image, (150, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.fire_timer = 0
        self.fire_rate = 200

    def shoot(self):
        if self.fire_timer <= 0 and self.ammo > 0:
            bullet_start_pos = self.get_barrel_position()
            target = second_player if self.owner == first_player else first_player
            bullet = Sniper_bullet(bullet_start_pos, target.rect.center, self.owner)
            bullets.add(bullet)
            sound_sniper.play()
            self.fire_timer = self.fire_rate
            self.ammo -= 1

        if self.ammo == 0:
            sound_no_ammo.play()

    def update(self, target):
        super().update(target)
        if self.fire_timer > 0:
            self.fire_timer -= 1


class Pistol(Weapon):
    def __init__(self, image_path, owner):
        super().__init__(image_path, owner)
        self.ammo = 10
        self.original_image = load_image(image_path, colorkey=-1)
        self.original_image = pygame.transform.scale(self.original_image, (60, 25))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.fire_timer = 0
        self.fire_rate = 100

    def shoot(self):
        if self.fire_timer <= 0 and self.ammo > 0:
            bullet_start_pos = self.get_barrel_position()
            target = second_player if self.owner == first_player else first_player
            bullet = Pistol_bullet(bullet_start_pos, target.rect.center, self.owner)
            bullets.add(bullet)
            sound_pistol.play()
            self.fire_timer = self.fire_rate
            self.ammo -= 1

        if self.ammo == 0:
            sound_no_ammo.play()

    def update(self, target):
        super().update(target)
        if self.fire_timer > 0:
            self.fire_timer -= 1


class Shotgun(Weapon):
    def __init__(self, image_path, owner):
        super().__init__(image_path, owner)
        self.ammo = 8
        self.fire_timer = 0
        self.fire_rate = 60
        self.original_image = load_image(image_path, colorkey=-1)
        self.original_image = pygame.transform.scale(self.original_image, (120, 120))
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def shoot(self):
        if self.fire_timer <= 0 and self.ammo > 0:
            bullet_start_pos = self.get_barrel_position()
            target = second_player if self.owner == first_player else first_player

            for i in range(3):
                bullet = Shotgun_bullet(bullet_start_pos, target.rect.center, self.owner)
                bullets.add(bullet)

            sound_shotgun.play()
            self.fire_timer = self.fire_rate
            self.ammo -= 1

        if self.ammo == 0:
            sound_no_ammo.play()


class Armor(pygame.sprite.Sprite):
    def __init__(self, armor_path, owner):
        super().__init__(protection)
        self.owner = owner

        self.image = load_image(armor_path, colorkey=-1)
        self.image = pygame.transform.scale(self.image, (90, 50))

        if self.owner is not None:
            self.rect = self.image.get_rect(center=owner.rect.center)
        else:
            self.rect = self.image.get_rect(center=(10, 10))
        self.hp = 100

    def spawn_armor(self):
        while True:
            self.rect.x = random.randrange(1920)
            self.rect.y = random.randrange(1080)
            if (not any(pygame.sprite.collide_rect(self, sprite) for sprite in protection if
                        sprite != self) and not pygame.sprite.spritecollideany(self, walls)
                    and not pygame.sprite.spritecollideany(self, iron_box)):
                break

    def update(self):
        self.rect = self.image.get_rect(center=self.owner.rect.center)
        if self.hp <= 0:
            self.owner.armor = None
            self.kill()


class Heart(Armor):
    def __init__(self, heart_pic, owner):
        super().__init__(heart_pic, owner)
        self.hp = 50
        self.image = load_image(heart_pic, colorkey=-1)
        self.image = pygame.transform.scale(self.image, (30, 30))


class Middle_Armor(Armor):
    def __init__(self, armor_path, owner):
        super().__init__(armor_path, owner)
        self.hp = 200
        # self.image = load_image(armor_path, colorkey=-1)
        # self.image = pygame.transform.scale(self.image, (100, 100))


class Heavy_Armor(Armor):
    def __init__(self, armor_path, owner):
        super().__init__(armor_path, owner)
        self.hp = 300


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(all_sprites, walls)
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color("black"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, surface):
        super().__init__(all_sprites)
        part = pygame.Surface([3, 3])
        color = 'red' if surface in players else 'gray'
        part.fill(color)
        fire = [part]
        for scale in (3, 3):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))
        self.original_images = fire
        self.image = random.choice(self.original_images)
        self.rect = self.image.get_rect(center=pos)

        self.velocity = [dx, dy]

        self.distance_blood = 0
        self.life_time = 150
        self.current_life = self.life_time

    def update(self, *keys):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.distance_blood += abs(self.velocity[0]) + abs(self.velocity[1])

        self.current_life -= 1

        if self.current_life <= 0:
            self.kill()
        else:
            alpha = int(255 * (self.current_life / self.life_time))
            self.image.set_alpha(alpha)
            self.rect = self.image.get_rect(center=self.rect.center)

        if not self.rect.colliderect(screen_rect) or self.distance_blood > 250:
            self.kill()


def create_particles(position, surface):
    particle_count = 20
    numbers = range(-5, 5)
    for i in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), surface)


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, surface):
        super().__init__(walls)
        self.image = tile_images[surface]
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.hp = 50

    def update(self):
        box_box = pygame.sprite.spritecollide(self, walls, False)
        if box_box is not None:
            for i in box_box:
                i.correct_position(self)

    def correct_position(self, object):
        if pygame.sprite.collide_rect(self, object):
            dx = object.rect.centerx - self.rect.centerx
            dy = object.rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5
            min_distance = (self.rect.width / 2) + (object.rect.width / 2)
            if distance < min_distance:
                overlap = min_distance - distance
                normal_x = 0
                normal_y = 0
                if distance != 0:
                    normal_x = dx / distance
                    normal_y = dy / distance
                self.rect.x -= normal_x * overlap / 2
                if pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.x += normal_x * overlap / 2
                self.rect.y -= normal_y * overlap / 2
                if pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.y += normal_x * overlap / 2


class Iron_box(pygame.sprite.Sprite):
    def __init__(self, x, y, surface):
        super().__init__(iron_box)
        self.image = tile_images[surface]
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, surface):
        super().__init__(floor)
        self.image = tile_images[surface]
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('floor1.jpg'),
    'iron_box': load_image('iron_box.png')
}
tile_width = tile_height = 100


def tile(tile_type, pos_x, pos_y):
    if tile_type == 'wall':
        Grass(pos_x, pos_y, 'empty')
        Box(pos_x, pos_y, tile_type)
    elif tile_type == 'empty':
        Grass(pos_x, pos_y, tile_type)
    else:
        Iron_box(pos_x, pos_y, tile_type)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                tile('empty', x, y)
            elif level[y][x] == '#':
                tile('wall', x, y)
                walls.add()
            elif level[y][x] == '@':
                tile('empty', x, y)
                # new_player = Ball(20, 955, 150, 'first_player')
            elif level[y][x] == '^':
                tile('iron_box', x, y)
    return new_player, x, y


def end_game():
    button_width = 400
    button_height = 35

    start_button = pygame.Rect(1920 // 2 - button_width // 2, 400, button_width, button_height)
    exit_button = pygame.Rect(1920 // 2 - button_width // 2, 500, button_width, button_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    sound_button.play()
                    return
                elif exit_button.collidepoint(event.pos):
                    sound_button.play()
                    start_screen()
                    return

        draw_button(screen, start_button, (200, 0, 0), (255, 0, 0), "Начать заново", (0, 0, 0))
        draw_button(screen, exit_button, (200, 0, 0), (255, 0, 0), "Выход в главное меню", (0, 0, 0))

        pygame.display.flip()
        clock.tick(fps)


MAX_WEAPONS = 5
MAX_ARMOR = 5
count_weapon = 0
count_protection = 0
player, level_x, level_y = generate_level(load_level('map.txt'))

last_spawn_time_weapon = 0
spawn_interval_weapon = 4000

last_spawn_time_armor = 0
spawn_interval_armor = 3000

last_spawn_time_heart = 0
spawn_interval_heart = 2000

rad = 20
first_player = Player(rad, 960, 150, 'first_player')
second_player = Player(rad, 960, 930, 'second_player')
running = True
start_screen()
pygame.mixer.music.load('music\\music_game1.wav')
pygame.mixer.music.play(-1)

armor_pic = load_image('armor.jpg')
armor_pic = pygame.transform.scale(armor_pic, (50, 50))
health_pic = load_image('health.jpg')
health_pic = pygame.transform.scale(health_pic, (50, 50))
ammo_pic = load_image('ammo.jpg')
ammo_pic = pygame.transform.scale(ammo_pic, (50, 50))

victory = False
initial_key_bindings = load_settings()["key_bindings"]
while running:
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    if keys[initial_key_bindings['first_shoot']] and first_player.weapon:
        first_player.weapon.shoot()
    if keys[initial_key_bindings['second_shoot']] and second_player.weapon:
        second_player.weapon.shoot()
    if keys[pygame.K_ESCAPE]:
        settings()
        initial_key_bindings = load_settings()["key_bindings"]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == initial_key_bindings['first_action']:
                for weapon in weapons:
                    if pygame.sprite.collide_rect(first_player, weapon):
                        if first_player.weapon:
                            dropped_weapon = first_player.weapon
                            dropped_weapon.owner = None
                            dropped_weapon.rect.center = first_player.rect.center
                            weapons.add(dropped_weapon)
                            first_player.weapon = None
                        sound_change_weapon.play()
                        first_player.weapon = weapon
                        weapon.owner = first_player
                        weapons.remove(weapon)
                        break
                for armor in protection:
                    if pygame.sprite.collide_rect(first_player, armor):
                        if first_player.armor:
                            dropped_armor = first_player.armor
                            dropped_armor.owner = None
                            dropped_armor.rect.center = first_player.rect.center
                            protection.add(dropped_armor)
                            first_player.armor = None
                        sound_change_armor.play()
                        first_player.armor = armor
                        armor.owner = first_player
                        protection.remove(armor)
                        break
            if event.key == initial_key_bindings['second_action']:
                for weapon in weapons:
                    if pygame.sprite.collide_rect(second_player, weapon):
                        if second_player.weapon:
                            dropped_weapon = second_player.weapon
                            dropped_weapon.owner = None
                            dropped_weapon.rect.center = second_player.rect.center
                            weapons.add(dropped_weapon)
                            second_player.weapon = None
                        sound_change_weapon.play()
                        second_player.weapon = weapon
                        weapon.owner = second_player
                        weapons.remove(weapon)
                        break
                for armor in protection:
                    if pygame.sprite.collide_rect(second_player, armor):
                        if second_player.armor:
                            dropped_armor = second_player.armor
                            dropped_armor.owner = None
                            dropped_armor.rect.center = second_player.rect.center
                            protection.add(dropped_armor)
                            second_player.armor = None
                        sound_change_armor.play()
                        second_player.armor = armor
                        armor.owner = second_player
                        protection.remove(armor)
                        break
    if current_time - last_spawn_time_weapon >= spawn_interval_weapon:
        if count_weapon <= MAX_WEAPONS:
            choose = random.randint(0, 5)
            if choose == 0:
                new_weapon = Weapon('m41.jpg', None)
            elif choose == 1:
                new_weapon = Uzi('uzi2.jpg', None)
            elif choose == 2:
                new_weapon = Sniper_rifle('sniper_rifle.png', None)
            elif choose == 3:
                new_weapon = Pistol('pistol.jpg', None)
            else:
                new_weapon = Shotgun('shotgun.jpg', None)
            new_weapon.spawn_weapon()
            weapons.add(new_weapon)
            count_weapon += 1
            last_spawn_time_weapon = current_time
    if current_time - last_spawn_time_armor >= spawn_interval_armor:
        if count_protection <= MAX_ARMOR:
            choose = random.randint(0, 2)
            if choose == 1:
                new_armor = Middle_Armor('middle_armor.jpg', None)
            elif choose == 0:
                new_armor = Armor('light_armor.png', None)
            else:
                new_armor = Heavy_Armor('heavy_armor.png', None)
            new_armor.spawn_armor()
            protection.add(new_armor)
            count_protection += 1
            last_spawn_time_armor = current_time
    if current_time - last_spawn_time_heart >= spawn_interval_heart:
        new_heart = Heart('heart.jpg', None)
        new_heart.spawn_armor()
        health.add(new_heart)
        last_spawn_time_heart = current_time

    first_health = pygame.sprite.spritecollideany(first_player, health)
    if first_health is not None and first_player.hp < 1000:
        first_player.hp += first_health.hp if first_player.hp <= 1000 else 0
        sound_heal.play()
        first_health.kill()
    second_health = pygame.sprite.spritecollideany(second_player, health)
    if second_health is not None and second_player.hp < 1000:
        second_player.hp += second_health.hp
        sound_heal.play()
        second_health.kill()

    screen.fill("black")
    all_sprites.update(initial_key_bindings)
    box_first_player = pygame.sprite.spritecollide(first_player, walls, False)
    if box_first_player is not None:
        for i in box_first_player:
            i.correct_position(first_player)
    box_second_player = pygame.sprite.spritecollide(second_player, walls, False)
    if box_second_player is not None:
        for i in box_second_player:
            i.correct_position(second_player)
    walls.update()
    floor.draw(screen)
    iron_box.draw(screen)
    walls.draw(screen)
    health.draw(screen)
    all_sprites.draw(screen)
    protection.draw(screen)
    weapons.draw(screen)
    if first_player.armor:
        screen.blit(first_player.armor.image, first_player.armor.rect)
    if second_player.armor:
        screen.blit(second_player.armor.image, second_player.armor.rect)
    if first_player.weapon:
        screen.blit(first_player.weapon.image, first_player.weapon.rect)
    if second_player.weapon:
        screen.blit(second_player.weapon.image, second_player.weapon.rect)
    clock.tick(fps)
    hp_first = font.render(f'{first_player.hp if first_player.hp > 0 else 0}', True,
                           'red')
    hp_second = font.render(f'{second_player.hp if second_player.hp > 0 else 0}', True,
                            'red')
    armor_first = font.render(f'{first_player.armor.hp if first_player.armor else 0}', True,
                              'black')
    armor_second = font.render(f'{second_player.armor.hp if second_player.armor else 0}', True,
                               'black')
    ammo_first = font.render(f'{first_player.weapon.ammo if first_player.weapon else 0}', True,
                             'black')
    ammo_second = font.render(f'{second_player.weapon.ammo if second_player.weapon else 0}', True,
                              'black')

    screen.blit(health_pic, (45, 1000))  # картинки первого игрока
    screen.blit(armor_pic, (45, 1040))
    screen.blit(ammo_pic, (195, 1010))

    screen.blit(hp_first, (100, 1000))  # параметры первого игрока
    screen.blit(armor_first, (100, 1040))
    screen.blit(ammo_first, (250, 1020))

    screen.blit(health_pic, (1830, 1000))  # картинки второго игрока
    screen.blit(armor_pic, (1830, 1040))
    screen.blit(ammo_pic, (1680, 1010))

    screen.blit(hp_second, (1750, 1000))  # параметры первого игрока
    screen.blit(armor_second, (1750, 1040))
    screen.blit(ammo_second, (1630, 1020))
    if victory:
        end_game()
    pygame.display.flip()
pygame.quit()
