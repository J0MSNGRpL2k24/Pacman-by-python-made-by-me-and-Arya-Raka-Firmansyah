import pygame
import random

# Inisialisasi Pygame
pygame.init()


# Konstanta warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 0, 255)
BLUE = (0, 0, 255)

# Ukuran layar
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pacman Game")

# Ukuran grid maze
grid_size = 20

# Font untuk teks
font = pygame.font.Font(None, 30)

# --- Kelas Pacman ---
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = grid_size
        self.speed = grid_size
        self.direction = "right"
        self.lives = 50  # Pacman memiliki 3 nyawa

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

    def move(self, direction, maze):
        if self.can_move(direction, maze):
            self.direction = direction
            if direction == "left":
                self.x -= self.speed
            elif direction == "right":
                self.x += self.speed
            elif direction == "up":
                self.y -= self.speed
            elif direction == "down":
                self.y += self.speed

        # Teleportasi sisi layar
        if self.x < 0:
            self.x = screen_width - grid_size
        elif self.x >= screen_width:
            self.x = 0

    def can_move(self, direction, maze):
        row = self.y // grid_size
        col = self.x // grid_size
        if direction == "left" and col > 0 and maze[row][col - 1] != 1:
            return True
        if direction == "right" and col < len(maze[0]) - 1 and maze[row][col + 1] != 1:
            return True
        if direction == "up" and row > 0 and maze[row - 1][col] != 1:
            return True
        if direction == "down" and row < len(maze) - 1 and maze[row + 1][col] != 1:
            return True
        return False

    def collect_dot(self, maze):
        row = self.y // grid_size
        col = self.x // grid_size
        if maze[row][col] == 0:
            maze[row][col] = 2  # Dot collected
            return 1
        return 0

# --- Kelas Hantu ---
class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = grid_size
        self.speed = grid_size
        self.color = BLUE

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self, maze, pacman):
        row = self.y // grid_size
        col = self.x // grid_size
        pacman_row = pacman.y // grid_size
        pacman_col = pacman.x // grid_size

        directions = []

        # Allow the ghost to move in any direction that is not blocked by a wall
        if col > 0 and maze[row][col - 1] != 1:  # Left
            directions.append("left")
        if col < len(maze[0]) - 1 and maze[row][col + 1] != 1:  # Right
            directions.append("right")
        if row > 0 and maze[row - 1][col] != 1:  # Up
            directions.append("up")
        if row < len(maze) - 1 and maze[row + 1][col] != 1:  # Down
            directions.append("down")

        # Choose a direction: Move towards Pacman or move randomly if no specific direction
        if pacman_col < col:
            directions = [dir for dir in directions if dir == "left"]
        elif pacman_col > col:
            directions = [dir for dir in directions if dir == "right"]
        if pacman_row < row:
            directions = [dir for dir in directions if dir == "up"]
        elif pacman_row > row:
            directions = [dir for dir in directions if dir == "down"]

        # If there are still directions left, move in one of them
        if directions:
            direction = random.choice(directions)
        else:
           direction = random.choice(["left", "right", "up", "down"])

        # Move the ghost based on the selected direction
        if direction == "left" and col > 0 and maze[row][col - 1] != 1:
            self.x -= self.speed
        elif direction == "right" and col < len(maze[0]) - 1 and maze[row][col + 1] != 1:
            self.x += self.speed
        elif direction == "up" and row > 0 and maze[row - 1][col] != 1:
            self.y -= self.speed
        elif direction == "down" and row < len(maze) - 1 and maze[row + 1][col] != 1:
            self.y += self.speed

    def check_collision(self, pacman):
        return self.x == pacman.x and self.y == pacman.y

# --- Maze ---
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
] 

# Inisialisasi Pacman, hantu, dan variabel lainnya
pacman = Pacman(40, 40)
pacman.lives = 5
ghosts = [Ghost(random.randint(1, 18) * grid_size, random.randint(1, 14) * grid_size) for _ in range(3)]
score = 0
dots_left = sum(row.count(0) for row in maze)  # Hitung jumlah dot awal

# Fungsi untuk menghitung jumlah dot yang tersisa
def count_dots_left(maze):
    return sum(row.count(0) for row in maze)

