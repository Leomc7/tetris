import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
COLORS = [
    (0, 255, 255),  # Cyan (I)
    (255, 255, 0),  # Yellow (O)
    (255, 165, 0),  # Orange (L)
    (0, 0, 255),    # Blue (J)
    (0, 255, 0),    # Green (S)
    (255, 0, 0),    # Red (Z)
    (128, 0, 128)   # Purple (T)
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 0], [1, 1, 1]]   # T
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def reset_game():
    """Reset the game state."""
    grid = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    tetromino = Tetromino(random.choice(SHAPES))
    next_tetromino = Tetromino(random.choice(SHAPES))
    score = 0
    fall_time = 0
    return grid, tetromino, next_tetromino, score, fall_time

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

def draw_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_tetromino(tetromino, ghost=False):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                if ghost:
                    # Make the ghost piece a lighter shade of the tetromino's color
                    ghost_color = tuple(min(c + 100, 255) for c in tetromino.color)
                    pygame.draw.rect(screen, ghost_color, ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(screen, tetromino.color, ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_ghost(tetromino, grid):
    ghost = Tetromino(tetromino.shape)
    ghost.color = tetromino.color
    ghost.x = tetromino.x
    ghost.y = tetromino.y
    while not check_collision(ghost, grid):
        ghost.y += 1
    ghost.y -= 1
    draw_tetromino(ghost, ghost=True)

def check_collision(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (tetromino.y + y >= len(grid) or  # Bottom boundary
                    tetromino.x + x < 0 or          # Left boundary
                    tetromino.x + x >= len(grid[0]) or  # Right boundary
                    grid[tetromino.y + y][tetromino.x + x]):  # Collision with other blocks
                    return True
    return False

def merge_tetromino(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_lines(grid):
    lines_cleared = 0
    for y in range(len(grid)):
        if all(grid[y]):  # Check if the row is fully filled
            del grid[y]  # Remove the row
            grid.insert(0, [0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])  # Add a new empty row at the top
            lines_cleared += 1
    return lines_cleared

def draw_score(score, high_score):
    font = pygame.font.SysFont("comicsans", 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

def game_over(score, high_score):
    font = pygame.font.SysFont("comicsans", 50)
    small_font = pygame.font.SysFont("comicsans", 30)
    text = font.render("Game Over!", True, WHITE)
    restart_text = small_font.render("Press R to Restart", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, high_score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True, high_score

def pause():
    font = pygame.font.SysFont("comicsans", 50)
    text = font.render("Paused", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True

def main():
    grid, tetromino, next_tetromino, score, fall_time = reset_game()
    high_score = 0
    paused = False

    running = True
    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetromino.move_left()
                    if check_collision(tetromino, grid):
                        tetromino.move_right()  # Undo move if collision
                if event.key == pygame.K_RIGHT:
                    tetromino.move_right()
                    if check_collision(tetromino, grid):
                        tetromino.move_left()  # Undo move if collision
                if event.key == pygame.K_DOWN:
                    tetromino.move_down()
                    if check_collision(tetromino, grid):
                        tetromino.y -= 1  # Move back up if collision
                if event.key == pygame.K_UP:
                    old_shape = tetromino.shape
                    tetromino.rotate()
                    if check_collision(tetromino, grid):
                        tetromino.shape = old_shape  # Revert rotation if collision
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        if not pause():
                            running = False

        if not paused:
            if fall_time >= 500:  # Fall speed in milliseconds
                tetromino.move_down()
                if check_collision(tetromino, grid):
                    tetromino.y -= 1  # Move back up if collision
                    merge_tetromino(tetromino, grid)  # Merge the tetromino into the grid
                    lines_cleared = clear_lines(grid)  # Clear completed lines
                    score += lines_cleared * 100  # Update score
                    high_score = max(score, high_score)  # Update high score
                    tetromino = next_tetromino  # Spawn a new tetromino
                    next_tetromino = Tetromino(random.choice(SHAPES))
                    if check_collision(tetromino, grid):  # Check if the new tetromino collides immediately
                        restart, high_score = game_over(score, high_score)  # Show game over screen
                        if restart:  # Restart the game if the player presses R
                            grid, tetromino, next_tetromino, score, fall_time = reset_game()
                        else:
                            running = False
                fall_time = 0

        draw_grid(grid)
        draw_ghost(tetromino, grid)  # Draw the ghost piece
        draw_tetromino(tetromino)
        draw_score(score, high_score)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()