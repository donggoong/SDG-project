import pygame
import os
import random

from pygame import rect
###############################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 480 # 가로 크기
screen_height = 640 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("똥 피하기 게임") # 게임 이름

# FPS
clock = pygame.time.Clock()
###############################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))
background_scale = pygame.transform.scale(background, (480, 640))

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_img = pygame.transform.scale(character, (40, 40))
character_size = character_img.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height
character_speed = 10

# 똥 만들기
ddong_list = list()
class ddong_class:
    ddong = pygame.image.load(os.path.join(image_path, "ddong.png"))
    ddong_scale = pygame.transform.scale(ddong, (30, 30))
    ddong_size = ddong_scale.get_rect().size
    ddong_width = ddong_size[0]
    ddong_height = ddong_size[1]
    ddong_x_pos = 0
    # ddong_x_pos = random.randint(0, screen_width - ddong_width)
    ddong_y_pos = 0
    ddong_speed = 0
    # ddong_speed = random.randint(5, 10)

    ddong_rect = ddong_scale.get_rect()
    ddong_rect.left = ddong_x_pos
    ddong_rect.top = ddong_y_pos\
    # ddong_rect = pygame.Rect(ddong_scale.get_rect())
    # ddong_rect.left = random.randint(0, screen_width - ddong_width)

    def __init__(self):
        self.ddong_speed = random.randint(5, 10)
        self.ddong_x_pos = random.randint(0, screen_width - self.ddong_width)
        self.ddong_y_pos = - self.ddong_height

    def ddong_move(self):
        self.ddong_y_pos += self.ddong_speed
        global total_score

        if self.ddong_y_pos > screen_height:
            ddong_list.remove(self)
            total_score += 1

    def ddong_coll(self):
        self.ddong_rect = self.ddong_scale.get_rect()
        self.ddong_rect.left = self.ddong_x_pos
        self.ddong_rect.top = self.ddong_y_pos


# 폰트 정의
game_font = pygame.font.SysFont("malgungothic", 40) # 폰트 객체 생성 (폰트, 크기)

# 점수
total_score = 0

# 레벨
level_control = 10
total_level = 0
total_level_list = [10, 30, 50, 70, 90, 100, 120, 150, 180, 200, 250, 300, 350, 400, 10000000]

# 시작 시간
start_ticks = pygame.time.get_ticks()

# 이동 위치
to_x_left = 0
to_x_right = 0

running = True
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임수를 설정

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x_left -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x_right += character_speed
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_x_left = 0
            elif event.key == pygame.K_RIGHT:
                to_x_right = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += to_x_left + to_x_right

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width - character_width):
        character_x_pos = (screen_width - character_width)

    if total_score >= total_level_list[total_level]:
        total_level += 1

    if total_level + level_control >= len(ddong_list):
        ddong_list.append(ddong_class())

    # 4. 충돌 처리
    character_rect = character_img.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for i in ddong_list:
        i.ddong_coll()
        if character_rect.colliderect(i.ddong_rect):
            print("충돌")
            print("점수 : ", total_score)
            running = False

    # if character_rect.colliderect(ddong_rect):
    #     print("충돌했습니다.")
    #     running = False
    
    # 점수 계산
    score = game_font.render("score : {}".format(str(total_score)), True, (255, 255, 255))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() + start_ticks) / 1000 # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시
    timer = game_font.render("Time : {}".format(int(elapsed_time)), True, (255, 255, 255)) # 출력할 글자, True, 색상

    # 5. 화면에 그리기
    screen.blit(background_scale, (0, 0))
    screen.blit(timer, (10, 10))
    screen.blit(score, (10, 50))
    screen.blit(character_img, (character_x_pos, character_y_pos))
    for i in ddong_list:
        i.ddong_move()
        screen.blit(i.ddong_scale, (i.ddong_x_pos, i.ddong_y_pos))
    # screen.blit(ddong_scale, (ddong_x_pos, ddong_y_pos))

    pygame.display.update()

pygame.quit()