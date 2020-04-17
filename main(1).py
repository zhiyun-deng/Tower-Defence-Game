"""
Mike Chen, David Deng, Yunkai Xiao
Computer Science 20
June.22nd 2016
"""

# Import needed varibles
import pygame
import random
import math
import os

# Set the constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255,180,0)
GRAY = (200,200,200)

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 800


class Player(pygame.sprite.Sprite):
    """ This is the class which contains the player in the game"""
    def __init__(self):
        """ Set up the basic data for player"""
        # Call the parent's constructor
        super().__init__()
        
        """ Set data for player"""
        # Times left for jumping
        self.times = 1
        
        # Image for player
        self.image = pygame.image.load(os.path.join("picture","1.png")).convert()
        self.ori_image=pygame.image.load(os.path.join("picture","1.png")).convert()
        # Set the transparent colour
        self.image.set_colorkey(WHITE)
        self.ori_image.set_colorkey(WHITE)
        
        self.pos = 0
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.dmg = 0
        self.level = None 
        self.grav=.5
        self.length=0
        self.rolling_length=0
        self.rolling=False
        self.angle=0
        self.hp = 120
        self.fram = 0
        self.change_x1 = 0
        self.hit_num = 0
        self.gold_num = 0
        self.faceFront=True
        self.turn=False
        self.fram = 0
        self.regeneration_time=0
    def update(self):
        """ 
        The method to update the player, include changing the facing direction,
        moving, checking collision, off screen check, rolling
        """
        # Changing the facing direction
        if self.faceFront == True:
            if (aim.rect.left + aim.rect.right) / 2 < (self.rect.left+self.rect.right) / 2:
                self.faceFront = False
                self.turn = True
                
        if self.faceFront == False:
            if (aim.rect.left + aim.rect.right) / 2 > (self.rect.left+self.rect.right) / 2:
                self.faceFront = True
                self.turn += True  
                
        if self.turn == True:
            self.image = pygame.transform.flip(self.image,True,False)
            self.turn = False 
        # Calculate the gravity
        self.gravity()
        
        # Move the player left / right
        self.rect.x += self.change_x
        
        #Regeneration
        if self.hp<120:
            self.regeneration_time+=1
            if self.regeneration_time>=300:
                self.hp+=1
                self.regeneration_time=0
        # Check the collision with platform, if collide, reset it to the edge of the platform
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list,False)

        for item in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit            
            if self.change_x > 0:
                self.rect.right = item.rect.left
                
            # Otherwise if we are moving left, do the opposite.    
            elif self.change_x < 0:
                self.rect.left = item.rect.right
                
        # Move the player up / down    
        self.rect.y += self.change_y
 
        # Check the collision with platform, if collide, reset it to the edge of the platform
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        
        for item in block_hit_list:
            
            # If we are falling,
            # set our bottom side to the top side of the item we hit             
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
                
            # Otherwise if we are jumping, do the opposite.  
            elif self.change_y < 0:
                self.rect.top = item.rect.bottom
            
            #Stop the moving if we hit the platform
            self.change_y = 0
            
        """ 
        Check the collision with enemy, boss,coins, and bullets from enemy
        """
        # All the hits would be happened to player in the game are contained in these lists below
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list , False)
        boss_hit_list = pygame.sprite.spritecollide(self, self.level.boss_list , False)
        bullet_hit_list =  pygame.sprite.spritecollide(self, self.level.bullet_list , True)
        coin_hit_list = pygame.sprite.spritecollide(self,self.level.coin_list_sprite, True)
        
        # Check if hit the enemy, if so, reduce the player's hp
        if len(enemy_hit_list) >= 1:
            if self.fram  == 0:
                for enemy in enemy_hit_list:
                    self.actual_dmg=enemy.dmg
          
                self.hp -= self.actual_dmg
                sound = pygame.mixer.Sound(os.path.join("music","hurt.wav"))
                sound.play()      
                self.fram=30
            self.fram -= 1
            for hp1 in current_level.hp_bar_group_player:
                hp1.length =  300 * self.hp / 120                    


        # Check if hit the boss, if so, reduce the player's hp
        if len(boss_hit_list) >= 1:
            if self.fram == 0:
                for enemy in boss_hit_list:
                    self.actual_dmg=enemy.dmg
          
                self.hp -= self.actual_dmg
                sound = pygame.mixer.Sound(os.path.join("music","hurt.wav"))
                sound.play()       
                self.fram=30
            self.fram += 1
            for hp1 in current_level.hp_bar_group_player:
                if self.hp >= 0:
                    hp1.length =  300 * self.hp / 120 
                elif self.hp < 0:
                    hp1.length =  0                       
        if len(boss_hit_list) == 0 and len(enemy_hit_list) == 0:
            self.fram=0
    
                      
        # Check if hit the bullet from boss, if so, reduce the player's hp    
        if len(bullet_hit_list) >= 1:
            self.hp -= 3
            
            for hp1 in current_level.hp_bar_group_player:
                if self.hp >= 0:
                    hp1.length =  300 * self.hp / 10 
                elif self.hp < 0:
                    hp1.length =  0
                    
        
        # Check if hit the coin, if so, increase the points        
        if len(coin_hit_list) >0 :
            self.gold_num += 1
            sound = pygame.mixer.Sound(os.path.join("music","get_coin.ogg"))
            sound.play()
            
        # Move the character by rolling
        if self.rolling>=True:
            self.rolling_length+=self.change_x
            self.angle+=100
            self.image=pygame.transform.rotate(self.ori_image,self.angle)
            if self.rolling_length>=200 or self.rolling_length<=-200:
                self.image=self.ori_image
                self.angle=0
                self.rolling=False
                self.change_x/=3
                self.rolling_length=0        

        # Off screen check   
        if self.rect.x > 940:
            self.change_x = 0
            self.rect.x = 940
            
        elif self.rect.x < 0:
            self.change_x = 0
            self.rect.x = 0
            
        if self.rect.y < 0:
            self.change_y = 0
            self.rect.y = 0
            
        elif self.rect.y > 740:
            self.change_y = 0
            self.rect.y = 740
        
        
    def gravity(self):
        """ change change_y according to gravity"""   
        if self.change_y == 0:
                
            self.change_y = 1
                
        else:
            self.change_y +=self.grav
 
            
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    def roll(self):
        """ Called when the user want the player to roll. """
        self.rolling=True
        self.change_x*=3 
    def jump(self):
        """ Called when the user hits the up arrow. """
        self.times -= 1    
        self.rect.y += 2   
        ground_hit_list = pygame.sprite.spritecollide (self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(ground_hit_list) > 0 or self.rect.y == 740:
            self.times = 1
        if self.times >= 0:      
            self.change_y = -10
                
        
        
        
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """    
        self.change_x = 6 
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0        
            
    
    
class Pistol_image(pygame.sprite.Sprite):
    """ The image for the pistol, which is the Machine_Gun1 class"""
    def __init__(self):
        # Set the basic varible for the pistol
        # Call the parent's constructor
        super().__init__()
        
        # Load the image
        self.image = pygame.image.load(os.path.join("picture","pistol.png")).convert()
        self.image.set_colorkey(WHITE)
        self.ori_image=pygame.image.load(os.path.join("picture","pistol.png")).convert()
        self.ori_image.set_colorkey(WHITE)
        
        # Set a referance to the image rect
        self.rect = self.image.get_rect()
        
        # Set the initial angle of the pistol
        self.angle=0
        
        # If the player face front
        self.faceFront=False
        
        # If the player needs to turn
        self.turn=False
    def update(self):
        """ Move the image of pistol"""
        # Set the position of the image
        self.rect.top=player.rect.top+20
        
        # Set the image's facing direction
        if self.faceFront:
            self.rect.left=(player.rect.left+player.rect.right)/2
            if not player.faceFront:
                self.faceFront = False
                self.turn = True
        if not self.faceFront:
            self.rect.right=(player.rect.left+player.rect.right)/2
            if player.faceFront==True:
                self.faceFront=True
                self.turn+=True   
        if self.turn==True:
            self.ori_image=pygame.transform.flip(self.ori_image,True,False)
            self.turn=False
            
        # Calculate the angle of the pistol according to aim
        self.difference_y =  aim.rect.y + 72 - self.rect.y 
        self.difference_x =  aim.rect.x + 100 - self.rect.x        
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)   
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi-self.angle
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi-self.angle   
        else:
            self.angle*=-1
            
        # Rotate the image
        self.image=pygame.transform.rotate(self.ori_image,math.degrees(self.angle))
        
        # Remove the image if not pistol
        if gun_num!=1:
            all_sprite_list.remove(self)
class Machine_gun_image(pygame.sprite.Sprite):
    """ The image for the pistol, which is the Machine_Gun2 class"""
    def __init__(self):
        # Call the parent's constructor
        super().__init__()
   
        # Set images for machine gun
        self.image = pygame.image.load(os.path.join("picture","machine_gun.png")).convert()
        self.image.set_colorkey (BLACK)
        self.ori_image = pygame.image.load(os.path.join("picture","machine_gun.png")).convert()
        self.ori_image.set_colorkey (BLACK)
        
        # Set a referance to the image rect
        self.rect = self.image.get_rect()
        
        # Set the initial angle
        self.angle = 0
        
        # Set the facing direction of player
        self.faceFront = True
        
        # If the player need to turn
        self.turn = False
    def update(self):
        """ Move the image """
        # Set the position of image
        self.rect.top=player.rect.top
        
        # Set the image's facing direction
        if self.faceFront == True:
            self.rect.left = player.rect.left
            if player.faceFront == False:
                self.faceFront = False
                self.turn += True
        if self.faceFront == False:
            self.rect.right=player.rect.right
            if player.faceFront == True:
                self.faceFront = True
                self.turn += True   
        if self.turn == True:
            self.ori_image = pygame.transform.flip(self.ori_image,True,False)
            self.turn = False 
            
        # Calculate the angle of the machine gun
        self.difference_y =  aim.rect.y + 72 - self.rect.y 
        self.difference_x =  aim.rect.x + 100 - self.rect.x        
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)   
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi-self.angle
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi-self.angle   
        else:
            self.angle*=-1
        # Rotate the image
        self.image=pygame.transform.rotate(self.ori_image,math.degrees(self.angle))
        
        # Remove the image if not machine gun
        if gun_num!=2:
            all_sprite_list.remove(self)
class Shot_gun_image(pygame.sprite.Sprite):
    """ The image for the pistol, which is the Machine_Gun1 class"""
    def __init__(self):
        # Call the parent's constructor
        super().__init__()
        
        # Set images for shotgun
        self.image = pygame.image.load(os.path.join("picture","shot_gun.png")).convert()
        self.image.set_colorkey(BLACK)
        self.ori_image=pygame.image.load(os.path.join("picture","shot_gun.png")).convert()
        self.ori_image.set_colorkey(BLACK)
        
        # Set a referance to the image rect
        self.rect = self.image.get_rect()
        
        # Set the initial angle of the shotgun
        self.angle=0
        
        # Set the facing direction of player
        self.faceFront = True
        
        # If the player need to turn
        self.turn=False
    def update(self):
        
        # Set the position of image
        self.rect.top=player.rect.top
        
        # Set the image's facing direction
        if self.faceFront==True:
            self.rect.left=player.rect.left
            if player.faceFront==False:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            self.rect.right=player.rect.right
            if player.faceFront==True:
                self.faceFront=True
                self.turn+=True   
        if self.turn==True:
            self.ori_image=pygame.transform.flip(self.ori_image,True,False)
            self.turn=False 
            
        # Calculate the angle of the machine gun    
        self.difference_y =  aim.rect.y + 72 - self.rect.y 
        self.difference_x =  aim.rect.x + 100 - self.rect.x        
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)   
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi-self.angle
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi-self.angle   
        else:
            self.angle*=-1
            
        
        # Rotate the image
        self.image=pygame.transform.rotate(self.ori_image,math.degrees(self.angle))
        
        # Remove the image if not machine gun        
        if gun_num!=3:
            all_sprite_list.remove(self)
class Rocket_launcher_image(pygame.sprite.Sprite):
    
    """ The image for the pistol, which is the Machine_Gun1 class"""
    def __init__(self):
        # Call the parent's constructor
        super().__init__()
        
        # Set images for rocket launcher
        self.image = pygame.image.load(os.path.join("picture","Rocket_launcher.png")).convert()
        self.image.set_colorkey(BLACK)
        self.ori_image=pygame.image.load(os.path.join("picture","Rocket_launcher.png")).convert()
        self.ori_image.set_colorkey(BLACK)
        
        # Set a referance to the image rect
        self.rect = self.image.get_rect()
        
        # Set the initial angle of the shotgun
        self.angle=0
        
        # Set the facing direction of player
        self.faceFront = True
        
        # If the player need to turn
        self.turn=False
    def update(self):
        
        # Set the position of image
        self.rect.top=player.rect.top
        
        # Set the image's facing direction
        if self.faceFront==True:
            self.rect.left=player.rect.left
            if player.faceFront==False:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            self.rect.right=player.rect.right
            if player.faceFront==True:
                self.faceFront=True
                self.turn+=True   
        if self.turn==True:
            self.ori_image=pygame.transform.flip(self.ori_image,True,False)
            self.turn=False 
            
        # Calculate the angle of the rocket launcher    
        self.difference_y =  aim.rect.y + 72 - self.rect.y 
        self.difference_x =  aim.rect.x + 100 - self.rect.x        
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)   
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi-self.angle
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi-self.angle   
        else:
            self.angle*=-1
            
        
        # Rotate the image
        self.image=pygame.transform.rotate(self.ori_image,math.degrees(self.angle))
        
        # Remove the image if not rocket launcher      
        if gun_num!=4:
            all_sprite_list.remove(self)
            
            
class Platform1(pygame.sprite.Sprite):
    """ A class to create the Platform with height and width """
    def __init__(self, height, width):
        super().__init__()
        
        
        self.image = pygame.Surface([height,width])
        self.image.fill (BLACK)
        
        self.rect = self.image.get_rect()
class Platform(pygame.sprite.Sprite):
    """ A class to create the Platform with image """
    def __init__(self, image):
        super().__init__()
        
        self.image = image
        
        self.rect = self.image.get_rect()
        
class MovingPlatform(Platform):
    """ A class to create moving platform """
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
        """ Move the platform """
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player.
            
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. 
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
                
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.top = self.rect.bottom
 
        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
        
class Trap(pygame.sprite.Sprite):
    """ A class to create the enemy """
    def __init__ (self, pos_x,pos_y,ability):
        # Call the parent's constrctor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","1.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a referance to the image rect and set the position of the rect
        self.rect = self.image.get_rect()
        self.rect.left = pos_x
        self.pos_x = pos_x
        self.rect.bottom = pos_y
        
        # Set the velocity
        self.change_x= random.randrange(-3,4,6)
        self.change_y=0
        
        # Set the gravity
        self.grav=.1
        
        # Set the cooldown time for spells
        self.cooldown=0
        
        # Set the facing direction
        self.faceFront=True
        
        # If the enemy need to turn
        self.turn=False
        
        # The varible to make enemy use their spell
        self.ability_shoot=False
        self.ability_run=False
        
        # Varible for calculating the distance of dash
        self.length=0
        
        # Damage when collide with the player
        self.dmg = 1
        self.running=False
        self.ability_magic=False
        
        # The spell the enemy has
        if ability==1:
            self.ability_shoot=True
        elif ability==2:
            self.ability_run=True
        elif ability==3:
            self.ability_magic=True            
    def update(self):
        
        """ Move the enemy and use their skill """
        
        # Calculate the gravity
        self.gravity()
        
        # Change the facing direction
        if self.faceFront==True:
            if player.rect.x>self.rect.x:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            if player.rect.x<=self.rect.x:
                self.faceFront=True
                self.turn+=True   
        if self.turn==True:
            self.image=pygame.transform.flip(self.image,True,False)
            self.turn=False   
            
        # update the cd time   
        if self.cooldown!=0:
            self.cooldown-=1
            
        # Move the enemy
        self.rect.x+=self.change_x

        if not self.running:
            if self.rect.x>self.pos_x+500+current_level.world_shift:
                self.change_x=-3
            if self.rect.x<self.pos_x-500+current_level.world_shift:
                self.change_x=3
        if self.rect.y > 740:
            self.change_y = 0
            self.rect.y = 740       
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
            
            if self.change_x > 0:
                self.jump()
                self.rect.right = item.rect.left
                
            elif self.change_x < 0:
                self.jump()
                self.rect.left = item.rect.right
            
        self.rect.y += self.change_y
 
        
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
            elif self.change_y < 0:
                self.rect.top = item.rect.bottom
            
            self.change_y = 0
            
        # Make enemy use the spell
        if self.ability_shoot==True:
            if self.rect.x<=player.rect.x+500 and self.rect.x>=player.rect.x-500 and self.cooldown==0:
                self.ability=Enemy_bullet((self.rect.left+self.rect.right)/2,(self.rect.top+self.rect.bottom)/2)
                current_level.enemy_list.add(self.ability)
                self.cooldown=300
        if self.ability_run==True:
            if self.rect.x<=player.rect.x+500 and self.rect.x>=player.rect.x-500 and self.cooldown==0: 
                self.run()
        if self.ability_magic==True:
            if self.rect.x<=player.rect.x+800 and self.rect.x>=player.rect.x-800 and self.cooldown==0:   
                self.ability=Enemy_magic_burst()
                current_level.special_list.add(self.ability)
                self.cooldown=300
                
    def gravity(self):
        # Calculate the gravity    
        if self.change_y == 0:
                
            self.change_y = 1
                
        else:
            self.change_y +=self.grav
 
            
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    def jump(self):
        """ Called when user press the up arrow key"""
        self.change_y = -6    
    def run(self):
        # the method to dash
        if not self.running:
            if self.rect.x-player.rect.x<0 and self.change_x<0:
                self.change_x*= -3
            elif self.rect.x-player.rect.x>0 and self.change_x>0:
                self.change_x*= -3
            elif self.rect.x-player.rect.x<0 and self.change_x>0:
                self.change_x*= 3       
            elif self.rect.x-player.rect.x>0 and self.change_x<0:
                self.change_x*= 3
            self.running=True
        if self.running==True:
            self.length += self.change_x
            if self.length >= 500 or self.length <= -500:
                self.running=False
                self.change_x/=3
                self.length=0
                self.cooldown=500
    
class Enemy_bullet(pygame.sprite.Sprite):
    """ A class contains the bullet the enemy would use"""
    def __init__(self,pos_x,pos_y):
        
        # Call the parent's constructor
        super().__init__()
        
        # Set the image for enemy_bullet
        self.image = pygame.image.load(os.path.join("picture","minion_bullet.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a referance to the image rect and the position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the velocity
        self.speed=7
        
        # Set the initial angle
        self.angle=0
        
        # Set the time for calculating the distance
        self.time=0
        
        
        # Calculate the direction of the bullet moving
        self.difference_y =  player.rect.y  - self.rect.y 
        self.difference_x =  player.rect.x  - self.rect.x
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)
            
        # Calculate the velocity
        self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
        self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))   
        
        # Set the damage of bullet
        self.dmg=3
    def update(self):
        """ Move the bullet"""
        self.rect.x +=self.change_x
        self.rect.y +=self.change_y      
        self.time+=1
        if self.rect.bottom<=0 or self.rect.top>=screen_y or self.time>=600:
            current_level.enemy_list.remove(self)
class Enemy_magic_burst(pygame.sprite.Sprite):
    """ A class contain the magic burst skill of enemy """
    
    def __init__(self):
        # Call the parent's constructor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","minion_spell.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a referance to the image rect and the position
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        
        # Set the time for cooling down
        self.time=60
        
    def update(self):
        # Produce bullets
        self.time-=1
        if self.time==0:
            new_magic_burst=Enemy_magic_burst1((self.rect.left+self.rect.right)/2,(self.rect.top+self.rect.bottom)/2)
            current_level.enemy_list.add(new_magic_burst)
            current_level.special_list.remove(self)
            
class Enemy_magic_burst1(pygame.sprite.Sprite):
    """ The magic burst skill for enemy """
    def __init__(self, pos_x, pos_y):
        # Call parent's constructor
        super().__init__()
        
        # Set the image and the size
        self.ori_image = pygame.image.load(os.path.join("picture","minion_spell1.png")).convert()
        self.ori_image.set_colorkey(WHITE)
        self.width=10
        self.height=10        
        self.image=pygame.transform.scale(self.ori_image,(self.width,self.height))
        
        # Set a referance to the image rect and the position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.po_x=pos_x
        self.rect.y = pos_y
        self.po_y=pos_y
        
        # Set the velocity
        self.rect_change_x=0
        self.rect_change_y=0
        self.boundary_width=200
        self.boundary_height=200
        
        
        # set the velocity
        self.change_speed = 20
        
        # set the damage of the burst
        self.dmg=3
    def update(self):
        # Change the size of the image
        self.width+=self.change_speed
        self.height+=self.change_speed
        self.rect_change_x-=int(self.change_speed/2)
        self.rect_change_y-=int(self.change_speed/2)
        self.image=pygame.transform.scale(self.ori_image,(self.width,self.height))
        
        # reset a referance to the image rect and the position
        self.rect=self.image.get_rect()
        self.rect.x=self.po_x+self.rect_change_x
        self.rect.y=self.po_y+self.rect_change_y          
        if self.width >= self.boundary_width and self.height>=self.boundary_height:
            current_level.enemy_list.remove(self)

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
    def __init__(self, player):
        # Set all the lists may be used in different levels
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.boss_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.hp_bar_group = pygame.sprite.Group()
        self.hp_bar_group_player = pygame.sprite.Group()
        self.hp_bar_group_ammo = pygame.sprite.Group()
        self.coin_list_sprite = pygame.sprite.Group()
        self.special_list = pygame.sprite.Group()
        
        # Set the player
        self.player = player
        
        # Varible for shifting the world
        self.world_shift = 0
        
        # Varible for background
        self.background = None
        
    
    def update(self):
        # Call the update function in the sprites in each group
        
        self.boss_list.update()
        self.platform_list.update()
        self.hp_bar_group_player.update()
        self.enemy_list.update()
        self.bullet_list.update()
        self.hp_bar_group.update()
        self.coin_list_sprite.update()
        self.hp_bar_group_ammo.update()
        self.special_list.update()
    def draw(self,screen):
        # Blit the sprite in each group to screen
        screen.fill(WHITE)
        screen.blit(background_image, [0,0])
        self.bullet_list.draw(screen)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen)
        self.hp_bar_group.draw(screen)
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)
        self.coin_list_sprite.draw(screen)
        self.special_list.draw(screen)
    def shift_world(self,shift_x):
        # Move all the platforms to make it look like the player are keep walking
        self.world_shift += shift_x
        
        for platform in self.platform_list:
            platform.rect.x += shift_x
            
        for trap in self.enemy_list:
            trap.rect.x += shift_x
            
        for boss in self.boss_list:
            boss.rect.x += shift_x
        for bullet in self.bullet_list:
            bullet.rect.x += shift_x
            
        for coin in self.coin_list_sprite:
            coin.rect.x += shift_x
        for special in self.special_list:
            special.rect.x += shift_x
            
            
# Create different levels
class Level_01(Level):
    """ Survival mode """
    
    def __init__(self,player):
        """ Create level 1. """
        # Call the parent constructor
        Level.__init__(self,player)
        
        # Create the trap list to contain the traps' position
        self.trap_list = []
       
       
        # Create the bar for the hp and ammo left 
        hp_player = hp_bar(300,15,0,100)
        
        self.hp_bar_group_player.add(hp_player)
        
        ammo_left = hp_bar(200,15,0,150)
        
        self.hp_bar_group_ammo.add(ammo_left)        
        self.level_limit = 50000
    def create(self): 
        """ Create platforms, coins, enemies """
        
        # Create the platforms
        level = []
        append = True
        for i in range(50):
           
            new_block = [random.randrange(50,250,50), random.randrange(50,60), random.randrange(player.rect.x + 400,player.rect.x + 1400),random.randrange(400,800,90)] # occupies the first 900 pix after person
            
            for item in level:
                if (new_block[3] < item[3] + 135) and (new_block[3] > item[3] - 135) and  (new_block[2] < item[2] + 265) and (new_block[2] > item[2] - 265):
                    append = False
                    break
            if append:
                level.append(new_block)
            append = True
            
        for platform in level:
            block = Platform1(platform[0],platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)        
        
        
        # Create the enemies and coins
        self.trap_list = []
        self.coin_list = []
        for i in range(10):
            place = random.randrange(len(level)) #random block to appear on
            appear = [level[place][2]+100, level[place][3]-100,0] #exact coordinate of appearance
            for i in self.trap_list:
                if appear[0] == i[0]:
                    append = False
                    break
            if append:
                self.trap_list.append(appear)
            append = True                    
            
            for trap in self.trap_list:
                traps = Trap( trap[0],trap[1],trap[2])
                           
                current_level.enemy_list.add(traps)   
                traps.image=pygame.image.load(os.path.join("picture","rd1_mini.png")).convert()
                traps.image.set_colorkey(WHITE)                
                trap_count = len( current_level.enemy_list)            
            
        for i in range(30):
            place = random.randrange(len(level))
        
            lent = level[place][0]/50
            lent = int(lent)
            for i in range(lent):
                appear = [level[place][2] + i*60, level[place][3]-30] 
                self.coin_list.append(appear) 
            
        for Coin in self.coin_list:
                    coins = coin(Coin[0],Coin[1])
                    self.coin_list_sprite.add(coins)
                               
        
        
        
       
        
        
        
class Level_02(Level):
    """ Challenge Mode """
    def __init__(self,player):
        # call the parent's contructor
        Level.__init__(self,player)
        
        # Create the platforms 
        level = [[70, 510, -20, 800],[1000, 70, 0, 800],[70, 510, 950, 800]]
        self.level_limit = 2000
    
        
        
        for platform in level:
            block = Platform1(platform[0],platform[1])
            block.rect.x = platform[2]
            block.rect.bottom = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        # Create bosses
        self.boss_num=0
        self.bossList = []
        boss = Boss_1()
        self.bossList.append(boss)
        boss = Boss_2()
        self.bossList.append(boss)
        boss = Boss_3()
        self.bossList.append(boss)
        boss = Boss_4()
        self.bossList.append(boss)
        boss = Boss_5()
        self.bossList.append(boss)        
        
        hp_player = hp_bar(300,15,0,100)
        self.hp_bar_group_player.add(hp_player)
        
class StLevel_01(Level):
    """ Definition for level 1 in story mode """
    def __init__(self,player):
        # Create the level
        
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","introLevelBg.jpg")).convert()
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=2000
        
        # Set all platforms
        level = [[0, 800],[490,800],[980,800],[1470,800],[1960,800],[400,620],[700,440],[1000,260],[1500,620]]
                 
        self.level_image=pygame.image.load(os.path.join("picture","introBlock.png")).convert()

                 
                 
                 
        # Set the trap's position
        trap_list = [[1500,700,0]]
        
        #create the platforms
        for platform in level:
            
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)  
                
        # Create the traps
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            traps.image=pygame.image.load(os.path.join("picture","singleDog.jpg")).convert()
            traps.image.set_colorkey(WHITE)
            self.enemy_list.add(traps)
            
                    
    def draw(self,screen):
        #blit them on the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen) 
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)
class StLevel_02(Level):
    """ Definition for level 2 in story mode """
    def __init__(self,player):
        # Create the level 2
        self.background_image = pygame.image.load(os.path.join("picture","rd1bg1.png")).convert()
        
        # Call the parent constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=5000
        
        # Create all platforms
        level = [[0, 800],[350, 800],
                 [700, 800],[1050, 800],
                 [1400, 800],[1750, 800],
                 [2100, 800],[2450, 800],
                 [2800, 800],[3150, 800],
                 [3500, 800],[3850, 800],
                 [4200, 800],[4550, 800],
                 [4900, 800],
                 [300,650],[600,350],[900,500],[1200,350],[1500,650],
                 [1800,350],[2100,500],[2400,650],[2700,500],[3000,350],
                 [3300,650],[3600,350],[3900,650],
                 [4200,350],[4500,500],[4800,650],
                 ]
        
                 
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd1Block.png")).convert()
        
        # Create the enemies
        trap_list = []
        for i in range (20):
            temp_list=[]
            value=random.randrange(600,self.level_limit-600)
            temp_list.append(value)
            value=random.randrange(100,700)
            temp_list.append(value)
            temp_list.append(0)
            trap_list.append(temp_list)        
        for platform in level:
            # Create stable platforms
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create moving platforms
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)         
    
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            self.enemy_list.add(traps)
            traps.image=pygame.image.load(os.path.join("picture","rd1_mini.png")).convert()
            traps.image.set_colorkey(WHITE)
               
    def draw(self,screen):
        # Blit all the sprites in the group
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen) 
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)        
class StLevel_03(Level):
    """ Definition for level 3 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd1bg2.png")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=5000
        
        # Create all platforms
        level = [[0, 800],[350, 800],
                 [700, 800],[1050, 800],
                 [1400, 800],[1750, 800],
                 [2100, 800],[2450, 800],
                 [2800, 800],[3150, 800],
                 [3500, 800],[3850, 800],
                 [4200, 800],[4550, 800],
                 [4900, 800],
                 [300,675],[600,550],[900,425],[1200,550],[1500,675],
                 [1800,550],[2100,425],[2400,300],
                 [2400,675],[2700,550],[3000,550],[3300,675],
                 [3300,300],[3600,425],[3900,550],[4200,675],
                 [4500,550],[4800,425]
                 ]
        
                
        # Set image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd1Block.png")).convert()
        
        # Create enemies
        trap_list = []
        
        # Create random position of enemy
        for i in range (25):
            temp_list=[]
            value=random.randrange(600,self.level_limit-600)
            temp_list.append(value)
            value=random.randrange(100,700)
            temp_list.append(value)
            temp_list.append(0)
            trap_list.append(temp_list)           
        for platform in level:
            # Create stable platforms
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create moving platforms
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)          
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            self.enemy_list.add(traps)
            traps.image=pygame.image.load(os.path.join("picture","rd1_mini.png")).convert()
            traps.image.set_colorkey(WHITE)   
    def draw(self,screen):
        # Blit all the sprites on the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen)  
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)        
class StLevel_04(Level):
    """ Definition for level 4 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd1bg3.png")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=2500
        
        # Set the position of platforms
        level = [[0, 800],[350, 800],
                 [700, 800],[1050, 800],
                 [1400, 800],[1750, 800],
                 [2100, 800],[2450, 800],
                 [0,425],[300,450],[600,475],
                 [1900,450],[1600,475],[2200,425],[2500,425],
                 [600,675],[1600,675],
                 [925,650],[1275,650]
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd1Block.png")).convert()
        
        # Create platforms
        for platform in level:
            if len(platform) == 2:
                
                # Create stable platforms
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
            if len(platform) == 8:
                
                # Create moving platforms
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)
                
        # Create boss     
        boss = Boss_1()
        self.boss_list.add(boss)
    def draw(self,screen):
        # Blit all the sprites to screen
        
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen)
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)
        self.hp_bar_group.draw(screen)
class StLevel_05(Level):
    """ Definition for level 5 in story mode """
    
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd2bg1.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=5000
        
        # Set the position of platforms
        level = [[0, 800],[200, 800],
                 [400, 800],[600, 800],
                 [800, 800],[1000, 800],
                 [1200, 800],[1400, 800],
                 [1600,800],[1800,800],
                 [2000,800],[2200,800],
                 [2400,800],[2600,800],
                 [2800,800],[3000,800],
                 [3200,800],[3400,800],
                 [3600,800],[3800,800],
                 [4000,800],[4200,800],
                 [4400,800],[4600,800],
                 [4800,800],[5000,800],
                 [200,650],[400,600],[600,550],[800,500],[1000,450],[1200,400],
                 [1400,350],[1800,250],[2000,200],[2200,150],
                 [4600,650],[4400,600],[4200,550],[4000,500],[3800,450],[3600,400],[3400,350],
                 [3000,250],[2800,200],[2600,150],
                 [800,700],[1000,650],[1200,600],[1400,550],[1800,450],[2000,400],[2200,350],
                 [4000,700],[3800,650],[3600,600],[3400,550],[3000,450],[2800,400],[2600,350],
                 [1600,700],[1800,650],[2000,600],[2200,550],
                 [3200,700],[3000,650],[2800,600],[2600,550],[2400,650]
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd2Block.png")).convert()
        
        # Create a list contains the position of enemies
        trap_list = []
        for i in range (20):
            # Create random position of enemy
            temp_list=[]
            value=random.randrange(600,self.level_limit-600)
            temp_list.append(value)
            value=random.randrange(100,700)
            temp_list.append(value)
            temp_list.append(1)
            trap_list.append(temp_list) 
            
        # Create platforms
        for platform in level:
            if len(platform) == 2:
                # Create stable platforms
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
            if len(platform) == 8:
                # Create moving platforms
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)
                
        # Create enemies
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            self.enemy_list.add(traps)
            traps.image=pygame.image.load(os.path.join("picture","rd2_mini.png")).convert()
            traps.image.set_colorkey(WHITE)            
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen) 
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)    
class StLevel_06(Level):
    """ Definition for level 6 in story mode """
    
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd2bg2.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=5000
        
        # Create a list contains the position of platforms
        level = [[0, 800],[200, 800],
                 [400, 800],[600, 800],
                 [800, 800],[1000, 800],
                 [1200, 800],[1400, 800],
                 [1600,800],[1800,800],
                 [2000,800],[2200,800],
                 [2400,800],[2600,800],
                 [2800,800],[3000,800],
                 [3200,800],[3400,800],
                 [3600,800],[3800,800],
                 [4000,800],[4200,800],
                 [4400,800],[4600,800],
                 [4800,800],[5000,800],
                 [200,200],[400,350],[600,650],[800,500],[800,200],[1000,350],[1200,500],[1400,650],
                 [1600,350],[1800,200],[1800,650],[2000,50],[2000,500],[2200,650],[2400,350],[2600,500],[2800,650],
                 [2800,200],[3000,50],[3200,350],[3200,650],[3400,200],[3400,500],[3600,200],[3600,500],[3800,350],
                 [4000,500],[4200,650],[4400,200],[4400,650],[4600,350],[4800,200],[4800,500]
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd2Block.png")).convert()
        
        # Create a list contain the enemies' position
        trap_list = []
        for i in range (30):
            # Create the enemy's position randomly
            temp_list=[]
            value=random.randrange(600,self.level_limit-600)
            temp_list.append(value)
            value=random.randrange(100,700)
            temp_list.append(value)
            temp_list.append(1)
            trap_list.append(temp_list)   
        
        # Create the platforms
        for platform in level:
            if len(platform) == 2:
                #Create stable platforms
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
            if len(platform) == 8:
                # Create moving platforms
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)
                
        # Create the enemies
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            self.enemy_list.add(traps) 
            traps.image=pygame.image.load(os.path.join("picture","rd2_mini.png")).convert()
            traps.image.set_colorkey(WHITE)            
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen) 
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)        
class StLevel_07(Level):
    """ Definition for level 8 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd2bg3.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=2500
        
        # Create a list to contain the positions of all platforms
        level = [[0, 800],[200, 800],
                 [400, 800],[600, 800],
                 [800, 800],[1000, 800],
                 [1200, 800],[1400, 800],
                 [1600,800],[1800,800],
                 [2000,800],[2200,800],
                 [2400,800],
                 [0,425],[200,675],[200,425],
                 [400,675],[400,425],
                 [2500,425],[2300,425],[2200,675],[2200,425],
                 [2000,675],[2000,425],  
                 [600,550],[800,550],[1000,550],[1200,550],[1400,550],
                 [1600,550],[1800,550],
                 [600,300],[800,300],
                 [1600,300],[1800,300]
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd2Block.png")).convert()
        
        
        # Create platforms
        for platform in level:
            if len(platform) == 2:
                # Create stable platforms
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
            if len(platform) == 8:
                # Create moving platforms
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)  

        # Create the boss    
        boss = Boss_2()
        self.boss_list.add(boss)
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen) 
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)
        self.hp_bar_group.draw(screen)
