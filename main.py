import os
import random
import sys
import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


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
    image_right = pygame.transform.scale(image, (25, 25))
    image_left = pygame.transform.rotate(image_right, 180)
    image_down = pygame.transform.rotate(image_right, -90)
    image_up = pygame.transform.rotate(image_right, 90)

    def __init__(self, pos, key):
        super().__init__(all_sprites)
        if key == 'w' or key == 'up':
            self.image = Bullet.image_up
        elif key == 'a' or key == 'left':
            self.image = Bullet.image_left
        elif key == 's' or key == 'down':
            self.image = Bullet.image_down
        elif key == 'd' or key == 'right':
            self.image = Bullet.image_right
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.v = 1000
        if key == 'w':
            self.rect.x = pos[0] + 15
            self.rect.y = pos[1] - 20
            self.direction = 'w'
        elif key == 'a':
            self.rect.x = pos[0] - 10
            self.rect.y = pos[1] + 15
            self.direction = 'a'
        elif key == 's':
            self.rect.x = pos[0] + 25
            self.rect.y = pos[1] + 85
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
        if pygame.sprite.collide_mask(self, second_player):
            second_player.hp -= 25
            create_particles((second_player.rect.x + 20, second_player.rect.y + 20))
            self.kill()
        if pygame.sprite.collide_mask(self, first_player):
            first_player.hp -= 25
            create_particles((first_player.rect.x + 20, first_player.rect.y + 20))
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
        self.hp = 100
        self.last_button = 's' if color == 'red' else 'up'
        self.v = 300

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
                self.last_button = 'w'
                self.current_animation = 'up'
            elif keys[pygame.K_s]:
                self.rect.y += self.v / fps
                self.last_button = 's'
                self.current_animation = 'down'
            elif keys[pygame.K_a]:
                self.rect.x -= self.v / fps
                self.last_button = 'a'
                self.current_animation = 'left'
            elif keys[pygame.K_d]:
                self.rect.x += self.v / fps
                self.last_button = 'd'
                self.current_animation = 'right'
            else:
                flag = True
        else:
            if keys[pygame.K_UP]:
                self.rect.y -= self.v / fps
                self.last_button = 'up'
                self.current_animation = 'up'
            elif keys[pygame.K_DOWN]:
                self.rect.y += self.v / fps
                self.last_button = 'down'
                self.current_animation = 'down'
            elif keys[pygame.K_LEFT]:
                self.rect.x -= self.v / fps
                self.last_button = 'left'
                self.current_animation = 'left'
            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.v / fps
                self.last_button = 'right'
                self.current_animation = 'right'
            else:
                flag = True
        if self.hp <= 0:
            self.rect.x = -300  # Костыль
        if not flag:
            self.animate()  # Вызов функции анимации
        else:
            self.image = self.animations['down'][0]

    def animate(self):
        # Выбор текущей анимации
        animation = self.animations.get(self.current_animation, self.animations[
            'down'])  # если нету в словаре, то анимация по умолчанию
        if animation:
            # Обновление кадра анимации
            self.current_frame = (self.current_frame + self.animation_speed) % len(
                animation)  # % len(animation) позволяет зациклить анимацию
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


screen_rect = (0, 0, width, height)


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
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Bullet(first_player.rect, first_player.last_button)
            if event.key == pygame.K_KP0:
                Bullet(second_player.rect, second_player.last_button)
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
