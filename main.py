from utils.parser import parse_args
from modules.agent import Agent
from modules.environment import Stage
import numpy as np
import time
import pygame
from config import BLACK, WHITE, RED, GREEN, BLUE, CELL_SIZE

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

def draw(action, screen, stage, GRID_SIZE):
    screen.fill(BLACK)
    # グリッドを描画
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pygame.draw.rect(screen, WHITE,
                            (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

    # 蛇の体を描画
    for segment in stage.snake:
        pygame.draw.rect(screen, GREEN,
                        (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE,
                        CELL_SIZE - 1, CELL_SIZE - 1))

    # 蛇の頭に目を描く
    head = stage.snake[0]  # 蛇の頭
    head_x, head_y = head[0] * CELL_SIZE, head[1] * CELL_SIZE
    eye_radius = CELL_SIZE // 8  # 目のサイズ
    eye_offset = CELL_SIZE // 4  # 目の位置のオフセット

    if action == 1:
        pygame.draw.circle(screen, BLACK,
                        (head_x + CELL_SIZE // 4, head_y + CELL_SIZE // 5),
                        eye_radius)
        pygame.draw.circle(screen, BLACK,
                        (head_x + 3 * CELL_SIZE // 4, head_y + CELL_SIZE // 5),
                        eye_radius)
    elif action == 0:
        pygame.draw.circle(screen, BLACK,
                        (head_x + CELL_SIZE // 4, head_y + 4 * CELL_SIZE // 5),
                        eye_radius)
        pygame.draw.circle(screen, BLACK,
                        (head_x + 3 * CELL_SIZE // 4, head_y + 4 * CELL_SIZE // 5),
                        eye_radius)
    elif action == 3:
        pygame.draw.circle(screen, BLACK,
                        (head_x + CELL_SIZE // 5, head_y + CELL_SIZE // 4),
                        eye_radius)
        pygame.draw.circle(screen, BLACK,
                        (head_x + CELL_SIZE // 5, head_y + 3 * CELL_SIZE // 4),
                        eye_radius)
    elif action == 2:
        pygame.draw.circle(screen, BLACK,
                        (head_x + 4 * CELL_SIZE // 5, head_y + CELL_SIZE // 4),
                        eye_radius)
        pygame.draw.circle(screen, BLACK,
                        (head_x + 4 * CELL_SIZE // 5, head_y + 3 * CELL_SIZE // 4),
                        eye_radius)

        # 赤いリンゴを描画
    pygame.draw.rect(screen, RED,
                    (stage.red_apple[0] * CELL_SIZE, stage.red_apple[1] * CELL_SIZE,
                    CELL_SIZE - 1, CELL_SIZE - 1))

    # 青いリンゴを描画
    for green_apple in stage.green_apples:
        pygame.draw.rect(screen, BLUE,
                        (green_apple[0] * CELL_SIZE, green_apple[1] * CELL_SIZE,
                        CELL_SIZE - 1, CELL_SIZE - 1))
    # 画面を更新
    pygame.display.flip()



def main():
    args = parse_args()
    if args.visualize:
        GRID_SIZE = args.size
        WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        pygame.init()
        screen = pygame.display.set_mode(WINDOW_SIZE)

    snake = Agent(not args.no_learning)
    stage = Stage(args.size)

    if args.load:
        snake.load_model(args.load)
        print(f"Loading model from {args.load}")

    episode = 0
    running = True
    snake_vision = snake.look_around(stage, print_vision=args.visualize)
    while running and episode < args.episodes:
        snake_vision = snake.look_around(stage, print_vision=args.terminal_visualize)
        vision_key = tuple(snake_vision)
        action = snake.get_action(vision_key)
        next_state, reward, game_over = stage.step(snake, action, snake_vision)
        snake_next_vision = snake.look_around(stage)
        next_vision_key = tuple(snake_next_vision)
        snake.learn(vision_key, next_vision_key, reward, action)
        snake_vision = snake_next_vision

        if game_over:
            print(f"Episode {episode} finished with length {len(stage.snake)}")
            episode += 1
            stage.reset()
        if args.visualize:
            draw(action, screen, stage, GRID_SIZE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif args.step_mode and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        continue
            if args.step_mode:  # スペースキーを押すまで待つ処理
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting = False  # 全体の終了
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            waiting = False

        if not args.step_mode:
            time.sleep(args.speed)

    if args.save:
        print(f"Saving model to {args.save}")
        snake.save(args.save)


if __name__ == "__main__":
    main()