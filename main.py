import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 1280))
clock = pygame.time.Clock()
running = True

player_dimensions = (10, 20)
player_velocity = 8  # pixels per frame
player_color = "white"
# y = 0 is at the top of the screen, and y increases as you go down the screen. x = 0 is at the left of the screen, and x increases as you go right on the screen.
# The player should not go above the lower third of the screen
# The player should not go below the bottom of the screen
player_y_min = screen.get_height() - screen.get_height() / 3
player_y_max = screen.get_height() - player_dimensions[1]
player_x_min = 0
player_x_max = screen.get_width() - player_dimensions[0]

player_pos = pygame.Vector2(screen.get_width() / 2,
                            # Start the player at the bottom center of the screen
                            screen.get_height() - player_dimensions[1])

bullets = []
bullet_dimensions = (3, 10)  # width and height of the bullet
bullet_velocity = 5  # pixels per frame
bullet_color = "yellow"


class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.dimensions = (10, 10)
        self.velocity = player_velocity * 0.25  # pixels per frame
        self.color = "purple"
        self.is_diving = False  # Flag to indicate if the enemy is diving

    def update(self):
        if self.is_diving:
            self.pos.y += self.velocity  # Move the enemy downwards


enemies = []

# Create grid of enemies
enemy_rows = 5
enemy_cols = 35
enemy_spacing_x = 30
enemy_spacing_y = 20
for row in range(enemy_rows):
    for col in range(enemy_cols):
        enemy_x = col * enemy_spacing_x + 100  # Start at x=100 to avoid the left edge
        enemy_y = row * enemy_spacing_y + 50   # Start at y=50 to avoid the top edge
        enemies.append(Enemy(enemy_x, enemy_y))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

     # Shoot a bullet when the spacebar is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet_pos = pygame.Vector2(player_pos.x + player_dimensions[0] / 2,
                                        player_pos.y)  # Start the bullet at the center of the player
            bullets.append(bullet_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= player_velocity
    if keys[pygame.K_RIGHT]:
        player_pos.x += player_velocity
    if keys[pygame.K_UP]:
        player_pos.y -= player_velocity
    if keys[pygame.K_DOWN]:
        player_pos.y += player_velocity

    # Keep the player within the screen boundaries
    # Clamped y-coordinates
    player_pos.y = max(player_y_min, min(player_pos.y, player_y_max))

    # Wrapped x-coordinates
    if player_pos.x < player_x_min:
        player_pos.x = player_x_max
    if player_pos.x > player_x_max:
        player_pos.x = 0

    # Bullet coordinates update
    for bullet in bullets:
        bullet.y -= bullet_velocity  # Move the bullet upwards

    # Update enemy positions
    for enemy in enemies:
        if random.random() < 0.0001:  # Random chance for an enemy to start diving
            enemy.is_diving = True
        enemy.update()

      # Collision detection between bullets and enemies using pygame Rect
    bullets_to_remove = []
    enemies_to_remove = []
    for bullet in bullets:
        bullet_rect = pygame.Rect(
            bullet.x, bullet.y, bullet_dimensions[0], bullet_dimensions[1])
        for enemy in enemies:
            enemy_rect = pygame.Rect(
                enemy.pos.x, enemy.pos.y, enemy.dimensions[0], enemy.dimensions[1])
            if bullet_rect.colliderect(enemy_rect):
                bullets_to_remove.append(bullet)
                enemies_to_remove.append(enemy)
                break  # Bullet can only hit one enemy
      # Remove collided bullets and enemies
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)
    for enemy in enemies_to_remove:
        if enemy in enemies:
            enemies.remove(enemy)

    # Remove bullets that have gone off the top of the screen
    bullets = [bullet for bullet in bullets if bullet.y +
               bullet_dimensions[1] > 0]

    # Remove enemies that have gone off the bottom of the screen
    enemies = [enemy for enemy in enemies if enemy.pos.y <
               screen.get_height() + enemy.dimensions[1]]

    screen.fill("black")

    # Draw the player as a rectangle (x, y, width, height)
    pygame.draw.rect(screen, player_color, (player_pos.x,
                     player_pos.y, player_dimensions[0], player_dimensions[1]))

    # Draw the enemies as rectangles (x, y, width, height)
    for enemy in enemies:
        pygame.draw.rect(screen, enemy.color, (enemy.pos.x,
                         enemy.pos.y, enemy.dimensions[0], enemy.dimensions[1]))

    # Draw the bullets as rectangles (x, y, width, height)
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet.x,
                         bullet.y, bullet_dimensions[0], bullet_dimensions[1]))

    pygame.display.flip()

    clock.tick(80)  # Limit the frame rate to 80 frames per second


pygame.quit()