class StLevel_08(Level):
    """ Definition for level 8 in story mode """
    
    def __init__(self,player):
        # Set the background image 
        self.background_image = pygame.image.load(os.path.join("picture","rd3bg1.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=5000
        
        # Create a list to contain the positions of all platforms
        level = [[0, 800],[300,800],
                 [600,800],[900,800],
                 [1200,800],[1500,800],
                 [1800,800],[2100,800],
                 [2400,800],[2700,800],
                 [3000,800],[3300,800],
                 [3600,800],[3900,800],
                 [4200,800],[4500,800],
                 [4800,800],
                 [300,200],[600,650],[900,350],[1200,500],[1500,650],
                 [1800,200],[2100,500],[2400,350],[2700,500],[3000,650],
                 [3300,200],[3600,350],[3900,650],[4200,500],[4500,650]
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd3Block.png")).convert()
        
        # Set a list to contain the position of enemy
        trap_list = []
        for i in range (25):
            # Create the enemy's position randomly
            temp_list=[]
            value=random.randrange(600,self.level_limit-600)
            temp_list.append(value)
            value=random.randrange(100,700)
            temp_list.append(value)
            temp_list.append(2)
            trap_list.append(temp_list)   
            
        # Create platforms
        for platform in level:
            # Create stable platforms
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
            
            # Create moving platforms
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block) 
                
        # Create enemies
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            self.enemy_list.add(traps)
            traps.image=pygame.image.load(os.path.join("picture","rd3_mini.png")).convert()
            traps.image.set_colorkey(WHITE)            
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen)   
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)        
class StLevel_09(Level):
    """ Definition for level 9 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd3bg2.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=5000
        
        # Create a list to contain the positions of all platforms
        level = [[0, 800],[300,800],
                 [600,800],[900,800],
                 [1200,800],[1500,800],
                 [1800,800],[2100,800],
                 [2400,800],[2700,800],
                 [3000,800],[3300,800],
                 [3600,800],[3900,800],
                 [4200,800],[4500,800],
                 [4800,800],
                 [300,500],[300,200],[900,650],[900,350],
                 [1500,650],[1500,350],[2100,500],[2100,200],
                 [2700,650],[2700,350],[3300,500],[3300,200],
                 [3900,500],[3900,200],[4500,650],[4500,350],
                 [600,361,0,random.randrange(-3,4,6),0,0,160,650],
                 [1800,562,0,random.randrange(-3,4,6),0,0,160,650],
                 [3000,263,0,random.randrange(-3,4,6),0,0,160,650],
                 [4200,452,0,random.randrange(-3,4,6),0,0,160,650]
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd3Block.png")).convert()
        
        # Set a list to contain the position of enemy
        trap_list = []
        for i in range (37):
            # Create the enemy's position randomly
            temp_list=[]
            value=random.randrange(600,self.level_limit-600)
            temp_list.append(value)
            value=random.randrange(100,700)
            temp_list.append(value)
            temp_list.append(2)
            trap_list.append(temp_list)
            
        # Create platforms
        for platform in level:
            # Create stable platforms
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create moving platforms
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)   
                
        # Create enemies
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            self.enemy_list.add(traps)       
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen)
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)        
class StLevel_10(Level):
    """ Definition for level 10 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd3bg3.png")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=2500
        
        # Create a list to contain the positions of all platforms
        level = [[0, 800],[300,800],
                 [600,800],[900,800],
                 [1200,800],[1500,800],
                 [1800,800],[2100,800],
                 [2400,800],
                 [0,500],[300,200],[2200,500],[1900,200],[2500,500],
                 [600,525,0,random.randrange(-3,4,6),0,0,160,650],
                 [1600,254,0,random.randrange(-3,4,6),0,0,160,650],
                 [900,350],[1300,350],[1100,350],
                 [300,650],[1900,650],[900,650],[1300,650]
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd3Block.png")).convert()
        
        
        # Create platforms  
        for platform in level:
            # Create Stable platforms
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
            
            # Create moving platforms
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)
                
        # Create boss  
        boss = Boss_3()
        self.boss_list.add(boss)                
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen)
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)
        self.hp_bar_group.draw(screen)
