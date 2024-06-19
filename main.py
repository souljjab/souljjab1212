import pygame  # Pygame 모듈을 가져옵니다.
import random  # Random 모듈을 가져옵니다.

# 초기화
pygame.init()  # Pygame을 초기화합니다.

# 화면 크기 설정
screen_width = 800  # 화면 너비를 설정합니다.
screen_height = 600  # 화면 높이를 설정합니다.
screen = pygame.display.set_mode((screen_width, screen_height))  # Pygame 화면을 설정된 크기로 만듭니다.
pygame.display.set_caption("souljjab")  # 창 제목을 설정합니다.

# 색 정의
WHITE = (255, 255, 255)  # 흰색 정의
BLACK = (0, 0, 0)  # 검은색 정의
RED = (255, 0, 0)  # 빨간색 정의

# 플레이어 설정
player_size = 50  # 플레이어 크기를 설정합니다.
player_x = screen_width // 2  # 플레이어 초기 x 위치를 설정합니다.
player_y = screen_height - 2 * player_size  # 플레이어 초기 y 위치를 설정합니다.
player_speed = 5  # 플레이어 이동 속도를 설정합니다.

# 장애물 설정
obstacle_width = 50  # 장애물 너비를 설정합니다.
obstacle_height = 50  # 장애물 높이를 설정합니다.
obstacle_list = []  # 전역 변수로 장애물 목록을 초기화합니다.

# 글꼴 설정
font = pygame.font.SysFont("monospace", 35)  # 글꼴과 크기를 설정합니다.

# 난이도 설정
difficulty_levels = {
    "Easy": 5,  # 쉬움 난이도의 장애물 속도
    "Normal": 10,  # 보통 난이도의 장애물 속도
    "Hard": 15,  # 어려움 난이도의 장애물 속도
    "Hardcore": 20  # 하드코어 난이도의 장애물 속도
}
selected_difficulty = None  # 선택된 난이도를 초기화합니다.

# 점수
score = 0  # 초기 점수를 설정합니다.

# 장애물 생성 함수
def create_obstacle():
    x_pos = random.randint(0, screen_width - obstacle_width)  # 랜덤한 x 위치를 설정합니다.
    y_pos = 0 - obstacle_height  # y 위치를 화면 위쪽으로 설정합니다.
    obstacle_list.append([x_pos, y_pos])  # 장애물 목록에 추가합니다.

# 장애물 이동 함수
def move_obstacles(obstacles, speed):
    for obstacle in obstacles:  # 각 장애물을 순회합니다.
        obstacle[1] += speed  # 장애물을 아래로 이동시킵니다.
    obstacles[:] = [obstacle for obstacle in obstacles if obstacle[1] < screen_height]  # 화면 밖으로 벗어난 장애물 제거

# 충돌 감지 함수
def detect_collision(player_pos, obstacle_pos):
    p_x, p_y = player_pos  # 플레이어 위치를 가져옵니다.
    o_x, o_y = obstacle_pos  # 장애물 위치를 가져옵니다.

    # 충돌 여부를 체크합니다.
    if (o_x < p_x < o_x + obstacle_width or o_x < p_x + player_size < o_x + obstacle_width) and \
       (o_y < p_y < o_y + obstacle_height or o_y < p_y + player_size < o_y + obstacle_height):
        return True  # 충돌 시 True 반환
    return False  # 충돌이 없을 시 False 반환

# 난이도 선택 화면 함수
def select_difficulty():
    global selected_difficulty  # 전역 변수를 사용합니다.
    selecting = True  # 난이도 선택 화면 플래그
    while selecting:
        screen.fill(BLACK)  # 화면을 검은색으로 채웁니다.
        title_text = font.render("Select Difficulty", True, WHITE)  # 제목 텍스트를 생성합니다.
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))  # 제목을 화면에 그립니다.

        y_offset = 0  # y 오프셋 초기화
        level_rects = []  # 난이도 버튼 리스트 초기화
        for level in difficulty_levels:  # 각 난이도를 순회합니다.
            level_text = font.render(level, True, WHITE)  # 난이도 텍스트 생성
            level_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))  # 텍스트 위치 설정
            screen.blit(level_text, level_rect)  # 텍스트를 화면에 그립니다.
            level_rects.append((level_rect, level))  # 텍스트 위치와 난이도를 리스트에 추가
            y_offset += 50  # y 오프셋 증가

        pygame.display.flip()  # 화면을 업데이트합니다.

        for event in pygame.event.get():  # 이벤트를 처리합니다.
            if event.type == pygame.QUIT:  # 종료 이벤트 처리
                selecting = False  # 난이도 선택 종료
                pygame.quit()  # Pygame 종료
                return None  # None 반환
            if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트 처리
                mouse_pos = event.pos  # 마우스 위치 가져오기
                for rect, level in level_rects:  # 각 난이도 버튼을 순회
                    if rect.collidepoint(mouse_pos):  # 마우스가 버튼에 클릭되었는지 확인
                        selected_difficulty = level  # 선택된 난이도 설정
                        selecting = False  # 난이도 선택 종료
                        break
    return difficulty_levels[selected_difficulty]  # 선택된 난이도의 속도 반환

