import pygame
import random

# Constants for easier adjustments
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 400
MOVEMENT_SPEED = 5
FONT_SIZE = 54

# Initialize pygame
pygame.init()

try:
    background_image = pygame.transform.scale(
        pygame.image.load("background.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
except FileNotFoundError:
    background_image = None

# Load font once at the beginning
font = pygame.font.SysFont("Times New Roman", FONT_SIZE)


class Sprite(pygame.sprite.Sprite): 
    def __init__(self, colour, height, width):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color('dodgerblue'))  # background color of the sprite
        pygame.draw.rect(self.image, colour, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

    def move(self, x_change, y_change):
        # Fixed boundary clamping logic
        self.rect.x = max(0, min(self.rect.x + x_change, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + y_change, SCREEN_HEIGHT - self.rect.height))


# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pet Food Collection Game")
all_sprites = pygame.sprite.Group()

# Create Pet Sprite
pet = Sprite(pygame.Color('black'), 30, 30)
pet.rect.x = random.randint(0, SCREEN_WIDTH - pet.rect.width)
pet.rect.y = random.randint(0, SCREEN_HEIGHT - pet.rect.height)
all_sprites.add(pet)

# Create multiple Food Sprites
food_list = []
for _ in range(5):  # Spawns 5 food items
    food = Sprite(pygame.Color('orange'), 20, 20)
    food.rect.x = random.randint(0, SCREEN_WIDTH - food.rect.width)
    food.rect.y = random.randint(0, SCREEN_HEIGHT - food.rect.height)
    all_sprites.add(food)
    food_list.append(food)

# Game loop control variables
running, won = True, False
clock = pygame.time.Clock()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            running = False

    if not won:
        keys = pygame.key.get_pressed()
        x_change = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * MOVEMENT_SPEED
        y_change = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * MOVEMENT_SPEED
        pet.move(x_change, y_change)

        # Check for collisions with food items
        for food in food_list[:]:
            if pet.rect.colliderect(food.rect):
                all_sprites.remove(food)
                food_list.remove(food)

        # Win condition when all food is collected
        if len(food_list) == 0:
            won = True

    # Drawing
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(pygame.Color('lightgreen'))

    all_sprites.draw(screen)

    # Display completion message
    if won:
        win_text = font.render("All Food Collected!", True, pygame.Color('black'))
        screen.blit(win_text, ((SCREEN_WIDTH - win_text.get_width()) // 2,
                                 (SCREEN_HEIGHT - win_text.get_height()) // 2))

    pygame.display.flip()
    clock.tick(90)


pygame.quit()