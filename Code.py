import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
FPS = 60
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def draw_shape(shape, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, WHITE, (x + j * BLOCK_SIZE, y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(shape, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                if x + j < 0 or x + j >= WIDTH // BLOCK_SIZE or y + i >= HEIGHT // BLOCK_SIZE or board[y + i][x + j]:
                    return True
    return False

def merge_shape(shape, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                board[y + i][x + j] = 1

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

def clear_lines():
    lines_to_clear = [i for i, row in enumerate(board) if all(row)]
    for line in lines_to_clear:
        del board[line]
        board.insert(0, [0] * (WIDTH // BLOCK_SIZE))
    return len(lines_to_clear)

def draw_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# Initialize game variables
current_shape = random.choice(SHAPES)
current_shape_x = WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2
current_shape_y = 0
board = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
score = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(current_shape, current_shape_x - 1, current_shape_y):
                    current_shape_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(current_shape, current_shape_x + 1, current_shape_y):
                    current_shape_x += 1
            elif event.key == pygame.K_DOWN:
                if not check_collision(current_shape, current_shape_x, current_shape_y + 1):
                    current_shape_y += 1
            elif event.key == pygame.K_UP:
                rotated_shape = rotate_shape(current_shape)
                if not check_collision(rotated_shape, current_shape_x, current_shape_y):
                    current_shape = rotated_shape

    # Move the shape down
    if not check_collision(current_shape, current_shape_x, current_shape_y + 1):
        current_shape_y += 1
    else:
        merge_shape(current_shape, current_shape_x, current_shape_y)
        lines_cleared = clear_lines()
        score += lines_cleared
        current_shape = random.choice(SHAPES)
        current_shape_x = WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2
        current_shape_y = 0

    # Draw background
    screen.fill(BLACK)
    draw_grid()

    # Draw the current shape
    draw_shape(current_shape, current_shape_x * BLOCK_SIZE, current_shape_y * BLOCK_SIZE)

    # Draw the merged shapes on the board
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, WHITE, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Draw the score
    draw_score(score)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
