import pygame
import random
import time
from datetime import datetime

# 1. 초기화
pygame.init()

# 2. 게임 화면 설정
size = [400, 900]
screen = pygame.display.set_mode(size)

title = "Pygame Ex"
pygame.display.set_caption(title)

# 3. 게임 내부에서의 설정 
clock = pygame.time.Clock()

class Object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def add_img(self,address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else :
            self.img = pygame.image.load(address)
            
        self.size_x,self.size_y = self.img.get_size()    
        
    def change_size(self,size_x,size_y):
        self.img = pygame.transform.scale(self.img,(size_x,size_y))
        self.size_x,self.size_y = self.img.get_size()
    
    def show(self):
        screen.blit(self.img,(self.x,self.y))

# 충돌 감지
def crash(a, b):
    if b.x >= a.x - b.size_x and b.x <= a.x + a.size_x:
        if b.y >= a.y - b.size_y and b.y <= a.y + a.size_y:
            return True
        else:
            return False
    return False
        
# 주인공 생성
spaceShip = Object()
spaceShip.add_img("C:/Users/Administrator/Pictures/pygame/spaceship.jpg")
spaceShip.change_size(50,80)
spaceShip.x = round(size[0] / 2) - round(spaceShip.size_x/2)
spaceShip.y = size[1] - spaceShip.size_y - 20
spaceShip.move = 8

left_move = False
right_move = False
space_move = False

black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)
red = (255,0,0)

k = 0

# 점수 변수
score = 0 # 미사일로 적 처치 시 증가
miss = 0 # 적이 화면 밖으로 나가면 증가

missile_list = []
enemy_list = []

wait_exit = True
game_over = False
system_exit = 0

# 시작 전 대기
while wait_exit:
    clock.tick(60)
#     입력장치 감지
    for event in pygame.event.get():
#         키보드 누를 때
        if event.type == pygame.KEYDOWN:
#             스페이스바 누르면 대기 종료
            if event.key == pygame.K_SPACE:
                wait_exit = False
#         종료버튼 누를 때 바로 종료
        elif event.type == pygame.QUIT:
            wait_exit = False
            system_exit = 1
            break
    
#     배경색 설정
    screen.fill(black)
    
#     시작 안내문 표시
    font = pygame.font.Font("AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc",20)
    text = font.render("Press Space !", True, white)
    screen.blit(text, (size[0]/2 - 60,size[1]/2 - 10))
    
#     설정 업데이트
    pygame.display.flip()
    
# 4. 메인이벤트
start_time = datetime.now()
while system_exit == 0:
#     print("score : {}".format(score))
#     print("miss : {}".format(miss))

    # 4-1. FPS(Frame per second) 설정
    clock.tick(60)
    
    # 4-2. 입력장치의 감지
    for event in pygame.event.get():
#         종료버튼 누를 때
        if event.type == pygame.QUIT:
            system_exit = 1
        
#         키보드 누를 때
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_move = True
            elif event.key == pygame.K_RIGHT:
                right_move = True
            elif event.key == pygame.K_SPACE:
                space_move = True
                k = 0
                
#         키보드 뗄 때
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_move = False
            elif event.key == pygame.K_RIGHT:
                right_move = False        
            elif event.key == pygame.K_SPACE:
                space_move = False
                
    # 4-3. 입력, 시간에 따른 변화
#     게임 시간 처리
    current_time = datetime.now()
    delta_time = round((current_time - start_time).total_seconds(),2)
    
    if left_move == True:
        spaceShip.x -= spaceShip.move
        if spaceShip.x <= 0:
            spaceShip.x = 0
    elif right_move == True:
        spaceShip.x += spaceShip.move
        if spaceShip.x >= size[0] - spaceShip.size_x:
            spaceShip.x = size[0] - spaceShip.size_x
    