class StLevel_11(Level):
    
    """ Definition for level 11 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd4bg1.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=5000
        
        # Create a list to contain the positions of all platforms
        level = [[0, 800],[300,800],
                 [600,800],[900,800],
                 [1200,800],[1500,800],
                 [1800,800],[2100,800],
                 [2400,800],[2700,800],
                 [3000,800],[3300,800],
                 [3600,800],[3900,800],
                 [4200,800],[4500,800],
                 [4800,800],
                 [300,650],[300,200],[1200,650],[1200,200],[2100,650],[2100,200],
                 [3000,650],[3000,200],[3900,650],[3900,200],[4800,650],[4800,200],
                 [750,245,0,random.randrange(-4,5,8),0,0,164,650],
                 [1650,345,0,random.randrange(-4,5,8),0,0,164,650],
                 [2550,521,0,random.randrange(-4,5,8),0,0,164,650],
                 [3450,352,0,random.randrange(-4,5,8),0,0,164,650],
                 [4350,524,0,random.randrange(-4,5,8),0,0,164,650],
                 [3214,500,random.randrange(-4,5,8),0,300,4400,0,0],
                 [1243,500,random.randrange(-4,5,8),0,300,4400,0,0],                 
                 [4224,350,random.randrange(-4,5,8),0,300,4400,0,0],
                 [2431,350,random.randrange(-4,5,8),0,300,4400,0,0]
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd4Block.png")).convert()
        
        # Set a list to contain the position of enemy
        trap_list = []
        for i in range (30):
            # Create the enemy's position randomly
            temp_list=[]
            value=random.randrange(600,self.level_limit-600)
            temp_list.append(value)
            value=random.randrange(100,700)
            temp_list.append(value)
            temp_list.append(3)
            trap_list.append(temp_list)
            
        # Create platforms
        for platform in level:
            
            # Create stable platforms
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create moving platforms
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)
                
        # Create enemies
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            self.enemy_list.add(traps)
            traps.image=pygame.image.load(os.path.join("picture","rd4_mini.png")).convert()
            traps.image.set_colorkey(WHITE)            
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen) 
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)        
class StLevel_12(Level):
    """ Definition for level 12 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd4bg2.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=5000
        
        # Create a list to contain the positions of all platforms
        level = [[0, 800],[300,800],
                 [600,800],[900,800],
                 [1200,800],[1500,800],
                 [1800,800],[2100,800],
                 [2400,800],[2700,800],
                 [3000,800],[3300,800],
                 [3600,800],[3900,800],
                 [4200,800],[4500,800],
                 [4800,800],
                 [300,650],[600,500],[900,350],[1500,200],[1800,350],[2100,500],
                 [2700,500],[3000,350],[3300,200],[3900,350],[4200,500],[4500,650],
                 [1200,575,15,0,300,4500,0,0],
                 [1200,425,15,0,300,4500,0,0],                 
                 [1200,275,15,0,300,4500,0,0],
                 [2400,575,15,0,300,4500,0,0],
                 [2400,425,15,0,300,4500,0,0],                 
                 [2400,275,15,0,300,4500,0,0],     
                 [3600,575,15,0,300,4500,0,0],
                 [3600,425,15,0,300,4500,0,0],                 
                 [3600,275,15,0,300,4500,0,0],                                       
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd4Block.png")).convert()
        
        # Set a list to contain the position of enemy
        trap_list = []
        for i in range (40):
            # Create the enemy's position randomly
            temp_list=[]
            value=random.randrange(600,self.level_limit-600)
            temp_list.append(value)
            value=random.randrange(100,700)
            temp_list.append(value)
            temp_list.append(3)
            trap_list.append(temp_list)   
            
        # Create platforms
        for platform in level:
            # Create stable platforms
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create moving platforms    
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)  
                
        # Create enemies
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            self.enemy_list.add(traps)
            traps.image=pygame.image.load(os.path.join("picture","rd4_mini.png")).convert()
            traps.image.set_colorkey(WHITE)            
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen)
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)        
class StLevel_13(Level):
    """ Definition for level 13 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd4bg3.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=2500
        
        # Create a list to contain the positions of all platforms
        level = [[0, 800],[300,800],
                 [600,800],[900,800],
                 [1200,800],[1500,800],
                 [1800,800],[2100,800],
                 [2400,800],
                 [0,575,3,0,0,2200,0,0],
                 [400,425,3,0,0,2200,0,0],                 
                 [800,275,3,0,0,2200,0,0],
                 [1200,575,3,0,0,2200,0,0],
                 [1600,425,3,0,0,2200,0,0],                 
                 [2000,275,3,0,0,2200,0,0],
                 [375,650,0,3,0,0,575,760],  
                 [875,650,0,3,0,0,575,760], 
                 [1375,650,0,3,0,0,575,760], 
                 [1875,650,0,3,0,0,575,760], 
                 [375,100,0,3,0,0,0,275],  
                 [875,100,0,3,0,0,0,275],  
                 [1375,100,0,3,0,0,0,275],  
                 [1875,100,0,3,0,0,0,275],  
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd4Block.png")).convert()
        
        # Create platforms
        for platform in level:
            # Create stable platforms
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create moving platforms
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block) 
                
        # Create boss  
        boss = Boss_4()
        self.boss_list.add(boss)           
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen)
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen) 
        self.hp_bar_group.draw(screen)
class StLevel_14(Level):
    
    """ Definition for level 14 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd5bg1.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=10000
        
        # Create a list to contain the positions of all platforms
        level = [[0, 800],[300,800],
                 [600,800],[900,800],
                 [1200,800],[1500,800],
                 [1800,800],[2100,800],
                 [2400,800],[2700,800],
                 [3000,800],[3300,800],
                 [3600,800],[3900,800],
                 [4200,800],[4500,800],
                 [4800,800],
                 [5100, 800],[5400,800],
                 [5700,800],[6000,800],
                 [6300,800],[6600,800],
                 [6900,800],[7200,800],
                 [7500,800],[7800,800],
                 [8100,800],[8400,800],
                 [8700,800],[9000,800],
                 [9300,800],[9600,800],
                 [9900,800],
                 [0, 640],
                 [600,640],[900,640],
                 [1500,640],
                 [1800,640],
                 [2400,640],[2700,640],
                 [3300,640],
                 [3600,640],
                 [4200,640],[4500,640],
                 [5100, 640],[5400,640],
                 [6000,640],
                 [6300,640],
                 [6900,640],[7200,640],
                 [7800,640],
                 [8100,640],
                 [8700,640],[9000,640],
                 [9600,640],
                 [9900,640],          
                 [0, 480],
                 [600,480],[900,480],
                 [1500,480],
                 [1800,480],
                 [2400,480],[2700,480],
                 [3300,480],
                 [3600,480],
                 [4200,480],[4500,480],
                 [5100, 480],[5400,480],
                 [6000,480],
                 [6300,480],
                 [6900,480],[7200,480],
                 [7800,480],
                 [8100,480],
                 [8700,480],[9000,480],
                 [9600,480],
                 [9900,480],         
                 [0, 320],
                 [600,320],[900,320],
                 [1500,320],
                 [1800,320],
                 [2400,320],[2700,320],
                 [3300,320],
                 [3600,320],
                 [4200,320],[4500,320],
                 [5100, 320],[5400,320],
                 [6000,320],
                 [6300,320],
                 [6900,320],[7200,320],
                 [7800,320],
                 [8100,320],
                 [8700,320],[9000,320],
                 [9600,320],
                 [9900,320],       
                 [0, 160],
                 [600,160],[900,160],
                 [1500,160],
                 [1800,160],
                 [2400,160],[2700,160],
                 [3300,160],
                 [3600,160],
                 [4200,160],[4500,160],
                 [5100, 160],[5400,160],
                 [6000,160],
                 [6300,160],
                 [6900,160],[7200,160],
                 [7800,160],
                 [8100,160],
                 [8700,160],[9000,160],
                 [9600,160],
                 [9900,160],
                 
                 [894,780,0],[1794,780,0],
                 [3594,780,0],
                 [4494,780,0],[5394,780,0],
                 [6294,780,0],[7194,780,0],
                 [8094,780,0],
                 [9894,780,0],       
                 
                 [894,620,0],[1794,620,0],
                 [2694,620,0],
                 [4494,620,0],[5394,620,0],
                 [6294,620,0],[7194,620,0],
                 [8094,620,0],[8994,620,0],
                 
                 
                 [1794,460,0],
                 [2694,460,0],[3594,460,0],
                 [4494,460,0],[5394,460,0],
                 [7194,460,0],
                 [8094,460,0],[8994,460,0],
                 [9894,460,0],          
                 
                 [894,300,0],
                 [2694,300,0],[3594,300,0],
                 [4494,300,0],
                 [6294,300,0],[7194,300,0],
                 [8994,300,0],
                 [9894,300,0],         
                 
                 [894,140,0],[1794,140,0],
                 [2694,140,0],[3594,140,0],
                 [5394,140,0],
                 [6294,140,0],
                 [8094,140,0],[8994,140,0],
                 [9894,140,0],  
                 
                 [300,575,0,5,0,0,70,770],
                 [1200,432,0,5,0,0,70,770],
                 [2100,543,0,5,0,0,70,770],
                 [3000,234,0,5,0,0,70,770],
                 [3900,123,0,5,0,0,70,770],
                 [4800,512,0,5,0,0,70,770],
                 [5700,423,0,5,0,0,70,770],
                 [6600,543,0,5,0,0,70,770],
                 [7500,654,0,5,0,0,70,770],
                 [8400,123,0,5,0,0,70,770],
                 [9300,423,0,5,0,0,70,770],
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd5Block.png")).convert()
        self.level_image2=pygame.image.load(os.path.join("picture","rd5Block1.png")).convert()
        
        # Set a list to contain the position of enemy
        trap_list = []
        for i in range (100):
            # Create the enemy's position randomly
            temp_list=[]
            value=random.randrange(600,self.level_limit-600)
            temp_list.append(value)
            value=random.randrange(100,700)
            temp_list.append(value)
            temp_list.append(random.randrange(1,4))
            trap_list.append(temp_list)  
            
        # Create platforms
        for platform in level:
            # Create stable platforms horizontally
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create stable platforms vertically
            if len(platform) == 3:
                block = Platform(self.level_image2)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create moving platforms
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block) 
                
        # Create enemies
        for trap in trap_list:
            traps = Trap( trap[0],trap[1],trap[2])
            self.enemy_list.add(traps) 
            traps.image=pygame.image.load(os.path.join("picture","rd5_mini.png")).convert()
            traps.image.set_colorkey(WHITE)             
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen) 
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)        
class StLevel_15(Level):
    """ Definition for level 15 in story mode """
    def __init__(self,player):
        # Set the background image
        self.background_image = pygame.image.load(os.path.join("picture","rd5bg2.jpg")).convert()
        
        # Call the parent's constructor
        Level.__init__(self,player)
        
        # Set the level limit
        self.level_limit=2500
        
        # Create a list to contain the positions of all platforms
        level = [[0, 800],[300,800],
                 [600,800],[900,800],
                 [1200,800],[1500,800],
                 [1800,800],[2100,800],
                 [2400,800],
                 [0,200],[300,350],[600,500],
                 [2500,200],[2200,200],[1900,350],[1600,500],
                 [950,650],[1250,650],
                 [800,725],[1400,725],
                 [900,350],[1300,350],
                 [1254,405,0],
                 [1094,780,0],
                 [1394,780,0],
                 [1194,780,0],
                 [1294,780,0],
                 ]
        
        # Set the image for platforms
        self.level_image=pygame.image.load(os.path.join("picture","rd5Block.png")).convert()
        self.level_image2=pygame.image.load(os.path.join("picture","rd5Block1.png")).convert()
        
        # Create platforms
        for platform in level:
            # Create stable platforms horizontally
            if len(platform) == 2:
                block = Platform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create stable platforms vertically
            if len(platform) == 3:
                block = Platform(self.level_image2)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.player = self.player
                self.platform_list.add(block)
                
            # Create moving platforms
            if len(platform) == 8:
                block = MovingPlatform(self.level_image)
                block.rect.left = platform[0]
                block.rect.bottom = platform[1]
                block.change_x = platform[2]
                block.change_y = platform[3]
                block.boundary_left = platform[4]
                block.boundary_right = platform[5]
                block.boundary_top = platform[6]
                block.boundary_bottom = platform[7]
                block.level=self
                block.player = self.player
                self.platform_list.add(block)          
        #Create boss       
        boss=Boss_5()
        self.boss_list.add(boss)
    def draw(self,screen):
        # Blit all the sprites to the screen
        screen.blit(self.background_image, [0,0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.boss_list.draw(screen) 
        self.special_list.draw(screen) 
        self.hp_bar_group_player.draw(screen)
        self.hp_bar_group_ammo.draw(screen)
        self.hp_bar_group.draw(screen)

        
    

class Machine_Gun(pygame.sprite.Sprite):
    """ A class to create the pistol """
    def __init__(self):
        # Call the parent's constructor
        super().__init__()
        
        # Set the image for bullets
        self.image = pygame.image.load(os.path.join("picture","pistol_bullet.png")).convert()
        self.image.set_colorkey(BLACK)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        
        # Set the inital angle
        self.angle = 0
        
        # Set the inital speed
        self.speed=0.35
        
        # Set the initial velocity 
        self.change_y=0
        self.change_x=0
        
        # Set the varibles to calculate the total distance of moving
        self.difference_x=0
        self.difference_y=0
        
        # The varibles to chech if the gun is warmed up
        self.heat=0
        self.heat_change=0
        
        # The total distance of bullets flying
        self.distance = 0
        
        # The damage of each bullet
        self.dmg = 2
        
        # The "Trigger"
        self.firing=False
        
        # Amount of ammo
        self.ammo = 80
        
    def update(self):
        """ Move the bullets and make the damage occur"""
        # Warm up the gun
        self.heat+=self.heat_change
        
        # Move the bullets
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y
        
        # If the gun is warmed up, shoot the bullets
        if (self.heat>=2) and (self.firing == False):
            # Pull the trigger, BOOOMMMMMMMMMMMMMM!!
            self.firing=True
            
            # Calculate the velocity and angle of the bullets
            self.difference_y =  aim.rect.y + 72 - self.rect.y 
            self.difference_x =  aim.rect.x + 100 - self.rect.x
            if self.difference_y>0 and self.difference_x<0:
                self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_y<=0 and self.difference_x<0:
                self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_x==0 and self.difference_y<=0:
                self.angle=math.radians(-90)
            elif self.difference_x==0 and self.difference_y>0:
                self.angle=math.radians(90)
            else:
                self.angle=math.atan(self.difference_y/self.difference_x)

            self.change_x=float(self.speed*math.degrees(math.cos(self.angle)))
            self.change_y=float(self.speed*math.degrees(math.sin(self.angle))) 
            
        # Set the position of the bullet to fit the gun's position
        elif self.firing == False:
            if gun_image.faceFront==True:
                self.rect.left=gun_image.rect.left
            if gun_image.faceFront==False:
                self.rect.right=gun_image.rect.right            
            self.rect.y=gun_image.rect.y      
        
        
            
        # Check the collision with other sprites    
        for bullet in machine_gun_list:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, current_level.enemy_list , False)
            block_hit_list = pygame.sprite.spritecollide(bullet, player.level.platform_list,False)
            boss_hit_list =  pygame.sprite.spritecollide(bullet, current_level.boss_list , False)
            
            # If it hits enemy, remove the enemy
            if len(enemy_hit_list) > 0:
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet) 
                sound1 = pygame.mixer.Sound(os.path.join("music","shot.wav"))
                sound1.play()
                for trap in enemy_hit_list:
                    current_level.enemy_list.remove(trap)
                    all_sprite_list.remove(trap)
                    
                player.hit_num += len(enemy_hit_list)
                
            # If it hits platform, remove itself
            if len(block_hit_list) > 0 :
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet) 
            
            # If it hits boss, remove boss's hp   
            if len(boss_hit_list) > 0:
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet)
                for boss in current_level.boss_list:
                    if boss.hp >= 2:
                        boss.hp -= self.dmg
                    if boss.hp <2:
                        boss.hp = 0
                        
                    if boss.hp == 0:
                        current_level.boss_list.remove(boss)
                        
                    for hp1 in current_level.hp_bar_group:
                        hp1_length = hp1.length
                        hp1_length =  600 * boss.hp /200
                        hp1.length = hp1_length
                        
    
    def check_firing(self):
        # Begin to warm up
        self.heat_change=1
    
    


    
