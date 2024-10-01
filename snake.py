#nessasary imports
import pygame
import random as r
#initialize pygame
pygame.init()
#for the score
font = pygame.font.SysFont(None, 24)
#width of each square
square_size = 20
#amout of squares for the baord
squares_per_side = 30
final_score = high_score = 0
clock = pygame.time.Clock()
keep_going = True
screen_width = square_size * squares_per_side
wd = pygame.display.set_mode((screen_width,screen_width))
blur_screen = pygame.Surface((screen_width,screen_width),pygame.SRCALPHA)
def build_board():
    pygame.draw.rect(wd,"#004902",pygame.Rect(0,0,screen_width,square_size))
    pygame.draw.rect(wd,"#004902",pygame.Rect(0,0,square_size,screen_width))
    pygame.draw.rect(wd,"#004902",pygame.Rect(screen_width-square_size,0,square_size,screen_width))
    pygame.draw.rect(wd,"#004902",pygame.Rect(0,screen_width-square_size,screen_width,square_size))
    for x in range(1, squares_per_side - 1):
        for y in range(1, squares_per_side - 1):
            squares_alternating_colours(x, y)
def squares_alternating_colours(x,y):
    if x % 2 == y % 2:
        pygame.draw.rect(wd,"#00a506" ,pygame.Rect(x * square_size, y * square_size, square_size, square_size))
    else:
        pygame.draw.rect(wd, "#6cff71", pygame.Rect(x * square_size, y * square_size, square_size, square_size))
def place_apple(x,y):
    pygame.draw.rect(wd, "red",pygame.Rect(x * square_size, y * square_size, square_size, square_size))
def updatescore(score):
    score = str(score)
    img = font.render(score, True, "white")


    pygame.draw.rect(wd, "#004902", pygame.Rect(0, 0, square_size * len(score), square_size))
    wd.blit(img, (0, 0))
def main_game_loop():
    build_board()
    quit_game = False
    start = False
    class snake_body():
        def __init__(self):
            self.started = False
            self.lenght = 3
            self.x = round(square_size/4)
            self.y = round(squares_per_side/2)
            self.direction  = "d"
            self.body = [[self.x,int(self.y)],[self.x - 1,int(self.y)],[self.x - 2,int(self.y)]]
            self.lost = False
            self.apple = (round(squares_per_side * 3/4),round(squares_per_side/2))
            place_apple(self.apple[0],self.apple[1])
            updatescore(self.lenght - 3)
            for i,j in self.body:
                pygame.draw.rect(wd,"#002aff",pygame.Rect(i * square_size,j * square_size,square_size,square_size))
        def move(self,direction = None):
            moving_into_itself = {"a":"d","d":"a","w": "s","s":"w",None:None}
            if self.started == False and (direction == None or moving_into_itself[direction] == self.direction):
                return None
            if direction and moving_into_itself[direction] != self.direction:
                self.started = True
                self.direction = direction
            if self.direction == "d":
                self.x += 1
            elif self.direction == "a":
                self.x -= 1
            elif self.direction == "w":
                self.y -= 1
            else:
                self.y += 1
            if self.y in [0,squares_per_side - 1]  or self.x in [0,squares_per_side - 1] or ((self.x,self.y) in self.body):
                self.lost = True
                return None
            self.body.insert(0, (self.x, self.y))
            pygame.draw.rect(wd, "#002aff",pygame.Rect(self.x * square_size, self.y * square_size, square_size, square_size))
            if (self.x,self.y) != self.apple:
                squares_alternating_colours(self.body[-1][0],self.body[-1][1])
                del self.body[-1]
                return None
            while True:
                self.lenght +=1
                updatescore(self.lenght - 3)
                self.apple = (r.randint(1,squares_per_side - 2),r.randint(1,squares_per_side - 2))
                if self.apple not in self.body:
                    place_apple(self.apple[0], self.apple[1])
                    break



    main_snake = snake_body()
    while True:
        if main_snake.lost == True:
            return True,main_snake.lenght-3

        key_down = False
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN:
                key_down = True
                if events.key in [pygame.K_d,pygame.K_RIGHT]:
                    main_snake.move("d")
                if events.key in [pygame.K_a,pygame.K_LEFT]:
                    main_snake.move("a")
                if events.key in [pygame.K_s,pygame.K_DOWN]:
                    main_snake.move("s")
                if events.key in [pygame.K_w,pygame.K_UP]:
                    main_snake.move("w")
            if events.type == pygame.QUIT:
                quit_game = True
        pygame.display.update()
        if quit_game == True:
            return False,0
        if key_down == False:
            main_snake.move()
        clock.tick(15)

while keep_going:
    pre_game = True
    close = False
    while pre_game:
        build_board()
        wd.blit(blur_screen,(0,0))
        pygame.draw.rect(blur_screen,(132,132,132,150),pygame.Rect(0,0,screen_width,screen_width))
        pygame.draw.rect(wd,"#0000ff",pygame.Rect(square_size * 7,square_size * 6,(square_size * squares_per_side/2)+square_size,square_size * 14))
        pygame.draw.rect(wd,"#ffffff",pygame.Rect( square_size * 15,square_size * 8,5,square_size * 10))
        pregame_font = pygame.font.SysFont(None, 60)
        pregame_font_word = pygame.font.SysFont(None, 30)
        high_score_img = pregame_font.render(str(high_score), True, "white")
        new_score_img = pregame_font.render(str(final_score), True, "white")
        high_score_img_words = pregame_font_word.render("High score", True, "white")
        new_score_img_word = pregame_font_word.render("Current score", True, "white")
        wd.blit(high_score_img,(square_size * 9,square_size * 13))
        wd.blit(new_score_img, (square_size * 20, square_size * 13))
        wd.blit(new_score_img_word, (square_size * 16, square_size * 9))
        wd.blit(high_score_img_words, (square_size * 8, square_size * 9))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                pre_game = False
                close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (square_size * 7 <= mouse_x <= square_size * (8 + squares_per_side/2)) and (square_size * 6 <= mouse_y <= square_size * (6 + 14)):
                    pass
                else:
                    pre_game = False
    if close == False:
        keep_going,final_score = main_game_loop()
        if high_score < final_score:
            high_score = final_score