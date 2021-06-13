from display import Display
from grid import Grid
from piece import Piece
import pygame
pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block

grid_row, grid_col = 20, 10
block_size = play_height // grid_row

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

def check_lost(positions):
    for x, y in positions:
        if y == 0:
            return True

    return False

def main(win):  # *
    locked_positions = {}
    change_piece = False
    run = True
    current_piece = Piece()
    next_piece = Piece()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level = 0
    score = 0

    while run:
        grid.update(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if score // 200 > level:
            level += 1
            fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(grid.valid_space(current_piece)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (grid.valid_space(current_piece)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (grid.valid_space(current_piece)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (grid.valid_space(current_piece)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (grid.valid_space(current_piece)):
                        current_piece.rotation -= 1

        shape_pos = current_piece.update_position()

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid.matrix[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = Piece()
            change_piece = False
            cur_score, locked = grid.clear_rows()
            score += cur_score
            if cur_score > 0:
                locked_positions = locked

        win.draw_window(grid, score)
        win.draw_next_shape(next_piece)
        pygame.display.update()

        if check_lost(locked_positions):
            win.draw_text_middle("Game Over!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            win.update_score(score)


def main_menu(win):  # *
    run = True
    while run:
        win.window.fill((0,0,0))
        win.draw_text_middle('Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()

if __name__ == '__main__':
    win = Display(s_width, s_height, play_width, play_height, block_size)
    grid = Grid(grid_row, grid_col)
    main_menu(win)