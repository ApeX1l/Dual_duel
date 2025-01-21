import os
import random
import sys
import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
    def __init__(self, pos, player, key):
        super().__init__(all_sprites)
        self.image = pygame.Surface([10, 10])
        self.image.fill('black')
        self.rect = self.image.get_rect()
        self.v = 500
        if key == 'w':
            self.rect.x = pos[0] + 15
            self.rect.y = pos[1] - 10
            self.direction = 'w'
        elif key == 'a':
            self.rect.x = pos[0] - 10
            self.rect.y = pos[1] + 15
            self.direction = 'a'
        elif key == 's':
            self.rect.x = pos[0] + 15
            self.rect.y = pos[1] + 40
            self.direction = 's'
        elif key == 'd':
            self.rect.x = pos[0] + 40
            self.rect.y = pos[1] + 15
            self.direction = 'd'
        if key == 'up':
            self.rect.x = pos[0] + 15
            self.rect.y = pos[1] - 10
            self.direction = 'up'
        elif key == 'left':
            self.rect.x = pos[0] - 10
            self.rect.y = pos[1] + 15
            self.direction = 'left'
        elif key == 'down':
            self.rect.x = pos[0] + 15
            self.rect.y = pos[1] + 40
            self.direction = 'down'
        elif key == 'right':
            self.rect.x = pos[0] + 40
            self.rect.y = pos[1] + 15
            self.direction = 'right'

    def update(self, *args):
        if self.direction == 's':
            self.rect.y += self.v / fps
        elif self.direction == 'w':
            self.rect.y -= self.v / fps
        elif self.direction == 'a':
            self.rect.x -= self.v / fps
        elif self.direction == 'd':
            self.rect.x += self.v / fps
        if self.direction == 'down':
            self.rect.y += self.v / fps
        elif self.direction == 'up':
            self.rect.y -= self.v / fps
        elif self.direction == 'left':
            self.rect.x -= self.v / fps
        elif self.direction == 'right':
            self.rect.x += self.v / fps
        if pygame.sprite.collide_rect(self, second_player):
            second_player.hp -= 25
            create_particles((second_player.rect.x + 20, second_player.rect.y + 20))
            self.kill()
        if pygame.sprite.collide_rect(self, first_player):
            first_player.hp -= 25
            create_particles((first_player.rect.x + 20, first_player.rect.y + 20))
            self.kill()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, color):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color(color),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.hp = 100
        self.last_button = 's' if color == 'red' else 'up'
        self.v = 300

    def update(self, keys):
        if self == first_player:
            if keys[pygame.K_w]:
                self.rect.y -= self.v / fps
                self.last_button = 'w'
            if keys[pygame.K_s]:
                self.rect.y += self.v / fps
                self.last_button = 's'
            if keys[pygame.K_a]:
                self.rect.x -= self.v / fps
                self.last_button = 'a'
            if keys[pygame.K_d]:
                self.rect.x += self.v / fps
                self.last_button = 'd'
        else:
            if keys[pygame.K_UP]:
                self.rect.y -= self.v / fps
                self.last_button = 'up'
            if keys[pygame.K_DOWN]:
                self.rect.y += self.v / fps
                self.last_button = 'down'
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.v / fps
                self.last_button = 'left'
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.v / fps
                self.last_button = 'right'
        if self.hp <= 0:
            self.rect.x = - 300  # костыль self.kill()

    def correct_position(self, other_ball):
        if pygame.sprite.collide_circle(self, other_ball):
            dx = other_ball.rect.centerx - self.rect.centerx
            dy = other_ball.rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5
            min_distance = self.radius + other_ball.radius
            if distance < min_distance:
                overlap = min_distance - distance
                normal_x = 0
                normal_y = 0
                if distance != 0:
                    normal_x = dx / distance
                    normal_y = dy / distance
                self.rect.x -= normal_x * overlap / 2
                self.rect.y -= normal_y * overlap / 2


screen_rect = (0, 0, width, height)


# GRAVITY = 1


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
first_player = Ball(rad, 250, 50, 'red')
second_player = Ball(rad, 250, 450, 'blue')
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Bullet(first_player.rect, 1, first_player.last_button)
            if event.key == pygame.K_KP0:
                Bullet(second_player.rect, 2, second_player.last_button)
    screen.fill("white")
    keys = pygame.key.get_pressed()
    all_sprites.update(keys)

    # отталкивание
    first_player.correct_position(second_player)
    second_player.correct_position(first_player)

    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
