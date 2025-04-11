import pygame
from pygame.locals import *
import time
import random


SIZE=40
SCREEN_WIDTH = 1000    
SCREEN_HEIGHT = 800  

#BACKGROUND_COLOR=(188,245,46)
BACKGROUND_COLOR=(155,52,235)

class Burger:
    def __init__(self,parent_screen):
        self.image=pygame.image.load("Resources/burger.jpg").convert()
        self.parent_screen=parent_screen
        self.x=SIZE*3
        self.y=SIZE*3
    
    def draw(self):
        
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()
    
    def movement(self):
        self.x=random.randint(0,24)*SIZE
        self.y=random.randint(0,19)*SIZE


class Snake:
    def __init__(self,parent_screen,length):
         self.length=length
         self.parent_screen=parent_screen
         self.block=pygame.image.load("Resources/block.jpg").convert()
         self.length=length
         self.x=[40]*length
         self.y=[40]*length
         self.direction='down'
         self.x = [SIZE * i for i in range(length)][::-1]  # ✅ Each segment is spaced apart
         self.y = [SIZE] * length


    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
    
   
    def move_left(self):
        self.direction='left'
    
    def move_right(self):
        self.direction='right'
    
    def move_up(self):
        self.direction='up'

    def move_down(self):
        self.direction='down' 
        

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
          self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction=='up':
            self.y[0]-=SIZE
        if self.direction=='down':
            self.y[0]+=SIZE
        
        
        if self.direction=='left':
            self.x[0]-=SIZE
        if self.direction=='right':
            self.x[0]+=SIZE

        self.x[0] %= 1000  # Width of screen
        self.y[0] %= 800   # Height of screen

        self.draw()

    
    

class Game:
   

    def __init__(self):
      
         pygame.init()
        #  pygame.display.set.caption("Snake eating burger game")
         pygame.mixer.init()
         self.play_background_music()
         self.surface=pygame.display.set_mode((1000,800))
        #  self.surface.fill((188,245,66))
         self.snake=Snake(self.surface,1)
         self.snake.draw()
         self.burger=Burger(self.surface)
         self.burger.draw()
         self.burger_eaten = 0  # Tracks how many burgers the snake has eaten
    
    def display_message(self, message):
       font = pygame.font.SysFont('Arial', 40)
       text = font.render(message, True, (255, 0, 0))  # Red 
       text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  
       self.surface.blit(text, text_rect)
       pygame.display.flip()

       # Pause the game for a moment
       time.sleep(2)  # Adjusting  the time according to my necessity

    

    def is_there_any_collision(self,x11,y11,x22,y22):
        if x11>=x22 and x11<x22+SIZE:
           if y11>=y22 and y11<y22+SIZE:
               
              return True
        
        return False
    
    def play_background_music(self):
        pygame.mixer.music.load("Resources/background_music.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        bgimg=pygame.image.load("Resources/background.jpg")
        self.surface.blit(bgimg,(0,0))
    
    

               

    

    def play(self):
         self.render_background()
         self.snake.walk()
         self.burger.draw()
         self.display_score()
         pygame.display.flip()
         if self.is_there_any_collision(self.snake.x[0],self.snake.y[0],self.burger.x,self.burger.y):
             
             sound=pygame.mixer.Sound("Resources/ding.mp3")
             pygame.mixer.Sound.play(sound)
             self.snake.increase_length()
             self.burger.movement()

             self.burger_eaten += 1

            # Check if the snake has eaten a multiple of 10 burgers
             if self.burger_eaten % 10 == 0:
               self.display_message("You've eaten too many burgers! Please stop.")

        #Snake colliding with itself!
         for i in range(1,self.snake.length):
           if self.is_there_any_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
               sound=pygame.mixer.Sound("Resources/crash.mp3")
               pygame.mixer.Sound.play(sound)
               raise "Game Over!"

    

    def display_score(self):
        font=pygame.font.SysFont('arial',40)
        score=font.render(f"Score:{self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(800,10))

    
    def show_game_over(self):
        self.render_background()
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('Arial', 30)
        line1=font.render(f"Game is over!Your score is {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(200,300))
        line2=font.render("To play again press Enter!",True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    
    def reset(self):
        self.snake=Snake(self.surface,1)
        self.burger=Burger(self.surface)






    

   


    def run(self):
       running=True
       pause=False

       while running:
        for event in pygame.event.get():
          if event.type == KEYDOWN:
                #pass
            if event.key==K_RETURN:
                pygame.mixer.music.unpause()
                pause=False
            if event.key==K_UP:
                self.snake.move_up()
            if event.key==K_DOWN:
                self.snake.move_down()
                
            if event.key==K_RIGHT:
                self.snake.move_right()
            if event.key==K_LEFT:
                self.snake.move_left()
            
          elif event.type == QUIT:
                running = False
        
        try:
         if not pause:
        
          self.play()
        except Exception as e:
          self.show_game_over()
          pause=True #After game over pause becomes true
          self.reset()

        time.sleep(0.2)
           





if __name__ == '__main__':

    game=Game()
    game.run()
   

    
  

