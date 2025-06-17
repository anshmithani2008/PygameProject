# Goofy ahh chopped maze
# Aditya Assets and designs
# Tim Collisions movement and game loop
# Ansh UI, timer, QOL...

VERSION = "0.4"

try:
    import sys
    import math
    import os
    import pygame
    from pygame.locals import *
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

WALL_COLOR = (255, 0, 0)

def is_red(color):
    r, g, b = color
    return r > 200 and g < 150 and b < 150

def box_collides_with_wall(rect, background, wall_color):
    points_to_check = [
        (rect.left, rect.top), (rect.right - 1, rect.top),
        (rect.left, rect.bottom - 1), (rect.right - 1, rect.bottom - 1),
        (rect.centerx, rect.top), (rect.centerx, rect.bottom - 1),
        (rect.left, rect.centery), (rect.right - 1, rect.centery)
    ]
    for (x, y) in points_to_check:
        if 0 <= x < background.get_width() and 0 <= y < background.get_height():
            color = background.get_at((int(x), int(y)))[:3]
            if is_red(color):
                return True
    return False

def main():
    pygame.init()
    LENGTH, WIDTH = 640, 480
    screen = pygame.display.set_mode((LENGTH, WIDTH))
    pygame.display.set_caption('Chopped Maze')

    background = pygame.image.load("Maze.jpg")
    background = pygame.transform.scale(background, (LENGTH, WIDTH))

    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Player setup
    player_size = 30
    player = pygame.Rect(30, 420, player_size, player_size)

    # Finish sensor rectangle (bottom right corner area)
    finish_sensor = pygame.Rect(LENGTH - 50, WIDTH - 50, 50, 50)

    clock = pygame.time.Clock()
    energy = 100
    start_ticks = pygame.time.get_ticks()
    game_over = False
    finished = False
    personal_best = None
    final_time = None

    while True:
        dt = clock.tick(60)
        dx = dy = 0
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        keys = pygame.key.get_pressed()

        if not game_over and not finished:
            if keys[K_LEFT]:
                dx = -dt / 20
            if keys[K_RIGHT]:
                dx = dt / 20
            if keys[K_UP]:
                dy = -dt / 20
            if keys[K_DOWN]:
                dy = dt / 20

            new_player = player.move(dx, 0)
            if not box_collides_with_wall(new_player, background, WALL_COLOR):
                player.x += dx
            else:
                energy -= 1

            new_player = player.move(0, dy)
            if not box_collides_with_wall(new_player, background, WALL_COLOR):
                player.y += dy
            else:
                energy -= 1

            player.x = max(0, min(LENGTH - player_size, player.x))
            player.y = max(0, min(WIDTH - player_size, player.y))

            energy -= 0.028  # passive drain

            if energy <= 0:
                energy = 0
                game_over = True
                final_time = elapsed_seconds  # save time when game over

            # Finish line detection using sensor
            if player.colliderect(finish_sensor):
                finished = True
                final_time = elapsed_seconds  # save time when finished
                if personal_best is None or final_time < personal_best:
                    personal_best = final_time

        # Draw everything
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, BLACK, player)
        # pygame.draw.rect(screen, GREEN, finish_sensor) 

        # Updated to black text
        energy_text = font.render(f"Energy: {int(energy)}%", True, BLACK)
        time_text = font.render(f"Time: {elapsed_seconds}s", True, BLACK)
        screen.blit(energy_text, (20, 20))
        screen.blit(time_text, (20, 60))

        if game_over:
            over_text = big_font.render("GAME OVER", True, RED)
            final_time_text = font.render(f"Final Time: {final_time}s", True, BLACK)
            screen.blit(over_text, (LENGTH // 2 - 150, WIDTH // 2 - 40))
            screen.blit(final_time_text, (LENGTH // 2 - 100, WIDTH // 2 + 40))

        if finished:
            win_text = big_font.render("YOU ESCAPED!", True, GREEN)
            final_time_text = font.render(f"Final Time: {final_time}s", True, BLACK)
            pb_text = font.render(f"Personal Best: {personal_best}s", True, GREEN)
            screen.blit(win_text, (LENGTH // 2 - 180, WIDTH // 2 - 40))
            screen.blit(final_time_text, (LENGTH // 2 - 100, WIDTH // 2 + 20))
            screen.blit(pb_text, (LENGTH // 2 - 120, WIDTH // 2 + 60))

        pygame.display.flip()

if __name__ == '__main__':
    main()
