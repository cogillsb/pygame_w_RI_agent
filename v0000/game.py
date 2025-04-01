# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:32:46 2023

@author: grace
"""


import pygame, sys, logging
from settings import *
from random import randint
import random 

class Obstacle(pygame.sprite
.Sprite):
    """ Intro logo animation """
 
    def __init__(self, pos, world):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface((100, 100))
        self.image.fill('black')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.world = world
       
        



class Bullet(pygame.sprite.Sprite):
    """ Intro logo animation """
 
    def __init__(self, start_pos, direction, col, shooter, world):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.col = col
        self.shooter = shooter
        self.image = pygame.Surface((10, 10))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.start_pos = start_pos
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.speed = 10
        self.direction = direction
        self.world = world
       
        
    def update(self):
        """ Update the player's position. """
        dx = self.direction[0]*self.speed
        dy = self.direction[1]*self.speed

        self.rect.x += dx
        self.rect.y += dy
        
        if (self.rect.x>WIDTH) or (self.rect.x<0):
            self.kill()
            
        if (self.rect.y>HEIGHT) or (self.rect.y<0):
            self.kill()
            
        for player in self.world.players:
            if pygame.sprite.collide_rect(self, player):                    
                player.current_health -= 1
                self.kill()
                
        for obstacle in self.world.obstacles:
            if pygame.sprite.collide_rect(self, obstacle):                    
                self.kill()


           
            
class Player(pygame.sprite.Sprite):
    """ Intro logo animation """
 
    def __init__(self, name, start_pos, health_pos, speed, screen, world):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.world = world
        self.name = name
        self.col = tuple([randint(0,255) for _ in range(3)])
        self.alive = True
        self.image = self.world.player_images[self.name]
        self.rect = self.image.get_rect()
        self.start_pos = start_pos
        self.rect.topleft = start_pos
        self.speed = speed
        self.steps = 20
        self.shoot_cooldown = 0
        self.dir = [randint(-1,1), randint(-1,1)]
        self.max_health = 3
        self.current_health = self.max_health
        self.health_pos = health_pos
        self.bullets = pygame.sprite.Group()
        self.screen = screen
       
        
    def update(self):
        """ Update the player's position. """
       
        self.ai()
        if self.current_health == 0:
            self.kill()
        self.bullets.update()
        self.bullets.draw(self.screen)
        
    def move(self):
        #moving        
        dx = self.dir[0]*self.speed
        dy = self.dir[1]*self.speed
        
        #check for collisions
        if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH: dx = 0
        if self.rect.top + dy < 0 or self.rect.bottom + dy > HEIGHT: dy = 0
        
        for obstacle in self.world.obstacles:
            if obstacle.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.w, self.rect.h):
                dx = 0
            if obstacle.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.w, self.rect.h):
                dy = 0
            
        if (dx==0) and (dy==0):
            self.steps = 0
 
        
        self.rect.x += dx
        self.rect.y += dy
        
    def draw(self):
        self.screen.blit(self.image, self.rect)
    
        
        
    def shoot(self, direction):
        if direction == [1,0]: self.bullets.add(Bullet(self.rect.midright, direction, self.col, self.name, self.world))
        if direction == [-1,0]: self.bullets.add(Bullet(self.rect.midleft, direction, self.col, self.name, self.world))
        if direction == [0,1]: self.bullets.add(Bullet(self.rect.midbottom, direction, self.col, self.name, self.world))
        if direction == [0,-1]: self.bullets.add(Bullet(self.rect.midtop, direction, self.col, self.name, self.world))
        if direction == [1,1]: self.bullets.add(Bullet(self.rect.bottomright, direction, self.col, self.name, self.world))
        if direction == [-1,-1]: self.bullets.add(Bullet(self.rect.topleft, direction, self.col, self.name, self.world))
        if direction == [1,-1]: self.bullets.add(Bullet(self.rect.topright, direction, self.col, self.name, self.world))
        if direction == [-1,1]: self.bullets.add(Bullet(self.rect.bottomleft, direction, self.col, self.name, self.world))
    
    
    def ai(self):
        #Put in some random movement
        if self.steps > 0:
            self.steps -= 1
            self.move()
        else:
            self.dir = [randint(-1,1), randint(-1,1)]
            self.steps =  randint(1,50)
        
        #Put in  random shooting
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            self.shoot_cooldown = 20
            direction = [randint(-1,1), randint(-1,1)]
            self.shoot([randint(-1,1), randint(-1,1)])
    


    



