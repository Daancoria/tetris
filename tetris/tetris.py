import pygame
import random
import time

# Game Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE, BLACK, GRAY, RED = (255, 255, 255), (0, 0, 0), (128, 128, 128), (255, 0, 0)
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
]

# Define a list of colors
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

def show_start_screen(screen, background, font_path):
    screen.blit(background, (0, 0))
    title_font = pygame.font.Font(font_path, 36)
    text = title_font.render("TETRIS", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(text, text_rect)
    text = pygame.font.Font(font_path, 14).render("Press SPACE to Start", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def show_pause_menu(screen, background, font_path):
    screen.blit(background, (0, 0))
    text = pygame.font.Font(font_path, 24).render("Paused", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text, text_rect)
    text = pygame.font.Font(font_path, 14).render("Press P to Resume", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

def show_game_over_screen(screen, score, font_path):
    screen.fill(BLACK)
    text = pygame.font.Font(font_path, 24).render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text, text_rect)
    text = pygame.font.Font(font_path, 14).render(f"Score: {score}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    text = pygame.font.Font(font_path, 14).render("Press R to Restart", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    screen.blit(text, text_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)  # Assign a random color
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move(self, dx, dy, board):
        new_x, new_y = self.x + dx, self.y + dy
        if not self.check_collision(new_x, new_y, board):
            self.x, self.y = new_x, new_y

    def rotate(self, board):
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
        if not self.check_collision(self.x, self.y, board, rotated_shape):
            self.shape = rotated_shape

    def check_collision(self, x, y, board, shape=None):
        shape = shape or self.shape
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                if cell:
                    new_x, new_y = x + col_index, y + row_index
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS or board[new_y][new_x][0]:
                        return True
        return False

def draw_grid(surface):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))

def draw_tetrimino(surface, tetrimino):
    for row_index, row in enumerate(tetrimino.shape):
        for col_index, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (tetrimino.x + col_index) * GRID_SIZE,
                    (tetrimino.y + row_index) * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE
                )
                pygame.draw.rect(surface, tetrimino.color, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)  # Draw the border

def draw_board(surface, board):
    for y, row in enumerate(board):
        for x, (cell, color) in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    x * GRID_SIZE,
                    y * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE
                )
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)  # Draw the border

def clear_lines(board, explosion_sound):
    new_board = [row for row in board if any(cell == 0 for cell, _ in row)]
    lines_cleared = ROWS - len(new_board)
    if lines_cleared > 0:
        explosion_sound.play()
    new_board = [[(0, BLACK)] * COLS for _ in range(lines_cleared)] + new_board
    return new_board, lines_cleared

def draw_score(surface, score, font_path):
    text = pygame.font.Font(font_path, 14).render(f"Score: {score}", True, WHITE)
    surface.blit(text, (10, 10))

def draw_timer(surface, start_time, font_path):
    elapsed_time = int(time.time() - start_time)
    text = pygame.font.Font(font_path, 14).render(f"Time: {elapsed_time}s", True, WHITE)
    surface.blit(text, (WIDTH - 120, 10))

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    board = [[(0, BLACK)] * COLS for _ in range(ROWS)]
    tetrimino = Tetrimino()
    score = 0
    drop_counter = 0
    drop_speed = 30  # Frames per drop
    start_time = time.time()
    
    # Load sounds
    explosion_sound = pygame.mixer.Sound("resources/audio/explosion.wav")
    pygame.mixer.music.load("resources/audio/soundtrack.mp3")
    pygame.mixer.music.play(-1)  # Play the background music in a loop
    
    # Load background image
    background = pygame.image.load("resources/images/background.webp")
    
    # Load font
    font_path = "resources/fonts/PressStart2P-Regular.ttf"
    
    show_start_screen(screen, background, font_path)
    
    while running:
        screen.fill(BLACK)
        draw_grid(screen)
        draw_board(screen, board)
        draw_tetrimino(screen, tetrimino)
        draw_score(screen, score, font_path)
        draw_timer(screen, start_time, font_path)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetrimino.move(-1, 0, board)
                elif event.key == pygame.K_RIGHT:
                    tetrimino.move(1, 0, board)
                elif event.key == pygame.K_DOWN:
                    tetrimino.move(0, 1, board)
                elif event.key == pygame.K_UP:
                    tetrimino.rotate(board)
                elif event.key == pygame.K_p:
                    show_pause_menu(screen, background, font_path)
        
        drop_counter += 1
        if drop_counter >= drop_speed:
            if not tetrimino.check_collision(tetrimino.x, tetrimino.y + 1, board):
                tetrimino.move(0, 1, board)
            else:
                for row_index, row in enumerate(tetrimino.shape):
                    for col_index, cell in enumerate(row):
                        if cell:
                            board[tetrimino.y + row_index][tetrimino.x + col_index] = (1, tetrimino.color)
                board, lines_cleared = clear_lines(board, explosion_sound)
                score += lines_cleared * 100
                tetrimino = Tetrimino()
                if tetrimino.check_collision(tetrimino.x, tetrimino.y, board):
                    running = False  # Game Over
            drop_counter = 0
        
        clock.tick(60)
    
    show_game_over_screen(screen, score, font_path)
    pygame.quit()
    print(f"Game Over! Your Score: {score}")

if __name__ == "__main__":
    main()