class Machine_Gun2(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent's constructor
        super().__init__()
        
        # Set the image for bullets
        self.image = pygame.image.load(os.path.join("picture","machine_gun_bullet.png")).convert()
        self.image.set_colorkey(BLACK)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        
        # Set the inital angle
        self.angle = 0
        
        # Set the inital speed
        self.speed=0.35
        
        # Set the initial velocity 
        self.change_x=0
        self.change_y=0
        
        # Set the varibles to calculate the total distance of moving
        self.difference_x=0
        self.difference_y=0
        
        # The varibles to chech if the gun is warmed up
        self.heat=0
        self.heat_change=0
        
        # The total distance of bullets flying
        self.distance = 0
        
        # The damage of each bullet
        self.dmg = 4
        
        # The "Trigger"
        self.firing=False
        
        # Amount of ammo
        self.ammo = 30
    def update(self):
        """ Move the bullets and make the damage occur"""
        # Warm up the gun
        self.heat+=self.heat_change
        
        # Move the bullets
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y
        
        # If the gun is warmed up, shoot the bullets
        if (self.heat>=60) and (self.firing == False):
            # Pull the trigger, BOOOMMMMMMMMMMMMMM!!
            self.firing=True
            
            # Calculate the velocity and angle of the bullets
            self.difference_y =  aim.rect.y + 72 - self.rect.y 
            self.difference_x =  aim.rect.x + 100 - self.rect.x
            if self.difference_y>0 and self.difference_x<0:
                self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_y<=0 and self.difference_x<0:
                self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_x==0 and self.difference_y<=0:
                self.angle=math.radians(-90)
            elif self.difference_x==0 and self.difference_y>0:
                self.angle=math.radians(90)
            else:
                self.angle=math.atan(self.difference_y/self.difference_x)

            self.change_x=float(self.speed*math.degrees(math.cos(self.angle)))
            self.change_y=float(self.speed*math.degrees(math.sin(self.angle))) 
            
        # Set the position of the bullet to fit the gun's position
        elif self.firing == False:
            if gun_image.faceFront==True:
                self.rect.left=gun_image.rect.left
            if gun_image.faceFront==False:
                self.rect.right=gun_image.rect.right            
            self.rect.y=gun_image.rect.y      
        
        
            
        # Check the collision with other sprites    
        for bullet in machine_gun_list:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, current_level.enemy_list , False)
            block_hit_list = pygame.sprite.spritecollide(bullet, player.level.platform_list,False)
            boss_hit_list =  pygame.sprite.spritecollide(bullet, current_level.boss_list , False)
            
            # If it hits enemy, remove the enemy
            if len(enemy_hit_list) > 0:
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet) 
                sound1 = pygame.mixer.Sound(os.path.join("music","shot.wav"))
                sound1.play()
                for trap in enemy_hit_list:
                    current_level.enemy_list.remove(trap)
                    all_sprite_list.remove(trap)
                    
                player.hit_num += len(enemy_hit_list)
                
            # If it hits platform, remove itself
            if len(block_hit_list) > 0 :
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet) 
            
            # If it hits boss, remove boss's hp   
            if len(boss_hit_list) > 0:
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet)
                for boss in current_level.boss_list:
                    if boss.hp >= 4:
                        boss.hp -= self.dmg
                    if boss.hp < 4:
                        boss.hp = 0
                        
                    if boss.hp == 0:
                        current_level.boss_list.remove(boss)
                        
                    for hp1 in current_level.hp_bar_group:
                        hp1_length = hp1.length
                        hp1_length =  600 * boss.hp /200
                        hp1.length = hp1_length
                
               
        
                
    def check_firing(self):
        # Begin to warm up
        self.heat_change=1
class Machine_Gun3(pygame.sprite.Sprite):
    """ A class to create the shot gun"""
    def __init__(self,ang):
        
        # Call parent's constructor
        super().__init__()
        
        # Set the image for bullets
        self.image = pygame.image.load(os.path.join("picture","shot_gun_bullet.png")).convert()
        self.image.set_colorkey(BLACK)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set the inital angle
        self.angle = 0
        
        # Set the inital speed
        self.speed=0.35
        
        # Set the initial velocity 
        self.change_x=0
        self.change_y=0
        
        # Set the varibles to calculate the total distance of moving
        self.difference_x=0
        self.difference_y=0
        
        # The varibles to chech if the gun is warmed up
        self.heat=0
        self.heat_change=0
        
        # The total distance of bullets flying
        self.distance = 0
        
        # The damage of each bullet
        self.dmg = 3
        
        # The "Trigger"
        self.firing=False
        
        # Amount of ammo
        self.ammo = 30
        
        # Set the angle change
        self.angle_change=ang
    def update(self):
        """ Warm up the gun and shoot the bullet """
        # Warm up
        self.heat+=self.heat_change
        
        # Move the bullet
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y
        
        # If warmed up, shoot the bullet
        if (self.heat>=2) and (self.firing == False):
            self.firing=True
            self.difference_y =  aim.rect.y + 72 - self.rect.y 
            self.difference_x =  aim.rect.x + 100 - self.rect.x
            if self.difference_y>0 and self.difference_x<0:
                self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_y<=0 and self.difference_x<0:
                self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_x==0 and self.difference_y<=0:
                self.angle=math.radians(-90)
            elif self.difference_x==0 and self.difference_y>0:
                self.angle=math.radians(90)
            else:
                self.angle=math.atan(self.difference_y/self.difference_x)

            self.change_x=float(self.speed*math.degrees(math.cos(self.angle+math.radians(self.angle_change))))
            self.change_y=float(self.speed*math.degrees(math.sin(self.angle+math.radians(self.angle_change))))
        
        # Change the facing direction
        elif self.firing == False:
            if gun_image.faceFront==True:
                self.rect.left=gun_image.rect.left
            if gun_image.faceFront==False:
                self.rect.right=gun_image.rect.right            
            self.rect.y=gun_image.rect.y      
        
        
            
        # If we hit something    
        for bullet in machine_gun_list:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, current_level.enemy_list , False)
            block_hit_list = pygame.sprite.spritecollide(bullet, player.level.platform_list,False)
            boss_hit_list =  pygame.sprite.spritecollide(bullet, current_level.boss_list , False)
            
            # Hit enemy, kill them
            if len(enemy_hit_list) > 0:
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet) 
                sound1 = pygame.mixer.Sound(os.path.join("music","shot.wav"))
                sound1.play()
                for trap in enemy_hit_list:
                    current_level.enemy_list.remove(trap)
                    all_sprite_list.remove(trap)
                # Count for the number of enemy which being killed    
                player.hit_num += len(enemy_hit_list)
                
            # Hit platforms, remove the bullets
            if len(block_hit_list) > 0 :
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet) 
            
            # Hit the boss, damage it   
            if len(boss_hit_list) > 0:
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet)
                for boss in current_level.boss_list:
                    if boss.hp >= 1:
                        boss.hp -= self.dmg
                    if boss.hp <1:
                        boss.hp = 0
                    
                    if boss.hp == 0:
                        current_level.boss_list.remove(boss)
                        
                for hp1 in current_level.hp_bar_group:
                    hp1_length = hp1.length
                    hp1_length =  600 * boss.hp /200
                    hp1.length = hp1_length
    def check_firing(self):
        # Begin to warm up
        self.heat_change=1
class Machine_Gun4(pygame.sprite.Sprite):
    """ A class to create the rocket launcher"""
    def __init__(self):
        # Call parent's constructor
        super().__init__()
        
        # Set the image for bullets
        self.image = pygame.image.load(os.path.join("picture","Rocket.png")).convert()
        self.image.set_colorkey(BLACK)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set the inital angle
        self.angle = 0
        
        # Set the inital speed
        self.speed=0.35
        
        # Set the initial velocity 
        self.change_x=0
        self.change_y=0
        
        # Set the varibles to calculate the total distance of moving
        self.difference_x=0
        self.difference_y=0
        
        # The varibles to chech if the gun is warmed up
        self.heat=0
        self.heat_change=0
        
        # The total distance of bullets flying
        self.distance = 0
        
        # The "Trigger"
        self.firing=False
        
        # Amount of ammo
        self.ammo = 12
        
        # Set the initial gravity
        self.grav=0
        
        # The varible to determine if the missle need to turn
        self.turn=False
    def update(self):
        """ Heat the gun and move the bullets"""
        
        # Warm up the gun
        self.heat+=self.heat_change
        
        # Move the rockets with gravity
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y
        self.change_y+=self.grav
        
        # if the launcher is warmed up, pulled the trigger
        if (self.heat>=2) and (self.firing == False):
            # Pull the trigger
            self.firing=True
            
            # Calculate the angle and velocity
            self.difference_y =  aim.rect.y + 72 - self.rect.y 
            self.difference_x =  aim.rect.x + 100 - self.rect.x
            if self.difference_y>0 and self.difference_x<0:
                self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_y<=0 and self.difference_x<0:
                self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_x==0 and self.difference_y<=0:
                self.angle=math.radians(-90)
            elif self.difference_x==0 and self.difference_y>0:
                self.angle=math.radians(90)
            else:
                self.angle=math.atan(self.difference_y/self.difference_x)

            self.change_x=float(self.speed*math.degrees(math.cos(self.angle)))
            self.change_y=float(self.speed*math.degrees(math.sin(self.angle)))
            self.grav=.5
            
        # Check to flip the rocket
        if self.change_x<0 and self.turn==False:
            self.image=pygame.transform.flip(self.image,True,False)
            self.turn=True
        # Reset the image's facing direction 
        elif self.firing == False:
            if gun_image.faceFront==True:
                self.rect.left=gun_image.rect.left
            if gun_image.faceFront==False:
                self.rect.right=gun_image.rect.right            
            self.rect.y=gun_image.rect.y      
 
        # Check the collision with other sprites
        enemy_hit_list = pygame.sprite.spritecollide(self, current_level.enemy_list , True)
        boss_hit_list =  pygame.sprite.spritecollide(self, current_level.boss_list , False)
        block_hit_list = pygame.sprite.spritecollide(self, player.level.platform_list,False)
        
        # If collide with enemy, exploid
        if len(enemy_hit_list) > 0:
            machine_gun_list.remove(self)
            all_sprite_list.remove(self) 
            explosion=Rocket_expolosion(self.rect.x,self.rect.y)
            machine_gun_list.add(explosion)
            all_sprite_list.add(explosion)
            
        # If collide with boss, exploid
        if len(boss_hit_list) > 0:
            machine_gun_list.remove(self)
            all_sprite_list.remove(self)
            explosion = Rocket_expolosion(self.rect.x,self.rect.y)
            machine_gun_list.add(explosion)
            all_sprite_list.add(explosion)
            
        # If collide with platforms, exploid        
        if len(block_hit_list) > 0 :
            machine_gun_list.remove(self)
            all_sprite_list.remove(self)  
            explosion=Rocket_expolosion(self.rect.x,self.rect.y)
            machine_gun_list.add(explosion)
            all_sprite_list.add(explosion)               
            
               
        
                
    def check_firing(self):
        # Begin to warm up
        self.heat_change=1
                
               
class Rocket_expolosion(pygame.sprite.Sprite):
    """ The expolosion of rocket after the collision with other sprites """
    def __init__ (self,pos_x,pos_y):
        # Call parent's constructor    
        super().__init__()
        
        # Set the original image
        self.ori_image = pygame.image.load(os.path.join("picture","Rocket_explosion.png")).convert()
        # Set the transparent image
        self.ori_image.set_colorkey(BLACK)
        
        # Set the size of the image
        self.width=10
        self.height=10
        self.image=pygame.transform.scale(self.ori_image,(self.width,self.height))
        
        # Set the initial speed for becoming bigger
        self.speed=20
        
        # Set a referance to the image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.po_x=pos_x
        self.po_y=pos_y
        
        # Set the velocity which to keep the picture from moving left or right
        self.rect_change_x=0
        self.rect_change_y=0
        
        # Set the damage each frame
        self.dmg=1.5
        
        # Trigger
        self.firing=True
        
        # Sound of explosion
        sound1 = pygame.mixer.Sound(os.path.join("music","explode.wav"))
        sound1.play()         
    def update(self):
        """ Change the size of the image """
        # Change the width and height
        self.width+=self.speed
        self.height+=self.speed
        
        # adjust the position of the image
        self.rect_change_x-=(self.speed/2)
        self.rect_change_y-=(self.speed/2)
        
        # Change the size of image
        self.image=pygame.transform.scale(self.ori_image,(self.width,self.height))
        
        # Reset the reference to the image rect and position
        self.rect=self.image.get_rect()
        self.rect.x=self.po_x+self.rect_change_x
        self.rect.y=self.po_y+self.rect_change_y
        
        # Check if the explosion collide something
        for bullet in (machine_gun_list):
            enemy_hit_list = pygame.sprite.spritecollide(bullet, current_level.enemy_list , False)
            
            boss_hit_list =  pygame.sprite.spritecollide(bullet, current_level.boss_list , False)
            
            # if it hits the enemy, remove the enemy
            if len(enemy_hit_list) > 0:
                sound1 = pygame.mixer.Sound(os.path.join("music","creeper_die.wav"))
                sound1.play()
                for trap in enemy_hit_list:
                    current_level.enemy_list.remove(trap)
                    all_sprite_list.remove(trap)
                    
                player.hit_num += len(enemy_hit_list)
                
            # if it hits the boss, do damage to boss, kill the boss when the boss's hp is 0
            if len(boss_hit_list) > 0:
                for boss in current_level.boss_list:
                    if boss.hp >= 1:
                        boss.hp -= self.dmg
                    if boss.hp <1:
                        boss.hp = 0
                        
                    if boss.hp == 0:
                        current_level.boss_list.remove(boss)
                        
                    for hp1 in current_level.hp_bar_group:
                        hp1_length = hp1.length
                        hp1_length =  600 * boss.hp /200
                        hp1.length = hp1_length
                        
        # if the explosion is too big, remove the image
        if self.width>=300 or self.height>=300:
            machine_gun_list.remove(self)
            all_sprite_list.remove(self)  
class Crosshair(pygame.sprite.Sprite):
    """ A class to create the aim """    
    
    def __init__(self):
        # Call parent's constructor
        super().__init__()
        
        # Set the image for the aim
        self.image = pygame.image.load(os.path.join("picture","this.tif")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a refrence to the image rect
        self.rect = self.image.get_rect()
        
    def update(self):
        """ Move the aim """
        # Set the position of aim the same as the mouse's position
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - 100
        self.rect.y = pos[1] - 72
        pygame.mouse.set_visible(False)
        
class Text():
    """ A class to help programmer print text on screen conveniently"""
    def display(text, color,coord, size):
        # Set the font
        font = pygame.font.SysFont('times new roman', size, True, True) # bold, italicize
        
        # Blit on the screen
        display = font.render(text, True, color)
        screen.blit(display, coord)

""" Create 5 bosses """
class Boss_1(pygame.sprite.Sprite):
    """ Create the dragon boss """
    def __init__ (self):
        # Call parent's constructor
        super().__init__()
        
        # Set the image of the boss
        self.image = pygame.image.load(os.path.join("picture","black.png")).convert()
        self.image.set_colorkey(BLACK)
        
        # Set a reference to the image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        
        # Set the initial velocity
        self.change_x=0
        self.change_y=3
        self.speed=14
        
        # Set the initial angle
        self.angle=0
        
        # Set the hp of the boss
        self.hp=200
        self.hp1 = 200
        
        # Set the "trigger" for dashing
        self.dash=False
        
        # Set the timer for dashing
        self.dash_point=0
        
        # Set the cooldown for spells
        self.cooldown=0
        
        # Set the damage for collision with player
        self.dmg = 10
        
        # Set the facing direction and varibles for if it needs to turn
        self.faceFront=True
        self.turn=False        
    def update(self):
        """ manage the cd of spells and moving the boss"""
        # Make a timer for counting the cooling down time
        self.cooldown+=1
        
        # Set the facing direction
        if self.faceFront==True:
            if player.rect.x>=self.rect.x:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            if player.rect.x<self.rect.x:
                self.faceFront=True
                self.turn+=True 
                
        # If it need to turn, flip the image
        if self.turn==True:
            self.image=pygame.transform.flip(self.image,True,False)
            self.turn=False      
            
        # Set the horizontal velocity when not dashing    
        if not self.dash:
            if self.rect.x < player.rect.x:
                self.change_x=3
            else:
                self.change_x=-3
                
        # Move the boss
        self.rect.x+=self.change_x
      
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
            
            if self.change_x > 0:
                self.rect.right = item.rect.left
                
            elif self.change_x < 0:
                self.rect.left = item.rect.right 
         # Set the vertical velocity when not dashing
        if not self.dash:
            if self.rect.y>500:
                self.change_y=-3
            elif self.rect.y<10:
                self.change_y=3
                
        
        # When dashing, count the time
        if self.rect.top<=0:
            self.rect.top=0
            if self.dash:
                self.dash_point+=1
                
        if self.rect.bottom>=screen_y:
            self.rect.bottom=screen_y
            if self.dash:
                self.dash_point+=1            
 
        #Move the boss
        self.rect.y += self.change_y
        
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
                if self.dash:
                    self.dash_point+=1
            elif self.change_y < 0:
                self.rect.top = item.rect.bottom
                if self.dash:
                    self.dash_point+=1
                    
        # When it dash more than 30 frames, stop it
        if self.dash_point>=30:
            self.dash=False
            self.dash_point=0
        
        # After 2 secs, boss use a random spell
        if self.cooldown>=120:
            self.cooldown=0
        
            self.spell=random.randrange(3)
            if self.spell==0:
                self.dashing()    
            elif self.spell==1:
                self.magic_ball=Spell_magic_ball(self.rect.x, self.rect.y)
                current_level.enemy_list.add(self.magic_ball)
            elif self.spell==2:
                self.magic_burst=Spell_magic_burst()
                current_level.enemy_list.add(self.magic_burst)

    def dashing(self):
        """ A class to let boss to dash """
        
        # Pull the "Trigger"
        self.dash=True
        
        # Calculate the velocity and angle
        self.difference_y =  player.rect.y  - self.rect.y 
        self.difference_x =  player.rect.x  - self.rect.x
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)

        self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
        self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))   

class Spell_magic_ball(pygame.sprite.Sprite):
    """ Boss 1 first spell """
    def __init__(self,pos_x,pos_y):
        # Call parent's constructor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","MysBall.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a reference to image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the initial velocity and angle
        self.speed=15
        self.angle=0
        
        # Set the time to remove the ball which is very far
        self.time=0
        
        # Set the damage of the ball
        self.dmg = 2
        
        # Calculate the velocity
        self.difference_y =  player.rect.y  - self.rect.y 
        self.difference_x =  player.rect.x  - self.rect.x
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)

        self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
        self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))           
    def update(self):
        # Move the ball
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y      
        self.time+=1
        if self.rect.bottom<=0 or self.rect.top>=screen_y or self.time>=600:
            current_level.enemy_list.remove(self)
