import pygame
class Display:
    def __init__(self, width, height, play_width, play_height, block_size):
        self.width = width
        self.height = height
        self.play_width = play_width
        self.play_height = play_height
        self.window = pygame.display.set_mode((width, height))
        self.block_size = block_size
        pygame.display.set_caption('Tetris')

    def draw_window(self, grid, score=0):
        self.window.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))

        top_left_x = (self.width - self.play_width) // 2
        top_left_y = self.height - self.play_height
        self.window.blit(label, (top_left_x + self.play_width / 2 - (label.get_width() / 2), 30))

        # current score
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(score), 1, (255, 255, 255))

        sx = top_left_x + self.play_width + 50
        sy = top_left_y + self.play_height / 2 - 100

        last_score = self.max_score()

        self.window.blit(label, (sx + 20, sy + 160))
        # last score
        label = font.render('High Score: ' + last_score, 1, (255, 255, 255))

        sx = top_left_x - 200
        sy = top_left_y + 200

        self.window.blit(label, (sx + 20, sy + 160))

        for i in range(grid.row):
            for j in range(grid.col):
                pygame.draw.rect(self.window, grid.matrix[i][j],
                                 (top_left_x + j * self.block_size, top_left_y + i * self.block_size, self.block_size, self.block_size), 0)

        pygame.draw.rect(self.window, (255, 0, 0), (top_left_x, top_left_y, self.play_width, self.play_height), 5)

        self.draw_grid(grid)

    def draw_text_middle(self, text, size, color):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)

        top_left_x = (self.width - self.play_width) // 2
        top_left_y = self.height - self.play_height

        self.window.blit(label, (
        top_left_x + self.play_width / 2 - (label.get_width() / 2), top_left_y + self.play_height / 2 - label.get_height() / 2))

    def draw_grid(self, grid):
        top_left_x = (self.width - self.play_width) // 2
        top_left_y = self.height - self.play_height
        sx = top_left_x
        sy = top_left_y

        for i in range(grid.row):
            pygame.draw.line(self.window, (128, 128, 128), (sx, sy + i * self.block_size),
                             (sx + self.play_width, sy + i * self.block_size))
            for j in range(grid.col):
                pygame.draw.line(self.window, (128, 128, 128), (sx + j * self.block_size, sy),
                                 (sx + j * self.block_size, sy + self.play_height))

    def draw_next_shape(self, shape):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255, 255, 255))

        top_left_x = (self.width - self.play_width) // 2
        top_left_y = self.height - self.play_height

        sx = top_left_x + self.play_width + 50
        sy = top_left_y + self.play_height // 2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(self.window, shape.color,
                                     (sx + j * self.block_size, sy + i * self.block_size, self.block_size, self.block_size), 0)

        self.window.blit(label, (sx + 10, sy - 30))

    def update_score(self, nscore):
        score = self.max_score()
        if score < nscore:
            with open('scores.txt', 'w') as f:
                f.write(str(nscore))

    def max_score(self):
        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            score = lines[0].strip()

        return score