class World():
    def __init__(self, screen):
        self.screen = screen
      
        self.player_images = {}
        self.round = 1
        #create sprite group for players
        self.players = pygame.sprite.Group()
 
        self.score_board = {x:0 for x in PLAYER_DAT.keys()}
        self.obstacles = pygame.sprite.Group()
        self.ob_prob = .3

        self.run_intro()
        
        
    def run_intro(self):
        #Load and format the logo.
        img = pygame.image.load('Assets/Original.png')
        img = pygame.transform.scale(img, (500, 500))
        r = img.get_rect()
        r.center = self.screen.get_rect().center
        self.screen.fill('white')  
        self.screen.blit(img, r)
        pygame.display.update()
        pygame.time.delay(1000)
        
        #Drift the logo
        chop = 200
        top = img.subsurface(0,0, r.w, r.h-chop)
        bottom = img.subsurface(0, r.h-chop, r.w, chop)
        
        top_r = top.get_rect()
        top_r.topleft = r.topleft
        bottom_r = bottom.get_rect()
        bottom_r.bottomleft = r.bottomleft
        
        self.screen.fill('white')  
        self.screen.blit(top, top_r)
        self.screen.blit(bottom, bottom_r)
        pygame.display.update()
        
        for i in range(100):
            top_r.y -= 1
            bottom_r.y += 1
            self.screen.fill('white')  
            self.screen.blit(top, top_r)
            self.screen.blit(bottom, bottom_r)
            pygame.display.update()
        
        #Shrink the logo
        sh_top_r = top_r.copy()
        sh_bottom_r = bottom_r.copy()
        sh_top_r.topleft = (0,0)
        sh_bottom_r.topleft = (0,0)
        top_r_target = pygame.Rect(150, 90, 200, 210)
        bottom_r_target = pygame.Rect((75, 0, 204, 70))
        alpha = top.get_alpha()
        
        while (sh_bottom_r!=bottom_r_target) or (sh_top_r!=top_r_target):
            if alpha > 55: alpha -= 1
            #decrement the top
            if sh_top_r.x != top_r_target.x: sh_top_r.x += 1
            if sh_top_r.y != top_r_target.y: sh_top_r.y += 1
            if sh_top_r.w != top_r_target.w: sh_top_r.w -= 1 
            if sh_top_r.h != top_r_target.h: sh_top_r.h -= 1

            top_ss = top.subsurface(sh_top_r)
            top_ss.set_alpha(alpha)
            top_ss_r = top_ss.get_rect()
            top_ss_r.center = top_r.center
            
            
            #decrement the bottom
            if sh_bottom_r.x != bottom_r_target.x: sh_bottom_r.x += 1
            if sh_bottom_r.y != bottom_r_target.y: sh_bottom_r.y += 1
            if sh_bottom_r.w != bottom_r_target.w: sh_bottom_r.w -= 1 
            if sh_bottom_r.h != bottom_r_target.h: sh_bottom_r.h -= 1
            
            bottom_ss = bottom.subsurface(sh_bottom_r)
            bottom_ss_r = bottom_ss.get_rect()
            bottom_ss_r.center = bottom_r.center
            
            self.screen.fill('white')  
            self.screen.blit(top_ss, top_ss_r)
            self.screen.blit(bottom_ss, bottom_ss_r)
            pygame.display.update()
        
        #save the top image
        self.player_images['bg'] = top_ss
        #split out the letters
        lets = {"K": (0, 57),
                "E": (57, 46),
                "S": (103, 46),
                "H": (149, 55),
                }
        #Split out the letter
        for k, v in lets.items():  
            self.player_images[k] = pygame.transform.scale(bottom_ss.subsurface(v[0], 0, v[1], bottom_ss_r.h), (50, 50))
            p = Player(k, PLAYER_DAT[k][0], PLAYER_DAT[k][0], 5, self.screen, self)
            p.rect.x = bottom_ss_r.x + lets[k][0]
            p.rect.y = bottom_ss_r.y
            self.players.add(p) 
        
        #Move to starting position
        check = True
        while check:
            check = False
            for p in self.players:
                if p.rect.topleft!=p.start_pos:
                    check = True
                    #move x
                    if p.rect.x > p.start_pos[0]: p.rect.x -= 1
                    if p.rect.x < p.start_pos[0]: p.rect.x += 1
                    #movey
                    if p.rect.y > p.start_pos[1]: p.rect.y -= 1
                    if p.rect.y < p.start_pos[1]: p.rect.y += 1
            if top_ss_r.center[1] != HEIGHT/2: top_ss_r.y += 1
            #draw everything
            self.screen.fill('white')  
            self.screen.blit(top_ss, top_ss_r)
            self.players.draw(self.screen)
            pygame.display.update()
            
        pygame.time.delay(3000)
        
        
    def update(self): 
        #check for the end of the roud
        if len(self.players)==1:
            self.round_reset()
        
        self.draw() 
        #update sprite group            
        self.players.update()
        self.players.draw(self.screen)
        self.obstacles.draw(self.screen)
        
    def build_obstacles(self):
        for o in self.obstacles:
            o.kill()
        # go point by point
        for i in range(2,7):
            for j in range(2, 7):
                if random.random()<self.ob_prob:
                    #place obstacle
                    self.obstacles.add(Obstacle((i*100, j*100), self))
  
        
    def draw_text(self, text):
        font = pygame.font.SysFont('Futura', 40)
        img = font.render(text, True, 'black')
        r = img.get_rect()
        
        return img, r

        
    def round_reset(self):
        if self.round>1:
            #Display the winner
            winner = self.players.sprites()[0].name
            self.score_board[winner] += 1

            #Draw winner message
            font = pygame.font.SysFont('Futura', 40)
            img = font.render(f'{winner} WINS', True, 'black')
            r = img.get_rect()
            r.center = self.screen.get_rect().center 
            r.y -= 100         
            self.screen.blit(img, r)
            pygame.display.update()
            pygame.time.delay(3000)
            
        self.screen.fill('white')  
        self.build_obstacles()
        
        #rebuild the players
        self.players = pygame.sprite.Group()
        
        #Add players to the group
        for k, v in PLAYER_DAT.items():
            self.players.add(Player(k, v[0], v[1], 5, self.screen, self))

        self.players.draw(self.screen)
        self.draw()
        
        #define font
        font = pygame.font.SysFont('Futura', 60)
        img = font.render(f'ROUND {self.round}', True, 'black')
        r = img.get_rect()
        r.center = self.screen.get_rect().center 
        r.y -= 100         
        self.screen.blit(img, r)
        pygame.display.update()
        #Pause for 5 secs
        pygame.time.delay(5000)
        
        self.round += 1
  
    
    def draw(self):
        #draw logo
        bg_r = self.player_images['bg'].get_rect()
        bg_r.center = self.screen.get_rect().center
        bg_r.y -= 100
        self.screen.blit(self.player_images['bg'], bg_r)
        
        #Draw a border for lower half off the screen
        pygame.draw.line(self.screen, 'black', (0, HEIGHT), (WIDTH, HEIGHT))
  
        #Draw a grid
        for i in range(1,8):
            pygame.draw.line(self.screen, 'grey', (0, i*100), (WIDTH, i*100))
            pygame.draw.line(self.screen, 'grey', (i*100, 0), (i*100, HEIGHT))
        img, r = self.draw_text(f'WINS: {self.score_board}')
        r.center = self.screen.get_rect().center
        r.y = HEIGHT + 10
        self.screen.blit(img, r)
    
        for player in  self.players:
            
            ratio = player.current_health / player.max_health
            pygame.draw.rect(self.screen, BLACK, (player.health_pos[0] - 2, player.health_pos[1] - 2, 204, 24))
            
            pygame.draw.rect(self.screen, RED, (player.health_pos[0], player.health_pos[1], 200, 20))
            pygame.draw.rect(self.screen, player.col, (player.health_pos[0], player.health_pos[1], 200 * ratio, 20)) 
            p_i = pygame.transform.scale(self.player_images[player.name], (24, 24))
            p_i_r = p_i.get_rect()
            p_i_r.x = player.health_pos[0]-26
            p_i_r.y = player.health_pos[1]-2
            self.screen.blit(p_i, p_i_r)
        

class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 200))
        pygame.display.set_caption("Kesho_AI")
        logo = pygame.image.load('Assets/Favicon Logo.png')
        pygame.display.set_icon(logo)
        self.clock = pygame.time.Clock()
        
        self.world = World(self.screen)      
        self.world.round_reset()
        
            
            

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()
            self.screen.fill('white')
            
            self.world.update()
            
            pygame.display.update()
            self.clock.tick(FPS)



if __name__ == "__main__":
    game = Game()
    game.run()