class Spell_magic_burst(pygame.sprite.Sprite):
    """ Boss 1 second spell """
    def __init__(self):
        # Call the parent's constructor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","MagicBurst1.jpg")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a reference to image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = -80
        
        # Set the vertical velocity
        self.change_y=25
        
        # Set the damage
        self.dmg = 2
    def update(self):
        
        # Move the sprite
        self.rect.y+=self.change_y
        
        # Check if we hit something
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        
        # If hit the platform
        # stop moving
        for item in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
            elif self.change_y < 0:
                self.rect.top = item.rect.bottom
            
            self.change_y = 0
        
        # Off screen check
        if self.rect.bottom>=screen_y:
            self.rect.bottom=screen_y
            self.change_y=0
            
        # exploid after stop moving
        if self.change_y==0:
            new_magic_burst=Spell_magic_burst1(self.rect.x-60, self.rect.y-28)
            current_level.enemy_list.add(new_magic_burst)
            current_level.enemy_list.remove(self)
            
class Spell_magic_burst1(pygame.sprite.Sprite):
    """ explosion after the second spell stop moving """
    def __init__(self, pos_x, pos_y):
        # Call the parent's constructor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","MagicBurst.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a reference to image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the lasting time
        self.lasting_time=60
        
        # Set the damage
        self.dmg = 2
    def update(self):
        # Remove after passing the lasting time
        
        self.lasting_time-=1
        if self.lasting_time<=0:
            current_level.enemy_list.remove(self)
            
class Boss_2(pygame.sprite.Sprite):
    """ The second boss, loli gunner """
    def __init__ (self):
        # Called the parent's constructor
        super().__init__()
        
        # Set the image of the gunner
        self.image = pygame.image.load(os.path.join("picture","loli_gunner.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a reference to image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 300
        
        # Set the initial velocity
        self.change_x=0
        self.change_y=0
        
        # Set the damage
        self.dmg = 10
        
        # Set the hp
        self.hp=200
        self.hp1 = 200
        
        # Set the cd timer
        self.cooldown=0
        
        # Set the facing direction and turn
        self.faceFront=False
        self.turn=False      
        
        # Set the gravity
        self.grav=.7
        
        # Set the cd for jumping
        self.rocket_jumping=False
        self.passive_cooldown=0
        
        # Set the trigger of firing
        self.startFiring=False
        
        # set the ammo and fire speed
        self.bullet=4
        self.fireRate=0
    def update(self):
        """ Move the boss and use the spells """
        # Calculate the gravity
        self.gravity()
        
        # Make a timer for spells' cooling down
        self.cooldown+=1
        self.fireRate+=1
        
        # Set the facing direction
        if self.faceFront==True:
            if player.rect.x>self.rect.x:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            if player.rect.x<=self.rect.x:
                self.faceFront=True
                self.turn+=True   
        if self.turn==True:
            self.image=pygame.transform.flip(self.image,True,False)
            self.turn=False      
            

        # Velocity if not jumping    
        if not self.rocket_jumping:
            if self.rect.x < player.rect.x:
                self.change_x=4
            else:
                self.change_x=-4
                
        # Move the boss
        self.rect.x+=self.change_x
      
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
            
            if self.change_x > 0:
                self.rect.right = item.rect.left
                
            elif self.change_x < 0:
                self.rect.left = item.rect.right   
                


        self.rect.y += self.change_y
        
        if self.rect.top<=0:
            self.rect.top=0
            self.rocket_jumping=False

                
        if self.rect.bottom>=screen_y:
            self.rect.bottom=screen_y
            self.rocket_jumping=False
    
 
        # Check if we hit anything, if hit, reset the position to the edge and stop moving
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
                self.rocket_jumping=False

            elif self.change_y < 0:
                self.rect.top = item.rect.bottom
                self.rocket_jumping=False
            self.change_y=0
            
        # Called the method to jump
        self.rocket_jump()
        
        # Begin shooting
        self.auto_gun_shoot()
        
        # Choose the way to shoot randomly
        if self.cooldown>=150:
            self.cooldown=0
        
            self.spell=random.randrange(2)
            if self.spell==0:
                self.startFiring=True
            elif self.spell==1:
                self.missile=Spell_missile(self.rect.x, self.rect.y)
                current_level.enemy_list.add(self.missile)




    def rocket_jump(self):
        """ A method for jumping """
        # If the boss is near the player and cd is ready, jump
        if self.rect.x <= player.rect.x+400 and self.rect.x >= player.rect.x+300 and self.rocket_jumping==False and self.passive_cooldown>=60:
            self.jump()
            self.change_x*=3
            self.rocket_jumping=True
            self.length=self.rect.x-player.rect.x
        if self.rect.x >= player.rect.x-400 and self.rect.x <= player.rect.x-300 and self.rocket_jumping==False and self.passive_cooldown>=60:
            self.jump()     
            self.change_x*=3
            self.rocket_jumping=True
            self.length=self.rect.x-player.rect.x
            
        # After jumping ,reset the cds
        if self.rocket_jumping==True:

            self.length+=self.change_x

            if self.change_x<0:
                if self.length<=0:
                    self.passive_cooldown=0
                    self.change_x=0
                    
            elif self.change_x>0:
                if self.length>=0:
                    self.passive_cooldown=0
                    self.change_x=0
        # After jumping ,reset the calculation of distance and begin to count the cd again           
        if not self.rocket_jumping:
            self.length=0
            self.passive_cooldown+=1
    def auto_gun_shoot(self):
        """ A method to shoot the auto gun """
        
        # Begin to shoot
        if self.startFiring==True:
            if self.bullet>0:
                if self.fireRate % 5==0:
                    self.auto_gun_bullet=Spell_auto_gun(self.rect.x,self.rect.y)
                    current_level.enemy_list.add(self.auto_gun_bullet)
                    self.bullet-=1
                    
        # Reload when no bullet in ammo
        if self.bullet<=0:
            self.startFiring=False
            self.bullet=4
        
    def gravity(self):
        """ Calculate the gravity """    
        if self.change_y == 0:
                
            self.change_y = 1
                
        else:
            self.change_y +=self.grav
 
            
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    def jump(self):
        """ Called to let the boss jump """
        self.change_y = -20     
class Spell_auto_gun(pygame.sprite.Sprite):
    """ The gun of the boss """
    def __init__(self,pos_x,pos_y):
        # Call the parent's constructor
        super().__init__()
        
        # Set the image for the bullet
        width = 8
        height = 5
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        
        # Set a reference to the image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the initial speed and angle
        self.speed=17
        self.angle=0
        
        # Set the time for cd 
        self.time=0
        
        # Set the damage
        self.dmg = 2
        
        # Set the velocity of the bullet
        self.difference_y =  player.rect.y  - self.rect.y 
        self.difference_x =  player.rect.x  - self.rect.x
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)

        self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
        self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))           
    def update(self):
        """ Move the bullets"""
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y
        
        # Calculate the cd for shooting
        self.time+=1
        if self.rect.bottom<=0 or self.rect.top>=screen_y or self.time>=600:
            current_level.enemy_list.remove(self)
class Spell_missile(pygame.sprite.Sprite):
    """ Make the boss to shoot missiles """
    def __init__(self, pos_x,pos_y):
        # Call the parent's constructor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","missile.png")).convert()
        self.ori_image = pygame.image.load(os.path.join("picture","missile.png")).convert()
        self.image.set_colorkey(WHITE)
        self.ori_image.set_colorkey(WHITE)
        
        # Set a reference to the image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the velocity
        self.change_x=0
        self.change_y=0
        self.speed=10
        
        # Set the damage
        self.dmg = 2
        
        # Set the initial angle
        self.angle=0
        
        # Set the cd and lasting time
        self.time=10
        self.lasting_time=0
        
        # Set the facing direction
        self.faceFront=True
        self.turn=False              
    def update(self):
        """ Move the missiles """
        
        # Change the facing direction
        if self.faceFront==True:
            if player.rect.x>=self.rect.x:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            if player.rect.x<self.rect.x:
                self.faceFront=True
                self.turn+=True   
        if self.turn==True:
            self.ori_image=pygame.transform.flip(self.ori_image,True,False)
            self.image=self.ori_image
            self.turn=False              
        # if cd is ready, shoot the missile
        if self.time>=10:
            # Calculate the velocity
            self.difference_y =  player.rect.y  - self.rect.y 
            self.difference_x =  player.rect.x  - self.rect.x
            if self.difference_y>0 and self.difference_x<0:
                self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_y<=0 and self.difference_x<0:
                self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
            elif self.difference_x==0 and self.difference_y<=0:
                self.angle=math.radians(-90)
            elif self.difference_x==0 and self.difference_y>0:
                self.angle=math.radians(90)
            else:
                self.angle=math.atan(self.difference_y/self.difference_x)
    
            self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
            self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))  
            if self.difference_y>0 and self.difference_x<0:
                self.angle=math.pi-self.angle
            elif self.difference_y<=0 and self.difference_x<0:
                self.angle=-1*math.pi-self.angle   
            else:
                self.angle*=-1
                
            # Rotate the image
            self.image=pygame.transform.rotate(self.ori_image,math.degrees(self.angle))
            
            # Reset the cd
            self.time=0
        # Count the cd time
        self.time+=1
        
        # Move the missiles
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y  
        
        # Check if hits,if hits, remove after 10 frames
        self.hit=pygame.sprite.collide_rect(self,player)
        if self.hit==True:
            self.lasting_time+=1
        if self.lasting_time>=10:
            current_level.enemy_list.remove(self)        

 
    
    
    
class hp_bar(pygame.sprite.Sprite):
    """ A class to make all the bars to show the amount left """
    def __init__(self,length,width,pos_x,pos_y):
        # Call parent's constructor
        super().__init__()
        
        # set the length and width of the bar
        self.length = length
        self.width = width
        self.length1 = length 
        
        # Set the image of the bar
        self.image = pygame.Surface([self.length,self.width])
        # Set a reference to the image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        

    def update(self):
        """ change colour when hp is too low """
        
        self.image = pygame.Surface([self.length,self.width])
         
        hp_percentage = self.length/self.length1
        if hp_percentage >= .5:
            self.image.fill(GREEN)
        elif hp_percentage <.5 and hp_percentage>=.2:
            self.image.fill(ORANGE)
        elif hp_percentage >0 and hp_percentage <.2:
            self.image.fill(RED)

        
    
class Dialogue():
    """ Stop everything and print things on the screen """
       
    def display1(text):
        done = False
        x = 0
        y = 0
        t = 0
        screen.fill(WHITE)
        

        text = str(text)  
        
        for i in text:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
            Text.display(i, RED, [x,y], 20)
            x += 20
            if x > 980:
                x = 0
                y += 40

            pygame.display.update()
            clock.tick(30)
        Text.display("Press enter to proceed", GREEN, [200,600], 40)
        pygame.display.update()
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True    
                
                    
    
                
            
class End_screen():
    """ To make the normal end screen for survival and challenge modes"""
    def display():
        # Clear everything
        screen.fill(WHITE)
        
        # Blit the image
        screen.blit(end_image, [0,0])
        
        # Print information about scores
        Text.display("Your Score: " + str(current_pos - 90 + player.hit_num*500 + player.gold_num * 100  ), ORANGE, [200,400], 48) # 500 points for each creeper hit
        Text.display("Defeated " + str(player.hit_num) + " creepers", ORANGE, [200, 470], 48)
        Text.display("Collected " + str(player.gold_num) + " coins", ORANGE, [200, 540], 48)
        
class End_screen_stmode():
    """ Create the end screen for story mode """
    def display():
        screen.fill(WHITE)
        screen.blit(dead_end_image, [-125,0])   
        
class End_screen_stmode1():
    def display():
        screen.fill(WHITE)
        screen.blit(good_end_image, [0,0])

class SpriteSheet(object):
    """ Catch the small image from sprite sheet """
 
    def __init__(self, file_name):
        # Set the sprite sheet
        self.sprite_sheet = pygame.image.load(os.path.join("picture",file_name)).convert()

    def get_image(self, x, y, width, height):
        # Get the small image from it
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(WHITE)
        return image
    
class coin(pygame.sprite.Sprite):
    """ Create the coin in Survival mode """
    def __init__(self,pos_x,pos_y):
        # Call the parent's constructor
        super().__init__()
        
        
        # Count the time for the changing pictures
        self.frame = 0
        self.frame1 = 0
        
        # Change picture rate
        self.frame_change = 1
        
        # Fill the list with the small images from sprite sheet
        self.coin_sprite_list = []
        self.sheet = SpriteSheet("coin_sprite.png")
        
        image = self.sheet.get_image(0,0,30,30)
        self.coin_sprite_list.append(image)
        
        image = self.sheet.get_image(33,0,22,30)
        self.coin_sprite_list.append(image)

        image = self.sheet.get_image(67,0,16,30)
        self.coin_sprite_list.append(image)        

        image = self.sheet.get_image(99,0,11,30)
        self.coin_sprite_list.append(image)        

        image = self.sheet.get_image(131,0,8,30)
        self.coin_sprite_list.append(image)        

        image = self.sheet.get_image(159,0,11,30)
        self.coin_sprite_list.append(image)        

        image = self.sheet.get_image(186,0,16,30)
        self.coin_sprite_list.append(image) 

        image = self.sheet.get_image(213,0,23,30)     
        self.coin_sprite_list.append(image)         

        image = self.sheet.get_image(241,0,27,30)             
        self.coin_sprite_list.append(image)
        
        image = self.sheet.get_image(270,0,30,30)                
        self.coin_sprite_list.append(image)
        
        # Set a reference to the image rect and position
        self.image = self.coin_sprite_list [0]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x 
        self.rect.y = pos_y

    def update(self):
        """ Change the pictures to make it look like an animation """
        
        #Count as a timer
        self.frame1 += 1
        
        # Change picture once eight frames
        if self.frame1 % 8 == 0:
            if self.frame >= 0:
                self.frame += self.frame_change
                self.image = self.coin_sprite_list [self.frame]
            
            if self.frame == 9:
                self.frame = 0
                
                self.image = self.coin_sprite_list [self.frame]
            
            if self.frame >= 0 and self.frame < 6:
                self.rect.x += 1.5       
                
            if self.frame >= 6 and self.frame <= 9:
                self.rect.x -= 1.5
                
class drawdialogue():
    """ Create dialogue follow the player """
        
    def display(): 
          
        
        if text_pos == 1:
            
            Text.display(text_list[text_pos] , WHITE, [player.rect.x + 60,player.rect.y - 70], 25)
            Text.display(text_list[text_pos + 1] , WHITE, [player.rect.x + 60,player.rect.y - 50], 25)
            pygame.draw.rect(screen, WHITE,(player.rect.x + 60,player.rect.y - 70, 400,85),2)
            Text.display ("press o to continue",WHITE, [player.rect.x + 60,player.rect.y -25],25)
        else:
            Text.display(text_list[text_pos] , WHITE, [player.rect.x + 60,player.rect.y - 70], 25)
            pygame.draw.rect(screen, WHITE,(player.rect.x + 60,player.rect.y - 70, 400,60),2)
            Text.display ("press o to continue",WHITE, [player.rect.x + 60,player.rect.y -45],25)
            
            
class Boss_3(pygame.sprite.Sprite):
    """ The class to create the Boss 3 """
    def __init__ (self):
        # Call the parent's constructor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","assassin.png")).convert()
        self.image_1 = pygame.image.load(os.path.join("picture","assassin.png")).convert()
        self.image_2 = pygame.image.load(os.path.join("picture","assassin1.png")).convert()
        self.image_1.set_colorkey(WHITE)
        self.image_2.set_colorkey(WHITE)
        self.image.set_colorkey(WHITE)
        
        # Set a reference to the image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 300
        
        # Set the initial velocity
        self.change_x=0
        self.change_y=0
        
        # Set the damage
        self.dmg = 10
        
        # Set the hp
        self.hp=200
        self.hp1 = 200 
        self.current_hp=self.hp
        
        # Set the cooldown time
        self.cooldown=0
        
        # Set the facing direction
        self.faceFront=False
        self.turn=False      
        
        # Set the gravity
        self.grav=.6
        
        # Set the trigger for using skill
        self.using_skill=False
        self.spelling_time=0
        self.change_time=0
        
        # Set the cd for running
        self.warming_time=0
        self.chance=0
        self.length=0
        self.running=False
    def update(self):
        """ Use the skill and move the boss """
        
        # Calculate the gravity
        self.gravity()
        
        # Not hittable while not using skills
        self.passive()
        
        # Set the timer for cd
        self.cooldown+=1
        
        # Change facing direction
        if self.faceFront==True:
            if player.rect.x>self.rect.x:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            if player.rect.x<=self.rect.x:
                self.faceFront=True
                self.turn+=True 
        if self.turn==True:
            self.image=pygame.transform.flip(self.image,True,False)
            self.turn=False 
            
        #Set the velocity when not running
        if not self.running:
            if self.rect.x < player.rect.x:
                self.change_x=4
            else:
                self.change_x=-4
        self.speed_run()
        
        # Move the boss
        self.rect.x+=self.change_x
      
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
            
            if self.change_x > 0:
                self.rect.right = item.rect.left
                
            elif self.change_x < 0:
                self.rect.left = item.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
                self.rocket_jumping=False

            elif self.change_y < 0:
                self.rect.top = item.rect.bottom
                self.rocket_jumping=False
            self.change_y=0
            
        # After cd is ready, use the skill
        if self.cooldown>=150:
            self.cooldown=0
            self.using_skill=True

        # Use a skill randomly
        if self.using_skill:
            self.spelling_time+=1
            if self.spelling_time==120:
                self.spell=random.randrange(3)
                if self.spell==0:
                    self.ability=Spell_throw_a_knief(self.rect.x,self.rect.y)
                    current_level.enemy_list.add(self.ability)
                elif self.spell==1:
                    self.chance=3           
                elif self.spell==2:
                    self.ability=Spell_throw_a_synthe(self.rect.x,self.rect.y)
                    current_level.enemy_list.add(self.ability)    
                self.using_skill=False
                self.spelling_time=0
    def gravity(self):
        """ Calculate the gravity """    
        if self.change_y == 0:
                
            self.change_y = 1
                
        else:
            self.change_y +=self.grav
 
            
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height    
    def passive(self):
        """ Make the boss not hittable"""
        if self.using_skill==False:
            self.hp=self.current_hp
            self.change_time+=1
            if self.change_time==10:
                self.image=self.image_1
            if self.change_time==20:
                self.image=self.image_2
                self.change_time=0
        if self.using_skill == True:
            self.current_hp=self.hp
            self.change_time=0
            self.image=self.image_1
    def speed_run(self):
        """ Make boss run """
        if self.running and self.chance>0:
            self.length+=self.change_x
            if self.length>=250 or self.length<=-250:
                self.length=0
                self.chance-=1
                self.running=False
        if not self.running:
            if self.warming_time>0:
                self.warming_time-=1
            if self.chance>0:
                if self.warming_time==0:
                    self.running=True
                    self.change_x*=4
                    self.warming_time=30                    
