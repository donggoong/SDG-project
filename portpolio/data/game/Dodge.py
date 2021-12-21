import pygame
import os
import random
import pymysql
from tkinter.simpledialog import *
###############################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()
pygame.mixer.init()

# conn = pymysql.connect(host="localhost", user="root", password="1234", db="sdgproject", charset="utf8")

# 화면 크기 설정
screen_width = 480 # 가로 크기
screen_height = 640 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Dodge") # 게임 이름

# FPS
clock = pygame.time.Clock()

###############################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "./data/images")
sound_path = os.path.join(current_path, "./data/sound")
font_path = os.path.join(current_path, "./data/font")

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "dodge_background.png"))
background_scale = pygame.transform.scale(background, (480, 640))

# 배경음악 만들기
pygame.mixer.music.load(os.path.join(sound_path, "dodge_bgm.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(10)

# 폰트 정의
game_font = pygame.font.Font(os.path.join(font_path, "BMHANNAPro.ttf"), 20)
game_over_font = pygame.font.Font(os.path.join(font_path, "BRANCHÉ Demo.ttf"), 72)

# 게임 종료 메세지
game_result = "Game Over"

# 시간
start_ticks = pygame.time.get_ticks()

# 점수
dodge_total_score = 0

# 레벨
level_control = 10
total_level = 0
total_level_list = [10, 30, 50, 70, 90, 100, 120, 150, 180, 200, 250, 300, 350, 400, 10000000]

# 플레이어 만들기
player = pygame.image.load(os.path.join(image_path, "player.png"))
player_scale = pygame.transform.scale(player, (30, 30))
player_size = player_scale.get_rect().size
player_width = player_size[0]
player_height = player_size[1]
player_x_pos = (screen_width / 2) - (player_width / 2)
player_y_pos = (screen_height / 2) - (player_height / 2)
player_speed = 0.3
player_to_left = 0
player_to_right = 0
player_to_up = 0
player_to_down = 0

meteor_list = list()
class meteor_class:
    meteor = pygame.image.load(os.path.join(image_path, "meteor.png"))
    meteor_scale = pygame.transform.scale(meteor, (10, 10))
    meteor_size = meteor_scale.get_rect().size
    meteor_width = meteor_size[0]
    meteor_height = meteor_size[1]
    meteor_spawnPoint = None
    meteor_speed = 0
    meteor_x_pos = 0
    meteor_y_pos = 0
    meteor_rad = 0

    meteor_rect = meteor_scale.get_rect()
    meteor_rect.left = meteor_x_pos
    meteor_rect.top = meteor_y_pos

    def __init__(self):
        self.meteor_speed = random.choice([1, 1.2, 1.4, 1.6, 1.8, 2])
        self.meteor_spawnPoint = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

        # 스폰 지점 설정
        if self.meteor_spawnPoint == 'LEFT':
            self.meteor_x_pos = - self.meteor_width
            self.meteor_y_pos = random.randint(0, screen_height - self.meteor_height)
            self.meteor_rad = random.choice([(1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 0), (1, -3), (1, -2), (2, -2), (2, -1), (3, -1)])
        elif self.meteor_spawnPoint == 'RIGHT':
            self.meteor_x_pos = screen_width
            self.meteor_y_pos = random.randint(0, screen_height - self.meteor_height)
            self.meteor_rad = random.choice([(-1, 3), (-1, 2), (-2, 2), (-2, 1), (-3, 1), (-3, 0), (-1, -3), (-1, -2), (-2, -2), (-2, -1), (-3, -1)])
        elif self.meteor_spawnPoint == 'UP':
            self.meteor_x_pos = random.randint(0, screen_width - self.meteor_width)
            self.meteor_y_pos = - self.meteor_height
            self.meteor_rad = random.choice([(3, 1), (2, 1), (2, 2), (1, 2), (1, 3), (0, 3), (-3, 1), (-2, 1), (-2, 2), (-1, 2), (-1, 3)])
        elif self.meteor_spawnPoint == 'DOWN':
            self.meteor_x_pos = random.randint(0, screen_width - self.meteor_width)
            self.meteor_y_pos = screen_height
            self.meteor_rad = random.choice([(3, -1), (2, -1), (2, -2), (1, -2), (1, -3), (0, -3), (-3, -1), (-2, -1), (-2, -2), (-1, -2), (-1, -3)])


    def meteor_move(self):
        global dodge_total_score
        self.meteor_x_pos += self.meteor_speed * self.meteor_rad[0]
        self.meteor_y_pos += self.meteor_speed * self.meteor_rad[1]
        
        def boundary_UP():
            if self.meteor_y_pos < -self.meteor_height:
                return True
        
        def boundary_DOWN():
            if self.meteor_y_pos > screen_height:
                return True
        
        def boundary_LEFT():
            if self.meteor_x_pos < -self.meteor_width:
                return True
        
        def boundary_RIGHT():
            if self.meteor_x_pos > screen_width:
                return True

        if self.meteor_spawnPoint == 'UP':
            if boundary_LEFT() or boundary_RIGHT() or boundary_DOWN():
                meteor_list.remove(self)
                dodge_total_score += 1

        if self.meteor_spawnPoint == 'DOWN':
            if boundary_LEFT() or boundary_RIGHT() or boundary_UP():
                meteor_list.remove(self)
                dodge_total_score += 1

        if self.meteor_spawnPoint == 'LEFT':
            if boundary_UP() or boundary_DOWN() or boundary_RIGHT():
                meteor_list.remove(self)
                dodge_total_score += 1

        if self.meteor_spawnPoint == 'RIGHT':
            if boundary_UP() or boundary_DOWN() or boundary_LEFT():
                meteor_list.remove(self)
                dodge_total_score += 1

    def meteor_coll(self):
        self.meteor_rect = self.meteor_scale.get_rect()
        self.meteor_rect.left = self.meteor_x_pos
        self.meteor_rect.top = self.meteor_y_pos

running = True
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임수를 설정

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_to_left -= player_speed
            if event.key == pygame.K_RIGHT:
                player_to_right += player_speed
            if event.key == pygame.K_UP:
                player_to_up -= player_speed
            if event.key == pygame.K_DOWN:
                player_to_down += player_speed
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_to_left = 0
            elif event.key == pygame.K_RIGHT:
                player_to_right = 0
            elif event.key == pygame.K_UP:
                player_to_up = 0
            elif event.key == pygame.K_DOWN:
                player_to_down = 0
    # 3. 게임 캐릭터 위치 정의
    player_x_pos += (player_to_left + player_to_right) * dt
    player_y_pos += (player_to_up + player_to_down) * dt

    if player_x_pos < 0:
        player_x_pos = 0
    elif player_x_pos > screen_width - player_width:
        player_x_pos = screen_width - player_width
    if player_y_pos < 0:
        player_y_pos = 0
    elif player_y_pos > screen_height - player_height:
        player_y_pos = screen_height - player_height

    # 적 생성
    if dodge_total_score >= total_level_list[total_level]:
        total_level += 1

    if total_level + level_control >= len(meteor_list):
        meteor_list.append(meteor_class())

    # 4. 충돌 처리
    player_rect = player_scale.get_rect()
    player_rect.left = player_x_pos
    player_rect.top = player_y_pos

    for i in meteor_list:
        i.meteor_coll()
        if player_rect.colliderect(i.meteor_rect):
            running = False

    # 5. 화면에 그리기
    screen.blit(background_scale, (0, 0))
    screen.blit(player_scale, (player_x_pos, player_y_pos))

    for i in meteor_list:
        i.meteor_move()
        screen.blit(i.meteor_scale, (i.meteor_x_pos, i.meteor_y_pos)) 

    elapsed_time = (pygame.time.get_ticks() + start_ticks) / 1000
    timer = game_font.render("시간 : {}".format(int(elapsed_time)), True, (255, 255, 255))

    screen.blit(timer, (10, 10))

    score = game_font.render("피한 개수 : {}".format(str(int(dodge_total_score))), True, (255, 255, 255))
    screen.blit(score, (screen_width - 140, 10))
    
    pygame.display.update() 

msg = game_over_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)

'''
pygame.display.update()   
pygame.time.delay(2000)

username = askstring("랭킹","이름입력")
if username != "" and username != None:
    cur = conn.cursor()
    sql = "INSERT INTO dodge VALUES('" + str(username) + "','" + str(int(dodge_total_score)) + "','" + str(int(elapsed_time)) + "')";
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
else :
    pygame.quit()  
'''
pygame.quit()