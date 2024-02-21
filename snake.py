import pygame
import random as r
pygame.init()
font = pygame.font.SysFont(None, 24)
square_size = 20
squares_per_side = 30
quit_game =  False
clock = pygame.time.Clock()
screen_width = square_size * squares_per_side
wd = pygame.display.set_mode((screen_width,screen_width))
pygame.draw.rect(wd,"#004902",pygame.Rect(0,0,screen_width,square_size))
pygame.draw.rect(wd,"#004902",pygame.Rect(0,0,square_size,screen_width))
pygame.draw.rect(wd,"#004902",pygame.Rect(screen_width-square_size,0,square_size,screen_width))
pygame.draw.rect(wd,"#004902",pygame.Rect(0,screen_width-square_size,screen_width,square_size))
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
    
class snake_body():
    def __init__(self):
        self.lenght = 3
        self.x = round(square_size/4)
        self.y = round(squares_per_side/2)
        self.direction  = "d"
        self.body = [[self.x,int(self.y)],[self.x - 1,int(self.y)],[self.x - 2,int(self.y)]]
        self.lost = False
        self.apple = (round(squares_per_side * 3/4),round(squares_per_side/2))
        place_apple(self.apple[0],self.apple[1])
        for i,j in self.body:
            pygame.draw.rect(wd,"#002aff",pygame.Rect(i * square_size,j * square_size,square_size,square_size))
    def move(self,direction = None):
        moving_into_itself = {"a":"d","d":"a","w": "s","s":"w"}
        if self.lost:
            return None
        if direction and moving_into_itself[direction] != self.direction:
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
            self.apple = (r.randint(1,squares_per_side - 2),r.randint(1,squares_per_side - 2))
            if self.apple not in self.body:
                place_apple(self.apple[0], self.apple[1])
                break



for x in range(1,squares_per_side-1):
    for y in range(1,squares_per_side-1):
        squares_alternating_colours(x,y)
main_snake = snake_body()
while True:
    key_down = False
    updatescore(main_snake.lenght-3)
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
        break
    if key_down == False:
        main_snake.move()
    clock.tick(14)