class Spell_throw_a_synthe(pygame.sprite.Sprite):
    """ The spell 1 of the boss 3 """
    def __init__(self,pos_x,pos_y):
        # Call the parent's constructor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","spell_blade.jpg")).convert()
        self.ori_image = pygame.image.load(os.path.join("picture","spell_blade.jpg")).convert()
        self.image.set_colorkey(WHITE)
        self.ori_image.set_colorkey(WHITE)
        
        # Set a reference to the image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the speed and angle
        self.speed=10
        self.angle=0
        
        # Varible for counting the distance
        self.distance=0
        
        # Set for cooling down
        self.time=0
        
        #Set the damage
        self.dmg=6
        
        # Trigger to come back
        self.back=False
        
        # Calculate the velocity and angle
        self.difference_y =  player.rect.y  - self.rect.y 
        self.difference_x =  player.rect.x  - self.rect.x
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)

        self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
        self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))   
        self.rotate_angle=0
    def update(self):
        """ Move the synthe """
        # Move it
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y
        
        # Rotate it
        self.rotate_angle+=80
        self.image=pygame.transform.rotate(self.ori_image,self.rotate_angle)        
        
        # Calculate the distance
        if self.distance<500:
            self.distance+=self.speed
        
        # If too far, come back
        if self.distance>=500:
            self.back=True
            
        # Come back
        if self.back:
            if self.time==0:
                #Change enemy_list to boss_list
                for boss in current_level.boss_list:
                    po_x=boss.rect.x
                    po_y=boss.rect.y
                self.difference_y =  po_y  - self.rect.y 
                self.difference_x = po_x - self.rect.x
                if self.difference_y>0 and self.difference_x<0:
                    self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
                elif self.difference_y<=0 and self.difference_x<0:
                    self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
                elif self.difference_x==0 and self.difference_y<=0:
                    self.angle=math.radians(-90)
                elif self.difference_x==0 and self.difference_y>0:
                    self.angle=math.radians(90)
                else:
                    self.angle=math.atan(self.difference_y/self.difference_x)
        
                self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
                self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))  
                self.time=5
            self.time-=1


            if self.difference_x<=50 and self.difference_x>=-50 and self.difference_y<=50 and self.difference_y>=-50:
                current_level.enemy_list.remove(self)
class Spell_throw_a_knief(pygame.sprite.Sprite):
    """ Throw a knief, if hitted, teleport the boss to player """
    def __init__(self,pos_x,pos_y):
        # Call the parent's constrcutor
        super().__init__()
        
        # Set the image 
        self.image = pygame.image.load(os.path.join("picture","spell_throw_knief.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a reference to the image rect and position
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the speed
        self.speed=10
        
        # Set the time for cd
        self.time=0
        
        # Set the damage
        self.dmg = 0
        
        # Set the velocity
        self.difference_y =  player.rect.y  - self.rect.y 
        self.difference_x =  player.rect.x  - self.rect.x
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)

        self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
        self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))   
        
        # Flip the image
        if self.change_x>0:
            self.image=pygame.transform.flip(self.image,True,False)              
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi-self.angle
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi-self.angle   
        else:
            self.angle*=-1
            
        #Rotate the image
        self.image=pygame.transform.rotate(self.image,math.degrees(self.angle))
 
    def update(self):
        """ Move the knife """
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y 
        
        self.time+=1
        # Off screen check
        if self.rect.bottom<=0 or self.rect.top>=screen_y or self.time>=600:
            current_level.enemy_list.remove(self)
        self.hit=pygame.sprite.collide_rect(self,player)
        
        # Teleport himself if hit
        if self.hit==True:
            current_level.enemy_list.remove(self)
            for boss in current_level.boss_list:
                boss.rect.x=self.rect.x
                boss.rect.y=self.rect.y
                self.hit_list = pygame.sprite.spritecollide(boss, current_level.platform_list, False)
                for block in self.hit_list:    
                    blockCentre=(block.rect.bottom+block.rect.top)/2
                    if boss.rect.y>blockCentre and block.rect.bottom<SCREEN_HEIGHT-100:
                        boss.rect.top=block.rect.bottom
                    else:
                        boss.rect.bottom=block.rect.top            
class Boss_4(pygame.sprite.Sprite):
    def __init__ (self):
        # Call the parent's constrcutor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","dark_mage.png")).convert()
        self.image.set_colorkey(WHITE)
        
        
        # Set a reference to the image rect and position        
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 300
        
        # Set the initial velocity
        self.change_x=0
        self.change_y=3
        
        # Set the damage
        self.dmg = 10
        
        # Set the hp and timer for cd
        self.hp=200
        self.hp1 = 200
        self.cooldown=0
        
        # Set the facing direction
        self.faceFront=True
        self.turn=False        
        
        # Set the timer for ghosty
        self.ghosty=False
        self.ghost_time=0
        
    def update(self):
        
        # Set the timer for cd
        self.cooldown+=1
        
        # Change the facing direction
        if self.faceFront==True:
            if player.rect.x>=self.rect.x:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            if player.rect.x<self.rect.x:
                self.faceFront=True
                self.turn+=True   
        if self.turn==True:
            self.image=pygame.transform.flip(self.image,True,False)
            self.turn=False      
            
            
        # Make him move towards the player
        if self.rect.x < player.rect.x:
            self.change_x=3
        else:
            self.change_x=-3
            
        # Make it use ghost walk
        self.ghost_walk()
        
        # Move the boss
        self.rect.x+=self.change_x
        
        # Set the velocity   
        if not self.ghosty:
            self.ghost_time+=1
            if self.rect.y>500:
                self.change_y=-3
            elif self.rect.y<10:
                self.change_y=3
                
        # Move him
        self.rect.y += self.change_y
        
        if self.rect.top<=0:
            self.rect.top=0

                
        if self.rect.bottom>=screen_y:
            self.rect.bottom=screen_y
        
        # Make him use skills
        if self.cooldown>=180:
            self.cooldown=0
        
            self.spell=random.randrange(4)
            if self.spell==0:
                self.spell=Spell_black_hole(self.rect.x,self.rect.y)    
                current_level.enemy_list.add(self.spell)
            elif self.spell==1:
                self.flash()
            elif self.spell>=2:
                self.spell=Spell_moon(self.rect.x,self.rect.y)
                current_level.enemy_list.add(self.spell)
    def ghost_walk(self):
        """ A functiont to make him use ghost walk """
        # if cd is ready, pull the trigger
        if self.ghost_time==300:
            self.ghosty=True
            
        if self.ghosty==True:
            if self.ghost_time%5==0:
                self.spell=Spell_shadow(self.rect.x,self.rect.y)
                current_level.special_list.add(self.spell)
            self.ghost_time-=1
            if self.rect.y < player.rect.y:
                self.change_y=4
            else:
                self.change_y=-4
            self.change_x*=2
            if self.ghost_time==0:
                self.ghosty=False
    def flash(self):
        # A method to make him flash
        if self.rect.x>player.rect.x:
            self.spell=Spell_shadow1(player.rect.left-100-49,player.rect.bottom)
        else:
            self.spell=Spell_shadow1(player.rect.right+100,player.rect.bottom)
        current_level.special_list.add(self.spell)
class Spell_shadow(pygame.sprite.Sprite):
    """ A class to use the shadow """
    def __init__ (self,pos_x,pos_y):
        # Call the parent's constrcutor
        super().__init__()
        
        # Set the image and position
        self.image = pygame.image.load(os.path.join("picture","dark_mage1.png")).convert()
        self.image.set_colorkey(WHITE)
        
        
        # Set a reference to the image rect and position        
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y    
        self.time=0
    def update(self):
        """ Set the lasting time """
        self.time+=1
        if self.time==5:
            current_level.special_list.remove(self)
class Spell_shadow1(pygame.sprite.Sprite):
    """ Another class for the shadow """
    def __init__ (self,pos_x,pos_y):
        # Call the parent's constrcutor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","dark_mage1.png")).convert()
        self.image.set_colorkey(WHITE)
        
        
        # Set a reference to the image rect and position        
        self.rect = self.image.get_rect()
        self.rect.left = pos_x
        self.rect.bottom = pos_y    
        self.time=0
    def update(self):
        
        """ Set the timer """
        # If the cd is ready, use the skill
        self.time+=1
        shadow_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for block in shadow_hit_list:    
            blockCentre=(block.rect.bottom+block.rect.top)/2
            if self.rect.y>blockCentre and block.rect.bottom<SCREEN_HEIGHT-80:
                self.rect.top=block.rect.bottom
            else:
                self.rect.bottom=block.rect.top
        if self.time==60:
            for boss in current_level.boss_list:
                boss.rect.x=self.rect.x
                boss.rect.y=self.rect.y
            current_level.special_list.remove(self)
            self.spell=Spell_magic_circle((self.rect.left+self.rect.right)/2-5,(self.rect.top+self.rect.bottom)/2-5)
            current_level.enemy_list.add(self.spell)
class Spell_magic_circle(pygame.sprite.Sprite):
    def __init__ (self,pos_x,pos_y):
        # Call the parent's constrcutor    
        super().__init__()
        
        # Set the image
        self.ori_image = pygame.image.load(os.path.join("picture","spell_purple_circle.png")).convert()
        self.ori_image.set_colorkey(WHITE)
        # Set the damage
        self.dmg = 2
        
        # Varibles for changing the size of the image
        self.width=10
        self.height=10
        self.speed=20
        self.image=pygame.transform.scale(self.ori_image,(self.width,self.height))
        
        # Set a reference to the image rect and position 
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.po_x=pos_x
        self.po_y=pos_y    
        
        # Set the velocity
        self.rect_change_x=0
        self.rect_change_y=0           
    def update(self):
        """ Change the size of the picture and reset the reference to the image rect and position """
        self.width+=self.speed
        self.height+=self.speed
        self.rect_change_x-=(self.speed/2)
        self.rect_change_y-=(self.speed/2)
        self.image=pygame.transform.scale(self.ori_image,(self.width,self.height))
        self.rect=self.image.get_rect()
        self.rect.x=self.po_x+self.rect_change_x
        self.rect.y=self.po_y+self.rect_change_y           
        if self.width>=300 or self.height>=300:
            current_level.enemy_list.remove(self)
        
class Spell_black_hole(pygame.sprite.Sprite):
    def __init__ (self,pos_x,pos_y):
        # Call the parent's constrcutor
        super().__init__()
        
        # Set the image
        self.ori_image = pygame.image.load(os.path.join("picture","spell_black_hole.png")).convert()
        self.ori_image.set_colorkey(BLACK)
        
        # Set the angle
        self.angle=0
        
        # Set the size of the picture
        self.width=10
        self.height=10
        self.ex_speed=1
        self.sh_speef=20
        self.image=pygame.transform.scale(self.ori_image,(self.width,self.height))
        
        # Set a reference to the image rect and position 
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.po_x=pos_x
        self.po_y=pos_y    
        
        # Set the velocity of changing
        self.rect_change_x=0
        self.rect_change_y=0 
        
        # Set the damage
        self.dmg = 2
        
        # The trigger to use the skill
        self.shrink=False
    def update(self):
        
        """ resize the picture and make player move slower """
        
        
        self.angle+=10
        if not self.shrink:
            self.width+=self.ex_speed
            self.height+=self.ex_speed
            self.rect_change_x-=(self.ex_speed/2)
            self.rect_change_y-=(self.ex_speed/2)
            if self.width>=200 or self.height>=200:
                self.shrink=True
        if self.shrink:
            self.width-=self.sh_speef
            self.height-=self.sh_speef
            self.rect_change_x+=(self.sh_speef/2)
            self.rect_change_y+=(self.sh_speef/2)
            if self.width<=0 or self.height<=0:
                current_level.enemy_list.remove(self)
        if player.rect.x<self.rect.x:
            player.rect.x+=3
        else:
            player.rect.x+=-3
        self.ori_image1=pygame.transform.scale(self.ori_image,(self.width,self.height))
        self.image=pygame.transform.rotate(self.ori_image1,self.angle)
        self.rect=self.image.get_rect()
        self.rect.x=self.po_x+self.rect_change_x
        self.rect.y=self.po_y+self.rect_change_y        
class Spell_moon(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        # Call the parent's constrcutor
        super().__init__()
        self.image = pygame.image.load(os.path.join("picture","spell_moon.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a reference to the image rect and position 
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the speed and angle
        self.speed=7
        self.angle=0
        
        # Set the time for cd
        self.time=0
        
        # Set the damage
        self.dmg = 2
        
        # Set the speed and angle
        self.difference_y =  player.rect.y  - self.rect.y 
        self.difference_x =  player.rect.x  - self.rect.x
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)

        self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
        self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))           
    def update(self):
        """ Move the moon """
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y      
        self.time+=1
        # Off screen check
        if self.rect.bottom<=0 or self.rect.top>=screen_y or self.time>=600:
            current_level.enemy_list.remove(self)
class Boss_5(pygame.sprite.Sprite):
    def __init__ (self):
        # Call the parent's constrcutor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","shine_shine.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a reference to the image rect and position 
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 300
        
        # Set the speed
        self.change_x=0
        self.change_y=0
        
        # Set the gravity
        self.grav=.5
        
        # Set the hp
        self.hp=200
        self.hp1 = 200
        
        # set the cd 
        self.cooldown=0
        
        # Set the damage
        self.dmg = 10
        
        # Set the facing direction
        self.faceFront=True
        self.turn=False        
        
        
    def update(self):
        
        """ Move the boss and use the skills """
        
        # Set the timer for cd
        self.cooldown+=1
        
        # Calculate the gravity
        self.gravity()
        
        # Change the facing directon
        if self.faceFront==True:
            if player.rect.x>=self.rect.x:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            if player.rect.x<self.rect.x:
                self.faceFront=True
                self.turn+=True   
        if self.turn==True:
            self.image=pygame.transform.flip(self.image,True,False)
            self.turn=False      
            
            
        # Make the boss move towards player
        if self.rect.x < player.rect.x:
            self.change_x=3
        else:
            self.change_x=-3
     
        # Move the boss
        self.rect.x+=self.change_x
      
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
            
            if self.change_x > 0:
                self.rect.right = item.rect.left
                self.jump()
            elif self.change_x < 0:
                self.rect.left = item.rect.right        
                self.jump()
        self.rect.y += self.change_y
        
        if self.rect.top<=0:
            self.rect.top=0

                
        if self.rect.bottom>=screen_y:
            self.rect.bottom=screen_y
        
 
        # If we hit platforms, stop
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = item.rect.top

            elif self.change_y < 0:
                self.rect.top = item.rect.bottom
            self.change_y=0
            
        # When the cd is ready, use skills randomly
        if self.cooldown>=180:
            self.cooldown=0
        
            self.spell=random.randrange(3)
            if self.spell==0:
                self.spell=Spell_a_storage_of_a_king() 
                current_level.special_list.add(self.spell)
            elif self.spell==1:
                self.spell=Spell_holy_sword(self.rect.x,self.rect.y) 
                current_level.enemy_list.add(self.spell)                
            elif self.spell>=2:
                self.spell=Spell_royal_guard(self.rect.x,self.rect.bottom,random.randrange(1,4))
                current_level.enemy_list.add(self.spell)
    def gravity(self):
        """ Calculate the gravity """    
        if self.change_y == 0:
                
            self.change_y = 1
                
        else:
            self.change_y +=self.grav
 
            
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height    
    def jump(self):
   
        self.change_y = -6       
class Spell_a_storage_of_a_king(pygame.sprite.Sprite):
    
    """ Create a storage to shoot swords """
    def __init__ (self):
        # Call the parent's constrcutor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","spell_magic_circle.png")).convert()
        self.image.set_colorkey(BLACK)
        
        # Set a reference to the image rect and position 
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(current_level.level_limit-200)
        self.rect.bottom = random.randrange(200,screen_y) 
        
        # Hit check
        blade_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for block in blade_hit_list:    
            blockCentre=(block.rect.bottom+block.rect.top)/2
            if self.rect.y>blockCentre and block.rect.bottom<SCREEN_HEIGHT-80:
                self.rect.top=block.rect.bottom
            else:
                self.rect.bottom=block.rect.top
                
        self.time=0
        self.lasting_time=0
    def update(self):
        
        """ Make it last and after the lasting time remove it """
        if self.lasting_time>=300:
            current_level.special_list.remove(self)
        if self.time==30:
            
            self.spell=Spell_blade_rain((self.rect.left+self.rect.right)/2,(self.rect.top+self.rect.bottom)/2-10,random.randrange(3))
            current_level.enemy_list.add(self.spell)   
            self.time=0
        self.time+=1
        self.lasting_time+=1
class Spell_blade_rain(pygame.sprite.Sprite):
    '''blades in the last level'''
    def __init__(self,pos_x,pos_y,sword):
        # Call the parent's constrcutor
        super().__init__()
        # Set the damage
        self.dmg = 2
        
        # Make it shoot different swords
        if sword==0:
            self.image = pygame.image.load(os.path.join("picture","spell_sword1.png")).convert()
        elif sword==1:
            self.image = pygame.image.load(os.path.join("picture","spell_sword2.png")).convert()        
        elif sword==2:
            self.image = pygame.image.load(os.path.join("picture","spell_sword3.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a reference to the image rect and position 
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the velocity and timer for cd
        self.speed=15
        self.time=0
        self.difference_y =  player.rect.y  - self.rect.y 
        self.difference_x =  player.rect.x  - self.rect.x
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)

        self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
        self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))   
        if self.change_x>0:
            self.image=pygame.transform.flip(self.image,True,False)              
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi-self.angle
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi-self.angle   
        else:
            self.angle*=-1
        self.image=pygame.transform.rotate(self.image,math.degrees(self.angle))
 
    def update(self):
        
        """ Move the swords """
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y      
        if self.rect.bottom<=0:
            current_level.enemy_list.remove(self)
        self.blade_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        if len(self.blade_hit_list)>0 or self.rect.bottom>=screen_y:
            self.change_x=0
            self.change_y=0
            if self.change_x==0 and self.change_y==0:
                self.time+=1
                if self.time>=120:
                    current_level.enemy_list.remove(self)
