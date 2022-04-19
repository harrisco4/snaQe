#Jack Valladares, Harris Collier

from pygame.locals import *
from random import randint
from QLearning import *
import pygame
import multiprocessing as mp
import time
import math
import sys
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)

flow = False
font = pygame.font.SysFont("Verdana", 12)
screen = pygame.display.set_mode((620, 320))





class Gradient():
    def __init__(self, palette, maximum):
        self.COLORS = palette
        self.N = len(self.COLORS)
        self.SECTION = maximum // (self.N - 1)
        
    def gradient(self, x):
        i = x // self.SECTION
        fraction = (x % self.SECTION) / self.SECTION
        c1 = self.COLORS[i % self.N]
        c2 = self.COLORS[(i+1) % self.N]
        col = [0, 0, 0]
        for k in range(3):
            col[k] = (c2[k] - c1[k]) * fraction + c1[k]
        return col

def wave(num):
    for x in range(0, 620+10, int(jmp.val)):
        ang_1 = (x + num) * math.pi * freq.val / 180
        ang_2 = ang_1 - phase.val
        cos_1 = math.cos(ang_1)
        cos_2 = math.cos(ang_2)
        y_1 = int(cos_1 * size.val) + 250
        y_2 = int(cos_2 * size.val) + 250

        radius_1 = int(pen.val + math.sin(ang_1 + focus.val) * pen.val / 2)
        radius_2 = int(pen.val + math.sin(ang_2 + focus.val) * pen.val / 2)

        if radius_1 > radius_2:  # draw the smaller circle before the larger one
            pygame.draw.circle(screen, xcolor(int(x + 620//2) + num * flow), (x, y_2), radius_2, 0)
            pygame.draw.circle(screen, xcolor(x + num * flow), (x, y_1), radius_1, 0)
        else:
            pygame.draw.circle(screen, xcolor(x + num * flow), (x, y_1), radius_1, 0)
            pygame.draw.circle(screen, xcolor(int(x + 620//2) + num * flow), (x, y_2), radius_2, 0)


 
class Apple:
    x = 0
    y = 0
    step = 64
    
 
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y))
        


class UI:
    x = 320
    y = 0
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 32)
    white = (255, 255, 255) 
    green = (0, 255, 0) 
    blue = (0, 0, 128)
        
    score = font.render('Score: ', True, green, blue) 




    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))
        #surface.blit(score, (1024, 200))



class Slider():
    
    def __init__(self, name, val, maxi, mini, pos):
        pygame.init()
        
        self.val = val
        self.maxi = maxi
        self.mini = mini
        self.xpos = pos
        self.ypos = 100
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False
        self.txt_surf = font.render(name, 1, BLACK)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))
        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, GREY, [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, ORANGE, [10, 10, 80, 10], 0)
        pygame.draw.rect(self.surf, WHITE, [10, 30, 80, 5], 0)
        self.surf.blit(self.txt_surf, self.txt_rect)
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, BLACK, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, ORANGE, (10, 10), 4, 0)
    def draw(self):
        surf = self.surf.copy()
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)
        screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi



 
class Player:
    x = [64]
    y = [128]
    step = 64
    direction = 0
    length = 3
    lastAction = "None"
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
       self.x = [64]	
       self.y = [64]
       for i in range(0,2000):
          self.x.append(-100)
          self.y.append(-100)
       self.lastAction = "None"
 
       # initial positions, no collision.
       self.x[1] = 1*64
       self.x[2] = 2*64
 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0




 
 
    def moveRight(self):
        if(self.lastAction != "Left"):
            self.direction = 0
            self.lastAction = "Right"
 
    def moveLeft(self):
        if(self.lastAction != "Right"):
            self.direction = 1
            self.lastAction = "Left"
 
    def moveUp(self):
        if(self.lastAction != "Down"):
            self.direction = 2
            self.lastAction = "Up"
 
    def moveDown(self):
        if(self.lastAction != "Up"):
            self.direction = 3
            self.lastAction = "Down" 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False



font = pygame.font.SysFont("Verdana", 12)
font2 = pygame.font.SysFont("Verdana", 18)
clock = pygame.time.Clock()
COLORS = [MAGENTA, RED, YELLOW, GREEN, CYAN, BLUE]
xcolor = Gradient(COLORS, 620).gradient

