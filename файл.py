import pygame 
from os import listdir
from os.path import isfile, join

pygame.init()
# okno
screen_W, screen_H = 900, 700
background = pygame.transform.scale(pygame.image.load('Background.png'), (screen_W, screen_H))
screen = pygame.display.set_mode((screen_W, screen_H))
pygame.display.set_caption('Платформер')

# таймер
clock = pygame.time.Clock()
FPS = 60

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir, width, height, direction=False):
    path = join("assets", dir)
    images = [f for f in listdir(path) if isfile(join(path, f))] 

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites 
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites 
# классы
class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_sprite_sheets("character", 32, 32, True)

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))

        self.x_vel = 5
        self.y_vel = 0
        self.fall_count = 0
        self.direction = "right" 

    def move(self, dx, dy):
        self.x_vel += dx
        self.y_vel += dy

    def move(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
            
    def hotkeys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.x_vel
        if keys[pygame.K_d] and self.rect.x < screen_W - 50:
            self.rect.x += self.x_vel

        #гравитация
        self.y_vel += min(1, (self.fall_count / FPS) * self.GRAVITY)
        self.rect.y += self.y_vel
        self.fall_count += 1

    def draw(self):
        self.sprite = self.SPRITES["idle_" + self.direction][0]
        screen.blit(self.sprite, (self.rect.x, self.rect.y))


# игровые обьекты
player = Player(100, 100, 50, 50)
# Игровой цикл
run_game = True
while run_game:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
    player.move()
    # отрисовка
    player.draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()