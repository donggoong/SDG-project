import tkinter as tk
from tkinter.simpledialog import *
from tkinter import *
import pygame
import os
import random
import pymysql
def dodge() :    
    ###############################################################
    # 기본 초기화 (반드시 해야 하는 것들)
    pygame.init()
    pygame.mixer.init()

    conn = pymysql.connect(host="127.0.0.1", user="root", password="1234",
                       db="sdgproject", charset="utf8")

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
    image_path = os.path.join(current_path, "data/images")
    sound_path = os.path.join(current_path, "data/sound")
    font_path = os.path.join(current_path, "data/font")

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
            nonlocal dodge_total_score
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

    pygame.display.update()   
    pygame.time.delay(2000)

    name = askstring("랭킹","이름입력")
    if name != "" and name != None:
        cur = conn.cursor()
        sql = "INSERT INTO dodge VALUES('" + str(name) + "','" + str(int(dodge_total_score)) + "','" + str(int(elapsed_time)) + "')";
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()   

    else :
        pygame.quit()  
    pygame.quit()

def dodge_ranking():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="1234",
                       db="sdgproject", charset="utf8")
    cur = conn.cursor()
    sql = "SELECT *, RANK() OVER (ORDER BY score DESC ) as rank from DODGE;";
    cur.execute(sql)

    resultlist = cur.fetchall()
    window=Tk()
    dodge_ranks = Listbox(window, width=35, height=10)
    dodge_ranks.grid(padx=5, pady=5, row = 4, column = 0, columnspan = 2)

    for result in resultlist:
        rank = result[3]
        name = result[0]
        score = result[1]
        time = result[2]
        info = "rank : {}, name : {}, score : {}, time : {}".format(rank, name, score, time)
        dodge_ranks.insert(END, info)

    cur.close()
    conn.commit()
    conn.close()

def dodge_rank_reset():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="1234",
                       db="sdgproject", charset="utf8")
    cur = conn.cursor()
    sql = "DELETE FROM dodge";
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

def squid() :
    ###############################################################
    # 기본 초기화 (반드시 해야 하는 것들)
    pygame.init()
    pygame.mixer.init()

    conn = pymysql.connect(host="127.0.0.1", user="root", password="1234",
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
    image_path = os.path.join(current_path, "data/images")
    sound_path = os.path.join(current_path, "data/sound")
    font_path = os.path.join(current_path, "data/font")

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
            nonlocal squid_total_score

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

    name = askstring("랭킹","이름입력")
    if name != "" and name != None:
        cur = conn.cursor()
        sql = "INSERT INTO squid VALUES('" + str(name) + "','" + str(int(squid_total_score)) + "','" + str(int(elapsed_time)) + "')";
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
    
    else :
        pygame.quit()
    pygame.quit()

def squid_ranking():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="1234",
                       db="sdgproject", charset="utf8")
    cur = conn.cursor()
    sql = "SELECT *, RANK() OVER (ORDER BY score DESC ) as rank from squid;";
    cur.execute(sql)

    resultlist = cur.fetchall()
    window=Tk()
    squid_ranks = Listbox(window, width=35, height=10)
    squid_ranks.grid(padx=5, pady=5, row = 4, column = 0, columnspan = 2)

    for result in resultlist:
        rank = result[3]
        name = result[0]
        score = result[1]
        time = result[2]
        info = "rank : {}, name : {}, score : {}, time : {}".format(rank, name, score, time)
        squid_ranks.insert(END, info)

    cur.close()
    conn.commit()
    conn.close()

def squid_rank_reset():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="1234",
                       db="sdgproject", charset="utf8")
    cur = conn.cursor()
    sql = "DELETE FROM squid";
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

class myApp():

    def switchFrame(self, classParam):
        if self.nowFrame:
            self.nowFrame.destroy()
        self.nowFrame = classParam
        self.nowFrame.grid()

    def __init__(self, window):
        self.nowFrame = None
        myMenu=tk.Menu(window)
        fileMenu=tk.Menu(myMenu)

        fileMenu.add_command(label="오징어게임",command=lambda:self.switchFrame(frameClass_1()))
        fileMenu.add_command(label="유성피하기",command=lambda:self.switchFrame(frameClass_2()))
        myMenu.add_cascade(label="Game", menu=fileMenu)

        window.config(menu=myMenu)
        window.mainloop()

class frameClass_1(tk.Frame):
    def __init__(self):
        super().__init__()
        button1 = Button(self, width = 10, height = 2, text = "오징어게임", command=squid)
        button1.grid(row =0 , column = 0)
        button2 = Button(self, width = 10, height = 2, text = "순위 보기", command=squid_ranking)
        button2.grid(row =0 , column = 1)
        button3 = Button(self, width = 10, height = 2, text = "초기화", command=squid_rank_reset)
        button3.grid(row =1 , column = 0)
        button4 = Button(self, width = 10, height = 2, text = "종료", command=exit)
        button4.grid(row =1 , column = 1)

class frameClass_2(tk.Frame):
    def __init__(self):
        super().__init__()
        button1 = Button(self, width = 10, height = 2, text = "유성피하기", command=dodge)
        button1.grid(row =0 , column = 0)
        button2 = Button(self, width = 10, height = 2, text = "순위 보기", command=dodge_ranking)
        button2.grid(row =0 , column = 1)
        button3 = Button(self, width = 10, height = 2, text = "초기화", command=dodge_rank_reset)
        button3.grid(row =1 , column = 0)
        button4 = Button(self, width = 10, height = 2, text = "종료", command=exit)
        button4.grid(row =1 , column = 1)

window = tk.Tk()
window.title('포트폴리오')
Label1 = Label(window, width = 40, height = 1, text = "오락실에 오신걸 환영합니다.")
Label1.grid()
Label2 = Label(window, width = 40, height = 1, text = "Game탭을 이용하세요.")
Label2.grid()
myApp(window)
