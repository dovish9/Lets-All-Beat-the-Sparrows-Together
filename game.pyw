#Let's All Beat the Sparrows Together
#주석은 항상 아래에 다는 것을 원칙으로 함
#디버깅: 대미지 비례상수, 무적, 파워아이템, 웨이브 길이 (default로 검색 가능) / path 저장 / 좌표 출력
#통계
# 점수
# 이동한 거리, 점프한 횟수, 해로운 새와의 충돌 횟수, 투사체와의 충돌 횟수, 받은 피해
# 돌을 날린 횟수, 명중한 횟수, (명중률)
# 죽인 해로운 새 수, 죽인 정예 해로운 새 수, 보너스 해로운 새 처치 여부
# 먹은 포션 개수, 먹은 뚱캔 개수, 파워아이템 획득 여부
# 건물 철거 여부, 우두머리 해로운 새 처치 여부
# 건물, 우두머리 해로운 새를 처치하는 데 걸린 시간
# 게임이 끝날 때 웨이브, 밀밭 잔여 내구도
import pygame, sys
from pygame.locals import *
# pygame.locals : pygame에서 사용하는 상수
import random as r
import math as m
import numpy as np #긴 배열 외부 저장
import os #커서 사진(reticle.png)이 계속 안 열려서 스택오버플로우에서 하라는 대로 경로 지정

current_path = os.path.dirname(__file__) # Where your .py file is located
# image_path = os.path.join(current_path, 'array') # The array folder path
font_path = os.path.join(current_path, 'font') # The font folder path

WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
#윈도우 창 크기 설정을 위한 변수
isFullscreen = False
#전체화면 상태
if not isFullscreen:
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    #0,32는 수정하지 않음
else:
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
pygame.display.set_caption('다같이 참새를 때려잡자') #게임창 상단 글씨

