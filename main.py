import math
import os
import random
import sys
import pygame
import time

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
screen_rect = (0, 0, width, height)


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


class Bullet(pygame.sprite.Sprite):
    image = load_image("bullet.png", colorkey=-1)
    image = pygame.transform.scale(image, (50, 50))

    def __init__(self, pos, target_pos):
        super().__init__(all_sprites)
        self.image = Bullet.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.v = 1000
        self.rect.y += 100
        # Вычисляем вектор направления
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            self.velocity = [0, 0]
        else:
            # Нормализуем вектор и добавляем небольшое отклонение
            angle_deviation = random.uniform(-0.1, 0.1)  # Случайное отклонение
            self.velocity = [
                (dx / distance) * self.v / fps + dy / distance * angle_deviation * self.v / fps,
                (dy / distance) * self.v / fps - dx / distance * angle_deviation * self.v / fps
            ]
            # Вычисляем угол поворота
            angle = math.degrees(math.atan2(dy, dx))
            self.image = pygame.transform.rotate(Bullet.image, -angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, *args):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if pygame.sprite.collide_mask(self, second_player):
            second_player.hp -= 25
            create_particles((second_player.rect.centerx, second_player.rect.centery))
            self.kill()
        if pygame.sprite.collide_mask(self, first_player):
            first_player.hp -= 25
            create_particles((first_player.rect.centerx, first_player.rect.centery))
            self.kill()
        if not self.rect.colliderect(screen_rect):
            self.kill()



class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, color, player_folder):
        super().__init__(all_sprites)
        self.radius = radius
        self.color = color
        self.player_folder = player_folder  # Папка с ресурсами игрока
        self.animations = {}  # Словарь для анимаций
        self.load_animations()
        self.current_frame = 0  # Текущий кадр анимации
        self.animation_speed = 0.1  # Скорость анимации(как часто кадр будет меняться)
        self.current_animation = 'down'  # Направление анимации по умолчанию
        self.image = self.animations['down'][0]  # Начальное изображение
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 1000000
        self.weapon = None
        self.last_button = 's' if color == 'red' else 'up'
        self.v = 300

    def shoot(self, target):
        bullet = Bullet(self.rect.center, target.rect.center)
        return bullet

    def load_animations(self):
        # Загрузка анимаций из папок
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
        # Управление движением
        if self == first_player:
            if keys[pygame.K_w]:
                self.rect.y -= self.v / fps
                self.current_animation = 'up'
            elif keys[pygame.K_s]:
                self.rect.y += self.v / fps
                self.current_animation = 'down'
            elif keys[pygame.K_a]:
                self.rect.x -= self.v / fps
                self.current_animation = 'left'
            elif keys[pygame.K_d]:
                self.rect.x += self.v / fps
                self.current_animation = 'right'
            else:
                flag = True
        else:
            if keys[pygame.K_UP]:
                self.rect.y -= self.v / fps
                self.current_animation = 'up'
            elif keys[pygame.K_DOWN]:
                self.rect.y += self.v / fps
                self.current_animation = 'down'
            elif keys[pygame.K_LEFT]:
                self.rect.x -= self.v / fps
                self.current_animation = 'left'
            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.v / fps
                self.current_animation = 'right'
            else:
                flag = True

        if self.hp <= 0:
            self.rect.x = -300  # Костыль

        if not flag:
            self.animate()  # Вызов функции анимации
        else:
            self.image = self.animations['down'][0]

        if first_flag_weapon:
            first_player.weapon.update(second_player)
        if second_flag_weapon:
            second_player.weapon.update(first_player)

    def animate(self):
        # Выбор текущей анимации
        animation = self.animations.get(self.current_animation, self.animations[
            'down'])  # если нету в словаре, то анимация по умолчанию
        if animation:
            # Обновление кадра анимации
            self.current_frame = (self.current_frame + self.animation_speed) % len(
                animation)  # позволяет зациклить анимацию
            self.image = animation[int(self.current_frame)]  # Выбор нужного кадра анимации

    def correct_position(self, other_ball):
        if pygame.sprite.collide_rect(self, other_ball):
            dx = other_ball.rect.centerx - self.rect.centerx
            dy = other_ball.rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5
            min_distance = (self.rect.width / 2) + (other_ball.rect.width / 2)
            if distance < min_distance:
                overlap = min_distance - distance
                normal_x = 0
                normal_y = 0
                if distance != 0:
                    normal_x = dx / distance
                    normal_y = dy / distance
                self.rect.x -= normal_x * overlap / 2
                self.rect.y -= normal_y * overlap / 2


