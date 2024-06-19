import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple 2D Game with Difficulty Levels")

# 색 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 플레이어 설정
player_size = 50
player_x = screen_width // 2
player_y = screen_height - 2 * player_size
initial_player_speed = 5

# 장애물 설정
obstacle_width = 50
obstacle_height = 50
obstacle_list = []  # 전역 변수로 설정

# 글꼴 설정
font = pygame.font.SysFont("monospace", 35)

# 난이도 설정
difficulty_levels = {
    "Easy": 5,
    "Normal": 10,
    "Hard": 15,
    "Hardcore": 20
}
selected_difficulty = None

# 점수
score = 0

# 장애물 생성 함수
def create_obstacle():
    x_pos = random.randint(0, screen_width - obstacle_width)
    y_pos = 0 - obstacle_height
    obstacle_list.append([x_pos, y_pos])

# 장애물 이동 함수
def move_obstacles(obstacles, speed):
    for obstacle in obstacles:
        obstacle[1] += speed
    obstacles[:] = [obstacle for obstacle in obstacles if obstacle[1] < screen_height]

# 충돌 감지 함수
def detect_collision(player_pos, obstacle_pos):
    p_x, p_y = player_pos
    o_x, o_y = obstacle_pos

    if (o_x < p_x < o_x + obstacle_width or o_x < p_x + player_size < o_x + obstacle_width) and \
       (o_y < p_y < o_y + obstacle_height or o_y < p_y + player_size < o_y + obstacle_height):
        return True
    return False

# 제작자 화면 함수
def show_creator():
    showing = True
    timer = 0
    while showing:
        screen.fill(BLACK)
        creator_text = font.render("Created by Souljjab", True, WHITE)
        screen.blit(creator_text, (screen_width // 2 - creator_text.get_width() // 2, screen_height // 2))
        pygame.display.flip()

        timer += 1
        if timer > 180:  # 3초 동안 표시
            showing = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showing = False
                pygame.quit()
                return False
    return True

# 메인 화면 함수
def main_menu():
    menu = True
    while menu:
        screen.fill(BLACK)
        title_text = font.render("Simple 2D Game", True, WHITE)
        start_button = font.render("Start Game", True, BLUE)
        start_button_rect = start_button.get_rect(center=(screen_width // 2, screen_height // 2))

        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))
        screen.blit(start_button, start_button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    return True
    return False

# 난이도 선택 화면 함수
def select_difficulty():
    global selected_difficulty
    selecting = True
    while selecting:
        screen.fill(BLACK)
        title_text = font.render("Select Difficulty", True, WHITE)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

        y_offset = 0
        level_rects = []
        for level in difficulty_levels:
            level_text = font.render(level, True, WHITE)
            level_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
            screen.blit(level_text, level_rect)
            level_rects.append((level_rect, level))
            y_offset += 50

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selecting = False
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, level in level_rects:
                    if rect.collidepoint(mouse_pos):
                        selected_difficulty = level
                        selecting = False
                        break
    return difficulty_levels[selected_difficulty]

# 게임 오버 화면 함수
def game_over():
    global score
    game_over_screen = True
    while game_over_screen:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over!", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        retry_text = font.render("Retry (R)", True, WHITE)
        quit_text = font.render("Quit (Q)", True, WHITE)

        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
        screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 50))
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_screen = False
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'retry'
                elif event.key == pygame.K_q:
                    game_over_screen = False
                    pygame.quit()
                    return None

# 게임 루프
def game_loop(obstacle_speed):
    global score, player_x, player_y, obstacle_list, initial_player_speed
    player_x = screen_width // 2
    player_y = screen_height - 2 * player_size
    player_speed = initial_player_speed
    obstacle_list = []
    score = 0
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
            player_x += player_speed

        if random.randint(0, 20) == 1:
            create_obstacle()

        move_obstacles(obstacle_list, obstacle_speed)

        for obstacle in obstacle_list:
            if detect_collision((player_x, player_y), obstacle):
                return 'game_over'

        for obstacle in obstacle_list:
            pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))

        score_text = font.render("Score: {}".format(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        score += 1
        player_speed = initial_player_speed + score // 100  # 점수에 따라 플레이어 속도 증가

        pygame.display.flip()
        clock.tick(30)

# 메인 실행 부분
if show_creator():  # 제작자 화면을 보여줍니다.
    while True:
        if main_menu():  # 메인 메뉴 화면을 보여줍니다.
            obstacle_speed = select_difficulty()  # 난이도 선택 화면을 보여줍니다.
            if obstacle_speed is None:
                break
            result = game_loop(obstacle_speed)  # 게임 루프를 실행합니다.
            if result == 'menu':
                continue
            elif result == 'game_over':
                decision = game_over()  # 게임 오버 화면을 보여줍니다.
                if decision == 'retry':
                    continue
                else:
                    break

pygame.quit()  # Pygame 종료