# Fungsi untuk menggambar maze
def draw_maze(maze):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, WHITE, (col * grid_size, row * grid_size, grid_size, grid_size))
            elif maze[row][col] == 0:
                pygame.draw.circle(screen, GREEN, (col * grid_size + grid_size // 2, row * grid_size + grid_size // 2), 4)

# Fungsi untuk menampilkan watermark
def draw_watermark():
    watermark_text = "Pacman Game by Jovan Sinaga & Arya Raka"
    watermark_font = pygame.font.SysFont("Consolas", 24)
    watermark_surface = watermark_font.render(watermark_text, True, (255, 255, 255))
    screen.blit(watermark_surface, (10, screen_height - 30))
# Fungsi untuk me-reset posisi hantu setelah tabrakan
def reset_ghost(ghost):
    ghost.x = random.randint(1, 18) * grid_size
    ghost.y = random.randint(1, 14) * grid_size
    
# Fungsi untuk mereset posisi Pacman setelah tabrakan
def reset_pacman():
    pacman.x = 40  # Posisi awal X
    pacman.y = 40  # Posisi awal Y

# Fungsi untuk menampilkan layar akhir
def show_end_screen(message, initial_lives, initial_dots_left):
    end_text = font.render(message, True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.fill(BLACK)
    screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 3))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    # Reset all initial game conditions
                    global pacman, ghosts, score, dots_left, maze  # Declare globals to reset values

                    maze = [
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
                        [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
                        [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
                        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                        [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                    ]

                    pacman = Pacman(40, 40)         # Reset Pacman position
                    pacman.lives = initial_lives    # Reset lives to initial value
                    ghosts = [Ghost(random.randint(1, 18) * grid_size, random.randint(1, 14) * grid_size) for _ in range(3)]  # Reset ghosts
                    score = 0                       # Reset score
                    dots_left = initial_dots_left   # Reset dots count

                    return True

                if event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    exit()

    return False


# Game loop
initial_lives = 5  # Set initial lives
initial_dots_left = sum(row.count(0) for row in maze)  # Calculate initial number of dots

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    draw_maze(maze)
    draw_watermark()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kontrol Pacman
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        pacman.move("up", maze)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        pacman.move("down", maze)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        pacman.move("left", maze)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        pacman.move("right", maze)

    # Perbarui Pacman
    score += pacman.collect_dot(maze)
    dots_left = count_dots_left(maze)  # Update dots_left dynamically
    pacman.draw()

    # Perbarui hantu dan periksa tabrakan
    for ghost in ghosts:
        ghost.move(maze, pacman)
        ghost.draw()
        if ghost.check_collision(pacman):
            pacman.lives -= 1
            reset_pacman()  # Reset posisi Pacman
            if pacman.lives == 0:
                if show_end_screen("Game Over!", initial_lives, initial_dots_left):
                    # Reset maze, posisi Pacman, posisi hantu, skor, dot, dan nyawa
                    maze = [row[:] for row in maze]  # Reset maze ke kondisi awal
                    pacman = Pacman(40, 40)          # Reset posisi Pacman
                    pacman.lives = initial_lives     # Set lives kembali ke nilai awal
                    ghosts = [Ghost(random.randint(1, 18) * grid_size, random.randint(1, 14) * grid_size) for _ in range(3)]  # Reset posisi hantu
                    score = 0                        # Reset skor menjadi 0
                    dots_left = initial_dots_left    # Hitung kembali jumlah dot
                else:
                    running = False

    # Tampilkan skor dan nyawa
    score_font = pygame.font.SysFont("Consolas", 20)
    lives_font = pygame.font.SysFont("Consolas", 20)
    score_text = score_font.render(f"Score: {score}", True, PINK)
    lives_text = lives_font.render(f"Lives: {pacman.lives}", True, RED)
    screen.blit(score_text, (485, 10))
    screen.blit(lives_text, (485, 40))

    # Periksa apakah semua dot sudah diambil (game win)
    if dots_left == 0:
        running = False
        if show_end_screen("You Win!", initial_lives, initial_dots_left):
            # Reset maze, posisi Pacman, posisi hantu, skor, dot, dan nyawa
            maze = [row[:] for row in maze]  # Reset maze ke kondisi awal
            pacman = Pacman(40, 40)          # Reset posisi Pacman
            pacman.lives = initial_lives     # Set lives kembali ke nilai awal
            ghosts = [Ghost(random.randint(1, 18) * grid_size, random.randint(1, 14) * grid_size) for _ in range(3)]  # Reset posisi hantu
            score = 0                        # Reset skor menjadi 0
            dots_left = initial_dots_left    # Hitung kembali jumlah dot
            running = True
        

    # Refresh layar
    pygame.display.flip()
    clock.tick(10)

pygame.quit()