class Spell_holy_sword(pygame.sprite.Sprite):
    """ Use the holy sword to attack player """
    def __init__(self,pos_x,pos_y):
        # Call the parent's constrcutor
        super().__init__()
        
        # Set the image
        self.image = pygame.image.load(os.path.join("picture","spell_holy_sword.png")).convert()
        self.ori_image = pygame.image.load(os.path.join("picture","spell_holy_sword.png")).convert()
        self.image.set_colorkey(WHITE)
        self.ori_image.set_colorkey(WHITE)
        
        # Set a reference to the image rect and position 
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Set the velocity and angle and damage
        self.speed=10
        self.time=0
        self.dmg = 2
        self.difference_y =  player.rect.y  - self.rect.y 
        self.difference_x =  player.rect.x  - self.rect.x
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi+math.atan((self.difference_y/self.difference_x))
        elif self.difference_x==0 and self.difference_y<=0:
            self.angle=math.radians(-90)
        elif self.difference_x==0 and self.difference_y>0:
            self.angle=math.radians(90)
        else:
            self.angle=math.atan(self.difference_y/self.difference_x)

        self.change_x=float(math.radians(self.speed)*math.degrees(math.cos(self.angle)))
        self.change_y=float(math.radians(self.speed)*math.degrees(math.sin(self.angle)))   
        if self.change_x>0:
            self.image=pygame.transform.flip(self.ori_image,True,False)              
        if self.difference_y>0 and self.difference_x<0:
            self.angle=math.pi-self.angle
        elif self.difference_y<=0 and self.difference_x<0:
            self.angle=-1*math.pi-self.angle   
        else:
            self.angle*=-1
        self.image=pygame.transform.rotate(self.image,math.degrees(self.angle))
        self.reset=False
        
        # Make it pull player back after hit
        self.pull=False
        self.fly=True
        self.distance_x=0
        self.distance_y=0
    def update(self):
        """ Move the swords and pull player back """
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y      
        self.distance_x+=self.change_x
        self.distance_y+=self.change_y
        self.time+=1
        if self.rect.bottom<=0 or self.rect.top>=screen_y or self.time>=600:
            current_level.enemy_list.remove(self)
        if self.fly:
            self.hit=pygame.sprite.collide_rect(self,player)
            if self.hit==True:
                self.reset=True
                self.fly=False

        if self.reset:
            self.change_x*=-1
            self.change_y*=-1
                 
            self.image=pygame.transform.rotate(self.image,180)
            
            
            self.reset=False
            self.pull=True
        
        if self.pull:
            player.change_x=self.change_x
            player.change_y=self.change_y
            if self.distance_x>=-5 and self.distance_x<=5 and self.distance_y>=-5 and self.distance_y<=5:
                self.pull=False
                current_level.enemy_list.remove(self)
class Spell_royal_guard(pygame.sprite.Sprite):
    # Make the boss summon the guard
    def __init__ (self, pos_x,pos_y,ability):
        # Call the parent's constrcutor
        super().__init__()
        self.image = pygame.image.load(os.path.join("picture","spell_royal_guard_image.png")).convert()
        self.image.set_colorkey(WHITE)
        
        # Set a reference to the image rect and position 
        self.rect = self.image.get_rect()
        self.rect.left = pos_x
        self.rect.bottom = pos_y
        
        # Set the damage and velocity
        self.dmg = 1
        self.change_x=0
        self.change_y=0
        
        #Set gravity 
        self.grav=.1
        
        # Set timer for cd
        self.cooldown=0
        
        # Set facing direction
        self.faceFront=True
        self.turn=False 
        
        # Trigger to use skill
        self.ability_shoot=False
        self.ability_run=False
        self.length=0
        self.running=False
        self.ability_magic=False
        if ability==1:
            self.ability_shoot=True
        elif ability==2:
            self.ability_run=True
        elif ability==3:
            self.ability_magic=True            
    def update(self):
        
        # Set the gravity
        self.gravity()
        
        # Set the facing direction
        if self.faceFront==True:
            if player.rect.x>self.rect.x:
                self.faceFront=False
                self.turn+=True
        if self.faceFront==False:
            if player.rect.x<=self.rect.x:
                self.faceFront=True
                self.turn+=True   
        if self.turn==True:
            self.image=pygame.transform.flip(self.image,True,False)
            self.turn=False   
        
        # Set the timer for cd    
        if self.cooldown!=0:
            self.cooldown-=1
            
        # Move the guard
        self.rect.x+=self.change_x

        if not self.running:
            if self.rect.x < player.rect.x:
                self.change_x=3
            else:
                self.change_x=-3
        if self.rect.y > 740:
            self.change_y = 0
            self.rect.y = 740       
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
            
            if self.change_x > 0:
                self.jump()
                self.rect.right = item.rect.left
                
            elif self.change_x < 0:
                self.jump()
                self.rect.left = item.rect.right
            
        self.rect.y += self.change_y
 
        # If we hit something , stop moving
        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for item in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
            elif self.change_y < 0:
                self.rect.top = item.rect.bottom
            
            self.change_y = 0 
            
        # Use the skills
        if self.ability_shoot==True:
            if self.rect.x<=player.rect.x+500 and self.rect.x>=player.rect.x-500 and self.cooldown==0:
                self.ability=Enemy_bullet((self.rect.left+self.rect.right)/2,(self.rect.top+self.rect.bottom)/2)
                current_level.enemy_list.add(self.ability)
                self.cooldown=300
        if self.ability_run==True:
            if self.rect.x<=player.rect.x+500 and self.rect.x>=player.rect.x-500 and self.cooldown==0: 
                self.run()
        if self.ability_magic==True:
            if self.rect.x<=player.rect.x+800 and self.rect.x>=player.rect.x-800 and self.cooldown==0:   
                self.ability=Enemy_magic_burst()
                current_level.special_list.add(self.ability)
                self.cooldown=300
                
    def gravity(self):
        """ Calculate the gravity """
        if self.change_y == 0:
                
            self.change_y = 1
                
        else:
            self.change_y +=self.grav
 
            
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    def jump(self):
        """ Make them jump """
        self.change_y = -6    
    def run(self):
        """ Make them dash """
        if not self.running:
            self.change_x*=3
            self.running=True
        if self.running==True:
            self.length+=self.change_x
            if self.length>=500 or self.length<=-500:
                self.running=False
                self.change_x/=3
                self.length=0
                self.cooldown=500
                
                
                
#done check for start menuw
done1 = False

#done check for main loop
done2 = True

#done check for end screen loop
done3 = True

done4 = True

done5 = True

clock = pygame.time.Clock()


# keeps the game running
game=True

#level checkpoint design
rd1=False
rd2=False
rd3=False
rd4=False
rd5=False

#Gun_limit
gun_limit=1