pen = Slider("Pen", 10, 15, 1, 25)
freq = Slider("Freq", 1, 3, 0.2, 150)
jmp = Slider("Jump", 10, 20, 1, 275)
size = Slider("Size", 200, 200, 20, 400)
focus = Slider("Focus", 0, 6, 0, 525)
phase = Slider("Phase", 3.14, 6, 0.3, 650)
slides = [pen, freq, jmp, size, focus, phase]

 
class App:

    
    windowWidth = 620
    #UI starts at 1024
    windowHeight = 320
    
    font = pygame.font.SysFont("Verdana", 12)
    font2 = pygame.font.SysFont("Verdana", 24)
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    clock = pygame.time.Clock()
    COLORS = [MAGENTA, RED, YELLOW, GREEN, CYAN, BLUE]
    xcolor = Gradient(COLORS, windowWidth).gradient

    player = 0
    apple = 0
    score = 0
    highScore = 0
    totalScore = 0
    reward = 0.0
    episode = 0
    lastAction = 5



    

 
    def __init__(self):
        self.speed = Slider("Speed", 2.5, 10, 1, 411)
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self._UI_surf = None
        self.game = Game()
        self.player = Player(3) 
        self.apple = Apple(5,5)
        self.UI = UI()
        self.score = 0
        self.reward = -.1
        self.num = 0

        self.title_surf = font2.render("Deep Learning SnaQe v1.0", 120, BLACK)
        self.title_surfRect = self.title_surf.get_rect()
        self.title_surfRect.center = (466, 170-90)

        self.txt_surf = font2.render("Speed: "+str(self.score), 120, BLACK)
        self.textRect = self.txt_surf.get_rect()
        self.textRect.center = (458, 170)

        self.txt2_surf = font2.render("Score: "+str(self.score), 120, BLACK)
        self.text2Rect = self.txt2_surf.get_rect()
        self.text2Rect.center = (458, 170+30)

        self.txt3_surf = font2.render("Total Score: "+str(self.totalScore), 120, BLACK)
        self.text3Rect = self.txt3_surf.get_rect()
        self.text3Rect.center = (458, 170+60) 
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Score: ' + str(self.score) + ' Episode: ' + str(self.episode) + ' High Score: ' + str(self.highScore) + ' Total Score: ' + str(self.totalScore))
        self._running = True
        self._image_surf = pygame.image.load("block.jpg").convert()
        self._apple_surf = pygame.image.load("apple.jpg").convert()
        self._UI_surf = pygame.image.load("UI.jpg").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def reset(self):
        self.player = Player(3)
        self.apple = Apple(3,3)
        self.score = 0
        self.reward = -1
        self.episode += 1
        self.lastAction = 5
        pygame.display.set_caption('Score: ' + str(self.score) + ' Episode: ' + str(self.episode) + ' High Score: ' + str(self.highScore) + ' Total Score: ' + str(self.totalScore))
 
    def on_loop(self):


        self.txt_surf = font2.render("Score: "+str(self.score), 120, BLACK)
        self.textRect = self.txt_surf.get_rect()
        self.textRect.center = (458, 170)

        self.txt2_surf = font2.render("High Score: "+str(self.highScore), 120, BLACK)
        self.text2Rect = self.txt2_surf.get_rect()
        self.text2Rect.center = (458, 170+30)

        self.txt3_surf = font2.render("Total Score: "+str(self.totalScore), 120, BLACK)
        self.text3Rect = self.txt3_surf.get_rect()
        self.text3Rect.center = (458, 170+60) 
        
        self.player.update()
        self.reward = -0.1

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.speed.button_rect.collidepoint(pos):
                    self.speed.hit = True
            elif event.type == pygame.MOUSEBUTTONUP:
                    self.speed.hit = False


        if self.speed.hit:
            self.speed.move()
            print("Touching speed slider... value: "+str(self.speed.val))


        self.speed.draw()
        self.num += 2
        wave(self.num)
        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i],44):

                self.player.length += 1
                self.score += 1
                self.totalScore += 1
                if(self.score > self.highScore):
                    self.highScore = self.score
                self.reward = 1
                pygame.display.set_caption('Score: ' + str(self.score) + ' Episode: ' + str(self.episode) + ' High Score: ' + str(self.highScore) + ' Total Score: ' + str(self.totalScore))
                # check if the apple respawned into the snake
                while True:
                    self.apple.x = randint(1,4) * 64
                    self.apple.y = randint(1,4) * 64
                    if not self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i],44):
                        break


 
 
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                self.reset()

        # does snake leave the room?
        if self.player.x[0] < 0 or self.player.x[0] > 320:
            self.reset()
        if self.player.y[0] < 0 or self.player.y[0] > 320:
            self.reset()
 
        pass
        return self.reward
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.UI.draw(self._display_surf, self._UI_surf)
        self.speed.draw()


        
        self._display_surf.blit(self.title_surf, self.title_surfRect)
        self._display_surf.blit(self.txt_surf, self.textRect)
        self._display_surf.blit(self.txt2_surf, self.text2Rect)
        self._display_surf.blit(self.txt3_surf, self.text3Rect) 
        
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 

            currentState = newState(self.player, self.apple)
            action = bestAction(currentState)
            
            # Move snake based on action just gathered
            if(action == 0 and self.lastAction != 1):
                self.player.moveUp()
                self.lastAction = 0

            if(action == 1 and self.lastAction != 0):
                self.player.moveDown()
                self.lastAction = 1
            
            if(action == 2 and self.lastAction != 3):
                self.player.moveLeft()
                self.lastAction = 2

            if(action == 3 and self.lastAction != 2):
                self.player.moveRight()
                self.lastAction = 3
    
            # Quit out with escape
            if (keys[K_ESCAPE]):
                self._running = False
 
            reward = self.on_loop()
            self.on_render()

            nextState = newState(self.player, self.apple)
            updateQTable(currentState, nextState, reward, action)
 
 
            time.sleep ((.1/self.speed.val)-.0099); #lower = faster
        self.on_cleanup()
 
if __name__ == "__main__" :
    
    theApp = App()
    theApp.on_execute()