class Weapon(pygame.sprite.Sprite):
    def __init__(self, image_path, owner):
        super().__init__()
        self.owner = owner
        self.original_image = load_image(image_path, colorkey=-1)
        self.original_image = pygame.transform.scale(self.original_image, (77, 26))
        self.image = self.original_image
        self.offset = pygame.math.Vector2(-20, 25)
        self.rect = self.image.get_rect(center=owner.rect.center + self.offset)
        self.start_pos = self.rect.center
        self.flip_x = False
        self.angle_offset = 0

    def update(self, target):
        # Вычисляем вектор от центра персонажа к цели
        dx = target.rect.centerx - self.owner.rect.centerx
        dy = target.rect.centery - self.owner.rect.centery

        # Вычисляем угол поворота
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


class Particle(pygame.sprite.Sprite):
    # Сгенерируем частицы разного размера
    part = pygame.Surface([3, 3])
    part.fill('red')
    fire = [part]
    for scale in (3, 3):  # Увеличил размеры, чтобы было заметнее уменьшение
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)  # Перенёс вызов all_sprites в __init__
        self.original_images = self.fire  # Сохраняем оригинальные изображения
        self.image = random.choice(self.original_images)
        self.rect = self.image.get_rect(center=pos)  # Задаём позицию по центру

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]

        self.distance_blood = 0
        self.life_time = 150
        self.current_life = self.life_time

    def update(self, *keys):
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.distance_blood += abs(self.velocity[0]) + abs(self.velocity[1])

        # Уменьшение прозрачности
        self.current_life -= 1

        if self.current_life <= 0:
            self.kill()
        else:
            alpha = int(255 * (self.current_life / self.life_time))
            self.image.set_alpha(alpha)
            self.rect = self.image.get_rect(center=self.rect.center)

        if not self.rect.colliderect(screen_rect) or self.distance_blood > 250:
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 5)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


rad = 20
fps = 60
first_player = Ball(rad, 250, 50, 'red', 'first_player')
second_player = Ball(rad, 250, 450, 'blue', 'first_player')
running = True
first_flag_weapon = 0
second_flag_weapon = 0
clock = pygame.time.Clock()
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and first_flag_weapon:
        bullets.add(first_player.shoot(second_player))
    if keys[pygame.K_KP0] and second_flag_weapon:
        bullets.add(second_player.shoot(first_player))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                first_flag_weapon += 1 if first_flag_weapon == 0 else -1
                if first_flag_weapon:
                    first_player.weapon = Weapon('m41.jpg', first_player)
                else:
                    first_player.weapon = None
            if event.key == pygame.K_RCTRL:
                second_flag_weapon += 1 if second_flag_weapon == 0 else -1
                if second_flag_weapon:
                    second_player.weapon = Weapon('m41.jpg', second_player)
                else:
                    second_player.weapon = None

    screen.fill("black")
    all_sprites.update(keys)

    # отталкивание
    first_player.correct_position(second_player)
    second_player.correct_position(first_player)

    all_sprites.draw(screen)
    if first_flag_weapon:
        screen.blit(first_player.weapon.image, first_player.weapon.rect)
    if second_flag_weapon:
        screen.blit(second_player.weapon.image, second_player.weapon.rect)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
