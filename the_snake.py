from random import randrange
import time

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

SCREEN_CENTER = (
    SCREEN_WIDTH // GRID_SIZE // 2 * GRID_SIZE,
    SCREEN_HEIGHT // GRID_SIZE // 2 * GRID_SIZE,
)
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет яблока
APPLE_COLOR = (255, 0, 0)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
screen.fill(BOARD_BACKGROUND_COLOR)

clock = pygame.time.Clock()


class GameObject:

    def __init__(self, body_color, position=SCREEN_CENTER) -> None:
        self.body_color = body_color
        self.position = position


class Apple(GameObject):

    def __init__(self, body_color, position=[0, 0]) -> None:
        super().__init__(body_color, position)
        self.flag = True
        self.position = self.randomize_position()

    def randomize_position(self):
        x_coord = randrange(0, SCREEN_WIDTH, GRID_SIZE)
        y_coord = randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        return (x_coord, y_coord)

    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self, body_color, start_position=SCREEN_CENTER) -> None:
        super().__init__(body_color, start_position)
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        return None

    def move(self):
        self.update_direction()
        self.last = self.positions[-1]

        x_after_move = self.positions[0][0] + self.direction[0] * GRID_SIZE
        if x_after_move >= SCREEN_WIDTH or x_after_move < 0:
            x_after_move = (x_after_move + SCREEN_WIDTH) % SCREEN_WIDTH

        y_after_move = self.positions[0][1] + self.direction[1] * GRID_SIZE
        if y_after_move >= SCREEN_HEIGHT or y_after_move < 0:
            y_after_move = (y_after_move + SCREEN_HEIGHT) % SCREEN_HEIGHT

        self.positions.insert(0, (x_after_move, y_after_move))
        self.positions = self.positions[0: self.length]
        return None

    def draw(self, surface):

        for pos in self.positions[:-1]:
            rect = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last and self.last not in self.positions:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.__init__(SNAKE_COLOR, SCREEN_CENTER)
        return None


player_moves = {
    pygame.K_UP: (DOWN, UP),
    pygame.K_DOWN: (UP, DOWN),
    pygame.K_LEFT: (RIGHT, LEFT),
    pygame.K_RIGHT: (LEFT, RIGHT),
}


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in player_moves:
                if game_object.direction != player_moves[event.key][0]:
                    game_object.next_direction = player_moves[event.key][1]
    return None


def apple_eated(snake, apple, start_time):
    snake.length += 1
    time_played = round(time.time() - start_time, 1)
    print(
        f"You are playing for {time_played} sec,",
        f"Current Score: {(snake.length - 1) * SPEED}",
    )
    new_apple_in_snake = True
    while new_apple_in_snake:
        new_apple_position = apple.randomize_position()
        if new_apple_position not in snake.positions:
            apple.position = new_apple_position
            new_apple_in_snake = False
    return None


def end_game(snake):
    print("GAME OVER, your Score", (snake.length - 1) * SPEED)
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.reset()
    return None


def main():
    print("Start Game")
    start_time = time.time()
    apple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()

        if snake.get_head_position() == apple.position:
            if snake.length >= (GRID_WIDTH * GRID_HEIGHT - 1):
                print("Your Score", (snake.length + 1) * SPEED)
                print("Congratulations! Your Won the Snake!")
                break
            else:
                apple_eated(snake, apple, start_time)

        if snake.get_head_position() in snake.positions[1:]:
            end_game(snake)


if __name__ == "__main__":
    main()
