import math
import os
import random
import sys
import pygame

with open('settings', 'w') as f:
    f.write('1 1' + '\n')
    f.write('w a s d e space' + '\n')
    f.write('up left down right num0 rctrl')
pygame.init()
fps = 60
clock = pygame.time.Clock()
size = width, height = 1920, 1080
button_width, button_height = 200, 50
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
weapons = pygame.sprite.Group()
protection = pygame.sprite.Group()
walls = pygame.sprite.Group()
iron_box = pygame.sprite.Group()
floor = pygame.sprite.Group()
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
screen_rect = (0, 0, width, height)

sound_walking_iron = pygame.mixer.Sound('sounds\\walking_on_iron.wav')
sound_button = pygame.mixer.Sound('sounds\\button_sound.wav')

sound_shoot = pygame.mixer.Sound('sounds\\shot_m4.wav')
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
              sound_injury1, sound_injury2, sound_injury3, sound_injury4, sound_death, sound_button]


def load_image(name, path='data', colorkey=None):
    fullname = os.path.join(path, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


font = pygame.font.Font(None, 50)
font_side = pygame.font.Font(None, 52)


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

    # Рисуем слайдер
    pygame.draw.rect(surface, slider_color, rect, border_radius=10)

    # Положение ползунка
    indicator_x = rect.x + int(value * rect.width)
    indicator_y = rect.centery

    pygame.draw.line(surface, 'black', (1920 // 2 - 100, 295 + button_height // 2),
                     (1920 // 2 + 100, 295 + button_height // 2), 3)  # sound
    pygame.draw.line(surface, 'black', (1920 // 2 - 100, 395 + button_height // 2),
                     (1920 // 2 + 100, 395 + button_height // 2), 3)
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


def settings():
    slider_sound = pygame.Rect(1920 // 2 - 100, 295, button_width, button_height)
    slider_music = pygame.Rect(1920 // 2 - 100, 395, button_width, button_height)
    button_back = pygame.Rect(1920 // 2 - 50, 900, button_width, button_height)

    button_first_forward = pygame.Rect(1920 // 2 - 275, 575, button_width * 1.5, button_height * 0.6)
    button_first_left = pygame.Rect(1920 // 2 - 275, 625, button_width * 1.5, button_height * 0.6)
    button_first_back = pygame.Rect(1920 // 2 - 275, 675, button_width * 1.5, button_height * 0.6)
    button_first_right = pygame.Rect(1920 // 2 - 275, 725, button_width * 1.5, button_height * 0.6)
    button_first_action = pygame.Rect(1920 // 2 - 275, 775, button_width * 1.5, button_height * 0.6)
    button_first_shoot = pygame.Rect(1920 // 2 - 275, 825, button_width * 1.5, button_height * 0.6)

    button_second_forward = pygame.Rect(1920 // 2 + 50, 575, button_width * 1.5, button_height * 0.6)
    button_second_left = pygame.Rect(1920 // 2 + 50, 625, button_width * 1.5, button_height * 0.6)
    button_second_back = pygame.Rect(1920 // 2 + 50, 675, button_width * 1.5, button_height * 0.6)
    button_second_right = pygame.Rect(1920 // 2 + 50, 725, button_width * 1.5, button_height * 0.6)
    button_second_action = pygame.Rect(1920 // 2 + 50, 775, button_width * 1.5, button_height * 0.6)
    button_second_shoot = pygame.Rect(1920 // 2 + 50, 825, button_width * 1.5, button_height * 0.6)

    music_value = 1
    sound_value = 1
    music_dragging = False
    sound_dragging = False
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
                elif button_back.collidepoint(event.pos):
                    sound_button.play()
                    return
            elif event.type == pygame.MOUSEBUTTONUP:
                music_dragging = False
                sound_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if music_dragging:
                    music_value = (event.pos[0] - slider_music.x) / slider_music.width
                    music_value = max(0, min(1, music_value))
                    pygame.mixer.music.set_volume(music_value)
                elif sound_dragging:
                    sound_value = (event.pos[0] - slider_music.x) / slider_music.width
                    sound_value = max(0, min(1, sound_value))
                    for sound in all_sounds:
                        sound.set_volume(sound_value)
        fon = pygame.transform.scale(load_image('main_menu_pic.jpg'), (1920, 1080))
        screen.blit(fon, (0, 0))

        draw_slider(screen, slider_sound, (200, 0, 0), (255, 0, 0), sound_value, sound_dragging)
        draw_slider(screen, slider_music, (200, 0, 0), (255, 0, 0), music_value, music_dragging)

        draw_text('Звуки:', font, 'black', screen, 1920 // 2, 270)
        draw_text('Музыка:', font, 'black', screen, 1920 // 2, 370)

        draw_text('Управление', font, 'black', screen, 1920 // 2, 475, True)
        draw_text('Первый игрок', font, 'black', screen, 1920 // 2 - 125, 525, True)
        draw_text('Второй игрок', font, 'black', screen, 1920 // 2 + 175, 525, True)

        draw_button(screen, button_back, (200, 0, 0), (255, 0, 0), "Назад", (0, 0, 0))

        draw_button(screen, button_first_forward, (200, 0, 0), (255, 0, 0), "Вперед - W", (0, 0, 0))
        draw_button(screen, button_first_left, (200, 0, 0), (255, 0, 0), "Налево - A", (0, 0, 0))
        draw_button(screen, button_first_back, (200, 0, 0), (255, 0, 0), "Назад - S", (0, 0, 0))
        draw_button(screen, button_first_right, (200, 0, 0), (255, 0, 0), "Направо - D", (0, 0, 0))
        draw_button(screen, button_first_action, (200, 0, 0), (255, 0, 0), "Действие - E", (0, 0, 0))
        draw_button(screen, button_first_shoot, (200, 0, 0), (255, 0, 0), "Стрельба- SPACE", (0, 0, 0))

        draw_button(screen, button_second_forward, (200, 0, 0), (255, 0, 0), "Вперед - стр.вврх", (0, 0, 0))
        draw_button(screen, button_second_left, (200, 0, 0), (255, 0, 0), "Налево - стр.влево", (0, 0, 0))
        draw_button(screen, button_second_back, (200, 0, 0), (255, 0, 0), "Назад - стр.вниз", (0, 0, 0))
        draw_button(screen, button_second_right, (200, 0, 0), (255, 0, 0), "Направо - стр.впр", (0, 0, 0))
        draw_button(screen, button_second_action, (200, 0, 0), (255, 0, 0), "Действие - NUM0", (0, 0, 0))
        draw_button(screen, button_second_shoot, (200, 0, 0), (255, 0, 0), "Стрельба- RCTRL", (0, 0, 0))
        pygame.display.flip()


class Bullet(pygame.sprite.Sprite):
    image = load_image("bullet.png", colorkey=-1)
    image = pygame.transform.scale(image, (50, 50))

    def __init__(self, pos, target_pos, owner):
        super().__init__(all_sprites)
        self.image = Bullet.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.owner = owner
        self.v = 1000
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            self.velocity = [0, 0]
        else:
            angle_deviation = random.uniform(-0.1, 0.1)
            self.velocity = [
                (dx / distance) * self.v / fps + dy / distance * angle_deviation * self.v / fps,
                (dy / distance) * self.v / fps - dx / distance * angle_deviation * self.v / fps
            ]
            angle = math.degrees(math.atan2(dy, dx))
            self.image = pygame.transform.rotate(Bullet.image, -angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, *args):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        box = pygame.sprite.spritecollideany(self, walls)
        if box is not None:
            box.hp -= 10
            print(box.hp)
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
                                i.hp -= 25
                                create_particles((i.rect.centerx, i.rect.centery), i)
                                if i.hp > 0:
                                    random.choice(sound_injury).play()
                        self.kill()
                else:
                    if pygame.sprite.collide_mask(self, i.armor):
                        i.armor.hp -= 10
                        create_particles((i.rect.centerx, i.rect.centery), i.armor)
                        sound_shoot_armor.play()
                        self.kill()
                        break

        if not self.rect.colliderect(screen_rect):
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, player_folder):
        super().__init__(all_sprites, players)
        self.radius = radius
        self.last_step_time = 0
        self.player_folder = player_folder
        self.animations = {}
        self.load_animations()
        self.current_frame = 0
        self.animation_speed = 0.1
        self.current_animation = 'down'
        self.image = self.animations['down'][0]

        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 1000
        self.weapon = None
        self.armor = None
        self.v = 300

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

    def update(self, keys):
        flag = False
        current_time = pygame.time.get_ticks()
        if self == first_player:
            if keys[pygame.K_w]:
                self.rect.y -= self.v / fps
                self.current_animation = 'up'
                if pygame.sprite.collide_mask(self, second_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.y += self.v / fps
            elif keys[pygame.K_s]:
                self.rect.y += self.v / fps
                self.current_animation = 'down'
                if pygame.sprite.collide_mask(self, second_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.y -= self.v / fps
            elif keys[pygame.K_a]:
                self.rect.x -= self.v / fps
                self.current_animation = 'left'
                if pygame.sprite.collide_mask(self, second_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.x += self.v / fps
            elif keys[pygame.K_d]:
                self.rect.x += self.v / fps
                self.current_animation = 'right'
                if pygame.sprite.collide_mask(self, second_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.x -= self.v / fps
            else:
                flag = True
        else:
            if keys[pygame.K_UP]:
                self.rect.y -= self.v / fps
                self.current_animation = 'up'
                if pygame.sprite.collide_mask(self, first_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.y += self.v / fps
            elif keys[pygame.K_DOWN]:
                self.rect.y += self.v / fps
                self.current_animation = 'down'
                if pygame.sprite.collide_mask(self, first_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.y -= self.v / fps
            elif keys[pygame.K_LEFT]:
                self.rect.x -= self.v / fps
                self.current_animation = 'left'
                if pygame.sprite.collide_mask(self, first_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.x += self.v / fps
            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.v / fps
                self.current_animation = 'right'
                if pygame.sprite.collide_mask(self, first_player) or pygame.sprite.spritecollideany(self, iron_box):
                    self.rect.x -= self.v / fps
            else:
                flag = True
        if not flag and current_time - self.last_step_time > 500:  # 500 мс = 0.5 секунды
            sound_walking_iron.play()

            self.last_step_time = current_time
        if self.hp <= 0:
            self.weapon = None
            self.kill()
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
        self.offset = pygame.math.Vector2(-20, 15)
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


class Armor(pygame.sprite.Sprite):
    def __init__(self, armor_path, owner):
        super().__init__(protection)
        self.owner = owner

        self.image = load_image(armor_path, colorkey=-1)
        self.image = pygame.transform.scale(self.image, (100, 50))

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


class Middle_Armor(Armor):
    def __init__(self, armor_path, owner):
        super().__init__(armor_path, owner)
        self.hp = 200
        # self.image = load_image(armor_path, colorkey=-1)
        # self.image = pygame.transform.scale(self.image, (100, 100))


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
                self.rect.y -= normal_y * overlap / 2


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
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
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
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


f1 = pygame.font.Font(None, 58)

MAX_WEAPONS = 5
MAX_ARMOR = 3
player, level_x, level_y = generate_level(load_level('map.txt'))

last_spawn_time = 0
spawn_interval = 1000
rad = 20
first_player = Player(rad, 960, 150, 'first_player')
second_player = Player(rad, 960, 930, 'first_player')
running = True
start_screen()
while running:
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and first_player.weapon:
        first_player.weapon.shoot()
    if keys[pygame.K_KP0] and second_player.weapon:
        second_player.weapon.shoot()
    if keys[pygame.K_ESCAPE]:
        settings()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
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
            if event.key == pygame.K_RCTRL:
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
    if current_time - last_spawn_time >= spawn_interval:
        if len(weapons) <= MAX_WEAPONS:  # MAX_WEAPONS — максимальное количество оружияd
            new_weapon = Weapon('m41.jpg', None)
            new_weapon.spawn_weapon()
            weapons.add(new_weapon)
            last_spawn_time = current_time
        if len(protection) <= MAX_ARMOR:
            new_armor = Armor('armor_first.jpg', None)
            middle_armor = Middle_Armor('middle_armor.jpg', None)
            new_armor.spawn_armor()
            middle_armor.spawn_armor()
            protection.add(new_armor)
            protection.add(middle_armor)
            last_spawn_time = current_time

    screen.fill("black")
    all_sprites.update(keys)
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
    hp_first = f1.render(f'ЗДОРОВЬЕ:{first_player.hp}', True,
                         'red')
    hp_second = f1.render(f'ЗДОРОВЬЕ:{second_player.hp}', True,
                          'red')
    armor_first = f1.render(f'БРОНЯ:{first_player.armor.hp if first_player.armor else 0}', True,
                            'black')
    armor_second = f1.render(f'БРОНЯ:{second_player.armor.hp if second_player.armor else 0}', True,
                             'black')
    ammo_first = f1.render(f'ПАТРОНЫ:{first_player.weapon.ammo if first_player.weapon else 0}', True,
                           'black')
    ammo_second = f1.render(f'ПАТРОНЫ:{second_player.weapon.ammo if second_player.weapon else 0}', True,
                            'black')
    screen.blit(hp_first, (10, 1000))
    screen.blit(armor_first, (10, 1040))
    screen.blit(ammo_first, (350, 1020))

    screen.blit(hp_second, (1340, 1000))
    screen.blit(armor_second, (1340, 1040))
    screen.blit(ammo_second, (1680, 1020))
    pygame.display.flip()
pygame.quit()
