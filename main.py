import pygame
from player import Player
import pickle
import os
from world import World
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Game")
clock = pygame.time.Clock() 

TILE_SIZE = 50

object_images = [
    
    pygame.transform.scale(
        pygame.image.load(f"./Pygame Test/game_world/Objects/{img}"), (TILE_SIZE, TILE_SIZE)
    ) for img in os.listdir("./Pygame Test/game_world/Objects")
]

tile_images = []
for img in os.listdir("./Pygame Test/game_world/Tiles"):
    tile_images.append(
        
            pygame.transform.scale(pygame.image.load(f"./Pygame Test/game_world/Tiles/{img}"), (TILE_SIZE, TILE_SIZE))
        
    )
object_images.extend(tile_images)

scroll = 1
level = 1
world_data = []
def load_level(level):
    global world_data
    with open(f"./Pygame Test/level{level}", "rb") as f:
        world_data = pickle.load(f)

bomb_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
energy_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
load_level(level)
game_world = World(world_data, object_images, scroll, 50, bomb_group, energy_group, box_group, obstacle_group)

my_player = Player(300, 300)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if my_player.jump  and my_player.attack:
        my_player.change_animation("JumpAttack")
    elif my_player.in_air:
        my_player.change_animation("Jump")
    elif my_player.attack and my_player.in_air == False:
        my_player.change_animation("Attack")
    elif my_player.animation_state == "Walk":
        my_player.change_animation("Walk")
    elif my_player.animation_state == "Run":
        my_player.change_animation("Run")
    elif my_player.animation_state == "Idle":
        my_player.change_animation("Idle")
    
    screen.fill(WHITE)

    my_player.update(screen, box_group, obstacle_group, bomb_group, energy_group)

    bomb_group.draw(screen)
    obstacle_group.draw(screen)
    energy_group.draw(screen)
    box_group.draw(screen)

    box_group.update()
    energy_group.update()
    bomb_group.update()
    obstacle_group.update()
    pygame.display.update()
    clock.tick(FPS)