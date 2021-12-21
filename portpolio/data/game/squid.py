import pygame
import os
import random
import pymysql
from tkinter.simpledialog import *
###############################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()
pygame.mixer.init()

conn = pymysql.connect(host="localhost", user="root", password="1234",
                       db="sdgproject", charset="utf8")

# 화면 크기 설정
screen_width = 480 # 가로 크기
screen_height = 640 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("오징어 게임") # 게임 이름

# FPS
clock = pygame.time.Clock()
###############################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")
sound_path = os.path.join(current_path, "sound")
font_path = os.path.join(current_path, "font")

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "squid_background.png"))
background_scale = pygame.transform.scale(background, (480, 640))

# 배경음악
pygame.mixer.music.load(os.path.join(sound_path, "squid_bgm.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_img = pygame.transform.scale(character, (25, 50))
character_size = character_img.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height
character_speed = 8

# 오징어 만들기
squid_list = list()
class squid_class:
    squid = pygame.image.load(os.path.join(image_path, "squid.png"))
    squid_scale = pygame.transform.scale(squid, (15, 30))
    squid_size = squid_scale.get_rect().size
    squid_width = squid_size[0]
    squid_height = squid_size[1]
    squid_x_pos = 0
    squid_y_pos = 0
    squid_speed = 0

    squid_rect = squid_scale.get_rect()
    squid_rect.left = squid_x_pos
    squid_rect.top = squid_y_pos\

    def __init__(self):
        self.squid_speed = random.randint(2, 7)
        self.squid_x_pos = random.randint(0, screen_width - self.squid_width)
        self.squid_y_pos = - self.squid_height

    def squid_move(self):
        self.squid_y_pos += self.squid_speed
        global squid_total_score

        if self.squid_y_pos > screen_height:
            squid_list.remove(self)
            squid_total_score += 1

    def squid_coll(self):
        self.squid_rect = self.squid_scale.get_rect()
        self.squid_rect.left = self.squid_x_pos
        self.squid_rect.top = self.squid_y_pos

# 폰트 정의
game_font = pygame.font.Font(os.path.join(font_path, "BMHANNAPro.ttf"), 20)
game_over_font = pygame.font.Font(os.path.join(font_path, "BRANCHÉ Demo.ttf"), 72)

# 게임 종료 메세지
game_result = "Game Over"

# 점수
squid_total_score = 0

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

    if squid_total_score >= total_level_list[total_level]:
        total_level += 1
    
    if total_level_list[total_level] == total_level_list[-1]:
        game_result = "Victory"
        running = False

    if total_level + level_control >= len(squid_list):
        squid_list.append(squid_class())

    # 4. 충돌 처리
    character_rect = character_img.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for i in squid_list:
        i.squid_coll()
        if character_rect.colliderect(i.squid_rect):
            running = False
    
    # 점수 계산
    score = game_font.render("피한 오징어 : {}".format(str(squid_total_score)), True, (255, 255, 255))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() + start_ticks) / 1000 # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시
    timer = game_font.render("시간 : {}".format(int(elapsed_time)), True, (255, 255, 255)) # 출력할 글자, True, 색상

    # 5. 화면에 그리기
    screen.blit(background_scale, (0, 0))
    screen.blit(timer, (10, 10))
    screen.blit(score, (10, 40))
    screen.blit(character_img, (character_x_pos, character_y_pos))
    for i in squid_list:
        i.squid_move()
        screen.blit(i.squid_scale, (i.squid_x_pos, i.squid_y_pos))

    pygame.display.update()
msg = game_over_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)

pygame.display.update()   
pygame.time.delay(2000)

username = askstring("랭킹","이름입력")
if username != "" and username != None:
    cur = conn.cursor()
    sql = "INSERT INTO squid VALUES('" + str(username) + "','" + str(int(squid_total_score)) + "','" + str(int(elapsed_time)) + "')";
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
else :
    pygame.quit()  

pygame.quit()