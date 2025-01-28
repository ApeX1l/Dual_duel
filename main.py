import math
import os
import random
import sys
import pygame

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
weapons = pygame.sprite.Group()
protection = pygame.sprite.Group()
walls = pygame.sprite.Group()
players = pygame.sprite.Group()
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

    def __init__(self, pos, target_pos, owner, weapon):
        super().__init__(all_sprites)
        self.image = Bullet.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.owner = owner
        self.weapon = weapon
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

        for armor in protection:
            if pygame.sprite.collide_mask(self, armor):
                armor.hp -= 10
                create_particles((armor.rect.centerx, armor.rect.centery), armor)
                self.kill()
                break

        if any(pygame.sprite.collide_mask(self, sprite) for sprite in players if
               sprite != self and sprite != self.owner):
            for i in players:
                if i != self.owner:
                    i.hp -= 25
                    create_particles((i.rect.centerx, i.rect.centery), i)
            self.kill()
        if not self.rect.colliderect(screen_rect):
            self.kill()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, player_folder):
        super().__init__(all_sprites, players)
        self.radius = radius

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
        self.v = 300

    def shoot(self, target):
        bullet = Bullet(self.rect.center, target.rect.center, self)
        return bullet

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
        print(first_player.rect.x, first_player.rect.y)
        if self.hp <= 0:
            self.rect.x = -300

        if not flag:
            self.animate()
        else:
            self.image = self.animations['down'][0]

        if first_player.weapon:
            first_player.weapon.update(second_player)
        if second_player.weapon:
            second_player.weapon.update(first_player)

    def animate(self):
        animation = self.animations.get(self.current_animation, self.animations['down'])
        if animation:
            self.current_frame = (self.current_frame + self.animation_speed) % len(animation)
            self.image = animation[int(self.current_frame)]

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
    image = load_image('m41.jpg', colorkey=-1)

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
        self.start_pos = self.rect.center
        self.flip_x = False
        self.angle_offset = 0
        self.fire_timer = 0

    def spawn_weapon(self):
        while True:
            self.rect.x = random.randrange(195, 1645)
            self.rect.y = random.randrange(100, 870)
            if not any(pygame.sprite.collide_rect(self, sprite) for sprite in weapons if
                       sprite != self) and not pygame.sprite.spritecollideany(self, walls):
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

    def shoot(self, bullet_image):
        if self.fire_timer == 0 and self.ammo > 0:
            bullet_start_pos = self.get_barrel_position()
            target = second_player if self.owner == first_player else first_player
            bullet = Bullet(bullet_start_pos, target.rect.center, self.owner, self)
            bullets.add(bullet)
            self.fire_timer = 10
            self.ammo -= 1


class Armor(pygame.sprite.Sprite):
    image = load_image('armor_first.jpg', colorkey=-1)
    image = pygame.transform.scale(image, (100, 50))

    def __init__(self, owner):
        super().__init__(all_sprites, protection)
        self.image = Armor.image
        self.rect = self.image.get_rect()
        self.rect.center = owner.rect.center
        self.hp = 100
        self.owner = owner

    def update(self, *keys):
        self.rect.center = self.owner.rect.center
        if self.hp == 0:
            self.kill()


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


Wall(0, 0, width, 1)
Wall(0, 0, 1, height)
Wall(0, height - 1, width, 1)
Wall(width - 1, 0, 1, height)
last_spawn_time = 0
spawn_interval = 5000
rad = 20
fps = 60
first_player = Ball(rad, 955, 150, 'first_player')
second_player = Ball(rad, 955, 920, 'first_player')
first_armor = Armor(first_player)
running = True
clock = pygame.time.Clock()
while running:
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and first_player.weapon:
        first_player.weapon.shoot('png bullet')
    if keys[pygame.K_KP0] and second_player.weapon:
        second_player.weapon.shoot('png bullet')
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
                        first_player.weapon = weapon
                        weapon.owner = first_player
                        weapons.remove(weapon)
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
                        second_player.weapon = weapon
                        weapon.owner = second_player
                        weapons.remove(weapon)
                        break

    if current_time - last_spawn_time >= spawn_interval:
        new_weapon = Weapon("m41.jpg", owner=None)
        new_weapon.spawn_weapon()
        weapons.add(new_weapon)
        last_spawn_time = current_time

    screen.fill("black")
    all_sprites.update(keys)

    first_player.correct_position(second_player)
    second_player.correct_position(first_player)

    all_sprites.draw(screen)
    weapons.draw(screen)
    if first_player.weapon:
        screen.blit(first_player.weapon.image, first_player.weapon.rect)
    if second_player.weapon:
        screen.blit(second_player.weapon.image, second_player.weapon.rect)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