#main loop
while game:
    pygame.init()
    
    screen_x = 1000
    screen_y = 800
    
    
    startFiring=False
    
    screen = pygame.display.set_mode ([screen_x,screen_y]) 
    # Set image
    background_image = pygame.image.load(os.path.join("picture","background.png")).convert() #used in Level
    end_image = pygame.image.load(os.path.join("picture","end.png")).convert()
    dead_end_image = pygame.image.load(os.path.join("picture","dead end.jpg")).convert()
    background_image2 = pygame.image.load(os.path.join("picture","background2.png")).convert()    
    background_image_start = pygame.image.load(os.path.join("picture","start_menu_bg.jpg")).convert()     
    good_end_image = pygame.image.load(os.path.join("picture", "winning_end.jpg")).convert()
    
    
    pygame.display.set_caption("Mike's Journey")
    
    
    
    
    #menu display
    start_menu_list=[["Story Mode",GRAY,[0,400],40],["Survival Mode",GRAY,[0,500],40],["Challenge Mode",GRAY,[0,600],40],["Quit Game",GRAY,[0,700],40]]
    rd_select_list=[["New Game",GRAY,[0,200],40],["01",GRAY,[0,300],40],["02",GRAY,[0,400],40],["03",GRAY,[0,500],40],["04",GRAY,[0,600],40],["05",GRAY,[0,700],40]]
    
    
    #sound convert
    start_menu_click=pygame.mixer.Sound(os.path.join("music","start_menu_click.wav"))
    start_menu_click1=pygame.mixer.Sound(os.path.join("music","start_menu_click1.wav"))
    pygame.mixer.music.load(os.path.join("music","start_menu_BGM.mp3"))
    pygame.mixer.music.play(-1,0.0)      
    
    
    
    #played the sound or not 
    play1=False
    play2=False
    play3=False
    play4=False
    play5=False
    play6=False
    
    story_mode=False
    
    #start menu loop
    while done1 == False:
        pos = pygame.mouse.get_pos()
        pos_x = pos[0]
        pos_y = pos[1]
        background_image3 = pygame.image.load(os.path.join("picture","start_menu_bg.jpg")).convert()            
        screen.blit(background_image3, [0, 0])     
        #Main start menu
        if not story_mode:
            for i in start_menu_list:
                Text.display(i[0],i[1],i[2],i[3])
        #Create short cut for player
        if story_mode:
            for i in range (len(rd_select_list)):
                if i <=0:
                    Text.display(rd_select_list[i][0],rd_select_list[i][1],rd_select_list[i][2],rd_select_list[i][3])
                if rd1 and i<=1:
                    Text.display(rd_select_list[i][0],rd_select_list[i][1],rd_select_list[i][2],rd_select_list[i][3])
                if rd2 and i<=2:
                    Text.display(rd_select_list[i][0],rd_select_list[i][1],rd_select_list[i][2],rd_select_list[i][3])
                if rd3 and i<=3:
                    Text.display(rd_select_list[i][0],rd_select_list[i][1],rd_select_list[i][2],rd_select_list[i][3])
                if rd4 and i<=4:
                    Text.display(rd_select_list[i][0],rd_select_list[i][1],rd_select_list[i][2],rd_select_list[i][3])
                if rd5 and i<=5:
                    Text.display(rd_select_list[i][0],rd_select_list[i][1],rd_select_list[i][2],rd_select_list[i][3])        
        #Enlarge the words and play the click sound.
        if not story_mode:
            if pos_x>=0 and pos_x<=200 and pos_y>= 400 and pos_y<=440:
                start_menu_list[0][1]=WHITE
                start_menu_list[0][3]=50
                if not play1:
                    start_menu_click.play()
                    play1=True
            else:
                play1=False
                start_menu_list[0][1]=GRAY
                start_menu_list[0][3]=40        
            if pos_x>=0 and pos_x<=250 and pos_y>= 500 and pos_y<=540:
                start_menu_list[1][1]=WHITE
                start_menu_list[1][3]=50        
                if not play2:
                    start_menu_click.play()
                    play2=True
            else:
                play2=False
                start_menu_list[1][1]=GRAY
                start_menu_list[1][3]=40                  
            
            if pos_x>=0 and pos_x<=350 and pos_y>= 600 and pos_y<=640:
                start_menu_list[2][1]=WHITE
                start_menu_list[2][3]=50
                if not play3:
                    start_menu_click.play()
                    play3=True
            else:
                play3=False
                start_menu_list[2][1]=GRAY
                start_menu_list[2][3]=40                 
            if pos_x>=0 and pos_x<=200 and pos_y>= 700 and pos_y<=750:
                start_menu_list[3][1]=WHITE
                start_menu_list[3][3]=50       
                if not play4:
                    start_menu_click.play()
                    play4=True
            else:
                play4=False
                start_menu_list[3][1]=GRAY
                start_menu_list[3][3]=40               
    
            for event in pygame.event.get():
                '''choosing modes according to clicks'''
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pos_x>=0 and pos_x<=250:
                        
                        if pos_y>= 500 and pos_y<=540:
                            pygame.mixer.music.fadeout(1500)
                            gun_limit = 4
                            done1 = True
                            done2 = False
                            current_level_now = 0
                            start_menu_click1.play()
                            Dialogue.display1("The only objective of this mode is to collect as many coins as you can while moving to the right. You have limited ammo. Watch your hp bar though! Ready? ")
                    if pos_x>=0 and pos_x<=350:
                        
                        if pos_y>= 600 and pos_y<=640:
                            gun_limit = 4
                            pygame.mixer.music.fadeout(1500)
                            current_level_now = 1
                            done1 = True
                            done2 = False
                            start_menu_click1.play()
                            Dialogue.display1("The only objective of this mode is to defeat as many monsters as you can! Bonus info: Press Q to change weapon.")
                    if pos_x>=0 and pos_x<=200:
                        if pos_y>= 700 and pos_y<=740:
                            pygame.quit()
                            
                    if pos_x>=0 and pos_x<=200:
                        if pos_y>= 400 and pos_y<=440:
                            current_level_now = 2
                            story_mode = True
                            done2 = False    
                            start_menu_click1.play()
                    print([pos_x,pos_y])
                if event.type == pygame.QUIT:
                    pygame.quit()
        
        
        if story_mode:
            if pos_x>=0 and pos_x<=180 and pos_y>= 200 and pos_y<=240:
                rd_select_list[0][1]=WHITE
                rd_select_list[0][3]=50
                if not play1:
                    start_menu_click.play()
                    play1=True
            else:
                play1=False
                rd_select_list[0][1]=GRAY
                rd_select_list[0][3]=40
            if rd1:
                if pos_x>=0 and pos_x<=100 and pos_y>= 300 and pos_y<=340:
                    rd_select_list[1][1]=WHITE
                    rd_select_list[1][3]=50        
                    if not play2:
                        start_menu_click.play()
                        play2=True
                else:
                    play2=False
                    rd_select_list[1][1]=GRAY
                    rd_select_list[1][3]=40                  
            if rd2:
                if pos_x>=0 and pos_x<=100 and pos_y>= 400 and pos_y<=440:
                    rd_select_list[2][1]=WHITE
                    rd_select_list[2][3]=50
                    if not play3:
                        start_menu_click.play()
                        play3=True
                else:
                    play3=False
                    rd_select_list[2][1]=GRAY
                    rd_select_list[2][3]=40           
            if rd3:
                if pos_x>=0 and pos_x<=100 and pos_y>= 500 and pos_y<=540:
                    rd_select_list[3][1]=WHITE
                    rd_select_list[3][3]=50       
                    if not play4:
                        start_menu_click.play()
                        play4=True
                else:
                    play4=False
                    rd_select_list[3][1]=GRAY
                    rd_select_list[3][3]=40        
            if rd4:
                if pos_x>=0 and pos_x<=100 and pos_y>= 600 and pos_y<=640:
                    rd_select_list[4][1]=WHITE
                    rd_select_list[4][3]=50       
                    if not play5:
                        start_menu_click.play()
                        play5=True
                else:
                    play5=False
                    rd_select_list[4][1]=GRAY
                    rd_select_list[4][3]=40       
            if rd5:
                if pos_x>=0 and pos_x<=100 and pos_y>= 700 and pos_y<=740:
                    rd_select_list[5][1]=WHITE
                    rd_select_list[5][3]=50       
                    if not play6:
                        start_menu_click.play()
                        play6=True
                else:
                    play6=False
                    rd_select_list[5][1]=GRAY
                    rd_select_list[5][3]=40           
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pos_x>=0 and pos_x<=180:
                        if pos_y>= 200 and pos_y<=240:
                            gun_limit = 1
                            pygame.mixer.music.fadeout(1500)
                            done1 = True
                            done2 = False
                            current_level_now = 2
                            start_menu_click1.play()                    
                    if rd1:
                        if pos_x>=0 and pos_x<=100:
                            if pos_y>= 300 and pos_y<=340:
                                gun_limit = 1
                                pygame.mixer.music.fadeout(1500)
                                current_level_now = 3
                                done1 = True
                                done2 = False
                                start_menu_click1.play()
                    if rd2:
                        if pos_x>=0 and pos_x<=100:
                            if pos_y>= 400 and pos_y<=440:
                                gun_limit = 2
                                pygame.mixer.music.fadeout(1500)
                                current_level_now = 6
                                done1 = True
                                done2 = False
                                start_menu_click1.play()
                    if rd3:
                        if pos_x>=0 and pos_x<=100:
                            if pos_y>= 500 and pos_y<=540:
                                gun_limit = 3
                                pygame.mixer.music.fadeout(1500)
                                current_level_now = 9
                                done1 = True
                                done2 = False    
                                start_menu_click1.play()
                    if rd4:
                        if pos_x>=0 and pos_x<=100:
                            if pos_y>= 600 and pos_y<=640:
                                gun_limit = 4
                                pygame.mixer.music.fadeout(1500)
                                current_level_now = 12
                                done1 = True
                                done2 = False    
                                start_menu_click1.play()       
                    if rd5:
                        if pos_x>=0 and pos_x<=100:
                            if pos_y>= 700 and pos_y<=740:
                                gun_limit = 4
                                pygame.mixer.music.fadeout(1500)
                                current_level_now = 15
                                done1 = True
                                done2 = False    
                                start_menu_click1.play()                
                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                            


        clock.tick(60)
        
        pygame.display.flip()
        
     
        
     
    
    
    #game loop
    
    screen_x = 1000
    screen_y = 800
    
    pygame.init()
    #General settings
    ammo1 = 50
    ammo2 = 30
    ammo3 = 30
    ammo4 = 12   
    screen = pygame.display.set_mode ([screen_x,screen_y])
    pygame.display.set_caption("Mike's Journey")

    #Settings for sprite group
    player = Player()
    player.rect.x = 90
    player.rect.y = 800
    total_diff = 0
    aim = Crosshair()
    gun_image=Pistol_image()
    
    
    
    level_list = []
    level_list.append ( Level_01(player) )
    level_list.append ( Level_02(player) )
    level_list.append ( StLevel_01(player) )
    level_list.append ( StLevel_02(player) )
    level_list.append ( StLevel_03(player) )
    level_list.append ( StLevel_04(player) )
    level_list.append ( StLevel_05(player) )
    level_list.append ( StLevel_06(player) )
    level_list.append ( StLevel_07(player) )
    level_list.append ( StLevel_08(player) )
    level_list.append ( StLevel_09(player) )
    level_list.append ( StLevel_10(player) )
    level_list.append ( StLevel_11(player) )
    level_list.append ( StLevel_12(player) )
    level_list.append ( StLevel_13(player) )    
    level_list.append ( StLevel_14(player) )
    level_list.append ( StLevel_15(player) )
    
    current_level = level_list[current_level_now]
    
    machine_gun_list=pygame.sprite.Group()
    all_sprite_list = pygame.sprite.Group()
    player.level = current_level
    
    machine_gun_limit=0
    all_sprite_list.add(gun_image)
    all_sprite_list.add(aim)
    all_sprite_list.add(player)
    
    gun_num = 1
    current_pos = 0
    trap_count = 0
    
    stdialogue = False
    jump = False
    create = False
    reload = False
    limit = 0
    time = 0
    #Draw hp bars for player and ammo
    hp_player = hp_bar(player.hp / 120 * 300,15,0,100)
        
    current_level.hp_bar_group_player.add(hp_player)
        
    ammo_left = hp_bar(ammo1 / 50 *200,15,0,150)
        
    current_level.hp_bar_group_ammo.add(ammo_left)    
    #main loop
    while done2 == False:

        for event in pygame.event.get():
            #Back to start menu
            if event.type == pygame.QUIT:
               
                done2 = True
                if current_level_now >= 2:
                    done3 = True
                    done4 = True
                    done1 = False
                elif current_level_now < 2:
                    done3 = True
                    done4 = True
                    done1 = False
                
            elif event.type == pygame.KEYDOWN:
                    #Move
                    if event.key == pygame.K_w:
                        player.jump()
                    if event.key == pygame.K_a:
                        player.go_left()
                                                 
                    if event.key == pygame.K_d:
                        player.go_right()
                    #Switching guns
                    if event.key == pygame.K_q:
                        gun_num += 1
                        if gun_num > gun_limit : # if greater than maximum num of weapon change back to original
                            gun_num = 1
                        if gun_num==1:
                            for hp in current_level.hp_bar_group_ammo:
                                hp.length = 200 *ammo1 / 50                            
                            gun_image=Pistol_image()
                            all_sprite_list.add(gun_image)
                        if gun_num==2:
                            for hp in current_level.hp_bar_group_ammo:
                                hp.length = 200 *ammo2 / 30                            
                            gun_image=Machine_gun_image()
                            all_sprite_list.add(gun_image)    
                        if gun_num==3:
                            for hp in current_level.hp_bar_group_ammo:
                                hp.length = 200 *ammo3 / 30                            
                            gun_image=Shot_gun_image()
                            all_sprite_list.add(gun_image)   
                        if gun_num==4:
                            for hp in current_level.hp_bar_group_ammo:
                                hp.length = 200 *ammo4 / 12                            
                            gun_image=Rocket_launcher_image()
                            all_sprite_list.add(gun_image)   
                    # Called the moving function
                    if event.key == pygame.K_LSHIFT:
                        player.roll()                       
                    if event.key == pygame.K_UP:
                        player.jump()
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                                         
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                                                
                            
                    # Reload the ammo
                    if event.key == pygame.K_r:
                        reload = True
                       
            # Shoot bullet when click the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    startFiring=True
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                    startFiring = False            
                        
                 
            #Stop when user let it off the keyboard
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a  and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()
            
                if event.key == pygame.K_LEFT  and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()                
        #Reset guns if not firing
        if startFiring==False:
            machine_gun_limit=0
            player.grav=.5
            for bullet in machine_gun_list:
                if bullet.firing==False:
                    machine_gun_list.remove(bullet)
                    all_sprite_list.remove(bullet)
        #Firing guns while not reloading
        if startFiring==True:
            if not reload:
                # Shoot the pistol
                if gun_num == 1:
                    if ammo1 > 0:
                        # Shoot every 10 frames
                        if machine_gun_limit % 10 ==0:
                            gun1= Machine_Gun()
                            ammo1 -= 1
                            gun1.check_firing()
                            machine_gun_list.add(gun1)
                            all_sprite_list.add(gun1)
                            
                            # Play the sound
                            sound1 = pygame.mixer.Sound(os.path.join("music","machine_gun.ogg"))
                            sound1.play()
                            
                            #Change the length of ammo bar
                            for hp in current_level.hp_bar_group_ammo:
                                hp.length = 200 *ammo1 / 50
                        # count for frames    
                        machine_gun_limit+=1  
                        
                    if ammo1 == 0:
                        sound1 = pygame.mixer.Sound(os.path.join("music","dry gun.wav"))
                        sound1.play()                        
                # Shoot the machine gun    
                elif gun_num == 2:
                    if ammo2 > 0:
                        # Shoot every 4 frames
                        if machine_gun_limit % 4 ==0:
                            for bullet in machine_gun_list:
                                if bullet.change_y != 0 or bullet.change_x != 0:
                                    ammo2 -= 1
                                    # Play the sound
                                    sound1 = pygame.mixer.Sound(os.path.join("music","machine_gun.ogg"))
                                    sound1.play()                                    
                                    break
                            gun2=Machine_Gun2()
                            
                            gun2.check_firing()
                            machine_gun_list.add(gun2)
                            all_sprite_list.add(gun2)
                            #Change the length of ammo bar
                            for hp in current_level.hp_bar_group_ammo:
                                hp.length = 200 * ammo2 / 30
                            
                        player.grav=2.5
                        machine_gun_limit+=1
                    if ammo2 == 0:
                        sound1 = pygame.mixer.Sound(os.path.join("music","dry gun.wav"))
                        sound1.play()                        
                # shoot the shot gun
                elif gun_num == 3:
                    if ammo3 > 0:
                        if machine_gun_limit == 60:
                            ammo3 -= 1
                            for i in range(-36,37,12):
                                gun3=Machine_Gun3(i)
                                gun3.check_firing()
                                machine_gun_list.add(gun3)
                                all_sprite_list.add(gun3)
                            # Play the sound
                            sound1 = pygame.mixer.Sound(os.path.join("music","Gun3sound.wav"))
                            sound1.play()
                            #Change the length of ammo bar
                            for hp in current_level.hp_bar_group_ammo:
                                hp.length = 200 *ammo3 / 30   
                            machine_gun_limit=0
                        player.grav=2.5
                        machine_gun_limit+=1
                    if ammo3 == 0:
                        sound1 = pygame.mixer.Sound(os.path.join("music","dry gun.wav"))
                        sound1.play()                     
                        
                # Shoot the rocket launcher
                elif gun_num == 4:
                    if ammo4 > 0:
                        if machine_gun_limit == 20:
                            # Play the sound
                            sound1 = pygame.mixer.Sound(os.path.join("music","rocket-launcher.wav"))
                            sound1.play()                            
                        if machine_gun_limit == 40:
                        
                            ammo4 -= 1
                            gun2=Machine_Gun4()
                            
                            gun2.check_firing()
                            machine_gun_list.add(gun2)
                            all_sprite_list.add(gun2)
                            #Change the length of ammo bar
                            for hp in current_level.hp_bar_group_ammo:
                                hp.length = 200 *ammo4 / 10
                            machine_gun_limit=0
                        player.grav=2.5
                        machine_gun_limit+=1
                        
                    if ammo4 == 0:
                        sound1 = pygame.mixer.Sound(os.path.join("music","dry gun.wav"))
                        sound1.play()                     
        
                     
        #updating survival mode
        current_position = player.rect.x + total_diff
         
        if current_level_now == 0:    
            if current_position > limit :
                create = True
                limit += 1500
            if create:
                current_level.create()
                create = False
                
    
        if current_position > current_pos:
            current_pos = current_position
        
        
        #Reload the guns
        if reload == True:
            
            sound1 = pygame.mixer.Sound(os.path.join("music","reload.wav"))
            
            time += 1
            sound1.play()
        if time >= 120:
                ammo1 = 50
                ammo2 = 30
                ammo3 = 10
                ammo4 = 10
                for hp in current_level.hp_bar_group_ammo:
                        hp.length = 200 *ammo1 / 50    
                for hp in current_level.hp_bar_group_ammo:
                        hp.length = 200 *ammo2 / 30
                for hp in current_level.hp_bar_group_ammo:
                        hp.length = 200 *ammo3 / 10   
                for hp in current_level.hp_bar_group_ammo:
                        hp.length = 200 *ammo4 / 10
                time = 0
                sound1.stop()
                reload = False
        #Sprite group update
        current_level.update()
        all_sprite_list.update()
        #Remove bullets that are too far away
        for bullet in machine_gun_list:
            if bullet.rect.x  >1000+player.rect.x or bullet.rect.x <-1000 + player.rect.x:
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet)
            if bullet.rect.y > 800 or bullet.rect.y < 0:
                machine_gun_list.remove(bullet)
                all_sprite_list.remove(bullet)
                             
        
      
        #Story mode world 
        if current_level_now >= 2:
            #Right
            if player.rect.right >= 600:
                if current_position<=current_level.level_limit-394:
                    diff = player.rect.right - 600
                    player.rect.right = 600
                    current_level.shift_world(-diff)
                    total_diff += diff
                            
             
            #Left
            if player.rect.left <= 120:
                if current_position>120:
                    diff = 120 - player.rect.left
                    player.rect.left = 120
                    current_level.shift_world(diff)
                    total_diff -= diff   
        #Survival mode world shift
        if current_level_now == 0:  
            #Right
            if player.rect.right >= 600:
                if current_position<=current_level.level_limit-394:
                    diff = player.rect.right - 600
                    player.rect.right = 600
                    current_level.shift_world(-diff)
                    total_diff += diff
                
 
            #Left
            if player.rect.left <= 120:
                if current_position>120:
                    diff = 120 - player.rect.left
                    player.rect.left = 120
                    current_level.shift_world(diff)
                    total_diff -= diff
                
        #BGM
        playing = pygame.mixer.music.get_busy()            
        if playing==False:
            
            if current_level_now==2:
                pygame.mixer.music.load(os.path.join("music","introBGM.mp3"))
                pygame.mixer.music.play(-1,0.0)                
            if current_level_now==3:
                pygame.mixer.music.load(os.path.join("music","rd1BGM1.mp3"))
                pygame.mixer.music.play(-1,0.0)
            if current_level_now==5:
                pygame.mixer.music.load(os.path.join("music","rd1BGM2.mp3"))
                pygame.mixer.music.play(-1,0.0)         
            if current_level_now==6:
                pygame.mixer.music.load(os.path.join("music","rd2BGM1.mp3"))
                pygame.mixer.music.play(-1,0.0)           
            if current_level_now==8:
                pygame.mixer.music.load(os.path.join("music","rd2BGM2.mp3"))
                pygame.mixer.music.play(-1,0.0)     
            if current_level_now==9:
                pygame.mixer.music.load(os.path.join("music","rd3BGM1.mp3"))
                pygame.mixer.music.play(-1,0.0)         
            if current_level_now==11:
                pygame.mixer.music.load(os.path.join("music","rd3BGM2.mp3"))
                pygame.mixer.music.play(-1,0.0) 
            if current_level_now==12:
                pygame.mixer.music.load(os.path.join("music","rd4BGM1.mp3"))
                pygame.mixer.music.play(-1,0.0)           
            if current_level_now==14:
                pygame.mixer.music.load(os.path.join("music","rd4BGM2.mp3"))
                pygame.mixer.music.play(-1,0.0)        
            if current_level_now==15:
                pygame.mixer.music.load(os.path.join("music","rd5BGM1.mp3"))
                pygame.mixer.music.play(-1,0.0)           
            if current_level_now==16:
                pygame.mixer.music.load(os.path.join("music","rd5BGM2.mp3"))
                pygame.mixer.music.play(-1,0.0)         

        #Can't pass the boss room without defeat the boss
        if current_level_now>=2:
            if len(current_level.boss_list)==0:
                next_level=True

            elif len(current_level.boss_list)!=0:
                next_level=False                
            if current_level_now==16:
                if len(current_level.boss_list)==0:
                    done2=True
                    done5=False 
        #Story mode level update
        if current_position > current_level.level_limit and current_level_now<len(level_list)-1 and next_level ==True:
            player.rect.x = 0  #reset to start pos
            current_position = 0
            total_diff=0
            if current_level_now == 11:
                Dialogue.display1("You must have picked up an explosive fungi on the way. It now follows you around and explodes every second.")
            if current_level_now == 10:
                Dialogue.display1("Careful! There is a ninja ahead. He looks tough. Do what you can to keep going.")
            if current_level_now == 11:
                Dialogue.display1("You must have picked up an explosive fungi on the way. It now follows you around and explodes every second")
            if current_level_now == 14:
                Dialogue.display1("You are about to enter a guarded structure. Use your cleverness to help you move to the right. Watch out for blasts!")                       
            if (current_level_now ==2) or (current_level_now ==4) or (current_level_now ==5) or (current_level_now == 7) or (current_level_now ==8) or (current_level_now ==10) or (current_level_now ==11) or (current_level_now ==13) or (current_level_now ==14) or (current_level_now ==15):
                pygame.mixer.music.fadeout(1500)              
            current_level_now += 1
            current_level = level_list[current_level_now]
            player.level = current_level
            hp_player = hp_bar(player.hp / 120 * 300,15,0,100)
            current_level.hp_bar_group_player.add(hp_player)
            if gun_num == 1:
                ammo_left = hp_bar(ammo1 / 50 *200,15,0,150)
            if gun_num == 2:
                ammo_left = hp_bar(ammo2 / 30 *200,15,0,150)
            if gun_num == 3:
                ammo_left = hp_bar(ammo3 / 30 *200,15,0,150)
            if gun_num == 4:
                ammo_left = hp_bar(ammo4 / 12 *200,15,0,150)                    
            current_level.hp_bar_group_ammo.add(ammo_left)
            for hp1 in current_level.hp_bar_group_ammo:
                    hp1.length1 += 1                  
            if len( current_level.boss_list) > 0: 
                for boss in current_level.boss_list:                    
                    hp_bar1 = hp_bar(boss.hp / 200 *600,25,200,200)
                    current_level.hp_bar_group.add(hp_bar1)
                    


        #Challenge mode boss update. Create another boss when the boss is killed
        if current_level_now==1:
            if current_level.boss_num<len(current_level.bossList):
                if len(current_level.boss_list)==0:
                    current_level.boss_list.add(current_level.bossList[current_level.boss_num])
                    player.hp += 30
                    current_level.boss_num += 1
                    if current_level.boss_num == 5:
                        current_level.boss_num = 0
                    hp_bar1 = hp_bar(600,25,200,200)
                    current_level.hp_bar_group.add(hp_bar1)               
        #drawing codes
        current_level.draw(screen)  
        all_sprite_list.draw(screen)
        
        
        #give users checkpoints and weapons as they advance
        if current_level_now ==15:
            rd5 = True
        if current_level_now ==12:
            rd4 = True                
            gun_limit = 4
            Text.display("Press Q to change weapon. You may have picked up a new gun on the way!", WHITE, [200,50], 25)
        if current_level_now ==9:
            rd3 = True
            gun_limit = 3
            Text.display("Press Q to change weapon. You may have picked up a new gun on the way!", WHITE, [200,50], 25)
        if current_level_now == 6:
            rd2 = True 
            gun_limit = 2
            Text.display("Press Q to change weapon. You may have picked up a new gun on the way!", WHITE, [200,50], 25)
        if current_level_now ==3:
            rd1 = True    


        #General information for player is shown on the screen
        if current_level_now <2:
            Text.display("You are on Level " + str(current_level_now + 1), BLACK, [0,0], 25)
            Text.display("player's hp: " + str(player.hp), BLACK, [0,75], 25)
            Text.display("Your score: " + str(current_pos - 90 + player.hit_num*500 + player.gold_num * 100 ), BLACK, [0,25], 25)            
            if gun_num == 1:
                Text.display("Submachine gun Ammo Left: ", BLACK, [0,125], 25)
            if gun_num == 2:
                Text.display("Machine Gun Ammo Left: ", BLACK, [0,125], 25)        
    
            if gun_num == 3:
                Text.display("Shotgun Ammo Left: ", BLACK, [0,125], 25) 
            if gun_num == 4:
                Text.display("Rocket Launcher Ammo Left: ", BLACK, [0,125], 25)            
        else:
            Text.display("You are on Level " + str(current_level_now - 1), WHITE, [0,0], 25)
            Text.display("player's hp: " + str(player.hp), WHITE, [0,75], 25)
            Text.display("Your score: " + str(current_pos - 90 + player.hit_num*500 + player.gold_num * 100 ), WHITE, [0,25], 25)
            if gun_num == 1:
                Text.display("Submachine gun Ammo Left: ", WHITE, [0,125], 25)
            if gun_num == 2:
                Text.display("Machine Gun Ammo Left: ", WHITE, [0,125], 25)        
        
            if gun_num == 3:
                Text.display("Shotgun Ammo Left: ", WHITE, [0,125], 25) 
            if gun_num == 4:
                Text.display("Rocket Launcher Ammo Left: ", WHITE, [0,125], 25) 
        #Introduction for levels.
        if current_level_now == 5:
                Text.display("Defeat the dragon with the gun you have", WHITE, [0,225],50)   
      
        if current_level_now == 3:
                        Text.display("Those enemies cost you health points! Keep an eye on hp bar!", WHITE, [0,225],25) 
        if current_level_now == 14:
                        Text.display("Good luck in this level, as the black holes conjured by The Dark Lady can seriously limit your", WHITE, [0,225],25)    
                        Text.display("movement if you're unlucky.", WHITE, [0,260],25)
        if current_level_now == 14:
            Text.display("Beware the orange swords! They pull you back!", WHITE, [0,225],25)  

       #Instruction
        if current_level_now <=2 :
            if current_position <= 400:
                Text.display("Press W to jump, double press for double jump", WHITE, [0,450], 25)
                Text.display("Press A to walk left", WHITE, [0,480], 25)
                Text.display("Press D to walk right", WHITE, [0,510], 25)
                Text.display("Or use the arrow keys", WHITE, [0,540], 25)
                Text.display("Press Q to change the weapon. Be surprised!", WHITE, [0,570], 25)
                
            elif current_position > 400 and current_position < 1000:
                Text.display("Use the mouse to aim and shoot", WHITE, [0,450], 25)
                Text.display("Use left shift to screw. (Only when you are moving)", WHITE, [0,480], 25)
            elif current_position> 1000:
                Text.display("Do you know: the right timing of the double pressing of the W or UP key make you jump higher.", WHITE, [0,450], 25)            
        if ammo1 < 10:
            Text.display("Press r to reload the weapon", WHITE, [0,450], 25)
        if startFiring == True and (gun_num == 3 or gun_num == 2):
            Text.display("Click and hold the mouse: the weapon needs to heat up.", WHITE, [0,600], 25)
            
        #Check if player is died.
        if player.hp <= 0:
            done2 = True
            
            if current_level_now >= 1:
                    done3 = True
                    done4 = False
                    
            elif current_level_now < 1:
                    done3 = False
                    done4 = True        
        #Dialogue.display()
        clock.tick(60)
        
        
        pygame.display.flip()
    pygame.init()    
    #End image for challenge and survival mode.
    while not done3:
        for event in pygame.event.get():
            #Back to start menu
            if event.type == pygame.QUIT:
                done3 = True     
                done1 = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done3 = True
                    done1 = False
        #Display end image
        End_screen.display()
        clock.tick(60)
        pygame.display.flip()
    #Dead end image for story mode.
    while not done4:
        for event in pygame.event.get():
            #Back to start menu
            if event.type == pygame.QUIT:
                done4 = True     
                done1 = False
            elif event.type == pygame.KEYDOWN:
               
                    done4 = True
                    done1 = False
        #Display end image
        End_screen_stmode.display()
        clock.tick(60)            
            
        pygame.display.flip()
    #Winning end image for story mode.
    while not done5:
        for event in pygame.event.get():
            #Back to start menu
            if event.type == pygame.QUIT:
                done5 = True     
                done1 = False
            elif event.type == pygame.KEYDOWN:

                    done5 = True
                    done1 = False
        #Display end image
        End_screen_stmode1.display()
        clock.tick(60)            
            
        pygame.display.flip() 
    #done3 = True
    pygame.quit()  
    
pygame.quit()     
        
