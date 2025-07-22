import sys
from pygame.sprite import Sprite
import pygame
import os
class Player(Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.animation_types = os.listdir("./Pygame Test/assets")
        self.all_images = {}
        for animation in self.animation_types:
            self.all_images[animation] = []
            for image in os.listdir(f"./Pygame Test/assets/{animation}"):
                img = pygame.image.load(f"./Pygame Test/assets/{animation}/{image}")
                img = pygame.transform.scale_by(img, 0.1)
                self.all_images[animation].append(img)
        self.current_animation = "Idle"
        self.current_frame = 0
        self.image = self.all_images[self.current_animation][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_animation_time = pygame.time.get_ticks()
        self.animation_state = "Idle"
        self.direction = 1
        self.flip = False
        self.in_air = False
        self.y_vel = 0
        self.attack = False
        self.attack_time = pygame.time.get_ticks()
        self.jump = False
        

    def update(self, screen, boxes, obstacles, bomb, energy):
        pygame.draw.line(screen, "red", (0,500), (1000,500), 1)
        pygame.draw.rect(screen, "blue", self.rect, 2)
        screen.blit(
            pygame.transform.flip(self.image, self.flip, False) 
            , self.rect)
        self.image = self.all_images[self.current_animation][self.current_frame]
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > 100:
            self.last_animation_time = pygame.time.get_ticks()
            self.current_frame += 1
        if self.current_frame >= len(self.all_images[self.current_animation]):
            self.current_frame = 0

        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and (keys[pygame.K_LSHIFT]):
            self.direction = -1
            self.animation_state = "Walk" 
            self.flip = True  
            dx -= 5
        elif keys[pygame.K_a] :
            self.direction = -1
            self.animation_state = "Run" 
            self.flip = True  
            dx -= 10
        if keys[pygame.K_d] and (keys[pygame.K_LSHIFT]):
            self.direction = 1
            self.animation_state = "Walk"
            self.flip = False
            dx += 5
        elif keys[pygame.K_d] :
            self.direction = 1
            self.animation_state = "Run"
            self.flip = False
            dx += 10
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.animation_state  = "Idle"
        
        if keys[pygame.K_SPACE] and not self.in_air:
            self.animation_state = "Jump"
            self.jump = True
            self.in_air = True
            self.y_vel = -15

        if pygame.mouse.get_pressed()[0]:
            self.attack = True
            self.attack_time = pygame.time.get_ticks()
        

        if pygame.time.get_ticks() - self.attack_time > 2000 and self.attack:
            self.attack_time = pygame.time.get_ticks()
            self.attack = False
            self.jump = False
        dy += self.y_vel
        for box in boxes.sprites():
            if self.rect.colliderect(box.rect.x , box.rect.y + dy, box.rect.size[0], box.rect.size[1]):
                self.y_vel = 0
                dy = box.rect.y - self.rect.bottom

        for obstacle in obstacles.sprites():
            if self.rect.colliderect(obstacle.rect.x , obstacle.rect.y + dy, obstacle.rect.size[0], obstacle.rect.size[1]):
                sys.exit()
                print("you died")

        for bomb in bomb.sprites():
            if self.rect.colliderect(bomb.rect.x , bomb.rect.y + dy, bomb.rect.size[0], bomb.rect.size[1]):
                sys.exit()
                print("you died")

        for energy in energy.sprites():
            if self.rect.colliderect(energy.rect.x , energy.rect.y + dy, energy.rect.size[0], energy.rect.size[1]):
                print("ENERGY")

        self.y_vel += 1
        self.rect.x += dx
        self.rect.y += dy

    def change_animation(self, animation_name):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_frame = 0
            self.last_animation_time = pygame.time.get_ticks()