# 게임 오버 화면 함수
def game_over():
    global score  # 전역 변수를 사용합니다.
    game_over_screen = True  # 게임 오버 화면 플래그
    while game_over_screen:
        screen.fill(BLACK)  # 화면을 검은색으로 채웁니다.
        game_over_text = font.render("Game Over!", True, WHITE)  # 게임 오버 텍스트 생성
        score_text = font.render(f"Score: {score}", True, WHITE)  # 점수 텍스트 생성
        retry_text = font.render("Retry (R)", True, WHITE)  # 재시작 텍스트 생성
        quit_text = font.render("Quit (Q)", True, WHITE)  # 종료 텍스트 생성

        # 텍스트들을 화면에 그립니다.
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
        screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 50))
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 100))

        pygame.display.flip()  # 화면을 업데이트합니다.

        for event in pygame.event.get():  # 이벤트를 처리합니다.
            if event.type == pygame.QUIT:  # 종료 이벤트 처리
                game_over_screen = False  # 게임 오버 화면 종료
                pygame.quit()  # Pygame 종료
                return None  # None 반환
            if event.type == pygame.KEYDOWN:  # 키보드 입력 이벤트 처리
                if event.key == pygame.K_r:  # 'R' 키를 누르면
                    return 'retry'  # 'retry' 반환
                elif event.key == pygame.K_q:  # 'Q' 키를 누르면
                    game_over_screen = False  # 게임 오버 화면 종료
                    pygame.quit()  # Pygame 종료
                    return None  # None 반환

# 게임 루프
def game_loop(obstacle_speed):
    global score, player_x, player_y, obstacle_list  # 전역 변수를 사용합니다.
    player_x = screen_width // 2  # 플레이어 초기 x 위치 설정
    player_y = screen_height - 2 * player_size  # 플레이어 초기 y 위치 설정
    obstacle_list = []  # 장애물 목록 초기화
    score = 0  # 점수 초기화
    running = True  # 게임 루프 플래그
    clock = pygame.time.Clock()  # Pygame 시계 객체 생성

    while running:
        screen.fill(BLACK)  # 화면을 검은색으로 채웁니다.

        for event in pygame.event.get():  # 이벤트를 처리합니다.
            if event.type == pygame.QUIT:  # 종료 이벤트 처리
                running = False  # 게임 루프 종료
            if event.type == pygame.KEYDOWN:  # 키보드 입력 이벤트 처리
                if event.key == pygame.K_ESCAPE:  # ESC 키를 누르면
                    return 'menu'  # 'menu' 반환

        keys = pygame.key.get_pressed()  # 키 입력 상태를 가져옵니다.
        if keys[pygame.K_LEFT] and player_x > 0:  # 왼쪽 화살표 키를 누르고 플레이어가 화면 왼쪽 경계를 넘지 않으면
            player_x -= player_speed  # 플레이어를 왼쪽으로 이동
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:  # 오른쪽 화살표 키를 누르고 플레이어가 화면 오른쪽 경계를 넘지 않으면
            player_x += player_speed  # 플레이어를 오른쪽으로 이동

        if random.randint(0, 20) == 1:  # 랜덤한 확률로 장애물을 생성합니다.
            create_obstacle()  # 장애물 생성

        move_obstacles(obstacle_list, obstacle_speed)  # 장애물을 이동시킵니다.

        for obstacle in obstacle_list:  # 각 장애물을 순회
            if detect_collision((player_x, player_y), obstacle):  # 충돌 감지
                return 'game_over'  # 'game_over' 반환

        for obstacle in obstacle_list:  # 각 장애물을 순회
            pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))  # 장애물을 그립니다.

        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))  # 플레이어를 그립니다.

        score_text = font.render("Score: {}".format(score), True, WHITE)  # 점수 텍스트 생성
        screen.blit(score_text, (10, 10))  # 점수를 화면에 그립니다.

        score += 1  # 점수 증가

        pygame.display.flip()  # 화면을 업데이트합니다.
        clock.tick(30)  # 프레임 속도를 설정합니다.

# 메인 실행 부분
while True:
    obstacle_speed = select_difficulty()  # 난이도 선택 화면 호출
    if obstacle_speed is None:  # 난이도가 None이면
        break  # 루프 종료
    result = game_loop(obstacle_speed)  # 게임 루프 실행
    if result == 'menu':  # 'menu' 반환 시
        continue  # 난이도 선택 화면으로 돌아갑니다.
    elif result == 'game_over':  # 'game_over' 반환 시
        decision = game_over()  # 게임 오버 화면 호출
        if decision == 'retry':  # 'retry' 반환 시
            continue  # 난이도 선택 화면으로 돌아갑니다.
        else:
            break  # 루프 종료

pygame.quit()  # Pygame 종료