while True:
    pygame.init()
    #초기화

    mainClock = pygame.time.Clock()
    #시계는 똑딱똑딱

    powerOverwhelming = False #무적 default: False
    timesDamage = 1 #데미지를 비례해서 증가시킴 default: 1
    #디버깅

    statistics_score = 0
    statistics_movingDistance = 0
    statistics_jumpCount = 0
    statistics_collideEnemyCount = 0
    statistics_collideProjectileCount = 0
    statistics_receivedDamage = 0
    statistics_throwingCount = 0
    statistics_hitCount = 0
    statistics_accuracy = 0 #크레딧에서의 통계와 데이터베이스 기록에서는 제외됨
    statistics_killEnemyCount = 0
    statistics_killEliteenemyCount = 0
    statistics_killDove = False
    statistics_killRaven = False
    statistics_killCrane = False
    statistics_killPelican = False
    statistics_killParrot = False
    statistics_drinkPotionCount = 0
    statistics_drinkPotionLargeCount = 0
    statistics_acquirePenetrable = False
    statistics_acquireShotgun = False
    statistics_acquireQuickcharge = False
    statistics_destroySpire = False
    statistics_destroyGreaterspire = False
    statistics_killHumanfacedbird = False
    statistics_killMedivh = False
    statistics_timeToDestroySpire = 0
    statistics_timeToDestroyGreaterspire = 0
    statistics_timeToKillHumanfacedbird = 0
    statistics_timeToKillMedivh = 0
    statistics_lastWave = 0
    statistics_remainWheatDurability = 0
    #통계, 도합 31개, accuracy 제외 30개

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    PINK = (255,0,255)
    ORANGE = (255, 127, 0)
    OCHER = (218, 165, 32)
    #색

    S_LOGO = 1
    S_MENU = 2
    S_MENU_SCOREBOARD = 3
    S_OPTION = 4
    S_CONTROLS = 5
    S_PROLOGUE = 6
    S_PARROT = 7
    S_GAME = 8
    S_GAME_OPTION = 9
    S_GAME_CONTROLS = 10
    S_DEATH = 11
    S_DEATH_EPILOGUE = 12
    S_VICTORY = 13
    S_VICTORY_EPILOGUE = 14
    S_CREDIT = 15
    S_SCOREBOARD = 16
    S_RESTART = 0
    #게임의 상태를 구분하는 변수

    MOVESPEED_HORIZONTAL = 6
    MOVESPEED_VERTICAL = 3
    GRAVITY = 1
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    moving = False
    jump = False
    mousebuttondown = False
    #움직임

    penetrable = False #default: False
    shotgun = False #default: False
    quickcharge = 1 #default: 1
    #아이템 능력치

    pygame.mouse.set_visible(False)
    reticleImage = pygame.image.load(os.path.join(current_path, 'img/reticle.png')).convert_alpha()
    def renderReticle():
        windowSurface.blit(reticleImage, (pygame.mouse.get_pos()[0]-16, pygame.mouse.get_pos()[1]-16))
    #마우스

    basicFont = pygame.font.SysFont(os.path.join(font_path, 'malgungothic'), 48)
    arcadeFont64 = pygame.font.Font(os.path.join(font_path, "ArcadeClassic.ttf"), 64)
    arcadeFont48 = pygame.font.Font(os.path.join(font_path, "ArcadeClassic.ttf"), 48)
    arcadeFont46 = pygame.font.Font(os.path.join(font_path, "ArcadeClassic.ttf"), 46)
    arcadeFont36 = pygame.font.Font(os.path.join(font_path, "ArcadeClassic.ttf"), 36)
    arcadeFont35 = pygame.font.Font(os.path.join(font_path, "ArcadeClassic.ttf"), 35)
    dunggeunmo64 = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 64)
    dunggeunmo48 = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 48)
    dunggeunmo36 = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 36)
    dunggeunmo24 = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 24)
    dunggeunmo22 = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 22)
    dunggeunmo12 = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 12)
    #폰트 설정

    logo_text48 = arcadeFont48.render('Lets  All  Beat  the  Sparrows  Together', True, PINK)
    logo_text48Rect = logo_text48.get_rect()
    logo_text48Rect.centerx = windowSurface.get_rect().centerx
    logo_text48Rect.centery = 40
    alpha_img = pygame.Surface(logo_text48.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    logo_text48.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    #범용 로고 텍스트 48

    logo_text46 = arcadeFont46.render('Lets  All  Beat  the  Sparrows  Together', True, PINK)
    logo_text46Rect = logo_text46.get_rect()
    logo_text46Rect.centerx = windowSurface.get_rect().centerx
    logo_text46Rect.centery = 40
    alpha_img = pygame.Surface(logo_text46.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    logo_text46.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    #범용 로고 텍스트 46

    arrow = 0
    arrow_text = dunggeunmo64.render('→', True, OCHER)
    arrow_textRect = arrow_text.get_rect()
    arrow_textRect.right = 360
    arrow_textRect.centery = 160
    #화살표 텍스트

    logoImage = pygame.image.load(os.path.join(current_path, 'img/logo.png')).convert_alpha()
    logoRect = pygame.Rect(0, 0, 408, 600) #변수 중 처음 두 개가 위치, 나중 두 개가 크기
    logoRect.centerx = windowSurface.get_rect().centerx
    logoRect.centery = windowSurface.get_rect().centery
    #로고 이미지

    logo_text_0 = arcadeFont64.render('Lets  All  Beat  the  Sparrows  Together', True, PINK)
    logo_textRect_0 = logo_text_0.get_rect()
    logo_textRect_0.right = 0
    logo_textRect_0.centery = windowSurface.get_rect().centery
    alpha_img = pygame.Surface(logo_text_0.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    logo_text_0.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    #로고 상단 텍스트

    logo_text_1 = arcadeFont36.render('press  ENTER  to  start  the  game', True, ORANGE)
    logo_textRect_1 = logo_text_1.get_rect()
    logo_textRect_1.centerx = windowSurface.get_rect().centerx
    logo_textRect_1.centery = windowSurface.get_rect().centery+320
    alpha_img = pygame.Surface(logo_text_1.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    logo_text_1.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    #로고 하단 텍스트 36

    logo_text_2 = arcadeFont35.render('press  ENTER  to  start  the  game', True, ORANGE)
    logo_textRect_2 = logo_text_2.get_rect()
    logo_textRect_2.centerx = windowSurface.get_rect().centerx
    logo_textRect_2.centery = windowSurface.get_rect().centery+320
    alpha_img = pygame.Surface(logo_text_2.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    logo_text_2.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    #로고 하단 텍스트 35

    menu_text_1 = dunggeunmo64.render('START NEW GAME', True, OCHER, BLACK)
    menu_textRect_1 = menu_text_1.get_rect()
    menu_textRect_1.centerx = windowSurface.get_rect().centerx
    menu_textRect_1.centery = windowSurface.get_rect().centery-200
    menu_text_2 = dunggeunmo64.render('SCOREBOARD', True, OCHER, BLACK)
    menu_textRect_2 = menu_text_2.get_rect()
    menu_textRect_2.centerx = windowSurface.get_rect().centerx
    menu_textRect_2.centery = windowSurface.get_rect().centery
    menu_text_3 = dunggeunmo64.render('OPTION', True, OCHER, BLACK)
    menu_textRect_3 = menu_text_3.get_rect()
    menu_textRect_3.centerx = windowSurface.get_rect().centerx
    menu_textRect_3.centery = windowSurface.get_rect().centery+200
    #메뉴 텍스트

    menu_lineNumber = 0
    menu_lineNumbers = [] #각 데이터의 점수 부분 라인 넘버
    menu_scores_made = False
    menu_scores = []
    menu_scoreboardRect_made = False
    menu_usernames = []
    menu_usernames_text = []
    menu_usernames_textRect = []
    menu_scores_text = []
    menu_scores_textRect = []
    backtothemenu_text = arcadeFont36.render('BACK TO THE MENU', True, OCHER, BLACK)
    backtothemenu_textRect = backtothemenu_text.get_rect()
    backtothemenu_textRect.right = windowSurface.get_rect().right
    backtothemenu_textRect.bottom = windowSurface.get_rect().bottom
    #메뉴 점수판

    option_text_1 = dunggeunmo64.render('CONTROLS', True, OCHER, BLACK)
    option_textRect_1 = option_text_1.get_rect()
    option_textRect_1.centerx = windowSurface.get_rect().centerx
    option_textRect_1.centery = windowSurface.get_rect().centery-200
    option_text_2 = dunggeunmo64.render('BACK TO THE MENU', True, OCHER, BLACK)
    option_textRect_2 = option_text_2.get_rect()
    option_textRect_2.centerx = windowSurface.get_rect().centerx
    option_textRect_2.centery = windowSurface.get_rect().centery
    option_text_3 = dunggeunmo64.render('QUIT', True, OCHER, BLACK)
    option_textRect_3 = option_text_3.get_rect()
    option_textRect_3.centerx = windowSurface.get_rect().centerx
    option_textRect_3.centery = windowSurface.get_rect().centery+200
    #옵션 텍스트

    controls_text = dunggeunmo48.render('OKAY', True, OCHER, BLACK)
    controls_textRect = controls_text.get_rect()
    controls_textRect.centerx = windowSurface.get_rect().centerx
    controls_textRect.centery = windowSurface.get_rect().centery+300
    #컨트롤 텍스트

    controlsImage = pygame.image.load(os.path.join(current_path, 'img/controls_guideline.png')).convert_alpha()
    controlsRect = controlsImage.get_rect()
    controlsRect.centerx = windowSurface.get_rect().centerx
    controlsRect.centery = windowSurface.get_rect().centery
    #컨트롤 이미지

    prologueImage_1 = pygame.image.load(os.path.join(current_path, 'img/storyline/prologue_1.png')).convert_alpha()
    prologueRect_1 = pygame.Rect(0, 0, 468, 210)
    prologueImage_1_0 = pygame.image.load(os.path.join(current_path, 'img/winnie-the-pooh.png')).convert_alpha()
    prologueRect_1_0 = pygame.Rect(1000, 545, 50, 28)
    prologueImage_2 = pygame.image.load(os.path.join(current_path, 'img/storyline/prologue_2.png')).convert_alpha()
    prologueRect_2 = pygame.Rect(0, 0, 468, 212)
    prologueImage_3 = pygame.image.load(os.path.join(current_path, 'img/storyline/prologue_3.png')).convert_alpha()
    prologueRect_3 = pygame.Rect(0, 0, 468, 302)
    prologueImage_4 = pygame.image.load(os.path.join(current_path, 'img/storyline/prologue_4.png')).convert_alpha()
    prologueRect_4 = pygame.Rect(0, 0, 468, 247)
    prologueImage_5 = pygame.image.load(os.path.join(current_path, 'img/storyline/prologue_5.png')).convert_alpha()
    prologueRect_5 = pygame.Rect(0, 0, 468,109)
    prologueImage_6 = pygame.image.load(os.path.join(current_path, 'img/chinaflag.png')).convert_alpha()
    prologueRect_6 = pygame.Rect(0, 0, 360,339)
    prologueRect_1.centerx = windowSurface.get_rect().centerx
    prologueRect_1.centery = windowSurface.get_rect().centery
    prologueRect_2.centerx = windowSurface.get_rect().centerx
    prologueRect_2.centery = windowSurface.get_rect().centery
    prologueRect_3.centerx = windowSurface.get_rect().centerx
    prologueRect_3.centery = windowSurface.get_rect().centery
    prologueRect_4.centerx = windowSurface.get_rect().centerx
    prologueRect_4.centery = windowSurface.get_rect().centery
    prologueRect_5.centerx = windowSurface.get_rect().centerx
    prologueRect_5.centery = windowSurface.get_rect().centery
    prologueRect_6.centerx = windowSurface.get_rect().centerx
    prologueRect_6.centery = windowSurface.get_rect().centery
    prologueImage = [prologueImage_1, prologueImage_2, prologueImage_3, prologueImage_4, prologueImage_5, prologueImage_6]
    prologueRect = [prologueRect_1, prologueRect_2, prologueRect_3, prologueRect_4, prologueRect_5, prologueRect_6]
    #프롤로그 이미지

    prologue_text_1 = dunggeunmo24.render('Every human being has a finger even if he is a Winnie-the-Pooh.', True, WHITE)
    prologue_textRect_1 = prologue_text_1.get_rect()
    prologue_text_2_1 = dunggeunmo24.render("Instruct; point out; direct; guide; all of them consist of a word \"finger\".", True, WHITE)
    prologue_textRect_2_1 = prologue_text_2_1.get_rect()
    prologue_text_2_2 = dunggeunmo24.render("When asked who is their hero to the Chinese who have produced many historical figures,", True, WHITE)
    prologue_textRect_2_2 = prologue_text_2_2.get_rect()
    prologue_text_2_3 = dunggeunmo24.render("most of them refer to portraits of Mao Tse-dong.", True, WHITE)
    prologue_textRect_2_3 = prologue_text_2_3.get_rect()
    prologue_text_3_1 = dunggeunmo24.render("Mao Tse-dong traveled to the Chinese continent in his dreamy youth.", True, WHITE)
    prologue_textRect_3_1 = prologue_text_3_1.get_rect()
    prologue_text_3_2 = dunggeunmo24.render("What is the way for 8 billion people to live in decline and cultural destruction?", True, WHITE)
    prologue_textRect_3_2 = prologue_text_3_2.get_rect()
    prologue_text_3_3 = dunggeunmo24.render("This was his young concern.", True, WHITE)
    prologue_textRect_3_3 = prologue_text_3_3.get_rect()
    prologue_text_4 = dunggeunmo24.render('Later he ordered everything with his fingers.', True, WHITE)
    prologue_textRect_4 = prologue_text_4.get_rect()
    prologue_text_5 = dunggeunmo48.render('XX', True, WHITE)
    prologue_textRect_5 = prologue_text_5.get_rect()
    prologue_text_6_1 = dunggeunmo48.render('그리하여', True, WHITE)
    prologue_textRect_6_1 = prologue_text_6_1.get_rect()
    prologue_text_6_2 = dunggeunmo48.render('위대한 중화인민공화국의 홍위병은', True, WHITE)
    prologue_textRect_6_2 = prologue_text_6_2.get_rect()
    prologue_text_6_3 = dunggeunmo48.render('중국인민지원군의 곡미를 갉아먹는', True, WHITE)
    prologue_textRect_6_3 = prologue_text_6_3.get_rect()
    prologue_text_6_4 = dunggeunmo48.render('흉조를 박멸하기 위해', True, WHITE)
    prologue_textRect_6_4 = prologue_text_6_4.get_rect()
    prologue_text_6_5 = dunggeunmo48.render('홀로 여정을 떠나게 된다.', True, WHITE)
    prologue_textRect_6_5 = prologue_text_6_5.get_rect()
        #텍스트 생성
    prologue_text = [[prologue_text_1],
                     [prologue_text_2_1, prologue_text_2_2, prologue_text_2_3],
                     [prologue_text_3_1, prologue_text_3_2, prologue_text_3_3],
                     [prologue_text_4],
                     [prologue_text_5],
                     [prologue_text_6_1, prologue_text_6_2, prologue_text_6_3, prologue_text_6_4, prologue_text_6_5]]
    prologue_textRect = [[prologue_textRect_1],
                         [prologue_textRect_2_1, prologue_textRect_2_2, prologue_textRect_2_3],
                         [prologue_textRect_3_1, prologue_textRect_3_2, prologue_textRect_3_3],
                         [prologue_textRect_4],
                         [prologue_textRect_5],
                         [prologue_textRect_6_1, prologue_textRect_6_2, prologue_textRect_6_3, prologue_textRect_6_4, prologue_textRect_6_5]]
        #배열
    prologue_textRect_1.centerx = windowSurface.get_rect().centerx
    prologue_textRect_1.centery = windowSurface.get_rect().centery+200
    prologue_textRect_2_1.centerx = windowSurface.get_rect().centerx
    prologue_textRect_2_1.centery = windowSurface.get_rect().centery+180
    prologue_textRect_2_2.centerx = windowSurface.get_rect().centerx
    prologue_textRect_2_2.centery = windowSurface.get_rect().centery+200
    prologue_textRect_2_3.centerx = windowSurface.get_rect().centerx
    prologue_textRect_2_3.centery = windowSurface.get_rect().centery+220
    prologue_textRect_3_1.centerx = windowSurface.get_rect().centerx
    prologue_textRect_3_1.centery = windowSurface.get_rect().centery+180
    prologue_textRect_3_2.centerx = windowSurface.get_rect().centerx
    prologue_textRect_3_2.centery = windowSurface.get_rect().centery+200
    prologue_textRect_3_3.centerx = windowSurface.get_rect().centerx
    prologue_textRect_3_3.centery = windowSurface.get_rect().centery+220
    prologue_textRect_4.centerx = windowSurface.get_rect().centerx
    prologue_textRect_4.centery = windowSurface.get_rect().centery+200
    prologue_textRect_5.centerx = windowSurface.get_rect().centerx
    prologue_textRect_5.centery = windowSurface.get_rect().centery+200
    prologue_textRect_6_1.centerx = windowSurface.get_rect().centerx
    prologue_textRect_6_1.centery = windowSurface.get_rect().centery-200
    prologue_textRect_6_2.centerx = windowSurface.get_rect().centerx
    prologue_textRect_6_2.centery = windowSurface.get_rect().centery-100
    prologue_textRect_6_3.centerx = windowSurface.get_rect().centerx
    prologue_textRect_6_3.centery = windowSurface.get_rect().centery
    prologue_textRect_6_4.centerx = windowSurface.get_rect().centerx
    prologue_textRect_6_4.centery = windowSurface.get_rect().centery+100
    prologue_textRect_6_5.centerx = windowSurface.get_rect().centerx
    prologue_textRect_6_5.centery = windowSurface.get_rect().centery+200
        #위치 조정
    alpha_img = pygame.Surface(prologue_text_1.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_1.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_2_1.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_2_1.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_2_2.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_2_2.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_2_3.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_2_3.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_3_1.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_3_1.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_3_2.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_3_2.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_3_3.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_3_3.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_4.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_4.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_5.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_5.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_6_1.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_6_1.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_6_2.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_6_2.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_6_3.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_6_3.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_6_4.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_6_4.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    alpha_img = pygame.Surface(prologue_text_6_5.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    prologue_text_6_5.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        #투명 배경
    prologueDict = {prologue_text_1:prologue_textRect_1, prologue_text_2_1:prologue_textRect_2_1, prologue_text_2_2:prologue_textRect_2_2,
                    prologue_text_2_3:prologue_textRect_2_3, prologue_text_3_1:prologue_textRect_3_1, prologue_text_3_2:prologue_textRect_3_2,
                    prologue_text_3_3:prologue_textRect_3_3, prologue_text_4:prologue_textRect_4, prologue_text_5:prologue_textRect_5,
                    prologue_text_6_1:prologue_textRect_6_1, prologue_text_6_2:prologue_textRect_6_2, prologue_text_6_3:prologue_textRect_6_3,
                    prologue_text_6_4:prologue_textRect_6_4, prologue_text_6_5:prologue_textRect_6_5}
        #반복문을 위한 딕셔너리
    #프롤로그 텍스트 1~6

    ParrotImage = pygame.image.load(os.path.join(current_path, 'img/parrot.png')).convert_alpha() #보너스 해로운 새 앵무새와 겹쳐서 첫 글자 대문자로
    parrotRect = pygame.Rect(390, 200, 500, 520)
    parrotSpriteImage = pygame.image.load(os.path.join(current_path, 'img/parrot_sprite.png')).convert_alpha()
    parrotSpriteRect = pygame.Rect(390, 200, 343, 301)
    #앵무새 이미지

    parrot_text = dunggeunmo64.render('WHISHING-PARROT present', True, GREEN)
    parrot_textRect = parrot_text.get_rect()
    alpha_img = pygame.Surface(parrot_text.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    parrot_text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    parrot_textRect.centerx = windowSurface.get_rect().centerx
    parrot_textRect.centery = 150
    #앵무새 텍스트

    bgImage = pygame.image.load(os.path.join(current_path, 'img/background/Game_play.png')).convert_alpha()
    bgRect = pygame.Rect(-2000,0,1280,720)
    #배경

    cloudsImage = []
    for i in range(1, 6, 1):
        cloudsImage.append(pygame.image.load(os.path.join(current_path, 'img/background/cloud{}.png'.format(i))).convert_alpha())
    cloudsRect = []
    randomDict = {0:0, 1:3, 2:1, 3:5, 4:8}
    for i in range(5):
        cloudsRect.append(pygame.Rect(1280-randomDict[i]*160,50+25*i,158,158))
    #구름

    player_headingRight = True
    playersImage_Idle = [pygame.image.load(os.path.join(current_path, 'img/player/Idle/idle1.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Idle/idle2.png')).convert_alpha(),
                         pygame.image.load(os.path.join(current_path, 'img/player/Idle/idle3.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Idle/idle4.png')).convert_alpha()]
    playersImage_Jump = [pygame.image.load(os.path.join(current_path, 'img/player/Jump/JumpWithoutAttack1.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Jump/JumpWithoutAttack2.png')).convert_alpha(),
                         pygame.image.load(os.path.join(current_path, 'img/player/Jump/JumpWithoutAttack3.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Jump/JumpWithoutAttack4.png')).convert_alpha()]
    playersImage_JumpAttack = [pygame.image.load(os.path.join(current_path, 'img/player/Jump_Attack/JumpAttack1.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Jump_Attack/JumpAttack2.png')).convert_alpha(),
                               pygame.image.load(os.path.join(current_path, 'img/player/Jump_Attack/JumpAttack3.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Jump_Attack/JumpAttack4.png')).convert_alpha()]
    playersImage_StayAttack = [pygame.image.load(os.path.join(current_path, 'img/player/Stay_Attack/StayAttack1.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Stay_Attack/StayAttack2.png')).convert_alpha(),
                               pygame.image.load(os.path.join(current_path, 'img/player/Stay_Attack/StayAttack3.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Stay_Attack/StayAttack4.png')).convert_alpha()]
    playersImage_Walk = [pygame.image.load(os.path.join(current_path, 'img/player/Walk/Walk1.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Walk/Walk2.png')).convert_alpha(),
                         pygame.image.load(os.path.join(current_path, 'img/player/Walk/Walk3.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/player/Walk/Walk4.png')).convert_alpha()]
    playerImage = playersImage_Idle[0]
    playerRect = pygame.Rect(0, 0, 33, 35)
    playerRect.left = 150
    playerRect.bottom = 580
    #플레이어

    jumpDict={0:0,
              1:-15, 2:-13, 3:-11, 4:-9, 5:-7, 6:-5, 7:-3, 8:-1,
              9:1, 10:3, 11:5, 12:7, 13:9, 14:11, 15:13, 16:15}
    #점프 딕셔너리

    guagesImage = []
    for i in range(1, 11, 1):
        guagesImage.append(pygame.image.load(os.path.join(current_path, 'img/guage/VIDA_{}.png'.format(i))).convert_alpha())
    guageRect = pygame.Rect(0, 0, 63, 7)
    #발사 게이지 이미지

    shoot_text = dunggeunmo24.render('SHOOT!', True, RED)
    shoot_textRect = shoot_text.get_rect()
    alpha_img = pygame.Surface(shoot_text.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    shoot_text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    shoot_textRect.centerx = playerRect.centerx
    shoot_textRect.bottom = guageRect.top
    wait_text = dunggeunmo24.render('WAIT!', True, RED)
    wait_textRect = wait_text.get_rect()
    alpha_img = pygame.Surface(wait_text.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    wait_text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    wait_textRect.centerx = playerRect.centerx
    wait_textRect.bottom = guageRect.top
    #발사 대기 텍스트

    foodsRect = []
    potionImage = pygame.image.load(os.path.join(current_path, 'img/food/potion.png')).convert_alpha()
    potionLargeImage = pygame.image.load(os.path.join(current_path, 'img/food/potionLarge.png')).convert_alpha()
    penetrableImage = pygame.image.load(os.path.join(current_path, 'img/food/penetrable.png')).convert_alpha()
    shotgunImage = pygame.image.load(os.path.join(current_path, 'img/food/shotgun.png')).convert_alpha()
    quickchargeImage = pygame.image.load(os.path.join(current_path, 'img/food/quickcharge.png')).convert_alpha()
    slotImage = pygame.image.load(os.path.join(current_path, 'img/food/slot.png')).convert_alpha()
    poweritemRect_0 = pygame.Rect(10, 45, 30, 30)
    poweritemRect_1 = pygame.Rect(45, 45, 30, 30)
    poweritemRect_2 = pygame.Rect(80, 45, 30, 30)
    class foodRect:
        def __init__(self, left, top, width, height, foodType):
            self.foodType = foodType
            self.movelimit = r.randint(565, 595)
            self.rect = pygame.Rect(left, top, width, height)
        def summon(self):
            foodsRect.append(self)
        def kill(self):
            foodsRect.remove(self)
        def move(self):
            SPEED_FOOD = 4
            if self.rect.bottom<self.movelimit:
                self.rect.bottom += SPEED_FOOD
        def testCollision(self):
            global remainheart
            global penetrable
            global shotgun
            global quickcharge
            global score
            global statistics_drinkPotionCount
            global statistics_drinkPotionLargeCount
            global statistics_acquirePenetrable
            global statistics_acquireShotgun
            global statistics_acquireQuickcharge
            HEAL_POTION = 3
            HEAL_POTIONLARGE = 6
            SCORE_POTION = 10
            SCORE_POTIONLARGE = 25
            SCORE_PENETRABLE = 100
            SCORE_SHOTGUN = 100
            SCORE_QUICKCHARGE = 250
            if playerRect.colliderect(self.rect):
                if self.foodType=="potion":
                    remainheart += HEAL_POTION
                    score += SCORE_POTION
                    statistics_drinkPotionCount += 1
                elif self.foodType=="potionLarge":
                    remainheart += HEAL_POTIONLARGE
                    score += SCORE_POTIONLARGE
                    statistics_drinkPotionLargeCount += 1
                elif self.foodType=="penetrable":
                    penetrable = True
                    score += SCORE_PENETRABLE
                    statistics_acquirePenetrable = True
                elif self.foodType=="shotgun":
                    shotgun = True
                    score += SCORE_SHOTGUN
                    statistics_acquireShotgun = True
                elif self.foodType=="quickcharge":
                    quickcharge = 2
                    score += SCORE_QUICKCHARGE
                    statistics_acquireQuickcharge = True
                self.kill()
        def render(self):
            if self.foodType=="potion":
                windowSurface.blit(potionImage, self.rect)
            if self.foodType=="potionLarge":
                windowSurface.blit(potionLargeImage, self.rect)
            if self.foodType=="penetrable":
                windowSurface.blit(penetrableImage, self.rect)
            if self.foodType=="shotgun":
                windowSurface.blit(shotgunImage, self.rect)
            if self.foodType=="quickcharge":
                windowSurface.blit(quickchargeImage, self.rect)
    #음식 클래스

    stoneImage = pygame.image.load(os.path.join(current_path, 'img/stone.png')).convert_alpha()
    stonesRect = []
    class stoneRect:
        def __init__(self, left, top, width, height):
            self.frame = 0
            self.rect = pygame.Rect(left, top, width, height)
            self.identityList = []
        def summon(self, stoneType):
            stonesRect.append(self)
            clickupPos = pygame.mouse.get_pos()
            difference_x = clickupPos[0]-playerRect.centerx
            difference_y = clickupPos[1]-playerRect.centery
            hypotenuse = m.sqrt(difference_x**2+difference_y**2)
            cos = difference_x/hypotenuse
            sin = difference_y/hypotenuse
            if stoneType==0:
                self.speedx = m.trunc(frame_click*cos*1.5) #프레임 클릭을 60에서 40으로 수정했기 때문에 속도에 1.5를 곱
                self.speedy = m.trunc(frame_click*sin*1.5)
            elif stoneType==1:
                self.speedx = m.trunc(frame_click*(cos-0.1)*1.5)
                self.speedy = m.trunc(frame_click*(sin+0.1)*1.5)
            elif stoneType==2:
                self.speedx = m.trunc(frame_click*(cos+0.1)*1.5)
                self.speedy = m.trunc(frame_click*(sin-0.1)*1.5)
            self.remainPenetration = 3
        def kill(self):
            stonesRect.remove(self)
        def progressFrame(self):
            self.frame += 1
        def move(self):
            self.rect.centerx += self.speedx
            self.rect.centery += self.speedy+GRAVITY*self.frame
        #def testCollision(self): 필요없었네 히히히
        def render(self):
            windowSurface.blit(stoneImage, self.rect)
    #돌 - 곡사 투사체

    wheatImage = pygame.image.load(os.path.join(current_path, 'img/wheat.png')).convert_alpha()
    wheatRect = pygame.Rect(0,490,150,123)
    class wheat:
        def __init__(self, wheatDurability):
            self.wheatDurability = wheatDurability
            self.text_bottom = dunggeunmo24.render('{}'.format(self.wheatDurability), True, RED)
            self.textRect_bottom = self.text_bottom.get_rect()
            self.text_top = dunggeunmo24.render('DURABILITY:', True, RED)
            self.textRect_top = self.text_top.get_rect() #이거 네 줄 없으면 오류 뜸
        def damage(self, damage):
            self.wheatDurability -= damage
        def makeText(self):
            self.text_bottom = dunggeunmo24.render('{}'.format(self.wheatDurability), True, RED)
            self.textRect_bottom = self.text_bottom.get_rect()
            self.textRect_bottom.centerx = wheatRect.centerx
            self.textRect_bottom.bottom = wheatRect.top
            alpha_img = pygame.Surface(self.text_bottom.get_size(), pygame.SRCALPHA)
            alpha_img.fill((255, 255, 255, 255))
            self.text_bottom.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.text_top = dunggeunmo24.render('DURABILITY:', True, RED)
            self.textRect_top = self.text_top.get_rect()
            self.textRect_top.centerx = wheatRect.centerx
            self.textRect_top.bottom = self.textRect_bottom.top
            alpha_img = pygame.Surface(self.text_top.get_size(), pygame.SRCALPHA)
            alpha_img.fill((255, 255, 255, 255))
            self.text_top.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        def check_destroyed(self):
            global Game_State
            global statistics_remainWheatDurability
            if self.wheatDurability<0:
                self.wheatDurability = 0
            if self.wheatDurability<1:
                Game_State = S_DEATH
            statistics_remainWheatDurability = self.wheatDurability
        def render(self):
            windowSurface.blit(wheatImage, wheatRect)
            windowSurface.blit(self.text_bottom, self.textRect_bottom)
            windowSurface.blit(self.text_top, self.textRect_top)
    WHEATDURABILITY = 500
    wheatField = wheat(WHEATDURABILITY)
    #밀 클래스

    laserbeamImage_1 = pygame.Surface((13, 656), pygame.SRCALPHA)
    laserbeamImage_1.fill((0, 0, 0, 15))
    laserbeamImage_2 = pygame.Surface((39, 656), pygame.SRCALPHA)
    laserbeamImage_2.fill((0, 255, 0, 127))
    caterpillarImage = pygame.image.load(os.path.join(current_path, 'img/bird/caterpillar.png')).convert_alpha()
    poopImage = pygame.image.load(os.path.join(current_path, 'img/humanfacedbird/poop.png')).convert_alpha()
    arcaneliftImage = pygame.image.load(os.path.join(current_path, 'img/medivh/arcanelift/arcanelift.png')).convert_alpha()
    hit_by_arcanelift = False
    projectilesRect = []
    willRemoved_in_projectilesRect = []
    class projectileRect:
        def __init__(self, left, top, width, height, projectileType, pattern, host):
            self.projectileType = projectileType
            self.pattern = pattern
            self.host = host
            self.rect = pygame.Rect(left, top, width, height)
            self.frame = 0
            self.frame_sprite = 0
            self.frame_extinguish = 0
            self.attack = True
            self.random = r.randint(0, 9)
            self.difference_x = 0
            self.difference_y = 0
            self.hypotenuse = 0
            self.cos = 0
            self.sin = 0
            self.theta = 0
        def summon(self):
            if self.projectileType=="laserbeam":
                if self.pattern==1:
                    projectilesRect.insert(-1, self)
                elif self.pattern==2:
                    projectilesRect.insert(0, self)
                self.frame_extinguish = 1
            elif self.projectileType=="caterpillar":
                if self.random<8:
                    self.difference_x = playerRect.centerx - self.rect.centerx
                    self.difference_y = playerRect.centery - self.rect.centery
                    self.hypotenuse = m.sqrt(self.difference_x**2+self.difference_y**2)
                    self.cos = self.difference_x/self.hypotenuse
                    self.sin = self.difference_y/self.hypotenuse
                else:
                    self.difference_x = wheatRect.centerx - self.rect.centerx
                    self.difference_y = wheatRect.centery - self.rect.centery
                    self.hypotenuse = m.sqrt(self.difference_x**2+self.difference_y**2)
                    self.cos = self.difference_x/self.hypotenuse
                    self.sin = self.difference_y/self.hypotenuse
                projectilesRect.append(self)
            elif self.projectileType=="poop":
                projectilesRect.append(self)
            elif self.projectileType=="arcanelift":
                self.difference_x = playerRect.centerx - self.rect.centerx
                self.difference_y = playerRect.centery - self.rect.centery
                self.hypotenuse = m.sqrt(self.difference_x**2+self.difference_y**2)
                self.cos = self.difference_x/self.hypotenuse
                self.sin = self.difference_y/self.hypotenuse
                self.theta = m.acos(self.cos)
                self.rotatedImage = pygame.transform.flip(pygame.transform.rotate(arcaneliftImage, m.floor(self.theta*180/m.pi)), False, True)
                projectilesRect.append(self)
        def kill(self):
            projectilesRect.remove(self)
        def progressFrame(self):
            self.frame += 1
            if self.projectileType=="laserbeam":
                if self.pattern==1:
                    if self.frame_extinguish<89:
                        self.frame_extinguish += 1
                    else:
                        self.frame = 0
                elif self.pattern==2:
                    if self.frame_extinguish<59:
                        self.frame_extinguish += 1
                    else:
                        self.frame = 0
            elif self.projectileType=="caterpillar":
                if self.frame_sprite<9:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
            elif self.projectileType=="arcanelift":
                if self.frame_extinguish<59:
                    self.frame_extinguish += 1
        def move(self):
            SPEED_CATERPILLAR = 13
            SPEED_POOP = 10
            SPEED_ARCANELIFT = 30
            if self.projectileType=="caterpillar":
                self.rect.centerx += m.floor(self.cos*SPEED_CATERPILLAR)
                self.rect.centery += m.floor(self.sin*SPEED_CATERPILLAR)
            elif self.projectileType=="poop":
                self.rect.centery += SPEED_POOP
            elif self.projectileType=="arcanelift":
                self.rect.centerx += m.trunc(self.cos*SPEED_ARCANELIFT)
                self.rect.centery += m.trunc(self.sin*SPEED_ARCANELIFT)
        def testCollision(self):
            global remainheart
            global willRemoved_in_projectilesRect
            global hit_by_arcanelift
            global statistics_collideProjectileCount
            global statistics_receivedDamage
            DAMAGE_LASERBEAM_PLAYER = 1 #원인 모를 오류로 데미지가 두 배로 들어감
            DAMAGE_LASERBEAM_WHEAT = 5 #원인 모를 오류로 데미지가 두 배로 들어감
            DAMAGE_CATERPILLAR_PLAYER = 1
            DAMAGE_CATERPILLAR_WHEAT = 5
            DAMAGE_POOP_PLAYER = 2
            DAMAGE_POOP_WHEAT = 4
            DAMAGE_ARCANELIFT_PLAYER = 2
            DAMAGE_ARCANELIFT_WHEAT = 3
            if self.projectileType=="laserbeam":
                if not self.host in enemiesRect:
                    if not self in willRemoved_in_projectilesRect:
                        willRemoved_in_projectilesRect.append(self)
                if self.pattern==2:
                    if playerRect.colliderect(self.rect) and self.attack:
                        remainheart -= DAMAGE_LASERBEAM_PLAYER
                        statistics_receivedDamage += DAMAGE_LASERBEAM_PLAYER
                        self.attack = False
                        statistics_collideProjectileCount += 1
                    if wheatRect.colliderect(self.rect) and self.attack:
                        wheatField.damage(DAMAGE_LASERBEAM_WHEAT)
                        self.attack = False
                if self.pattern==1:
                    if self.frame_extinguish==89:
                        if not self in willRemoved_in_projectilesRect:
                            willRemoved_in_projectilesRect.append(self)
                elif self.pattern==2:
                    if self.frame_extinguish==59:
                        if not self in willRemoved_in_projectilesRect:
                            willRemoved_in_projectilesRect.append(self)
            elif self.projectileType=="caterpillar":
                if playerRect.colliderect(self.rect):
                    if not self in willRemoved_in_projectilesRect:
                        willRemoved_in_projectilesRect.append(self)
                    remainheart -= DAMAGE_CATERPILLAR_PLAYER
                    statistics_receivedDamage += DAMAGE_CATERPILLAR_PLAYER
                    statistics_collideProjectileCount += 1
                if wheatRect.colliderect(self.rect):
                    if not self in willRemoved_in_projectilesRect:
                        willRemoved_in_projectilesRect.append(self)
                    wheatField.damage(DAMAGE_CATERPILLAR_WHEAT)
                if self.rect.top>720:
                    self.kill()
            elif self.projectileType=="poop":
                if playerRect.colliderect(self.rect):
                    if not self in willRemoved_in_projectilesRect:
                        willRemoved_in_projectilesRect.append(self)
                    remainheart -= DAMAGE_POOP_PLAYER
                    statistics_receivedDamage += DAMAGE_POOP_PLAYER
                    statistics_collideProjectileCount += 1
                if wheatRect.colliderect(self.rect):
                    if not self in willRemoved_in_projectilesRect:
                        willRemoved_in_projectilesRect.append(self)
                    wheatField.damage(DAMAGE_POOP_WHEAT)
                if self.rect.top>720:
                    self.kill()
            elif self.projectileType=="arcanelift":
                if playerRect.colliderect(self.rect):
                    if not self in willRemoved_in_projectilesRect:
                        willRemoved_in_projectilesRect.append(self)
                    remainheart -= DAMAGE_ARCANELIFT_PLAYER
                    statistics_receivedDamage += DAMAGE_ARCANELIFT_PLAYER
                    statistics_collideProjectileCount += 1
                    hit_by_arcanelift = True
                if wheatRect.colliderect(self.rect):
                    if not self in willRemoved_in_projectilesRect:
                        willRemoved_in_projectilesRect.append(self)
                    wheatField.damage(DAMAGE_ARCANELIFT_WHEAT)
                if self.frame_extinguish==59:
                    if not self in willRemoved_in_projectilesRect:
                        willRemoved_in_projectilesRect.append(self)
            for projectile in willRemoved_in_projectilesRect:
                projectile.kill()
            willRemoved_in_projectilesRect = []
        def render(self):
            if self.projectileType=="laserbeam":
                if self.pattern==1:
                    windowSurface.blit(laserbeamImage_1, self.rect)
                if self.pattern==2:
                    windowSurface.blit(laserbeamImage_2, self.rect)
            elif self.projectileType=="caterpillar":
                windowSurface.blit(caterpillarImage, self.rect, (22*self.frame_sprite+1, 0, self.rect.width, self.rect.height))
            elif self.projectileType=="poop":
                windowSurface.blit(poopImage, self.rect)
            elif self.projectileType=="arcanelift":
                windowSurface.blit(self.rotatedImage, (m.trunc(self.rect.centerx+arcaneliftImage.get_width()/2-self.rotatedImage.get_width()/2), m.trunc(self.rect.centery+arcaneliftImage.get_height()/2-self.rotatedImage.get_height()/2)))
    #직사 투사체

    path = []
    class makePath:
        global path
        def savePath(self):
            path.append(pygame.mouse.get_pos())
        def printPath(self):
            print(path)
    a = makePath()
    #경로 저장 방법론 pygame.mouse.get_pos()

    whishingDove = False
    whishingRaven = False
    whishingCrane = False
    whishingPelican = False
    whishingParrot = False
    quickchargeSummoned = False
    doveImage = pygame.image.load(os.path.join(current_path, "img/bonus/dove.png")).convert_alpha()
    ravenImage = pygame.image.load(os.path.join(current_path, "img/bonus/raven.png")).convert_alpha()
    craneImage = pygame.image.load(os.path.join(current_path, "img/bonus/crane.png")).convert_alpha()
    pelicanImage = pygame.image.load(os.path.join(current_path, "img/bonus/pelican.png")).convert_alpha()
    parrotImage = pygame.image.load(os.path.join(current_path, "img/bonus/parrot.png")).convert_alpha()
    doveSprite = pygame.image.load(os.path.join(current_path, "img/bonus/dove_sprite.png")).convert_alpha()
    ravenSprite = pygame.image.load(os.path.join(current_path, "img/bonus/raven_sprite.png")).convert_alpha()
    craneSprite = pygame.image.load(os.path.join(current_path, "img/bonus/crane_sprite.png")).convert_alpha()
    pelicanSprite = pygame.image.load(os.path.join(current_path, "img/bonus/pelican_sprite.png")).convert_alpha()
    parrotSprite = pygame.image.load(os.path.join(current_path, "img/bonus/parrot_sprite.png")).convert_alpha()
    bonusbirdRect_0 = pygame.Rect(10, 10, 30, 30)
    bonusbirdRect_1 = pygame.Rect(45, 10, 30, 30)
    bonusbirdRect_2 = pygame.Rect(80, 10, 30, 30)
    bonusbirdRect_3 = pygame.Rect(115, 10, 30, 30)
    bonusbirdRect_4 = pygame.Rect(150, 10, 30, 30)
    bonusbirdPath = np.load(os.path.join(current_path, 'array/bonusbirdPath.npy'))
    bonusbirdsRect = []
    willRemoved_in_bonusbirdsRect = []
    class bonusbirdRect:
        def __init__(self, left, top, width, height, bonusbirdType):
            self.bonusbirdType = bonusbirdType
            self.rect = pygame.Rect(left, top, width, height)
            self.frame = 0
            self.frame_sprite = 0
            self.frame_sprite_sized = 0
            self.moving = False
            self.destination = (r.randint(500,1200), r.randint(100,300))
            self.difference_x = 1
            self.difference_y = 1
            self.hypotenuse = m.sqrt(2)
            self.cos = 1/m.sqrt(2)
            self.sin = 1/m.sqrt(2)
            self.tan = 1
            self.theta = m.pi/2
            self.heading = 0
            self.headingRight = False
            self.extinguish = False
        def summon(self):
            bonusbirdsRect.append(self)
        def kill(self):
            bonusbirdsRect.remove(self)
        def progressFrame(self):
            self.frame += 1
            if self.bonusbirdType=="dove" or self.bonusbirdType=="raven":
                if self.frame_sprite<8:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//3
            elif self.bonusbirdType=="crane":
                if self.frame_sprite<11:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//6
            elif self.bonusbirdType=="parrot":
                if self.frame_sprite<26:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//3
        def move(self):
            SPEED = 3
            if not self.moving:
                self.moving = True
                self.destination = bonusbirdPath[r.randint(0, len(bonusbirdPath)-1)]
                self.difference_x = self.destination[0]-self.rect.centerx
                self.difference_y = self.destination[1]-self.rect.centery
                self.hypotenuse = m.sqrt(self.difference_x**2+self.difference_y**2)
                self.cos = self.difference_x/self.hypotenuse
                self.sin = self.difference_y/self.hypotenuse
                if self.cos!=0:
                    self.tan = self.sin/self.cos
                    if self.cos>=0:
                        self.theta = m.atan(self.tan)
                    else:
                        self.theta = m.atan(self.tan)+m.pi
                else:
                    if self.sin>=0:
                        self.theta = m.pi/2
                    else:
                        self.theta = -m.pi/2 #self.cos=0일 경우를 대비한 번거로운 조치
            if self.moving:
                self.rect.centerx += m.trunc(self.cos*SPEED)
                self.rect.centery += m.trunc(self.sin*SPEED)
            if ((self.cos>=0 and self.destination[0]<=self.rect.centerx) or (self.cos<0 and self.destination[0]>=self.rect.centerx)) or ((self.sin>=0 and self.destination[1]<=self.rect.centery) or (self.sin>=0 and self.destination[1]<=self.rect.centery)):
                if not self.extinguish:
                    self.moving = False
            if (self.rect.centerx<0 or self.rect.centerx<0>1280) or (self.rect.centery<0 or self.rect.centery>720):
                if not self.extinguish:
                    self.moving = False
            if self.bonusbirdType=="crane" or self.bonusbirdType=="pelican" or self.bonusbirdType=="parrot":
                if self.cos>=0:
                    self.headingRight = True
                else:
                    self.headingRight = False
        def testCollision(self):
            global whishingDove
            global whishingRaven
            global whishingCrane
            global whishingPelican
            global whishingParrot
            SCORE_DOVE = 10
            SCORE_RAVEN = 20
            SCORE_CRANE = 50
            SCORE_PELICAN = 100
            SCORE_PARROT = 200
            global remainheart
            global score
            global willRemoved_in_bonusbirdsRect
            global statistics_collideEnemyCount
            global statistics_killDove
            global statistics_killRaven
            global statistics_killCrane
            global statistics_killPelican
            global statistics_killParrot
            global statistics_receivedDamage
            global statistics_hitCount
            global statistics_killEnemyCount
            for stone in stonesRect:
                if self.rect.colliderect(stone.rect):
                    stone.remainPenetration -= 1
                    statistics_hitCount += 1
                    if not self in willRemoved_in_bonusbirdsRect:
                        willRemoved_in_bonusbirdsRect.append(self)
                    if not penetrable or stone.remainPenetration==0:
                        stone.kill()
            if playerRect.colliderect(self.rect):
                remainheart -= 1
                statistics_receivedDamage += 1
                statistics_collideEnemyCount += 1
                if not self in willRemoved_in_bonusbirdsRect:
                    willRemoved_in_bonusbirdsRect.append(self)
            # if self.extinguish and ((self.rect.centerx<-100 or self.rect.centerx>1380) or self.rect.centery<-100):
            #     self.kill()
            for bonusbird in willRemoved_in_bonusbirdsRect:
                bonusbird.kill()
                statistics_killEnemyCount += 1
                if self.bonusbirdType=="dove":
                    score += SCORE_DOVE
                    whishingDove = True
                    statistics_killDove = True
                elif self.bonusbirdType=="raven":
                    score += SCORE_RAVEN
                    whishingRaven = True
                    statistics_killRaven = True
                elif self.bonusbirdType=="crane":
                    score += SCORE_CRANE
                    whishingCrane = True
                    statistics_killCrane = True
                elif self.bonusbirdType=="pelican":
                    score += SCORE_PELICAN
                    whishingPelican = True
                    statistics_killPelican = True
                elif self.bonusbirdType=="parrot":
                    score += SCORE_PARROT
                    whishingParrot = True
                    statistics_killParrot = True
            willRemoved_in_bonusbirdsRect = []
        def render(self):
            if self.bonusbirdType=="dove":
                if self.theta>=m.pi*3/4 and self.theta<m.pi*5/4:
                    self.heading = 2
                if self.theta>=m.pi*5/4 or self.theta<-m.pi/4:
                    self.heading = 6
                if self.theta>=m.pi/4 and self.theta<m.pi*3/4:
                    self.heading = 0
                if self.theta>=-m.pi/4 and self.theta<m.pi/4:
                    self.heading = 4
                windowSurface.blit(doveSprite, self.rect, (self.rect.width*self.frame_sprite_sized, self.heading*self.rect.height, self.rect.width, self.rect.height))
            elif self.bonusbirdType=="raven":
                if self.theta>=m.pi*3/4 and self.theta<m.pi*5/4:
                    self.heading = 2
                if self.theta>=m.pi*5/4 or self.theta<-m.pi/4:
                    self.heading = 6
                if self.theta>=m.pi/4 and self.theta<m.pi*3/4:
                    self.heading = 0
                if self.theta>=-m.pi/4 and self.theta<m.pi/4:
                    self.heading = 4
                windowSurface.blit(ravenSprite, self.rect, (self.rect.width*self.frame_sprite_sized, self.heading*self.rect.height, self.rect.width, self.rect.height))
            elif self.bonusbirdType=="crane":
                if self.headingRight:
                    windowSurface.blit(craneSprite, self.rect, (0, self.frame_sprite_sized*self.rect.height, self.rect.width, self.rect.height))
                else:
                    windowSurface.blit(pygame.transform.flip(craneSprite, True, False), self.rect, (0, self.frame_sprite_sized*self.rect.height, self.rect.width, self.rect.height))
            elif self.bonusbirdType=="pelican":
                if not self.headingRight:
                    windowSurface.blit(pelicanSprite, self.rect, (0, 0, self.rect.width, self.rect.height))
                else:
                    windowSurface.blit(pygame.transform.flip(pelicanSprite, True, False), self.rect, (0, 0, self.rect.width, self.rect.height))
            elif self.bonusbirdType=="parrot":
                if self.headingRight:
                    windowSurface.blit(parrotSprite, self.rect, (self.rect.width*(self.frame_sprite_sized%3), self.rect.height*(self.frame_sprite_sized//3), self.rect.width, self.rect.height))
                else:
                    windowSurface.blit(pygame.transform.flip(parrotSprite, True, False), self.rect, (self.rect.width*(self.frame_sprite_sized%3), self.rect.height*(self.frame_sprite_sized//3), self.rect.width, self.rect.height))
    #보너스 해로운 새

    enemiesRect = []
    willRemoved_in_enemiesRect = []
    ostrichImage = pygame.image.load(os.path.join(current_path, 'img/bird/ostrich_sprite.png')).convert_alpha()
    sparrowImage = [pygame.image.load(os.path.join(current_path, 'img/bird/bird_1_bluejay.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/bird/bird_1_red.png')).convert_alpha(),
                    pygame.image.load(os.path.join(current_path, 'img/bird/bird_2_brown_1.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/bird/bird_2_cardinal.png')).convert_alpha(),
                    pygame.image.load(os.path.join(current_path, 'img/bird/bird_3_robin.png')).convert_alpha(), pygame.image.load(os.path.join(current_path, 'img/bird/bird_3_sparrow.png')).convert_alpha()]
    sparrowPath = np.load(os.path.join(current_path, 'array/sparrowPath.npy'))
    ufoImage = pygame.image.load(os.path.join(current_path, 'img/bird/ufo.png')).convert_alpha()
    ufoPath = np.load(os.path.join(current_path, 'array/ufoPath.npy'))
    locustImage = pygame.image.load(os.path.join(current_path, 'img/bird/locust.png')).convert_alpha()
    locustCounter = 0
    LIMITLOCUST = 160
    class enemyRect:
        def __init__(self, left, top, width, height, enemyType, pattern):
            self.enemyType = enemyType
            self.pattern = pattern
            self.frame = 0
            self.frame_sprite = 0
            self.frame_sprite_sized = 0
            self.frame_wait = 0
            self.rect = pygame.Rect(left, top, width, height)
            self.moving = False
            self.stopMoving = False
            self.stopAttack = False
            self.destination = (r.randint(500,1200), r.randint(100,300))
            self.difference_x = 1
            self.difference_y = 1
            self.hypotenuse = m.sqrt(2)
            self.cos = 1/m.sqrt(2)
            self.sin = 1/m.sqrt(2)
            self.tan = 1
            self.theta = m.pi/2
            self.facing = 0
            self.speed_ostrich = r.randint(1, 3)
            self.limit = r.randint(550, 580)
        def summon(self):
            enemiesRect.append(self)
        def kill(self):
            enemiesRect.remove(self)
        def progressFrame(self):
            self.frame += 1
            if self.enemyType=="ostrich":
                if self.frame_sprite<17:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//3
            elif self.enemyType=="sparrow":
                if self.frame_sprite <8:
                    self.frame_sprite +=1
                else:
                    self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//3
            elif self.enemyType=="ufo":
                if self.frame_sprite<35:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//3
                if self.frame_wait>0 and self.frame_wait<119:
                    self.frame_wait += 1
                else:
                    self.frame_wait = 0
        def move(self):
            SPEED_SPARROW = 5
            SPEED_UFO = 7
            SPEED_LOCUST = 12
            if self.enemyType=="ostrich":
                self.rect.centerx -= self.speed_ostrich
            elif self.enemyType=="sparrow":
                if not self.moving:
                    self.moving = True
                    self.destination = sparrowPath[r.randint(0, len(sparrowPath)-1)]
                    self.difference_x = self.destination[0]-self.rect.centerx
                    self.difference_y = self.destination[1]-self.rect.centery
                    self.hypotenuse = m.sqrt(self.difference_x**2+self.difference_y**2)
                    self.cos = self.difference_x/self.hypotenuse
                    self.sin = self.difference_y/self.hypotenuse
                    if self.cos!=0:
                        self.tan = self.sin/self.cos
                        if self.cos>=0:
                            self.theta = m.atan(self.tan)
                        else:
                            self.theta = m.atan(self.tan)+m.pi
                    else:
                        if self.sin>=0:
                            self.theta = m.pi/2
                        else:
                            self.theta = -m.pi/2 #self.cos=0일 경우를 대비한 번거로운 조치
                if self.moving:
                    self.rect.centerx += m.trunc(self.cos*SPEED_SPARROW)
                    self.rect.centery += m.trunc(self.sin*SPEED_SPARROW)
                if ((self.cos>=0 and self.destination[0]<=self.rect.centerx) or (self.cos<0 and self.destination[0]>=self.rect.centerx)) or ((self.sin>=0 and self.destination[1]<=self.rect.centery) or (self.sin>=0 and self.destination[1]<=self.rect.centery)):
                    self.moving = False
                if (self.rect.centerx<0 or self.rect.centerx<0>1280) or (self.rect.centery<0 or self.rect.centery>720):
                    self.moving = False
            elif self.enemyType=="ufo":
                if not self.moving:
                    self.moving = True
                    self.destination = ufoPath[r.randint(0, 8)]
                    if self.destination[0]-self.rect.centerx>=0:
                        self.heading = 1
                    else:
                        self.heading = -1
                if self.moving and not self.stopMoving:
                    self.rect.centerx += self.heading*SPEED_UFO
                if (self.heading==1 and self.rect.centerx>self.destination[0]) or (self.heading==-1 and self.rect.centerx<=self.destination[0]):
                    self.moving = False
            elif self.enemyType=="locust":
                self.rect.centerx -= SPEED_LOCUST
                if self.rect.centery<self.limit:
                    self.rect.centery += 50-self.frame*GRAVITY*2
        def testCollision(self):
            DAMAGE_OSTRICH_PLAYER = 1
            DAMAGE_OSTRICH_WHEAT = 1
            SCORE_OSTRICH = 1
            DAMAGE_SPARROW_PLAYER = 1
            DAMAGE_SPARROW_WHEAT = 1
            SCORE_SPARROW = 1
            SCORE_UFO = 20
            DAMAGE_LOCUST_PLAYER = 2
            DAMAGE_LOCUST_WHEAT = 10
            SCORE_LOCUST = 3
            global remainheart
            global score
            global willRemoved_in_enemiesRect
            global statistics_collideEnemyCount
            global statistics_receivedDamage
            global statistics_hitCount
            global statistics_killEnemyCount
            for stone in stonesRect:
                if self.rect.colliderect(stone.rect):
                    stone.remainPenetration -= 1
                    statistics_hitCount += 1
                    if not self in willRemoved_in_enemiesRect:
                        willRemoved_in_enemiesRect.append(self)
                    if not penetrable or stone.remainPenetration==0:
                        stone.kill()
            if playerRect.colliderect(self.rect):
                if not self in willRemoved_in_enemiesRect:
                    willRemoved_in_enemiesRect.append(self)
                if self.enemyType=="ostrich":
                    remainheart -= DAMAGE_OSTRICH_PLAYER
                    statistics_receivedDamage += DAMAGE_OSTRICH_PLAYER
                elif self.enemyType=="sparrow":
                    remainheart -= DAMAGE_SPARROW_PLAYER
                    statistics_receivedDamage += DAMAGE_SPARROW_PLAYER
                elif self.enemyType=="locust":
                    remainheart -= DAMAGE_LOCUST_PLAYER
                    statistics_receivedDamage += DAMAGE_LOCUST_PLAYER
                statistics_collideEnemyCount += 1
            if wheatRect.colliderect(self.rect):
                if not self in willRemoved_in_enemiesRect:
                    self.kill()
                if self.enemyType=="ostrich":
                    wheatField.damage(DAMAGE_OSTRICH_WHEAT)
                elif self.enemyType=="sparrow":
                    wheatField.damage(DAMAGE_SPARROW_WHEAT)
                elif self.enemyType=="locust":
                    wheatField.damage(DAMAGE_LOCUST_WHEAT)
            if self.enemyType=="ufo": #ufo만을 위한 x축 충돌 검사
                if (self.rect.centerx-playerRect.centerx>-10 and self.rect.centerx-playerRect.centerx<10) and self.frame_wait==0 and not self.stopAttack:
                    self.stopMoving = True
                    self.stopAttack = True
                    self.frame_wait = 1
                if self.frame_wait==1:
                    projectileRect(self.rect.centerx-6, self.rect.centery, 13, 656, "laserbeam", 1, self).summon()
                elif self.frame_wait==29:
                    projectileRect(self.rect.centerx-19, self.rect.centery, 39, 656, "laserbeam", 2, self).summon()
                elif self.frame_wait==89:
                        self.stopMoving = False
                elif self.frame_wait==119:
                    self.stopAttack = False
                if (self.rect.centerx-wheatRect.centerx>-10 and self.rect.centerx-wheatRect.centerx<10) and self.frame_wait==0 and not self.stopAttack:
                    self.stopMoving = True
                    self.stopAttack = True
                    self.frame_wait = 1
                if self.frame_wait==1:
                    projectileRect(self.rect.centerx-6, self.rect.centery, 13, 656, "laserbeam", 1, self).summon()
                elif self.frame_wait==29:
                    projectileRect(self.rect.centerx-19, self.rect.centery, 39, 656, "laserbeam", 2, self).summon()
                elif self.frame_wait==89:
                        self.stopMoving = False
                elif self.frame_wait==119:
                    self.stopAttack = False
            for enemy in willRemoved_in_enemiesRect:
                if self.enemyType=="ostrich":
                    score += SCORE_OSTRICH
                elif self.enemyType=="sparrow":
                    score += SCORE_SPARROW
                elif self.enemyType=="ufo":
                    score += SCORE_UFO
                elif self.enemyType=="locust":
                    score += SCORE_LOCUST
                enemy.kill()
                statistics_killEnemyCount += 1
                if r.randint(0, 31)==0:
                    foodRect(enemy.rect.centerx+15, enemy.rect.top-30, 30, 30, "potion").summon() #포션 드랍 6.25%
            willRemoved_in_enemiesRect = [] #이렇게 안 하면 두 개 이상 동시에 충돌할 때 not in list 에러가 뜸
        def render(self):
            if self.enemyType=="ostrich":
                windowSurface.blit(ostrichImage, self.rect, (self.rect.width*self.frame_sprite_sized, 0, self.rect.width, self.rect.height))
            elif self.enemyType=="sparrow":
                if self.theta>=m.pi*3/4 and self.theta<m.pi*5/4:
                    self.heading = 0
                if self.theta>=m.pi*5/4 or self.theta<-m.pi/4:
                    self.heading = 1
                if self.theta>=m.pi/4 and self.theta<m.pi*3/4:
                    self.heading = 2
                if self.theta>=-m.pi/4 and self.theta<m.pi/4:
                    self.heading = 3
                windowSurface.blit(sparrowImage[self.pattern], self.rect, (self.rect.width*self.frame_sprite_sized, self.heading*self.rect.height, self.rect.width, self.rect.height))
            elif self.enemyType=="ufo":
                windowSurface.blit(ufoImage, self.rect, (self.rect.width*self.frame_sprite_sized, 0, self.rect.width, self.rect.height))
            elif self.enemyType=="locust":
                windowSurface.blit(locustImage, self.rect)
    #해로운 새 enemy

    eliteenemiesRect = []
    frame_player_hit = 0
    player_hit = False
    healthbarImage = []
    for i in range(1, 11, 1):
        healthbarImage.append(pygame.image.load(os.path.join(current_path, 'img/healthbar/VIDA_{}.png'.format(i))).convert_alpha())
    eliteostrichImage = pygame.image.load(os.path.join(current_path, 'img/bird/eliteostrich_sprite.png')).convert_alpha()
    mutaliskImage = pygame.image.load(os.path.join(current_path, 'img/bird/mutalisk_sprite_cut.png')).convert_alpha()
    mutaliskCounter = 0
    LIMITMUTALISK = 120
    broodlordImage = []
    for i in range(1, 9, 1):
        broodlordImage.append(pygame.image.load(os.path.join(current_path, 'img/bird/broodlord/broodlord{}.png'.format(i))).convert_alpha())
    broodlordCounter = 0
    LIMITBROODLORD = 240
    identityNumber = 0 #아이덴티티 넘버
    class eliteenemyRect:
        def __init__(self, left, top, width, height, eliteenemyType, pattern, identity):
            global identityNumber
            self.identity = identity
            identityNumber += 1
            self.eliteenemyType = eliteenemyType
            self.pattern = pattern
            self.frame = 0
            self.frame_sprite = 0
            self.frame_sprite_sized = 0
            self.rect = pygame.Rect(left, top, width, height)
            self.healthbarRect = pygame.Rect(self.rect.centerx-47, self.rect.top-10, 95, 10)
            self.destination = (r.randint(600,1200), r.randint(100,200))
            self.difference_x = 1
            self.difference_y = 1
            self.hypotenuse = m.sqrt(2)
            self.cos = 1/m.sqrt(2)
            self.sin = 1/m.sqrt(2)
            self.tan = 1
            self.theta = m.pi/2
            self.limit = r.randint(550, 580)
            self.arrive = False
            self.origin = (640, 360)
            self.origin_made = False
            self.a = r.randint(200, 300)
            self.speed_eliteostrich = r.randint(16, 25)
            self.frame_theta = 0
            self.frame_spawn = 0
            if self.eliteenemyType=="eliteostrich":
                self.health = 200
            elif self.eliteenemyType=="mutalisk":
                self.health = 300
            elif self.eliteenemyType=="broodlord":
                self.health = 1500
        def summon(self):
            eliteenemiesRect.append(self)
        def kill(self):
            eliteenemiesRect.remove(self)
        def progressFrame(self):
            self.frame += 1
            if self.eliteenemyType=="eliteostrich":
                if self.frame_sprite<5:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
            elif self.eliteenemyType=="mutalisk":
                if self.frame_sprite<14:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//3
                if self.origin_made:
                    if self.frame_theta<99:
                        self.frame_theta += 1
                    else:
                        self.frame_theta = 0
            elif self.eliteenemyType=="broodlord":
                if self.frame_sprite<23:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//3
                if self.frame_spawn<119:
                    self.frame_spawn += 1
                else:
                    self.frame_spawn = 0
        def move(self):
            SPEED_MUTALISK = 10
            SPEED_BROODLORD = 2
            if self.eliteenemyType=="eliteostrich":
                self.rect.centerx -= self.speed_eliteostrich
                self.healthbarRect.centerx = self.rect.centerx
                self.healthbarRect.bottom = self.rect.top
            elif self.eliteenemyType=="mutalisk":
                self.difference_x = playerRect.centerx-self.rect.centerx
                self.difference_y = playerRect.centery-self.rect.centery
                self.hypotenuse = m.sqrt(self.difference_x**2+self.difference_y**2)
                self.cos = self.difference_x/self.hypotenuse
                self.sin = self.difference_y/self.hypotenuse
                if self.cos!=0:
                    self.tan = self.sin/self.cos
                    if self.cos>=0:
                        self.theta = m.atan(self.tan)
                    else:
                        self.theta = m.atan(self.tan)+m.pi
                else:
                    if self.sin>=0:
                        self.theta = m.pi/2
                    else:
                        self.theta = -m.pi/2 #self.cos=0일 경우를 대비한 번거로운 조치
                if not self.arrive:
                    self.difference_x = self.destination[0]-self.rect.centerx
                    self.difference_y = self.destination[1]-self.rect.centery
                    self.hypotenuse = m.sqrt(self.difference_x**2+self.difference_y**2)
                    self.cos = self.difference_x/self.hypotenuse
                    self.sin = self.difference_y/self.hypotenuse
                    if self.cos!=0:
                        self.tan = self.sin/self.cos
                        if self.cos>=0:
                            self.theta = m.atan(self.tan)
                        else:
                            self.theta = m.atan(self.tan)+m.pi
                    else:
                        if self.sin>=0:
                            self.theta = m.pi/2
                        else:
                            self.theta = -m.pi/2 #self.cos=0일 경우를 대비한 번거로운 조치
                    self.rect.centerx += m.trunc(self.cos*SPEED_MUTALISK)
                    self.rect.centery += m.trunc(self.sin*SPEED_MUTALISK)
                    self.healthbarRect.centerx = self.rect.centerx
                    self.healthbarRect.bottom = self.rect.top
                if ((self.cos>=0 and self.destination[0]<=self.rect.centerx) or (self.cos<0 and self.destination[0]>=self.rect.centerx)) or ((self.sin>=0 and self.destination[1]<=self.rect.centery) or (self.sin>=0 and self.destination[1]<=self.rect.centery)):
                    self.arrive = True
                if self.arrive:
                    if not self.origin_made:
                        self.origin = (self.destination[0]-self.a, self.destination[1])
                        self.origin_made = True
                    theta = self.frame_theta/50*m.pi
                    scale = 2/(3-m.cos(2*theta))
                    self.rect.centerx = self.origin[0]+m.trunc(self.a*scale*m.cos(theta))
                    self.rect.centery = self.origin[1]+m.trunc(self.a*scale*m.cos(theta)*m.sin(theta))
                    self.healthbarRect.centerx = self.rect.centerx
                    self.healthbarRect.bottom = self.rect.top
            elif self.eliteenemyType=="broodlord":
                if self.rect.centerx>self.limit+80:
                    self.rect.centerx -= SPEED_BROODLORD
                self.healthbarRect.centerx = self.rect.centerx
                self.healthbarRect.bottom = self.rect.top
        def damage(self, damage):
            self.health -= damage
        def testCollision(self):
            global remainheart
            global score
            global frame_player_hit
            global player_hit
            global statistics_collideEnemyCount
            global statistics_receivedDamage
            global statistics_hitCount
            for stone in stonesRect:
                if self.rect.colliderect(stone.rect) and self.identity not in stone.identityList:
                    stone.identityList.append(self.identity)
                    stone.remainPenetration -= 1
                    statistics_hitCount += 1
                    stoneSpeed = m.floor(m.sqrt(stone.speedx**2+stone.speedy**2))
                    self.damage(timesDamage*stoneSpeed*2)
                    if not penetrable or stone.remainPenetration==0:
                        stone.kill()
            if playerRect.colliderect(self.rect) and not player_hit:
                player_hit = True
                frame_player_hit = 1
                if self.eliteenemyType=="eliteostrich":
                    remainheart -= self.health//50
                    statistics_receivedDamage += self.health//50
                elif self.eliteenemyType=="mutalisk":
                    remainheart -= self.health//100
                    statistics_receivedDamage += self.health//100
                elif self.eliteenemyType=="broodlord":
                    remainheart -= self.health//200
                    statistics_receivedDamage += self.health//200
                self.damage(100)
                statistics_collideEnemyCount += 1
            if wheatRect.colliderect(self.rect):
                if self.eliteenemyType=="eliteostrich":
                    wheatField.damage(self.health//10)
                elif self.eliteenemyType=="mutalisk":
                    wheatField.damage(self.health//30)
                elif self.eliteenemyType=="broodlord":
                    wheatField.damage(self.health//10)
                self.kill()
            if self.eliteenemyType=="mutalisk": #뮤탈이 쐐기벌레를 날리기 위한 구문
                if self.frame_theta==50:
                    projectileRect(self.rect.centerx-10, self.rect.centery-12, 19, 25, "caterpillar", 0, self).summon()
            elif self.eliteenemyType=="broodlord": #그저 무리군주가 식충을 쏘아보낼 뿐인 코드
                if self.frame_spawn==0:
                    enemyRect(r.randint(self.rect.centerx, self.rect.centerx+50), r.randint(self.rect.centery-10, self.rect.centery+10), 60, 37, "locust", 0).summon()
        def render(self):
            if self.eliteenemyType=="eliteostrich":
                windowSurface.blit(eliteostrichImage, self.rect, (self.rect.width*self.frame_sprite, 0, self.rect.width, self.rect.height))
                for i in range(0, 10, 1):
                    if self.health>20*i and self.health<=20*(i+1):
                        windowSurface.blit(healthbarImage[i], self.healthbarRect)
            elif self.eliteenemyType=="mutalisk":
                if self.cos>=0:
                    for i in range(0, 9, 1):
                        if self.theta+m.pi/2>=i*m.pi/8-m.pi/16 and self.theta+m.pi/2<(i+1)*m.pi/8-m.pi/16:
                            windowSurface.blit(mutaliskImage, self.rect, (67*i+2, 75*self.frame_sprite_sized+2, self.rect.width, self.rect.height))
                else:
                    for i in range(0, 9, 1):
                        if self.theta-m.pi/2>=i*m.pi/8-m.pi/16 and self.theta-m.pi/2<(i+1)*m.pi/8-m.pi/16:
                            windowSurface.blit(pygame.transform.flip(mutaliskImage, True, False), self.rect, (67*i+1, 75*self.frame_sprite_sized+2, self.rect.width, self.rect.height))
                for i in range(0, 10, 1):
                    if self.health>30*i and self.health<=30*(i+1):
                        windowSurface.blit(healthbarImage[i], self.healthbarRect)
            elif self.eliteenemyType=="broodlord":
                windowSurface.blit(broodlordImage[self.frame_sprite_sized], self.rect)
                for i in range(0, 10, 1):
                    if self.health>150*i and self.health<=150*(i+1):
                        windowSurface.blit(healthbarImage[i], self.healthbarRect)
    #정예 해로운 새 elite enemy

    spireDestroyed = False
    greaterspireDestroyed = False
    spireImage = pygame.image.load(os.path.join(current_path, "img/tower/spire.png")).convert_alpha()
    greaterspireImage = pygame.image.load(os.path.join(current_path, "img/tower/greaterspire.png")).convert_alpha()
    towersRect = []
    class towerRect:
        def __init__(self, left, top, width, height, towerType, pattern, identity):
            global identityNumber
            self.identity = identity
            identityNumber += 1
            self.towerType = towerType
            self.pattern = pattern
            self.rect = pygame.Rect(left, top, width, height)
            self.healthbarRect = pygame.Rect(self.rect.centerx-47, self.rect.top-10, 95, 10)
            self.frame = 0
            self.frame_spawn_mutalisk = 0
            self.frame_spawn_broodlord = 0
            self.settled = True
            if self.towerType=="spire":
                self.health = 6000
            elif self.towerType=="greaterspire":
                self.health = 12000
        def summon(self):
            towersRect.append(self)
        def kill(self):
            global spireDestroyed
            global greaterspireDestroyed
            if self.towerType=="spire":
                foodRect(self.rect.left,self.rect.centery, 30, 30, "penetrable").summon()
                spireDestroyed = True
            towersRect.remove(self)
            if self.towerType=="greaterspire":
                greaterspireDestroyed = True
        def damage(self, damage):
            self.health -= damage
        def progressFrame(self):
            self.frame += 1
            if self.settled:
                if self.towerType=="spire":
                    if self.frame_spawn_mutalisk<499:
                        self.frame_spawn_mutalisk += 1
                    else:
                        self.frame_spawn_mutalisk = 0
                elif self.towerType=="greaterspire":
                    if self.frame_spawn_mutalisk<249:
                        self.frame_spawn_mutalisk += 1
                    else:
                        self.frame_spawn_mutalisk = 0
                    if self.frame_spawn_broodlord<399:
                        self.frame_spawn_broodlord += 1
                    else:
                        self.frame_spawn_broodlord = 0
        def move(self):
            if self.rect.bottom<640:
                self.rect.bottom += 4
            else:
                self.settled = True
            self.healthbarRect.centerx = self.rect.centerx
            self.healthbarRect.bottom = self.rect.top
        def spawn(self):
            if self.settled:
                if self.frame_spawn_mutalisk==249:
                    eliteenemyRect(r.randint(self.rect.left, self.rect.right), r.randint(50, 250), 64, 72, "mutalisk", 0, identityNumber).summon()
                if self.frame_spawn_broodlord==399:
                    eliteenemyRect(r.randint(self.rect.left, self.rect.right), r.randint(10, 150), 200, 154, "broodlord", 0, identityNumber).summon()
        def testCollision(self):
            global remainheart
            global score
            global frame_player_hit
            global player_hit
            global statistics_collideEnemyCount
            global statistics_receivedDamage
            global statistics_hitCount
            for stone in stonesRect:
                if self.rect.colliderect(stone.rect) and self.identity not in stone.identityList:
                    stone.identityList.append(self.identity)
                    stone.remainPenetration -= 1
                    statistics_hitCount += 1
                    stoneSpeed = m.floor(m.sqrt(stone.speedx**2+stone.speedy**2))
                    self.damage(timesDamage*stoneSpeed*2)
                    if not penetrable or stone.remainPenetration==0:
                        stone.kill()
            if playerRect.colliderect(self.rect) and not player_hit:
                player_hit = True
                frame_player_hit = 1
                if self.towerType=="spire":
                    remainheart -= 2
                    statistics_receivedDamage += 2
                elif self.towerType=="greaterspire":
                    remainheart -= 3
                    statistics_receivedDamage += 3
                self.damage(200)
                statistics_collideEnemyCount += 1
        def render(self):
            if self.towerType=="spire":
                windowSurface.blit(spireImage, self.rect)
                for i in range(0, 10, 1):
                    if self.health>=600*i and self.health<600*(i+1):
                        windowSurface.blit(healthbarImage[i], self.healthbarRect)
            elif self.towerType=="greaterspire":
                windowSurface.blit(greaterspireImage, self.rect)
                for i in range(0, 10, 1):
                    if self.health>=1200*i and self.health<1200*(i+1):
                        windowSurface.blit(healthbarImage[i], self.healthbarRect)
    #건물 tower 아 힘들어

    humanfacedbirdImage = []
    for i in range(1, 11, 1):
        humanfacedbirdImage.append(pygame.image.load(os.path.join(current_path, "img/humanfacedbird/HumanFacedBird{}.png".format(i))).convert_alpha())
    buttonleftImage = pygame.image.load(os.path.join(current_path, "img/humanfacedbird/buttonleft.png")).convert_alpha()
    buttonrightImage = pygame.image.load(os.path.join(current_path, "img/humanfacedbird/buttonright.png")).convert_alpha()
    bossbarImage = pygame.image.load(os.path.join(current_path, "img/healthbar/bossbar.png")).convert_alpha()
    humanfacedbirdsRect = []
    class humanfacedbirdRect:
        def __init__(self, left, top, width, height, identity):
            global identityNumber
            self.identity = identity
            identityNumber += 1
            self.rect = pygame.Rect(left, top, width, height)
            self.bossbar_backRect = pygame.Rect(160, 10, 960, 10)
            self.bossbar_frontRect = pygame.Rect(160, 10, 960, 10)
            self.buttonleftRect = pygame.Rect(640, 1080, 82, 90)
            self.buttonrightRect = pygame.Rect(640, 1080, 82, 90)
            self.health = 2880
            self.frame = 0
            self.frame_sprite = 0
            self.frame_sprite_sized = 0
            self.frame_rain = 0
            self.frame_pattern = 0
            self.frame_dance = 0
            self.letsleft = False
            self.text = dunggeunmo24.render("춤을 추지 않으면 잡아먹을 테야!", True, WHITE)
            self.textRect = self.text.get_rect()
            self.textRect.right = self.rect.centerx
            self.textRect.bottom = self.rect.top
            alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
            alpha_img.fill((255, 255, 255, 255))
            self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        def summon(self):
            humanfacedbirdsRect.append(self)
        def kill(self):
            global midBossFallen
            foodRect(self.rect.left, self.rect.centery, 30, 30, "shotgun").summon()
            midBossFallen = True
            humanfacedbirdsRect.remove(self)
        def damage(self, damage):
            self.health -= damage
        def progressFrame(self):
            self.frame += 1
            if self.frame_sprite<59:
                self.frame_sprite += 1
            else:
                self.frame_sprite = 0
            self.frame_sprite_sized = self.frame_sprite//6
            if self.frame_rain>0 and self.frame_rain<120:
                self.frame_rain += 1
            else:
                self.frame_rain = 0
            if self.frame_pattern <479:
                self.frame_pattern += 1
            else:
                self.frame_pattern = 0
                self.frame_dance = 1
            if self.frame_dance>0 and self.frame_dance<240:
                self.frame_dance += 1
            else:
                self.frame_dance = 0
            if self.frame_dance==0:
                self.pattern = r.randint(0, 4)
        def move(self):
            if self.rect.left>900:
                self.rect.centerx -= 5
            if self.frame_dance>0 and self.frame_dance<121:
                self.buttonleftRect.right = playerRect.centerx-20
                self.buttonleftRect.bottom = shoot_textRect.top
                self.buttonrightRect.left = playerRect.centerx+40
                self.buttonrightRect.bottom = shoot_textRect.top
            elif self.frame_dance>120 and self.frame_dance<241:
                self.buttonleftRect.right = playerRect.centerx-20
                self.buttonleftRect.bottom = shoot_textRect.top
                self.buttonrightRect.left = playerRect.centerx+40
                self.buttonrightRect.bottom = shoot_textRect.top
                if not player_headingRight and moving:
                    self.buttonleftRect.bottom = shoot_textRect.top+30
                elif player_headingRight and moving:
                    self.buttonrightRect.bottom = shoot_textRect.top+30
            self.textRect.right = self.rect.centerx
            self.textRect.bottom = self.rect.top
        def testCollision(self):
            DAMAGE_HUMANFACEDBIRD_PLAYER = 1
            global remainheart
            global score
            global frame_player_hit
            global player_hit
            global statistics_collideEnemyCount
            global statistics_receivedDamage
            global statistics_hitCount
            for stone in stonesRect:
                if self.rect.colliderect(stone.rect) and self.identity not in stone.identityList:
                    stone.identityList.append(self.identity)
                    stone.remainPenetration -= 1
                    statistics_hitCount += 1
                    stoneSpeed = m.floor(m.sqrt(stone.speedx**2+stone.speedy**2))
                    self.damage(timesDamage*stoneSpeed*2)
                    if not penetrable or stone.remainPenetration==0:
                        stone.kill()
            if playerRect.colliderect(self.rect) and not player_hit:
                player_hit = True
                frame_player_hit = 1
                remainheart -= DAMAGE_HUMANFACEDBIRD_PLAYER
                statistics_receivedDamage += DAMAGE_HUMANFACEDBIRD_PLAYER
                self.damage(20)
                statistics_collideEnemyCount += 1
        def rain(self):
            if self.frame_rain==0:
                for enemy in enemiesRect:
                    if enemy.enemyType=="sparrow":
                        projectileRect(enemy.rect.centerx-10, enemy.rect.centery, 20, 35, "poop", 0, self).summon()
                self.frame_rain = 1
        def dance(self):
            if self.frame_dance>0 and self.frame_dance<241:
                if self.pattern==0: #← → ← →
                    if (self.frame_dance>120 and self.frame_dance<151) or (self.frame_dance>180 and self.frame_dance<211):
                        self.letsleft = True
                    if self.frame_dance==150 or self.frame_dance==210:
                        if not (not player_headingRight and moving):
                            self.rain()
                    if (self.frame_dance>150 and self.frame_dance<181) or (self.frame_dance>210 and self.frame_dance<241):
                        self.letsleft = False
                    if self.frame_dance==180 or self.frame_dance==240:
                        if not (player_headingRight and moving):
                            self.rain()
                elif self.pattern==1: #← ← → ←
                    if (self.frame_dance>120 and self.frame_dance<181) or (self.frame_dance>210 and self.frame_dance<241):
                        self.letsleft = True
                    if self.frame_dance==150 or self.frame_dance==150 or self.frame_dance==240:
                        if not (not player_headingRight and moving):
                            self.rain()
                    if self.frame_dance>180 and self.frame_dance<211:
                        self.letsleft = False
                    if self.frame_dance==210:
                        if not (player_headingRight and moving):
                            self.rain()
                elif self.pattern==2: #→ ← ← →
                    if self.frame_dance>150 and self.frame_dance<211:
                        self.letsleft = True
                    if self.frame_dance==180 or self.frame_dance==210:
                        if not (not player_headingRight and moving):
                            self.rain()
                    if (self.frame_dance>120 and self.frame_dance<151) or (self.frame_dance>210 and self.frame_dance<241):
                        self.letsleft = False
                    if self.frame_dance==150 or self.frame_dance==240:
                        if not (player_headingRight and moving):
                            self.rain()
                elif self.pattern==3: #→ ← → →
                    if self.frame_dance>150 and self.frame_dance<181:
                        self.letsleft = True
                    if self.frame_dance==180:
                        if not (not player_headingRight and moving):
                            self.rain()
                    if (self.frame_dance>120 and self.frame_dance<151) or (self.frame_dance>180 and self.frame_dance<241):
                        self.letsleft = False
                    if self.frame_dance==150 or self.frame_dance==210 or self.frame_dance==240:
                        if not (player_headingRight and moving):
                            self.rain()
                elif self.pattern==4: #←/→/← →/←
                    if (self.frame_dance>120 and self.frame_dance<151) or (self.frame_dance>180 and self.frame_dance<196) or (self.frame_dance>210 and self.frame_dance<241):
                        self.letsleft = True
                    if self.frame_dance==150 or self.frame_dance==195 or self.frame_dance==240:
                        if not (not player_headingRight and moving):
                            self.rain()
                    if (self.frame_dance>150 and self.frame_dance<181) or (self.frame_dance>195 and self.frame_dance<211):
                        self.letsleft = False
                    if self.frame_dance==180 or self.frame_dance==210:
                        if not (player_headingRight and moving):
                            self.rain()
        def render(self):
            windowSurface.blit(humanfacedbirdImage[self.frame_sprite_sized], self.rect)
            if self.frame_dance>0 and self.frame_dance<121:
                if (self.frame_dance>0 and self.frame_dance<31) or (self.frame_dance>60 and self.frame_dance<91):
                    windowSurface.blit(buttonleftImage, self.buttonleftRect)
                    windowSurface.blit(buttonrightImage, self.buttonrightRect)
            elif self.frame_dance>120 and self.frame_dance<241:
                if self.letsleft:
                    windowSurface.blit(buttonleftImage, self.buttonleftRect)
                else:
                    windowSurface.blit(buttonrightImage, self.buttonrightRect)
            if self.frame_rain==0 and not self.frame_dance==0:
                windowSurface.blit(self.text, self.textRect)
            windowSurface.blit(bossbarImage, self.bossbar_backRect, (0, 0, 960, 10))
            self.bossbar_frontRect = pygame.Rect(160, 10, self.health//3, 10)
            windowSurface.blit(bossbarImage, self.bossbar_frontRect, (0, 10, self.bossbar_frontRect.width, self.bossbar_frontRect.height))
    #중간보스 인면조 human faced bird

    medivhImage_fly = []
    for i in range(1, 9, 1):
        medivhImage_fly.append(pygame.image.load(os.path.join(current_path, "img/medivh/fly/fly{}.png".format(i))).convert_alpha())
    medivhImage_downwardAndShoot = []
    for i in range(1, 11, 1):
        medivhImage_downwardAndShoot.append(pygame.image.load(os.path.join(current_path, "img/medivh/downwardAndShoot/downwardAndShoot{}.png".format(i))).convert_alpha())
    medivhImage_shoot = []
    for i in range(1, 6, 1):
        medivhImage_shoot.append(pygame.image.load(os.path.join(current_path, "img/medivh/shoot/shoot{}.png".format(i))).convert_alpha())
    medivhImage_upward_bottom = []
    for i in range(1, 13, 1):
        medivhImage_upward_bottom.append(pygame.image.load(os.path.join(current_path, "img/medivh/upward_bottom/upward_bottom{}.png".format(i))).convert_alpha())
    medivhImage_upward_top = []
    for i in range(7, 13, 1):
        medivhImage_upward_top.append(pygame.image.load(os.path.join(current_path, "img/medivh/upward_top/upward_top{}.png".format(i))).convert_alpha())
    medivhPath = np.load(os.path.join(current_path, "array/medivhPath.npy"))
    medivhsRect = []
    class medivhRect:
        def __init__(self, left, top, width, height, identity):
            global identityNumber
            self.identity = identity
            identityNumber += 1
            self.rect = pygame.Rect(left, top, width, height)
            self.upwardTopRect = pygame.Rect(self.rect.left, self.rect.top-149, 210, 149)
            self.flyRect = pygame.Rect(self.rect.left, self.rect.top-235, 210, 320)
            self.bossbar_backRect = pygame.Rect(160, 10, 960, 10)
            self.bossbar_frontRect = pygame.Rect(160, 10, 960, 10)
            self.health = 5760
            self.frame = 0
            self.frame_sprite = 0
            self.frame_sprite_sized = 0
            self.state = 0
            self.frame_wait = 0
            self.remainArcanelift = 2
            self.moving = False
            self.destination = (1280, 225)
            self.heading = -1
            self.random = 0
        def summon(self):
            medivhsRect.append(self)
        def kill(self):
            global finalBossFallen
            medivhsRect.remove(self)
            finalBossFallen = True
        def damage(self, damage):
            self.health -= damage
        def progressState(self):
            if self.state<3:
                self.state += 1
            else:
                self.state = 0
            self.frame_sprite = 0
        def progressFrame(self):
            global hit_by_arcanelift
            self.frame += 1
            self.random = r.randint(0, 200)
            if self.state==0:
                if self.frame_sprite<23:
                    self.frame_sprite += 1
                else:
                    self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//3
            elif self.state==1:
                if self.frame_sprite<9:
                    self.frame_sprite += 1
                else:
                    self.progressState()
                self.frame_sprite_sized = self.frame_sprite//1
            elif self.state==2:
                if self.frame_wait<99:
                    self.frame_wait += 1
                if self.frame_sprite<4:
                    self.frame_sprite += 1
                else:
                    if self.remainArcanelift!=0:
                        self.frame_sprite = 0
                        self.remainArcanelift -= 1
                    elif self.remainArcanelift==0 and self.frame_wait==99 and not hit_by_arcanelift:
                        self.frame_wait = 0
                        self.remainArcanelift = 2
                        self.progressState()
                    elif self.remainArcanelift==0 and self.frame_wait==99 and hit_by_arcanelift:
                        self.frame_wait = 0
                        hit_by_arcanelift = False
                        self.remainArcanelift = 2
                        self.frame_sprite = 0
                self.frame_sprite_sized = self.frame_sprite//1
            elif self.state==3:
                if self.frame_sprite<47:
                    self.frame_sprite += 1
                else:
                    self.progressState()
                self.frame_sprite_sized = self.frame_sprite//4
        def move(self):
            SPEED_MEDIVH = 8
            if self.state==0:
                if not self.moving:
                    self.moving = True
                    self.destination = medivhPath[r.randint(0, 10)]
                    if self.destination[0]-self.rect.centerx>=0:
                        self.heading = 1
                    else:
                        self.heading = -1
                if self.moving:
                    self.rect.centerx += self.heading*SPEED_MEDIVH
                if (self.heading==1 and self.rect.centerx>self.destination[0]) or (self.heading==-1 and self.rect.centerx<=self.destination[0]):
                    self.moving = False
                if self.random==200:
                    self.progressState()
            else:
                if playerRect.centerx-self.rect.centerx>=0:
                    self.heading = 1
                else:
                    self.heading = -1
            self.upwardTopRect = pygame.Rect(self.rect.left, self.rect.top-149, 210, 149)
            self.flyRect = pygame.Rect(self.rect.left, self.rect.top-235, 210, 320)
        def testCollision(self):
            DAMAGE_MEDIVH_PLAYER = 1
            global hit_by_arcanelift
            global remainheart
            global score
            global frame_player_hit
            global player_hit
            global statistics_collideEnemyCount
            global statistics_receivedDamage
            global statistics_hitCount
            if self.state==1 or self.state==2 or self.state==3:
                for stone in stonesRect:
                    if self.rect.colliderect(stone.rect) and self.identity not in stone.identityList:
                        stone.identityList.append(self.identity)
                        stone.remainPenetration -= 1
                        statistics_hitCount += 1
                        stoneSpeed = m.floor(m.sqrt(stone.speedx**2+stone.speedy**2))
                        self.damage(timesDamage*stoneSpeed*2)
                        if not penetrable or stone.remainPenetration==0:
                            stone.kill()
                if playerRect.colliderect(self.rect) and not player_hit:
                    player_hit = True
                    frame_player_hit = 1
                    remainheart -= DAMAGE_MEDIVH_PLAYER
                    statistics_receivedDamage += DAMAGE_MEDIVH_PLAYER
                    self.damage(40)
                    statistics_collideEnemyCount += 1
            if self.state==0:
                for stone in stonesRect:
                    if self.flyRect.colliderect(stone.rect) and self.identity not in stone.identityList:
                        stone.identityList.append(self.identity)
                        stone.remainPenetration -= 1
                        stoneSpeed = m.floor(m.sqrt(stone.speedx**2+stone.speedy**2))
                        self.damage(timesDamage*stoneSpeed//3) #메디브 까마귀 폼일 때는 피격 시 대미지가 6분의 1
                        if not penetrable or stone.remainPenetration==0:
                            stone.kill()
                if playerRect.colliderect(self.flyRect) and not player_hit:
                    player_hit = True
                    frame_player_hit = 1
                    remainheart -= DAMAGE_MEDIVH_PLAYER
                    self.damage(10)
        def shootArcanelift(self):
            if (self.state==1 and self.frame_sprite_sized==9) or (self.state==2 and self.frame_sprite_sized==0):
                projectileRect(self.rect.left+69, self.rect.top-20, 69, 75, "arcanelift", 0, self).summon()
        def render(self):
            if self.state==0:
                if self.heading==1:
                    windowSurface.blit(medivhImage_fly[self.frame_sprite_sized], self.flyRect)
                elif self.heading==-1:
                    windowSurface.blit(pygame.transform.flip(medivhImage_fly[self.frame_sprite_sized], True, False), self.flyRect)
            if self.state==1:
                if self.heading==1:
                    windowSurface.blit(medivhImage_downwardAndShoot[self.frame_sprite_sized], self.rect)
                elif self.heading==-1:
                    windowSurface.blit(pygame.transform.flip(medivhImage_downwardAndShoot[self.frame_sprite_sized], True, False), self.rect)
            if self.state==2:
                if self.heading==1:
                    windowSurface.blit(medivhImage_shoot[self.frame_sprite_sized], self.rect)
                elif self.heading==-1:
                    windowSurface.blit(pygame.transform.flip(medivhImage_shoot[self.frame_sprite_sized],True, False), self.rect)
            if self.state==3:
                if self.heading==1:
                    windowSurface.blit(medivhImage_upward_bottom[self.frame_sprite_sized], self.rect)
                    if self.frame_sprite_sized>=6:
                        windowSurface.blit(medivhImage_upward_top[self.frame_sprite_sized-6], self.upwardTopRect)
                elif self.heading==-1:
                    windowSurface.blit(pygame.transform.flip(medivhImage_upward_bottom[self.frame_sprite_sized], True, False), self.rect)
                    if self.frame_sprite_sized>=6:
                        windowSurface.blit(pygame.transform.flip(medivhImage_upward_top[self.frame_sprite_sized-6], True, False), self.upwardTopRect)
            windowSurface.blit(bossbarImage, self.bossbar_backRect, (0, 0, 960, 10))
            self.bossbar_frontRect = pygame.Rect(160, 10, self.health//6, 10)
            windowSurface.blit(bossbarImage, self.bossbar_frontRect, (0, 10, self.bossbar_frontRect.width, self.bossbar_frontRect.height))
    #막보스 메디브 medivh

    LENGTH_WAVE = 2400 #default: 2400
    midBossFallen = False
    finalBossFallen = False
    sparrowCounter = 0
    LIMITSPARROW = 150
    ostrichCounter = 0
    LIMITOSTRICH = 120
    eliteostrichCounter = 0
    LIMITELITEOSTRICH = 1200
    ufoCounter = 0
    LIMITUFO = 750
    class progressWave:
        def __init__(self):
            self.frame = 0
            self.midBossSummoned = False
            self.finalBossSummoned = False
            self.text = arcadeFont64.render('WAVE 0', True, WHITE)
            self.textRect = self.text.get_rect()
            self.textRect.left = windowSurface.get_rect().left
            self.textRect.bottom = windowSurface.get_rect().bottom
            alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
            alpha_img.fill((255, 255, 255, 255))
            self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        def summon_sparrow(self):
            global sparrowCounter
            if sparrowCounter>=LIMITSPARROW:
                sparrowCounter = 0
                enemyRect(1280, 0, 32, 32, "sparrow", r.randint(0, 5)).summon()
            else:
                sparrowCounter += 1
        def summon_ostrich(self):
            global ostrichCounter
            if ostrichCounter>=LIMITOSTRICH:
                ostrichCounter = 0
                enemyRect(r.randint(WINDOWWIDTH, WINDOWWIDTH+300), r.randint(512, 552), 48, 48, "ostrich", 0).summon()
            else:
                ostrichCounter += 1
        def summon_eliteostrich(self):
            global eliteostrichCounter
            if eliteostrichCounter>=LIMITELITEOSTRICH:
                eliteostrichCounter = 0
                eliteenemyRect(r.randint(WINDOWWIDTH, WINDOWWIDTH+300), r.randint(470, 510), 96, 96, "eliteostrich", 0, identityNumber).summon()
            else:
                eliteostrichCounter += 1
        def summon_spire(self):
            towerRect(850, -400, 252, 400, "spire", 0, identityNumber).summon()
        def summon_ufo(self):
            global ufoCounter
            if ufoCounter>=LIMITUFO:
                ufoCounter = 0
                enemyRect(1280, 44, 58, 40, "ufo", 0).summon()
            else:
                ufoCounter += 1
        def summon_humandfacedbird(self):
            humanfacedbirdRect(1280, 176, 410, 364, identityNumber).summon()
        def summon_greaterspire(self):
            towerRect(850, -400, 252, 400, "greaterspire", 0, identityNumber).summon()
        def summon_medivh(self):
            medivhRect(1280, 340, 210, 280, identityNumber).summon()
        def progressFrame(self):
            if self.frame<3*LENGTH_WAVE:
                self.frame += 1
            elif self.frame<4*LENGTH_WAVE and midBossFallen:
                self.frame += 1
        def waveN(self):
            global statistics_timeToDestroySpire
            global statistics_timeToDestroyGreaterspire
            global statistics_timeToKillHumanfacedbird
            global statistics_timeToKillMedivh
            if self.frame>0: #0
                self.summon_sparrow()
            if self.frame==LENGTH_WAVE//8: #0+450
                bonusbirdRect(1280, 0, 32, 32, "dove").summon() #보너스 비둘기
            if self.frame>LENGTH_WAVE//2: #1800
                self.summon_ostrich()
                self.summon_eliteostrich()
            if self.frame==LENGTH_WAVE//2+1: #1801
                for bonusbird in bonusbirdsRect:
                    bonusbird.extinguish = True
            if self.frame==LENGTH_WAVE//2+LENGTH_WAVE//8: #1800+450
                bonusbirdRect(1280, 0, 32, 32, "raven").summon() #보너스 깨매기
            if self.frame==LENGTH_WAVE+1: #3601
                self.summon_spire()
                for bonusbird in bonusbirdsRect:
                    bonusbird.extinguish = True
            if self.frame>LENGTH_WAVE and not spireDestroyed: #3600
                statistics_timeToDestroySpire += 1
            if self.frame==LENGTH_WAVE+LENGTH_WAVE//4: #3600+900
                bonusbirdRect(1280, 0, 64, 50, "crane").summon() #보너스 드로미
            if self.frame>2*LENGTH_WAVE: #7200
                self.summon_ufo()
            if self.frame==2*LENGTH_WAVE+1: #7201
                for bonusbird in bonusbirdsRect:
                    bonusbird.extinguish = True
            if self.frame==2*LENGTH_WAVE+LENGTH_WAVE//4: #7200+900
                bonusbirdRect(1280, 0, 64, 64, "pelican").summon() #보너스 펠리컨
            if self.frame==3*LENGTH_WAVE and not self.midBossSummoned: #10800
                self.summon_humandfacedbird()
                self.midBossSummoned = True
                for bonusbird in bonusbirdsRect:
                    bonusbird.extinguish = True
            if self.frame==3*LENGTH_WAVE+LENGTH_WAVE//8: #10800+450
                self.summon_greaterspire()
            if self.frame>3*LENGTH_WAVE+LENGTH_WAVE//8 and not greaterspireDestroyed: #10800+450
                statistics_timeToDestroyGreaterspire += 1
            if self.frame==3*LENGTH_WAVE+LENGTH_WAVE//4: #10800+900
                bonusbirdRect(1280, 0, 45, 40, "parrot").summon() #보너스 앵무새
            if self.frame==4*LENGTH_WAVE and not self.finalBossSummoned: #14400
                self.summon_medivh()
                self.finalBossSummoned = True
                for bonusbird in bonusbirdsRect:
                    bonusbird.extinguish = True
            if self.midBossSummoned and not midBossFallen:
                statistics_timeToKillHumanfacedbird += 1
            if self.finalBossSummoned and not finalBossFallen:
                statistics_timeToKillMedivh += 1
        def render(self):
            global statistics_lastWave #여기가 좀 깔끔해서 waveN() 대신 여기에서
            if self.frame>0 and self.frame<=LENGTH_WAVE//2:
                self.text = arcadeFont64.render('WAVE 1', True, WHITE)
                self.textRect = self.text.get_rect()
                self.textRect.left = windowSurface.get_rect().left
                self.textRect.bottom = windowSurface.get_rect().bottom
                alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
                alpha_img.fill((255, 255, 255, 255))
                self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                statistics_lastWave = 1
            elif self.frame>LENGTH_WAVE//2 and self.frame<=LENGTH_WAVE:
                self.text = arcadeFont64.render('WAVE 2', True, WHITE)
                self.textRect = self.text.get_rect()
                self.textRect.left = windowSurface.get_rect().left
                self.textRect.bottom = windowSurface.get_rect().bottom
                alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
                alpha_img.fill((255, 255, 255, 255))
                self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                statistics_lastWave = 2
            elif self.frame>LENGTH_WAVE and self.frame<=2*LENGTH_WAVE:
                self.text = arcadeFont64.render('WAVE 3', True, WHITE)
                self.textRect = self.text.get_rect()
                self.textRect.left = windowSurface.get_rect().left
                self.textRect.bottom = windowSurface.get_rect().bottom
                alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
                alpha_img.fill((255, 255, 255, 255))
                self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                statistics_lastWave = 3
            elif self.frame>2*LENGTH_WAVE and self.frame<3*LENGTH_WAVE:
                self.text = arcadeFont64.render('WAVE 4', True, WHITE)
                self.textRect = self.text.get_rect()
                self.textRect.left = windowSurface.get_rect().left
                self.textRect.bottom = windowSurface.get_rect().bottom
                alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
                alpha_img.fill((255, 255, 255, 255))
                self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                statistics_lastWave = 4
            elif self.frame==3*LENGTH_WAVE:
                self.text = arcadeFont64.render('WAVE 5', True, WHITE)
                self.textRect = self.text.get_rect()
                self.textRect.left = windowSurface.get_rect().left
                self.textRect.bottom = windowSurface.get_rect().bottom
                alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
                alpha_img.fill((255, 255, 255, 255))
                self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                statistics_lastWave = 5
            elif self.frame>3*LENGTH_WAVE and self.frame<4*LENGTH_WAVE:
                self.text = arcadeFont64.render('WAVE 6', True, WHITE)
                self.textRect = self.text.get_rect()
                self.textRect.left = windowSurface.get_rect().left
                self.textRect.bottom = windowSurface.get_rect().bottom
                alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
                alpha_img.fill((255, 255, 255, 255))
                self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                statistics_lastWave = 6
            elif self.frame==4*LENGTH_WAVE:
                self.text = arcadeFont64.render('WAVE 7', True, WHITE)
                self.textRect = self.text.get_rect()
                self.textRect.left = windowSurface.get_rect().left
                self.textRect.bottom = windowSurface.get_rect().bottom
                alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
                alpha_img.fill((255, 255, 255, 255))
                self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                statistics_lastWave = 7
            windowSurface.blit(self.text, self.textRect)
    wave = progressWave()
    #웨이브 와 미춌네 미춌어 진짜

    score = 0
    score_text = dunggeunmo48.render('SCORE: {}'.format(score), True, BLACK)
    score_textRect = score_text.get_rect()
    score_textRect.right = windowSurface.get_rect().right
    score_textRect.top = windowSurface.get_rect().top
    alpha_img = pygame.Surface(score_text.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    score_text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    #점수

    def makeHearts(remainheart):
        heartsImage = []
        heartsRect = []
        for i in range(remainheart//2):
            heartsImage.append(pygame.image.load(os.path.join(current_path, 'img/heart/heart_2.png')).convert_alpha())
        for i in range(remainheart%2):
            heartsImage.append(pygame.image.load(os.path.join(current_path, 'img/heart/heart_1.png')).convert_alpha())
        for i in range(5-remainheart//2-remainheart%2):
            heartsImage.append(pygame.image.load(os.path.join(current_path, 'img/heart/heart_0.png')).convert_alpha())
        for i in range(5):
            heartsRect.append(pygame.Rect(478+65*i,647,65,63))
        return [heartsImage, heartsRect]
    remainheart = 10
    makeHearts(remainheart)
    #생명력

    object_text = dunggeunmo64.render('OBJECT: Protect the wheat field!', True, PINK)
    object_textRect = object_text.get_rect()
    object_textRect.centerx = windowSurface.get_rect().centerx
    object_textRect.centery = windowSurface.get_rect().centery
    #목표 텍스트

    game_optionImage = pygame.image.load(os.path.join(current_path, 'img/option.png')).convert_alpha()
    game_optionRect = pygame.Rect(0,0,100,100)
    game_optionRect.right = windowSurface.get_rect().right
    game_optionRect.bottom = windowSurface.get_rect().bottom
    #게임 내 옵션 아이콘

    game_option_text_1 = arcadeFont64.render('RESUME GAME', True, OCHER)
    game_option_textRect_1 = game_option_text_1.get_rect()
    game_option_textRect_1.centerx = windowSurface.get_rect().centerx
    game_option_textRect_1.centery = windowSurface.get_rect().centery-200
    alpha_img = pygame.Surface(game_option_text_1.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    game_option_text_1.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    game_option_text_2 = arcadeFont64.render('CONTROLS', True, OCHER)
    game_option_textRect_2 = game_option_text_2.get_rect()
    game_option_textRect_2.centerx = windowSurface.get_rect().centerx
    game_option_textRect_2.centery = windowSurface.get_rect().centery
    alpha_img = pygame.Surface(game_option_text_2.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    game_option_text_2.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    game_option_text_3 = arcadeFont64.render('QUIT', True, OCHER)
    game_option_textRect_3 = game_option_text_3.get_rect()
    game_option_textRect_3.centerx = windowSurface.get_rect().centerx
    game_option_textRect_3.centery = windowSurface.get_rect().centery+200
    alpha_img = pygame.Surface(game_option_text_3.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255))
    game_option_text_3.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    #게임옵션 텍스트

    game_controls_text = dunggeunmo48.render('OKAY', True, OCHER, BLACK)
    game_controls_textRect = game_controls_text.get_rect()
    game_controls_textRect.centerx = windowSurface.get_rect().centerx
    game_controls_textRect.centery = windowSurface.get_rect().centery+300
    #게임 컨트롤 텍스트

    game_controlsImage = controlsImage = pygame.image.load(os.path.join(current_path, 'img/controls_guideline.png')).convert_alpha()
    game_controlsRect = game_controlsImage.get_rect()
    game_controlsRect.centerx = windowSurface.get_rect().centerx
    game_controlsRect.centery = windowSurface.get_rect().centery
    #게임 컨트롤 이미지

    brokenheartImage = pygame.image.load(os.path.join(current_path, 'img/heart/broken_heart.png')).convert_alpha()
    brokenheartRect = pygame.Rect(0, 0, 840,561)
    brokenheartRect.centerx = windowSurface.get_rect().centerx
    brokenheartRect.centery = windowSurface.get_rect().centery
    #데스화면 이미지

    death_epilogue_text_1 = dunggeunmo48.render("Though he was fallen, however, sparrows survived.", True, WHITE, BLACK)
    death_epilogue_textRect_1 = death_epilogue_text_1.get_rect()
    death_epilogue_textRect_1.centerx = windowSurface.get_rect().centerx
    death_epilogue_textRect_1.centery = windowSurface.get_rect().centery+100
    death_epilogue_text_2 = dunggeunmo48.render("So severeal millions of Chinese", True, WHITE, BLACK)
    death_epilogue_textRect_2 = death_epilogue_text_2.get_rect()
    death_epilogue_textRect_2.centerx = windowSurface.get_rect().centerx
    death_epilogue_textRect_2.centery = windowSurface.get_rect().centery+150
    death_epilogue_text_3 = dunggeunmo48.render("didn't have to starve.", True, WHITE, BLACK)
    death_epilogue_textRect_3 = death_epilogue_text_3.get_rect()
    death_epilogue_textRect_3.centerx = windowSurface.get_rect().centerx
    death_epilogue_textRect_3.centery = windowSurface.get_rect().centery+200
    #데스 에필로그 텍스트

    death_epilogueImage = pygame.transform.flip(playersImage_Idle[0], False, True)
    death_epilogueRect = death_epilogueImage.get_rect()
    death_epilogueRect.centerx = windowSurface.get_rect().centerx
    death_epilogueRect.centery = windowSurface.get_rect().centery
    #데스 에필로그 이미지

    victory_text = arcadeFont64.render("VICTORY", True, WHITE, BLACK)
    victory_textRect = victory_text.get_rect()
    victory_textRect.centerx = windowSurface.get_rect().centerx
    victory_textRect.centery = windowSurface.get_rect().centery
    #승리 텍스트

    victory_epilogueImage_1 = pygame.image.load(os.path.join(current_path, 'img/storyline/epilogue_1.png')).convert_alpha()
    victory_epilogueRect_1 = pygame.Rect(0, 0, 244, 365)
    victory_epilogueRect_1.centerx = windowSurface.get_rect().centerx
    victory_epilogueRect_1.centery = windowSurface.get_rect().centery
    victory_epilogueImage_2 = pygame.image.load(os.path.join(current_path, 'img/storyline/epilogue_2.png')).convert_alpha()
    victory_epilogueRect_2 = pygame.Rect(0, 0, 216, 364)
    victory_epilogueRect_2.centerx = windowSurface.get_rect().centerx
    victory_epilogueRect_2.centery = windowSurface.get_rect().centery
    # 승리 에필로그 이미지

    victory_epilogue_text_1_1 = dunggeunmo24.render("With that one word, all the sparrows were wiped out.", True, WHITE, BLACK)
    victory_epilogue_textRect_1_1 = victory_epilogue_text_1_1.get_rect()
    victory_epilogue_textRect_1_1.centerx = windowSurface.get_rect().centerx
    victory_epilogue_textRect_1_1.centery = windowSurface.get_rect().centery+230
    victory_epilogue_text_1_2 = dunggeunmo24.render("However, the pests that were the prey of the sparrow surged,", True, WHITE, BLACK)
    victory_epilogue_textRect_1_2 = victory_epilogue_text_1_2.get_rect()
    victory_epilogue_textRect_1_2.centerx = windowSurface.get_rect().centerx
    victory_epilogue_textRect_1_2.centery = windowSurface.get_rect().centery+260
    victory_epilogue_text_1_3 = dunggeunmo24.render("causing the Chinese continent to suffer from famine.", True, WHITE, BLACK)
    victory_epilogue_textRect_1_3 = victory_epilogue_text_1_3.get_rect()
    victory_epilogue_textRect_1_3.centerx = windowSurface.get_rect().centerx
    victory_epilogue_textRect_1_3.centery = windowSurface.get_rect().centery+290
    victory_epilogue_text_2_1 = dunggeunmo24.render("According to one report, 40 million Chinese died of hunger at that time.", True, WHITE, BLACK)
    victory_epilogue_textRect_2_1 = victory_epilogue_text_2_1.get_rect()
    victory_epilogue_textRect_2_1.centerx = windowSurface.get_rect().centerx
    victory_epilogue_textRect_2_1.centery = windowSurface.get_rect().centery+240
    victory_epilogue_text_2_2 = dunggeunmo24.render("It was a tragic result of the fingers of the 'hero'.", True, WHITE, BLACK)
    victory_epilogue_textRect_2_2 = victory_epilogue_text_2_2.get_rect()
    victory_epilogue_textRect_2_2.centerx = windowSurface.get_rect().centerx
    victory_epilogue_textRect_2_2.centery = windowSurface.get_rect().centery+270
    #승리 에필로그 텍스트

    statistics_texts_left = []
    statistics_textsRect_left = []
    statistics_texts_right = []
    statistics_textsRect_right = []
    statisticsArray_made = False
    creditImage = pygame.image.load(os.path.join(current_path, 'img/credit.png')).convert_alpha()
    creditRect = pygame.Rect(0, 0, 1280, 720)
    #크레딧

    scoreboardImage = pygame.image.load(os.path.join(current_path, 'img/scoreboard.png')).convert_alpha()
    scoreboardRect = pygame.Rect(0, 0, 1280, 720)
    yourname_text = dunggeunmo48.render("Your Name:", True, RED, BLACK)
    yourname_textRect = yourname_text.get_rect()
    yourname_textRect.right = 1250
    yourname_textRect.top = 30 #커서 추가 시급
    tooLong = False
    username_made = False
    username = ""
    username_text = dunggeunmo24.render("no name", True, WHITE, BLACK)
    username_textRect = username_text.get_rect()
    cursorImage = pygame.image.load(os.path.join(current_path, 'img/cursor.png')).convert_alpha()
    cursorRect = pygame.Rect(1250, 85, 4, 15)
    whenyoutype_text = dunggeunmo24.render("when you type", True, OCHER, BLACK)
    whenyoutype_textRect = whenyoutype_text.get_rect()
    whenyoutype_textRect.right = 1250
    whenyoutype_textRect.top = yourname_textRect.bottom+100
    allyourname_text = dunggeunmo24.render("all your name", True, OCHER, BLACK)
    allyourname_textRect = allyourname_text.get_rect()
    allyourname_textRect.right = 1250
    allyourname_textRect.top = whenyoutype_textRect.bottom
    pressenter_text = dunggeunmo36.render("Press Enter", True, OCHER, BLACK)
    pressenter_textRect = pressenter_text.get_rect()
    pressenter_textRect.right = 1250
    pressenter_textRect.top = allyourname_textRect.bottom
    ifyouwantto_text = dunggeunmo24.render('if you want to', True, OCHER, BLACK)
    ifyouwantto_textRect = ifyouwantto_text.get_rect()
    ifyouwantto_textRect.right = 1250
    ifyouwantto_textRect.top = pressenter_textRect.bottom+50
    restartthegame_text = dunggeunmo24.render('restart the game', True, OCHER, BLACK)
    restartthegame_textRect = restartthegame_text.get_rect()
    restartthegame_textRect.right = 1250
    restartthegame_textRect.top = ifyouwantto_textRect.bottom
    pressenter_text_0 = dunggeunmo36.render("Press Enter", True, OCHER, BLACK)
    pressenter_textRect_0 = pressenter_text_0.get_rect()
    pressenter_textRect_0.right = 1250
    pressenter_textRect_0.top = restartthegame_textRect.bottom
    lineNumber = 0
    lineNumbers = [] #각 데이터의 점수 부분 라인 넘버
    scores_made = False
    scores = []
    scoreboardRect_made = False
    usernames = []
    usernames_text = []
    usernames_textRect = []
    scores_text = []
    scores_textRect = []
    quit_text = arcadeFont64.render('QUIT', True, RED, BLACK)
    quit_textRect = quit_text.get_rect()
    quit_textRect.right = windowSurface.get_rect().right
    quit_textRect.bottom = windowSurface.get_rect().bottom
    #점수판

    frame_logo = 1
    frame_logo_top = 0
    frame_logo_bottom = 1
    frame_prologue = 0
    frame_parrot = 0
    frame_player = 0
    frame_object = 0
    frame_jump = 2
    frame_click = 0
    frame_ostrich = 0
    frame_death = 0
    frame_victory = 0
    frame_victory_epilogue = 0
    frame_cursor = 0
    #프레임

    def Init():
        global Game_State
        Game_State=S_LOGO

    def Update_Logo():
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_RETURN:
                    Game_State = S_MENU
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        #키보드 입력 감지
        global frame_logo_top
        global logo_text_0
        global logo_textRect_0
        if logo_textRect_0.centerx<windowSurface.get_rect().centerx:
            logo_textRect_0.centerx += 3
        if logo_textRect_0.centerx>windowSurface.get_rect().centerx:
            logo_textRect_0.centerx = windowSurface.get_rect().centerx
        if logo_textRect_0.centerx==windowSurface.get_rect().centerx and logo_textRect_0.centery>40 and frame_logo_top<240:
            frame_logo_top += 1
            frame_logo_top_sized = frame_logo_top//15
            logo_text_0 = pygame.font.Font(os.path.join(font_path, "ArcadeClassic.ttf"), 64-frame_logo_top_sized).render('Lets  All  Beat  the  Sparrows  Together', True, PINK)
            logo_textRect_0 = logo_text_0.get_rect()
            logo_textRect_0.centerx = windowSurface.get_rect().centerx
            logo_textRect_0.centery = windowSurface.get_rect().centery-m.trunc(4/3*frame_logo_top)
        #로고 상단
        global frame_logo
        if frame_logo_top==240:
            if frame_logo<120:
                frame_logo += 1
            else:
                frame_logo = 1
        #범용 프레임 로고
        global frame_logo_bottom
        if frame_logo_bottom<120:
            frame_logo_bottom += 1
        else:
            frame_logo_bottom = 1
        #로고 하단 프레임

    def Update_Menu():
        global arrow
        global arrow_textRect
        arrow_textRect.centery = 160+200*arrow
        #화살표
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                clickPos = event.pos
                if event.button==1 and menu_textRect_1.collidepoint(clickPos):
                    Game_State=S_PROLOGUE
                elif event.button==1 and menu_textRect_2.collidepoint(clickPos):
                    Game_State=S_MENU_SCOREBOARD
                elif event.button==1 and menu_textRect_3.collidepoint(clickPos):
                    Game_State=S_OPTION #텍스트 클릭
            elif event.type==KEYDOWN:
                if event.key == K_RETURN:
                    if arrow==0:
                        Game_State=S_PROLOGUE
                    if arrow==1:
                        Game_State=S_MENU_SCOREBOARD
                    if arrow==2:
                        Game_State=S_OPTION
                elif event.key==K_UP:
                    if arrow!=0:
                        arrow -= 1
                elif event.key==K_DOWN:
                    if arrow!=2:
                        arrow += 1
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        #마우스 입력 감지
        global frame_logo
        if frame_logo<120:
            frame_logo += 1
        else:
            frame_logo = 1
        #범용 프레임 로고

    def Update_Menu_Scoreboard():
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==MOUSEBUTTONUP:
                clickPos = event.pos
                if event.button==1 and backtothemenu_textRect.collidepoint(clickPos):
                    Game_State = S_MENU
            elif event.type==KEYDOWN:
                if event.key==K_RETURN:
                    Game_State = S_MENU
        global menu_lineNumber
        global menu_lineNumbers
        global menu_scores_made
        global menu_scores
        if not menu_scores_made:
            with open(os.path.join(current_path, 'database'), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.split(":")[0]=="statistics" and line.split(":")[2]=="start":
                        menu_lineNumbers.append(menu_lineNumber+1)
                    menu_lineNumber += 1
                for i in menu_lineNumbers:
                    menu_scores.append(lines[i].split(':')[1]) #점수 배열 scores 완성
            menu_scores_made = True
        global menu_scoreboardRect_made
        global menu_usernames
        global menu_usernames_text
        global menu_usernames_textRect
        global menu_scores_text
        global menu_scores_textRect
        if not menu_scoreboardRect_made:
            with open(os.path.join(current_path, 'database_username'), 'r') as f:
                names = f.read().split(":")
                for name in names:
                    menu_usernames.append(name)
            for username in menu_usernames:
                member = dunggeunmo24.render(username, True, WHITE, BLACK)
                menu_usernames_text.append(member)
                menu_usernames_textRect.append(member.get_rect())
            for score in menu_scores:
                member = dunggeunmo24.render(score, True, WHITE, BLACK)
                menu_scores_text.append(member)
                menu_scores_textRect.append(member.get_rect())
            menu_usernames_textRect[0].left = 350
            menu_usernames_textRect[0].top = 15
            menu_scores_textRect[0].right = 930
            menu_scores_textRect[0].top = 15
            for i in range(len(menu_usernames_textRect)-1): #이 앞에 초항 필요
                menu_usernames_textRect[i+1].left = 350
                menu_usernames_textRect[i+1].top = menu_usernames_textRect[i].bottom
            for i in range(len(menu_scores_textRect)-1):
                menu_scores_textRect[i+1].right = 930
                menu_scores_textRect[i+1].top = menu_scores_textRect[i].bottom
            menu_scoreboardRect_made = True

    def Update_Option():
        global arrow
        global arrow_textRect
        arrow_textRect.centery = 160+200*arrow
        #화살표
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                clickPos = event.pos
                if event.button==1 and option_textRect_1.collidepoint(clickPos):
                    Game_State=S_CONTROLS
                elif event.button==1 and option_textRect_2.collidepoint(clickPos):
                    Game_State=S_MENU
                elif event.button==1 and option_textRect_3.collidepoint(clickPos):
                    pygame.quit()
                    sys.exit() #텍스트 클릭
            elif event.type==KEYDOWN:
                if event.key == K_RETURN:
                    if arrow==0:
                        Game_State=S_CONTROLS
                    if arrow==1:
                        Game_State=S_MENU
                    if arrow==2:
                        pygame.quit()
                        sys.exit()
                elif event.key==K_UP:
                    if arrow!=0:
                        arrow -= 1
                elif event.key==K_DOWN:
                    if arrow!=2:
                        arrow += 1
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        #마우스 입력 감지
        global frame_logo
        if frame_logo<120:
            frame_logo += 1
        else:
            frame_logo = 1
        #범용 프레임 로고

    def Update_Controls():
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                clickPos = event.pos
                if event.button==1 and controls_textRect.collidepoint(clickPos):
                    Game_State=S_OPTION #텍스트 클릭
            elif event.type==KEYDOWN:
                if event.key == K_RETURN:
                    Game_State=S_OPTION
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        #마우스 입력 감지
        global frame_logo
        if frame_logo<120:
            frame_logo += 1
        else:
            frame_logo = 1
        #범용 프레임 로고

    def Update_Prologue():
        global Game_State
        global windowSurface
        global isFullscreen
        global frame_prologue
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_RETURN:
                    if frame_prologue<5:
                        frame_prologue += 1
                    else:
                        Game_State = S_PARROT
                elif event.key==K_LEFT:
                    if frame_prologue>0 and frame_prologue<=5:
                        frame_prologue -= 1
                elif event.key==K_RIGHT:
                    if frame_prologue<5:
                        frame_prologue += 1
                    else:
                        Game_State = S_PARROT
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        #마우스 또는 키보드 입력 감지

    def Update_Parrot():
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        #종료
        global frame_parrot
        frame_parrot += 1
        if frame_parrot>119 and frame_parrot<239:
            parrotSpriteRect.centerx += 11
            parrotSpriteRect.centery -= 7
        elif frame_parrot==240:
            Game_State = S_GAME
        #앵무새 프레임

    def Update_Game():
        global Game_State
        global windowSurface
        global isFullscreen
        global moveLeft 
        global moveRight 
        global moveUp 
        global moveDown
        global moving
        global jump
        global playerImage
        global playerRect
        global frame_jump
        global player_headingRight
        global mousebuttondown
        global frame_click
        global statistics_jumpCount
        global statistics_throwingCount
        for i in range(5):
            if cloudsRect[i].right>0:
                cloudsRect[i].right -= i//3+1
            else:
                cloudsRect[i].left = 1280
        #구름
        if frame_jump<33 and jump==True:
            frame_jump += 1
        elif frame_jump==33 and jump==True:
            frame_jump = 2
            jump = False
        frame_jump_sized = frame_jump//2
        #점프 프레임 1
        for event in pygame.event.get():
            if event.type==QUIT:
                #a.printPath() #path디버깅
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mousebuttondown = True
            elif event.type==pygame.MOUSEBUTTONUP:
                #a.savePath() #path디버깅
                clickPos = event.pos
                if event.button==1 and game_optionRect.collidepoint(clickPos):
                    Game_State=S_GAME_OPTION
                if event.button==1 and frame_click!=0 and ((shotgun==False and len(stonesRect)<6) or (shotgun==True and len(stonesRect)<4)): #돌 6개 리미트
                    stoneRect(playerRect.centerx, playerRect.centery, 20, 20).summon(0)
                    statistics_throwingCount += 1
                    if shotgun:
                        stoneRect(playerRect.centerx, playerRect.centery, 20, 20).summon(1)
                        stoneRect(playerRect.centerx, playerRect.centery, 20, 20).summon(2)
                        statistics_throwingCount += 2
                    mousebuttondown = False
                    frame_click = 0
                else:
                    mousebuttondown = False
                    frame_click = 0
                # if event.button==1: #좌표 디버깅
                    # print(clickPos) #좌표 디버깅
            elif event.type == KEYDOWN:
                if event.key==ord('a'):
                    moveRight = False
                    moveLeft = True
                    player_headingRight = False
                if event.key==ord('d'):
                    moveLeft = False
                    moveRight = True
                    player_headingRight = True
                if event.key==ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key==ord('s'):
                    moveUp = False
                    moveDown = True
                if event.key==K_SPACE and jump==False:
                    jump = True
                    statistics_jumpCount += 1
                if event.key==ord('o'):
                    Game_State=S_GAME_OPTION
                if event.key==K_ESCAPE:
                    Game_State=S_GAME_OPTION
                if event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
            if event.type==KEYUP:
                if event.key==ord('a'):
                    moveLeft = False
                if event.key==ord('d'):
                    moveRight = False
                if event.key==ord('w'):
                    moveUp = False
                if event.key==ord('s'):
                    moveDown = False
            #키 입력에 따라 방향 설정
        global statistics_movingDistance
        if moveDown and not jump and playerRect.bottom < 600:
            playerRect.top += MOVESPEED_VERTICAL
            statistics_movingDistance += MOVESPEED_VERTICAL
        if moveUp and not jump and playerRect.bottom > 565:
            playerRect.bottom -= MOVESPEED_VERTICAL
            statistics_movingDistance += MOVESPEED_VERTICAL
        if moveLeft and playerRect.left > 140:
            playerRect.left -= MOVESPEED_HORIZONTAL
            statistics_movingDistance += MOVESPEED_VERTICAL
        if moveRight and playerRect.right < 1280:
            playerRect.right += MOVESPEED_HORIZONTAL
            statistics_movingDistance += MOVESPEED_VERTICAL
        #방향에 따라 이동
        global frame_player
        if frame_player<27:
            frame_player += 1
        else: frame_player = 0
        frame_player_sized = frame_player//7
        global frame_player_hit
        global player_hit
        if frame_player_hit>0 and frame_player_hit<29:
            frame_player_hit += 1
        else:
            frame_player_hit = 0
            player_hit = False
        #플레이어 프레임
        if moveDown==True or moveUp==True or moveLeft==True or moveRight==True:
            moving = True
        if moveDown==False and moveUp==False and moveLeft==False and moveRight==False:
            moving = False
        #움직임 여부
        if moving==True and jump==False and mousebuttondown==False:
            playerImage = playersImage_Walk[frame_player_sized]
        if moving==False and jump==False and mousebuttondown==False:
            playerImage = playersImage_Idle[frame_player_sized]
        if jump==True and mousebuttondown==False:
            playerImage = playersImage_Jump[frame_player_sized]
        if jump==False and mousebuttondown==True:
            playerImage = playersImage_StayAttack[frame_player_sized]
        if jump==True and mousebuttondown==True:
            playerImage = playersImage_JumpAttack[frame_player_sized]
        #움직임 여부에 따라 동작 바꾸기    
        if jump==True:
            playerRect.bottom += jumpDict[frame_jump_sized]
        if playerRect.bottom>600:
            playerRect.bottom = 600 #플레이어가 땅으로 꺼지는 걸 방지
        #점프 실행하기
        if frame_click<39 and mousebuttondown==True:
            frame_click += quickcharge
        #클릭 프레임
        guageRect.centerx = playerRect.centerx
        guageRect.bottom = playerRect.top
        #게이지 위치
        shoot_textRect.centerx = playerRect.centerx
        shoot_textRect.bottom = guageRect.top
        wait_textRect.centerx = playerRect.centerx
        wait_textRect.bottom = guageRect.top
        #발사 대기 텍스트
        for food in foodsRect:
            food.move()
            food.testCollision()
        #음식
        for stone in stonesRect:
            stone.progressFrame()
            #돌 프레임
        for stone in stonesRect:
            stone.move()
            #돌 이동
        for stone in stonesRect:
            if (stone.rect.centerx<0 or stone.rect.centerx>1280) or (stone.rect.centery>720):
                stone.kill()
            #돌 삭제
        #돌
        for projectile in projectilesRect:
            projectile.progressFrame()
            projectile.move()
            projectile.testCollision()
        #직사 투사체
        for bonusbird in bonusbirdsRect:
            bonusbird.progressFrame()
            bonusbird.move()
            bonusbird.testCollision()
        global quickchargeSummoned
        if whishingDove and whishingRaven and whishingCrane and whishingPelican and whishingParrot and not quickchargeSummoned:
            quickchargeSummoned = True
            foodRect(r.randint(300, 500), -30, 30, 30, "quickcharge").summon()
        #보너스 해로운 새
        for enemy in enemiesRect:
            enemy.progressFrame()
            enemy.move()
            enemy.testCollision()
        #해로운 새
        global score
        global statistics_killEliteenemyCount
        SCORE_ELITEOSTRICH = 30
        SCORE_MUTALISK = 10
        SCORE_BROODLORD = 70
        for eliteenemy in eliteenemiesRect:
            eliteenemy.progressFrame()
            eliteenemy.move()
            eliteenemy.testCollision()
            if eliteenemy.health<=0:
                if eliteenemy.eliteenemyType=="eliteostrich":
                    score += SCORE_ELITEOSTRICH
                elif eliteenemy.eliteenemyType=="mutalisk":
                    score += SCORE_MUTALISK
                elif eliteenemy.eliteenemyType=="broodlord":
                    score += SCORE_BROODLORD
                if not eliteenemy.eliteenemyType=="eliteostrich":
                    if r.randint(0, 15)==0:
                        foodRect(eliteenemy.rect.centerx+15, eliteenemy.rect.top-30, 30, 30, "potionLarge").summon() #포션 드랍 6.25%
                eliteenemy.kill()
                statistics_killEliteenemyCount += 1
        #정예 해로운 새
        global statistics_destroySpire
        global statistics_destroyGreaterspire
        SCORE_SPIRE = 200
        SCORE_GREATERSPIRE = 500
        for tower in towersRect:
            tower.progressFrame()
            tower.move()
            tower.spawn()
            tower.testCollision()
            if tower.health<=0:
                foodRect(tower.rect.centerx+15, tower.rect.top-30, 30, 30, "potionLarge").summon() #포션 드랍
                if tower.towerType=="spire":
                    score += SCORE_SPIRE
                    statistics_destroySpire = True
                if tower.towerType=="greaterspire":
                    score += SCORE_GREATERSPIRE
                    statistics_destroyGreaterspire = True
                tower.kill()
        #타워
        global statistics_killHumanfacedbird
        SCORE_HUMANFACEDBIRD = 350
        for humanfacedbird in humanfacedbirdsRect:
            humanfacedbird.progressFrame()
            humanfacedbird.move()
            humanfacedbird.testCollision()
            humanfacedbird.dance()
            if humanfacedbird.health<=0:
                score += SCORE_HUMANFACEDBIRD
                humanfacedbird.kill()
                foodRect(humanfacedbird.rect.centerx+15, humanfacedbird.rect.top-30, 30, 30, "potionLarge").summon() #포션 드랍
                statistics_killHumanfacedbird = True
        #인면조
        global statistics_killMedivh
        SCORE_MEDIVH = 1000
        for medivh in medivhsRect:
            medivh.progressFrame()
            medivh.move()
            medivh.testCollision()
            medivh.shootArcanelift()
            if medivh.health<=0:
                score += SCORE_MEDIVH
                medivh.kill()
                statistics_killMedivh = True
                Game_State = S_VICTORY
        #메디브
        wheatField.makeText()
        wheatField.check_destroyed()
        #밀
        #global score
        global score_text
        global score_textRect
        score_text = dunggeunmo48.render('SCORE: {}'.format(score), True, BLACK)
        score_textRect = score_text.get_rect()
        score_textRect.right = windowSurface.get_rect().right
        score_textRect.top = windowSurface.get_rect().top
        alpha_img = pygame.Surface(score_text.get_size(), pygame.SRCALPHA)
        alpha_img.fill((255, 255, 255, 255))
        score_text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        global remainheart
        if remainheart>10:
            remainheart = 10
        if remainheart<0:
            remainheart = 0
        if remainheart==0:
            Game_State = S_DEATH
        if powerOverwhelming: #무적
            remainheart = 10
        #생명력
        #점수 텍스트 생성
        global frame_object
        if frame_object<160:
            frame_object += 1
        #목표 텍스트
        wave.progressFrame()
        wave.waveN()
        #웨이브

    def Update_Game_Option():
        global arrow
        global arrow_textRect
        arrow_textRect.centery = 160+200*arrow
        #화살표
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                clickPos = event.pos
                if event.button==1 and game_option_textRect_1.collidepoint(clickPos):
                    Game_State=S_GAME
                elif event.button==1 and game_option_textRect_2.collidepoint(clickPos):
                    Game_State=S_GAME_CONTROLS
                elif event.button==1 and game_option_textRect_3.collidepoint(clickPos):
                    pygame.quit()
                    sys.exit() #텍스트 클릭
            elif event.type==KEYDOWN:
                if event.key == K_ESCAPE:
                    Game_State=S_GAME
                if event.key == K_RETURN:
                    if arrow==0:
                        Game_State=S_GAME
                    if arrow==1:
                        Game_State=S_GAME_CONTROLS
                    if arrow==2:
                        pygame.quit()
                        sys.exit()
                elif event.key==K_UP:
                    if arrow!=0:
                        arrow -= 1
                elif event.key==K_DOWN:
                    if arrow!=2:
                        arrow += 1
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        #키보드 혹은 마우스 입력 감지
        global frame_logo
        if frame_logo<120:
            frame_logo += 1
        else:
            frame_logo = 1
        #범용 프레임 로고

    def Update_Game_Controls():
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                clickPos = event.pos
                if event.button==1 and game_controls_textRect.collidepoint(clickPos):
                    Game_State=S_GAME_OPTION #텍스트 클릭
            elif event.type==KEYDOWN:
                if event.key == K_RETURN:
                    Game_State=S_GAME_OPTION
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        #키보드 혹은 마우스 입력 감지
        global frame_logo
        if frame_logo<120:
            frame_logo += 1
        else:
            frame_logo = 1
        #범용 프레임 로고

    def Update_Death():
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        global frame_death
        if frame_death<179:
            frame_death += 1
        else:
            frame_death = 0
            Game_State = S_DEATH_EPILOGUE

    def Update_Death_Epilogue():
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_RETURN:
                    Game_State = S_CREDIT
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False

    def Update_Victory():
        global Game_State
        global windowSurface
        global isFullscreen
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        global frame_victory
        if frame_victory<179:
            frame_victory += 1
        else:
            frame_victory = 0
            Game_State = S_VICTORY_EPILOGUE

    def Update_Victory_Epilogue():
        global Game_State
        global windowSurface
        global isFullscreen
        global frame_victory_epilogue
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_RETURN:
                    if frame_victory_epilogue<1:
                        frame_victory_epilogue += 1
                    else:
                        frame_victory_epilogue = 0
                        Game_State = S_CREDIT
                elif event.key==K_LEFT:
                    if frame_victory_epilogue==1:
                        frame_victory_epilogue -= 1
                elif event.key==K_RIGHT:
                    if frame_victory_epilogue==0:
                        frame_victory_epilogue += 1
                    elif frame_victory_epilogue==1:
                        Game_State = S_CREDIT
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False

    def Update_Credit():
        global Game_State
        global windowSurface
        global isFullscreen
        global statistics_score
        statistics_score = score
        global statistics_accuracy
        if statistics_throwingCount==0:
            statistics_accuracy = 0
        else:
            statistics_accuracy = round(statistics_hitCount/statistics_throwingCount*100, 2)
        global statistics_texts_left
        global statistics_textsRect_left
        global statistics_texts_right
        global statistics_textsRect_right
        global statisticsArray_made
        if not statisticsArray_made:
            statisticsArray_left = ["점수",
                                    "움직인 거리",
                                    "점프한 횟수",
                                    "해로운 새와의 충돌 횟수",
                                    "투사체와의 충돌 횟수",
                                    "받은 피해",
                                    "돌을 날린 횟수",
                                    "돌이 명중한 횟수",
                                    "죽인 해로운 새 수",
                                    "죽인 정예 해로운 새 수",
                                    "비둘기 사살",
                                    "까마귀 사살",
                                    "두루미 사살",
                                    "펠리컨 사살",
                                    "앵무새 사살",
                                    "먹은 포션 개수",
                                    "먹은 뚱캔 개수",
                                    "관통",
                                    "샷건",
                                    "빠른 장전",
                                    "스파이어 철거",
                                    "스파이어를 철거하는 데 걸린 시간",
                                    "그레이터 스파이어 철거",
                                    "그레이터 스파이어를 철거하는 데 걸린 시간",
                                    "우두머리 해로운 새 인면조 사살",
                                    "인면조를 사살하는 데 걸린 시간",
                                    "우두머리 해로운 새 메디브 사살",
                                    "메디브를 사살하는 데 걸린 시간",
                                    "게임이 끝날 때의 웨이브",
                                    "잔여 밀밭 내구도"]
            statisticsArray_right = [str(statistics_score),
                                     str(statistics_movingDistance)+"pixels",
                                     str(statistics_jumpCount)+"회",
                                     str(statistics_collideEnemyCount)+"회",
                                     str(statistics_collideProjectileCount)+"회",
                                     str(round(statistics_receivedDamage/2, 1))+"hearts",
                                     str(statistics_throwingCount)+"회",
                                     str(statistics_hitCount)+"회",
                                     str(statistics_killEnemyCount)+"마리",
                                     str(statistics_killEliteenemyCount)+"마리",
                                     str(statistics_killDove),
                                     str(statistics_killRaven),
                                     str(statistics_killCrane),
                                     str(statistics_killPelican),
                                     str(statistics_killParrot),
                                     str(statistics_drinkPotionCount)+"개",
                                     str(statistics_drinkPotionLargeCount)+"개",
                                     str(statistics_acquirePenetrable),
                                     str(statistics_acquireShotgun),
                                     str(statistics_acquireQuickcharge),
                                     str(statistics_destroySpire),
                                     str(int(statistics_destroySpire)*statistics_timeToDestroySpire//24)+"s",
                                     str(statistics_destroyGreaterspire),
                                     str(int(statistics_destroyGreaterspire)*statistics_timeToDestroyGreaterspire//24)+"s",
                                     str(statistics_killHumanfacedbird),
                                     str(int(statistics_killHumanfacedbird)*statistics_timeToKillHumanfacedbird//24)+"s",
                                     str(statistics_killMedivh),
                                     str(int(statistics_killMedivh)*statistics_timeToKillMedivh//24)+"s",
                                     "WAVE"+str(statistics_lastWave),
                                     str(statistics_remainWheatDurability)]
            with open(os.path.join(current_path, 'database'), 'a') as f:
                f.write("\n")
            with open(os.path.join(current_path, 'database'), 'r') as f:
                lines = f.readlines()
                statisticsDataNumber = int(lines[-1].split(':')[1])+1
            with open(os.path.join(current_path, 'database'), 'a') as f:
                f.write("\nstatistics:"+str(statisticsDataNumber)+":start:")
                for i in range(len(statisticsArray_left)):
                    f.write("\n"+statisticsArray_left[i]+":"+statisticsArray_right[i]+":")
                f.write("\nstatistics:"+str(statisticsDataNumber)+":end:")
            with open(os.path.join(current_path, 'database_username'), 'a') as f: #noname
                f.write(":no name")
            for i in statisticsArray_left:
                member = dunggeunmo22.render(i, True, WHITE, BLACK)
                statistics_texts_left.append(member)
                statistics_textsRect_left.append(member.get_rect())
            for i in statisticsArray_right:
                member = dunggeunmo22.render(i, True, OCHER, BLACK)
                statistics_texts_right.append(member)
                statistics_textsRect_right.append(member.get_rect())
            statistics_textsRect_left[0].left = 350
            statistics_textsRect_left[0].top = 720
            statistics_textsRect_right[0].right = 930
            statistics_textsRect_right[0].top = 720
            for i in range(len(statistics_textsRect_left)-1):
                statistics_textsRect_left[i+1].left = 350
                statistics_textsRect_left[i+1].top = statistics_textsRect_left[i].bottom
            for i in range(len(statistics_textsRect_right)-1):
                statistics_textsRect_right[i+1].right = 930
                statistics_textsRect_right[i+1].top = statistics_textsRect_right[i].bottom
            statisticsArray_made = True
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_RETURN:
                    Game_State = S_SCOREBOARD #재시작
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        if statistics_textsRect_left[0].top>15:
            for i in statistics_textsRect_left:
                i.top -= 5
            for i in statistics_textsRect_right:
                i.top -= 5

    def Update_Scoreboard():
        global Game_State
        global windowSurface
        global isFullscreen
        global tooLong
        global username_made
        global username
        if len(username)<20: #글자 20개 제한
            tooLong = False
        else:
            tooLong = True
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==MOUSEBUTTONUP:
                clickPos = event.pos
                if event.button==1 and quit_textRect.collidepoint(clickPos):
                    pygame.quit()
                    sys.exit()
            elif event.type==KEYDOWN:
                if event.unicode.isalpha():
                    if not username_made and not tooLong:
                        username += event.unicode
                elif event.key==K_SPACE:
                    if not username_made and not tooLong:
                        username += " "
                elif event.key==K_0 or event.key==K_KP0:
                    if not username_made and not tooLong:
                        username += "0"
                elif event.key==K_1 or event.key==K_KP1:
                    if not username_made and not tooLong:
                        username += "1"
                elif event.key==K_2 or event.key==K_KP2:
                    if not username_made and not tooLong:
                        username += "2"
                elif event.key==K_3 or event.key==K_KP3:
                    if not username_made and not tooLong:
                        username += "3"
                elif event.key==K_4 or event.key==K_KP4:
                    if not username_made and not tooLong:
                        username += "4"
                elif event.key==K_5 or event.key==K_KP5:
                    if not username_made and not tooLong:
                        username += "5"
                elif event.key==K_6 or event.key==K_KP6:
                    if not username_made and not tooLong:
                        username += "6"
                elif event.key==K_7 or event.key==K_KP7:
                    if not username_made and not tooLong:
                        username += "7"
                elif event.key==K_8 or event.key==K_KP8:
                    if not username_made and not tooLong:
                        username += "8"
                elif event.key==K_9 or event.key==K_KP9:
                    if not username_made and not tooLong:
                        username += "9"
                elif event.key==K_BACKSPACE:
                    if not username_made:
                        username = username[:-1]
                elif event.key==K_RETURN:
                    if not username_made:
                        if not username=="":
                            with open(os.path.join(current_path, 'database_username'), 'r') as f:
                                names = f.read().split(":")
                            with open(os.path.join(current_path, 'database_username'), 'w') as f:
                                f.write("username")
                            with open(os.path.join(current_path, 'database_username'), 'a') as f:
                                for i in range(1, len(names)-1, 1):
                                    f.write(":"+names[i])
                                f.write(":"+username)
                            username_made = True
                    else:
                        Game_State = S_RESTART
                elif event.key==K_F11:
                    if not isFullscreen:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
                        isFullscreen = True
                    else:
                        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
                        isFullscreen = False
        global username_text
        global username_textRect
        username_text = dunggeunmo24.render(username, True, WHITE, BLACK)
        username_textRect = username_text.get_rect()
        username_textRect.right = yourname_textRect.right
        username_textRect.top = yourname_textRect.bottom
        global frame_cursor
        if frame_cursor<59:
            frame_cursor += 1
        else:
            frame_cursor = 0
        global lineNumber
        global lineNumbers
        global scores_made
        global scores
        if not scores_made:
            with open(os.path.join(current_path, 'database'), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.split(":")[0]=="statistics" and line.split(":")[2]=="start":
                        lineNumbers.append(lineNumber+1)
                    lineNumber += 1
                for i in lineNumbers:
                    scores.append(lines[i].split(':')[1]) #점수 배열 scores 완성
            scores_made = True
        global scoreboardRect_made
        global usernames
        global usernames_text
        global usernames_textRect
        global scores_text
        global scores_textRect
        if username_made:
            if not scoreboardRect_made:
                with open(os.path.join(current_path, 'database_username'), 'r') as f:
                    names = f.read().split(":")
                    for name in names:
                        usernames.append(name)
                for username in usernames:
                    member = dunggeunmo24.render(username, True, WHITE, BLACK)
                    usernames_text.append(member)
                    usernames_textRect.append(member.get_rect())
                for score in scores:
                    member = dunggeunmo24.render(score, True, WHITE, BLACK)
                    scores_text.append(member)
                    scores_textRect.append(member.get_rect())
                usernames_textRect[0].left = 350
                usernames_textRect[0].top = 15
                scores_textRect[0].right = 930
                scores_textRect[0].top = 15
                for i in range(len(usernames_textRect)-1): #이 앞에 초항 필요
                    usernames_textRect[i+1].left = 350
                    usernames_textRect[i+1].top = usernames_textRect[i].bottom
                for i in range(len(scores_textRect)-1):
                    scores_textRect[i+1].right = 930
                    scores_textRect[i+1].top = scores_textRect[i].bottom
                scoreboardRect_made = True

    def Update():
        if Game_State==S_LOGO:
            Update_Logo()
        elif Game_State==S_MENU:
            Update_Menu()
        elif Game_State==S_MENU_SCOREBOARD:
            Update_Menu_Scoreboard()
        elif Game_State==S_OPTION:
            Update_Option()
        elif Game_State==S_CONTROLS:
            Update_Controls()
        elif Game_State==S_PROLOGUE:
            Update_Prologue()
        elif Game_State==S_PARROT:
            Update_Parrot()
        elif Game_State==S_GAME:
            Update_Game()
        elif Game_State==S_GAME_OPTION:
            Update_Game_Option()
        elif Game_State==S_GAME_CONTROLS:
            Update_Game_Controls()
        elif Game_State==S_DEATH:
            Update_Death()
        elif Game_State==S_VICTORY:
            Update_Victory()
        elif Game_State==S_DEATH_EPILOGUE:
            Update_Death_Epilogue()
        elif Game_State==S_VICTORY_EPILOGUE:
            Update_Victory_Epilogue()
        elif Game_State==S_CREDIT:
            Update_Credit()
        elif Game_State==S_SCOREBOARD:
            Update_Scoreboard()

    def Render_Logo():
        windowSurface.fill(BLACK)
        #검은 배경
        windowSurface.blit(logoImage, logoRect)
        #로고 이미지
        if frame_logo_top<240:
            windowSurface.blit(logo_text_0, logo_textRect_0)
        #로고 상단 텍스트
        if frame_logo_top==240: #로고 상단 텍스트의 이동이 끝난 후
            if frame_logo_bottom<61:
                windowSurface.blit(logo_text_1, logo_textRect_1)
            else:
                windowSurface.blit(logo_text_2, logo_textRect_2)
        #로고 하단 텍스트
        if frame_logo_top==240:
            if frame_logo<61:
                windowSurface.blit(logo_text48, logo_text48Rect)
            else:
                windowSurface.blit(logo_text46, logo_text46Rect)
        #범용 로고 텍스트 렌더
        renderReticle()

    def Render_Menu():
        windowSurface.fill(BLACK)
        windowSurface.blit(arrow_text, arrow_textRect)
        #화살표
        windowSurface.blit(menu_text_1, menu_textRect_1)
        windowSurface.blit(menu_text_2, menu_textRect_2)
        windowSurface.blit(menu_text_3, menu_textRect_3)
        #메뉴
        global frame_logo
        if frame_logo<61:
            windowSurface.blit(logo_text48, logo_text48Rect)
        else:
            windowSurface.blit(logo_text46, logo_text46Rect)
        #범용 로고 텍스트 렌더
        renderReticle()

    def Render_Menu_Scoreboard():
        windowSurface.fill(BLACK)
        for i in range(len(menu_usernames_text)):
            windowSurface.blit(menu_usernames_text[i], menu_usernames_textRect[i])
        for i in range(len(menu_scores_text)):
            windowSurface.blit(menu_scores_text[i], menu_scores_textRect[i])
        windowSurface.blit(scoreboardImage, scoreboardRect)
        windowSurface.blit(backtothemenu_text, backtothemenu_textRect)
        renderReticle()

    def Render_Option():
        windowSurface.fill(BLACK)
        windowSurface.blit(arrow_text, arrow_textRect)
        #화살표
        windowSurface.blit(option_text_1, option_textRect_1)
        windowSurface.blit(option_text_2, option_textRect_2)
        windowSurface.blit(option_text_3, option_textRect_3)
        #옵션
        global frame_logo
        if frame_logo<61:
            windowSurface.blit(logo_text48, logo_text48Rect)
        else:
            windowSurface.blit(logo_text46, logo_text46Rect)
        #범용 로고 텍스트 렌더
        renderReticle()

    def Render_Controls():
        windowSurface.fill(BLACK)
        windowSurface.blit(controlsImage, controlsRect)
        windowSurface.blit(controls_text, controls_textRect)
        #컨트롤 안내문
        global frame_logo
        if frame_logo<61:
            windowSurface.blit(logo_text48, logo_text48Rect)
        else:
            windowSurface.blit(logo_text46, logo_text46Rect)
        #범용 로고 텍스트 렌더
        renderReticle()

    def Render_Prologue():
        windowSurface.fill(BLACK)
        if frame_prologue==0:
            windowSurface.blit(prologueImage_1_0, prologueRect_1_0)
        windowSurface.blit(prologueImage[frame_prologue], prologueRect[frame_prologue])
        for i in prologue_text[frame_prologue]:
            windowSurface.blit(i, prologueDict[i])
        #프롤로그
        renderReticle()

    def Render_Parrot():
        windowSurface.fill(BLACK)
        global frame_parrot
        if frame_parrot<120:
            windowSurface.blit(ParrotImage, parrotRect)
            windowSurface.blit(parrot_text, parrot_textRect)
        elif frame_parrot<240:
            frame_parrot_sized = (frame_parrot-120)%18
            frame_parrot_sized_twicce = frame_parrot_sized//2
            windowSurface.blit(parrotSpriteImage, parrotSpriteRect, (frame_parrot_sized_twicce%3*parrotSpriteRect.width, frame_parrot_sized_twicce//3*parrotSpriteRect.height, parrotSpriteRect.width, parrotSpriteRect.height))
        #앵무새
        renderReticle()

    def Render_Game():
        windowSurface.fill(BLACK)
        windowSurface.blit(bgImage, bgRect)
        windowSurface.blit(game_optionImage, game_optionRect)
        windowSurface.blit(score_text, score_textRect)
        #옵션 버튼
        for i in range(5):
            windowSurface.blit(cloudsImage[i], cloudsRect[i])
        #구름
        for tower in towersRect:
            tower.render()
        #타워
        for humanfacedbird in humanfacedbirdsRect:
            humanfacedbird.render()
        #인면조
        for medivh in medivhsRect:
            medivh.render()
        #메디브
        if player_headingRight:
            windowSurface.blit(playerImage, playerRect)
        else:
            windowSurface.blit(pygame.transform.flip(playerImage, True, False), playerRect)
        #플레이어
        for food in foodsRect:
            food.render()
        #음식
        for stone in stonesRect:
            stone.render()
        #돌
        wheatField.render()
        #밀
        global frame_click
        if frame_click<4:
            windowSurface.blit(guagesImage[0], guageRect)
        elif frame_click<8:
            windowSurface.blit(guagesImage[1], guageRect)
        elif frame_click<12:
            windowSurface.blit(guagesImage[2], guageRect)
        elif frame_click<16:
            windowSurface.blit(guagesImage[3], guageRect)
        elif frame_click<20:
            windowSurface.blit(guagesImage[4], guageRect)
        elif frame_click<24:
            windowSurface.blit(guagesImage[5], guageRect)
        elif frame_click<28:
            windowSurface.blit(guagesImage[6], guageRect)
        elif frame_click<32:
            windowSurface.blit(guagesImage[7], guageRect)
        elif frame_click<36:
            windowSurface.blit(guagesImage[8], guageRect)
        elif frame_click<=40:
            windowSurface.blit(guagesImage[9], guageRect)
        #게이지
        for projectile in projectilesRect:
            projectile.render()
        #직사투사체
        for bonusbird in bonusbirdsRect:
            bonusbird.render()
        #보너스 해로운 새
        for enemy in enemiesRect:
            enemy.render()
        #해로운 새
        for eliteenemy in eliteenemiesRect:
            eliteenemy.render()
        #정예 해로운 새
        if ((shotgun==False and len(stonesRect)<6) or (shotgun==True and len(stonesRect)<4)):
            windowSurface.blit(shoot_text, shoot_textRect)
        else: 
            windowSurface.blit(wait_text, wait_textRect) #돌이 6개이면 WAIT! 표시
        #발사 대기 텍스트
        windowSurface.blit(score_text, score_textRect)
        #점수
        for i in range(5):
            windowSurface.blit(makeHearts(remainheart)[0][i], makeHearts(remainheart)[1][i])
        #생명력
        if penetrable:
            windowSurface.blit(penetrableImage, poweritemRect_0)
        windowSurface.blit(slotImage, poweritemRect_0)
        if shotgun:
            windowSurface.blit(shotgunImage, poweritemRect_1)
        windowSurface.blit(slotImage, poweritemRect_1)
        if quickcharge==2:
            windowSurface.blit(quickchargeImage, poweritemRect_2)
        windowSurface.blit(slotImage, poweritemRect_2)
        #파워아이템
        if whishingDove:
            windowSurface.blit(doveImage, bonusbirdRect_0)
        windowSurface.blit(slotImage, bonusbirdRect_0)
        if whishingRaven:
            windowSurface.blit(ravenImage, bonusbirdRect_1)
        windowSurface.blit(slotImage, bonusbirdRect_1)
        if whishingCrane:
            windowSurface.blit(craneImage, bonusbirdRect_2)
        windowSurface.blit(slotImage, bonusbirdRect_2)
        if whishingPelican:
            windowSurface.blit(pelicanImage, bonusbirdRect_3)
        windowSurface.blit(slotImage, bonusbirdRect_3)
        if whishingParrot:
            windowSurface.blit(parrotImage, bonusbirdRect_4)
        windowSurface.blit(slotImage, bonusbirdRect_4)
        #보너스 해로운 새
        if frame_object<160:
            windowSurface.blit(object_text, object_textRect)
        #목표 텍스트
        wave.render()
        #웨이브
        renderReticle()

    def Render_Game_Option():
        windowSurface.fill(BLACK)
        windowSurface.blit(arrow_text, arrow_textRect)
        #화살표
        windowSurface.blit(game_option_text_1, game_option_textRect_1)
        windowSurface.blit(game_option_text_2, game_option_textRect_2)
        windowSurface.blit(game_option_text_3, game_option_textRect_3)
        #게임 옵션 텍스트
        global frame_logo
        if frame_logo<61:
            windowSurface.blit(logo_text48, logo_text48Rect)
        else:
            windowSurface.blit(logo_text46, logo_text46Rect)
        #범용 로고 텍스트 렌더
        renderReticle()

    def Render_Game_Controls():
        windowSurface.fill(BLACK)
        windowSurface.blit(game_controlsImage, game_controlsRect)
        windowSurface.blit(game_controls_text, game_controls_textRect)
        #컨트롤 안내문
        global frame_logo
        if frame_logo<61:
            windowSurface.blit(logo_text48, logo_text48Rect)
        else:
            windowSurface.blit(logo_text46, logo_text46Rect)
        #범용 로고 텍스트 렌더
        renderReticle()

    def Render_Death():
        windowSurface.fill(BLACK)
        windowSurface.blit(brokenheartImage, brokenheartRect)
        renderReticle()

    def Render_Death_Epilogue():
        windowSurface.fill(BLACK)
        windowSurface.blit(death_epilogue_text_1, death_epilogue_textRect_1)
        windowSurface.blit(death_epilogue_text_2, death_epilogue_textRect_2)
        windowSurface.blit(death_epilogue_text_3, death_epilogue_textRect_3)
        windowSurface.blit(death_epilogueImage, death_epilogueRect)
        renderReticle()

    def Render_Victory():
        windowSurface.fill(BLACK)
        windowSurface.blit(victory_text, victory_textRect)
        renderReticle()

    def Render_Victory_Epilogue():
        windowSurface.fill(BLACK)
        if frame_victory_epilogue==0:
            windowSurface.blit(victory_epilogueImage_1, victory_epilogueRect_1)
            windowSurface.blit(victory_epilogue_text_1_1, victory_epilogue_textRect_1_1)
            windowSurface.blit(victory_epilogue_text_1_2, victory_epilogue_textRect_1_2)
            windowSurface.blit(victory_epilogue_text_1_3, victory_epilogue_textRect_1_3)
        if frame_victory_epilogue==1:
            windowSurface.blit(victory_epilogueImage_2, victory_epilogueRect_2)
            windowSurface.blit(victory_epilogue_text_2_1, victory_epilogue_textRect_2_1)
            windowSurface.blit(victory_epilogue_text_2_2, victory_epilogue_textRect_2_2)
        renderReticle()

    def Render_Credit():
        windowSurface.fill(BLACK)
        for i in range(len(statistics_texts_left)):
            windowSurface.blit(statistics_texts_left[i], statistics_textsRect_left[i])
        for i in range(len(statistics_texts_right)):
            windowSurface.blit(statistics_texts_right[i], statistics_textsRect_right[i])
        windowSurface.blit(creditImage, creditRect)
        renderReticle()

    def Render_Scoreboard():
        windowSurface.fill(BLACK)
        if username_made:
            for i in range(len(usernames_text)):
                windowSurface.blit(usernames_text[i], usernames_textRect[i])
            for i in range(len(scores_text)):
                windowSurface.blit(scores_text[i], scores_textRect[i])
        windowSurface.blit(scoreboardImage, scoreboardRect)
        windowSurface.blit(yourname_text, yourname_textRect)
        windowSurface.blit(username_text, username_textRect)
        if not username_made:
            if frame_cursor<30:
                windowSurface.blit(cursorImage, cursorRect)
        if not username_made:
            windowSurface.blit(whenyoutype_text, whenyoutype_textRect)
            windowSurface.blit(allyourname_text, allyourname_textRect)
            windowSurface.blit(pressenter_text, pressenter_textRect)
        if username_made:
            windowSurface.blit(ifyouwantto_text, ifyouwantto_textRect)
            windowSurface.blit(restartthegame_text, restartthegame_textRect)
            windowSurface.blit(pressenter_text_0, pressenter_textRect_0)
        windowSurface.blit(quit_text, quit_textRect)
        renderReticle()

    def Render():
        if Game_State==S_LOGO:
            Render_Logo()
        elif Game_State==S_MENU:
            Render_Menu()
        elif Game_State==S_MENU_SCOREBOARD:
            Render_Menu_Scoreboard()
        elif Game_State==S_OPTION:
            Render_Option()
        elif Game_State==S_CONTROLS:
            Render_Controls()
        elif Game_State==S_PROLOGUE:
            Render_Prologue()
        elif Game_State==S_PARROT:
            Render_Parrot()
        elif Game_State==S_GAME:
            Render_Game()
        elif Game_State==S_GAME_OPTION:
            Render_Game_Option()
        elif Game_State==S_GAME_CONTROLS:
            Render_Game_Controls()
        elif Game_State==S_DEATH:
            Render_Death()
        elif Game_State==S_VICTORY:
            Render_Victory()
        elif Game_State==S_DEATH_EPILOGUE:
            Render_Death_Epilogue()
        elif Game_State==S_VICTORY_EPILOGUE:
            Render_Victory_Epilogue()
        elif Game_State==S_CREDIT:
            Render_Credit()
        elif Game_State==S_SCOREBOARD:
            Render_Scoreboard()

    Init()
    while True:
        Update()
        Render()
        pygame.display.update()
        if Game_State==S_RESTART:
            break
        if Game_State==S_GAME:
            mainClock.tick(24) #미숙한 실력으로 잘못 제작하여 이미지가 많은 게임 씬에서만 24프레임 기준으로 제작됨
        else:
            mainClock.tick(60)
