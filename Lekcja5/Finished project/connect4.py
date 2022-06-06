import pygame as pg
import sys
import math
import random
from config import *
from board import *

pg.init()
pg.display.set_caption('Connect 4')

width = COLUMNS * DISC_SIZE
height = (ROWS + 1) * DISC_SIZE
size = (COLUMNS * DISC_SIZE, (ROWS + 1) * DISC_SIZE)
screen = pg.display.set_mode(size)

my_font = pg.font.SysFont('Calibri', 60)


def draw_grid(grid):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pg.draw.rect(screen, BLUE, (c * DISC_SIZE, r * DISC_SIZE + DISC_SIZE, DISC_SIZE, DISC_SIZE))
            pg.draw.circle(screen, WHITE, (int(c * DISC_SIZE + DISC_SIZE / 2),
                                           int(r * DISC_SIZE + DISC_SIZE + DISC_SIZE / 2)), DISC_RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if grid[r][c] == REAL_PLAYER_PIECE:
                pg.draw.circle(screen, RED, (int(c * DISC_SIZE + DISC_SIZE / 2),
                                             height - int(r * DISC_SIZE + DISC_SIZE / 2)), DISC_RADIUS)
            elif grid[r][c] == AI_PLAYER_PIECE:
                pg.draw.circle(screen, YELLOW, (int(c * DISC_SIZE + DISC_SIZE / 2),
                                                height - int(r * DISC_SIZE + DISC_SIZE / 2)), DISC_RADIUS)
    pg.display.update()

	
def search_win_move(grid, piece):
    # horizontal
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if grid[r][c] == piece and grid[r][c + 1] == piece \
                    and grid[r][c + 2] == piece and grid[r][c + 3] == piece:
                return True

    # vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if grid[r][c] == piece and grid[r + 1][c] == piece \
                    and grid[r + 2][c] == piece and grid[r + 3][c] == piece:
                return True

    # positively sloped diaganols
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if grid[r][c] == piece and grid[r + 1][c + 1] == piece \
                    and grid[r + 2][c + 2] == piece and grid[r + 3][c + 3] == piece:
                return True

    # negatively sloped diaganols
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if grid[r][c] == piece and grid[r - 1][c + 1] == piece \
                    and grid[r - 2][c + 2] == piece and grid[r - 3][c + 3] == piece:
                return True


def rate_score(window, piece):
    score = 0
    opp_piece = REAL_PLAYER_PIECE
    if piece == REAL_PLAYER_PIECE:
        opp_piece = AI_PLAYER_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def total_score(grid, piece):
    score = 0

    center_array = [int(i) for i in list(grid[:, COLUMNS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(ROWS):
        row_array = [int(i) for i in list(grid[r, :])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + MAIN_WINDOW]
            score += rate_score(window, piece)

    for c in range(COLUMNS):
        col_array = [int(i) for i in list(grid[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + MAIN_WINDOW]
            score += rate_score(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [grid[r + i][c + i] for i in range(MAIN_WINDOW)]
            score += rate_score(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [grid[r + 3 - i][c + i] for i in range(MAIN_WINDOW)]
            score += rate_score(window, piece)

    return score


def is_terminal_node(grid):
    return search_win_move(grid, REAL_PLAYER_PIECE) or search_win_move(grid, AI_PLAYER_PIECE) or len(get_valid_position(grid)) == 0


def minimax(grid, depth, alpha, beta, max_player):
    valid_position = get_valid_position(grid)
    terminal = is_terminal_node(grid)
    if depth == 0 or terminal:
        if terminal:
            if search_win_move(grid, AI_PLAYER_PIECE):
                return (None, 10**14)
            elif search_win_move(grid, REAL_PLAYER_PIECE):
                return (None, -(10**13))
            else:
                return (None, 0)
        else:
            return (None, total_score(grid, AI_PLAYER_PIECE))
    if max_player:
        value = -math.inf
        column = random.choice(valid_position)
        for col in valid_position:
            row = get_next_open_row(grid, col)
            grid_copy = grid.copy()
            grid_copy[row][col] = AI_PLAYER_PIECE
            new_score = minimax(grid_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_position)
        for col in valid_position:
            row = get_next_open_row(grid, col)
            grid_copy = grid.copy()
            grid_copy[row][col] = REAL_PLAYER_PIECE
            new_score = minimax(grid_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def pick_best_move(grid, piece):
    valid_position = get_valid_position(grid)
    best_score = -10000
    best_col = random.choice(valid_position)
    for col in valid_position:
        row = get_next_open_row(grid, col)
        temp_grid = grid.copy()
        temp_grid[row][col] = piece
        score = total_score(temp_grid, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def main():
    grid = new_grid()

    draw_grid(grid)
    pg.display.update()

    pick_random = random.randint(REAL_PLAYER, AI_PLAYER)

    game_over = False
    while not game_over:

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
            elif event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEMOTION:
                pg.draw.rect(screen, WHITE, (0, 0, width, DISC_SIZE))
                position_x = event.pos[0]
                if pick_random == REAL_PLAYER:
                    pg.draw.circle(screen, RED, (position_x, int(DISC_SIZE / 2)), DISC_RADIUS)
            pg.display.update()

            if event.type == pg.MOUSEBUTTONDOWN:
                pg.draw.rect(screen, WHITE, (0, 0, width, DISC_SIZE))
                if pick_random == REAL_PLAYER:
                    position_x = event.pos[0]
                    col = int(math.floor(position_x / DISC_SIZE))

                    if is_valid_position(grid, col):
                        row = get_next_open_row(grid, col)
                        grid[row][col] = REAL_PLAYER_PIECE

                        if search_win_move(grid, REAL_PLAYER_PIECE):
                            label = my_font.render("Player 1 wins!", 1, RED)
                            screen.blit(label, (10, 10))
                            game_over = True

                        pick_random += 1
                        pick_random = pick_random % 2

                        draw_grid(grid)

        if pick_random == AI_PLAYER and not game_over:
            col, minimax_score = minimax(grid, 5, -math.inf, math.inf, True)

            if is_valid_position(grid, col):
                row = get_next_open_row(grid, col)
                grid[row][col] = AI_PLAYER_PIECE

                if search_win_move(grid, AI_PLAYER_PIECE):
                    label = my_font.render("Player 2 wins!", 1, YELLOW)
                    screen.blit(label, (10, 10))
                    game_over = True

                draw_grid(grid)

                pick_random += 1
                pick_random = pick_random % 2

        if game_over:
            pg.time.wait(2500)


if __name__ == '__main__':
    main()
    pg.quit()
