import pygame
import sys
import random 
import time

GAME_WIDTH = 600
GAME_HEIGHT = 600


def draw():
    if not game_started:
        window.fill("black")
        title_font = pygame.font.SysFont("Comic Sans MS" , 45)
        button_font = pygame.font.SysFont("Comic Sans MS" , 30)
        title  = title_font.render("Thief runner", True,"white")
        button_text = button_font.render("START", True,"white")

        window.blit(title,(170,170))
        pygame.draw.rect(window, "green", start_button)
        window.blit(button_text, (245, 295))
        return 

    window.blit(background_image, (0,0))
    window.blit(thief.img, thief.rect)
    window.blit(police_image, police_rect)


    for brick in bricks:
        window.blit(brick.img, brick.rect)
        text_str = str(int(score))
        if game_over:
            text_str = "Game Over: " + text_str
        

        text_font = pygame.font.SysFont("Comic Sans MS", 45)
        text_render = text_font.render(text_str, True, "white")
        window.blit(text_render, (5,0))


pygame.init()
window = pygame.display.set_mode((GAME_WIDTH , GAME_HEIGHT))
pygame.display.set_caption(("thief runner"))
Clock = pygame.time.Clock()

create_bricks_timer = pygame.USEREVENT + 0 
pygame.time.set_timer(create_bricks_timer, 1500)
# THEIF
thief_x = GAME_WIDTH/60
thief_y = GAME_HEIGHT/60
thief_width = 60 
theif_height = 60
# theif class
class Thief:
    def __init__(self, img):
        self.img = img
        self.rect = img.get_rect()
        self.rect.x = 100
        self.rect.y = 270

#  BRICK
brick_x = 400
brick_y = 0
brick_width = 80
brick_height = 400
# brick class
class Brick:
    def __init__(self, img, x, y):
        self.img = img
        self.rect = img.get_rect(topleft=(x,y))
        self.passed = False


background_image = pygame.image.load("assets/night_city_background.png").convert()
thief_image = pygame.image.load("assets/thief.png").convert_alpha()
thief_image = pygame.transform.scale(thief_image , (60,60))
police_image = pygame.image.load("assets/police.png").convert_alpha()
police_image = pygame.transform.scale(police_image , (70,70))
upper_brick_wall_image = pygame.image.load("assets/upper_brick_wall_1.png").convert_alpha()
upper_brick_wall_image = pygame.transform.scale(upper_brick_wall_image,(80, 400))
lower_brick_wall_image = pygame.image.load("assets/lower_brick_wall_2.png").convert_alpha()
lower_brick_wall_image = pygame.transform.scale(lower_brick_wall_image,(80, 400))
Clock = pygame.time.Clock()

# logic
thief = Thief(thief_image)
police_rect = police_image.get_rect(topleft=(10,270))
bricks = []
velocity_x = -2
velocity_y = 0 
gravity = 0.4
score = 0
game_over = False
game_started = False
start_button = pygame.Rect(200, 280, 200, 70)

def move():
  global velocity_y, score, game_over
  velocity_y += gravity
  thief.rect.y  += velocity_y
  thief.rect.y = max(thief.rect.y, 0)
  if thief.rect.y > GAME_HEIGHT:
      game_over = True
      return
  
  police_rect.x += 0.7

  
  for brick in bricks:
    brick.rect.x += velocity_x
    if not brick.passed and thief.rect.left > brick.rect.right:
        score += 0.5
        brick.passed = True

    if thief.rect.colliderect(brick.rect):
        game_over = True
        return
    if police_rect.colliderect(thief.rect):
        game_over = True
        return
    
while len(bricks) > 0 and bricks[0].rect.right < 0:
    bricks.pop(0)



def create_bricks():
    random_brick_y = brick_y - brick_height/4 - random.random()*(brick_height/2)
    opening_space = 200
    upper_brick_wall = Brick(upper_brick_wall_image, 400,0)
    upper_brick_wall.rect.y = random_brick_y
    lower_brick_wall = Brick(lower_brick_wall_image,400,0)
    lower_brick_wall.rect.y = upper_brick_wall.rect.bottom + opening_space
    bricks.append(upper_brick_wall)
    bricks.append(lower_brick_wall)

    print(len(bricks))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_bricks_timer and game_started and not game_over:
            create_bricks()

        if event.type == pygame.KEYDOWN:
         if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
            velocity_y = -6

            if game_over:
                thief.rect.y = thief_y
                bricks.clear()
                score = 0 
                game_over = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                game_started = True

    if game_started and not game_over:
            move()
           
    draw()
    pygame.display.update()
    Clock.tick(60)