#     미사일 생성
    if space_move == True and k % 12 == 0:
        missile = Object()
        missile.add_img("C:/Users/Administrator/Pictures/pygame/missile.png")
        missile.change_size(10,20)
        missile.x = round(spaceShip.x + spaceShip.size_x/2 - missile.size_x/2)
        missile.y = spaceShip.y - missile.size_y - 10
        missile.move = 13
        missile_list.append(missile)
        
    k += 1
    
#     1.5% 확률로 적 생성
    if random.random() > 0.985:
        enemy = Object()
        enemy.add_img("C:/Users/Administrator/Pictures/pygame/enemy.png")
        enemy.change_size(40,40)
        enemy.x = random.randrange(0,size[0] - enemy.size_x - round(spaceShip.size_x/2))
        enemy.y = 15
        enemy.move = 8
        enemy_list.append(enemy)
        
#     삭제시킬 객체를 담은 리스트
    enemy_del_list = []
    missile_del_list = []
    
#     화면에서 벗어나면 미사일 삭제
    for i in range(len(missile_list)):
        m = missile_list[i]
        m.y -= m.move
#         화면에서 벗어나면 삭제시킬 리스트에 객체를 담는다.
        if m.y <= -m.size_y:
            missile_del_list.append(m)
    
#     화면에서 벗어나면 적 삭제
#     놓친 적 카운트 증가
    for i in range(len(enemy_list)):
        e = enemy_list[i]
        e.y += e.move
        if e.y >= size[1]:
            enemy_del_list.append(e)
            miss += 1
    
#     주인공과 적 충돌
    for e in enemy_list:
        if crash(spaceShip, e):
            time.sleep(0.5) # 0.5초간 일시정지
            system_exit = 1
            game_over = True
            
#     미사일과 적 충돌
#     충돌했을 때 객체 제거를 위해 제거 리스트에 추가
#     점수 증가
    for m in missile_list:
        for e in enemy_list:
            if crash(m, e):
                missile_del_list.append(m)
                enemy_del_list.append(e)
                score += 1
                
#     리스트의 중복 제거 set()함수 : list로 반환되지 않기 때문에 list로 다시 묶는다.
    missile_del_list = list(set(missile_del_list))
    enemy_del_list = list(set(enemy_del_list))

#     삭제시킬 객체 리스트로 각 객체를 삭제
# try : 시도 해보고 안되면 excopt : pass 한다.
    try:
#     삭제시킬 객체를 역순으로 재정렬 하고 삭제 : 역순처리 안하면 인덱스 오류 발생
        missile_del_list.reverse()
        for d in missile_del_list:
            missile_list.remove(d)
#             del missile_list[missile_list.index(d)] # remove 처럼 사용가능

        enemy_del_list.reverse()
        for d in enemy_del_list:
            enemy_list.remove(d)
    except:
        pass
        
    # 4-4. 전사작업(그리기)
    screen.fill(black)
    spaceShip.show()
    for m in missile_list:
        m.show()
    for e in enemy_list:
        e.show()
    
#     점수판 표시
#     font = pygame.font.Font("C:/Users/Administrator/AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc",20)
    font = pygame.font.Font("AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc",20)
    text_score = font.render("score : {}  miss : {}".format(score, miss), True, white)
    screen.blit(text_score, (10,10))
    
#   시간 표시
    text_time = font.render("Time : {}".format(delta_time), True, white)
    screen.blit(text_time, (10,50))
    
    # 4-5. 업데이트
    pygame.display.flip()
    
# 5. 종료
while game_over:
    clock.tick(60)
#     입력장치 감지
    for event in pygame.event.get():
#         종료버튼 누를 때 반복문 탈출
        if event.type == pygame.QUIT:
            game_over = False
    
#     배경색 설정
    screen.fill(white)
    
#     시작 안내문 표시
    font = pygame.font.Font("AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc",40)
    text = font.render("Game Over !", True, red)
    screen.blit(text, (size[0]/2 - 100,size[1]/2 - 10))
    
#     설정 업데이트
    pygame.display.flip()
    
    
pygame.quit()
