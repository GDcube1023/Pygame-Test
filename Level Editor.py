import pygame
import os
from button import Button
import pickle


pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 600
FPS = 60
SIDE_MARGIN = 400
LOWER_MARGIN = 100
TILE_SIZE = 50
COLS = 150
ROWS = HEIGHT // TILE_SIZE

selected_btn_index = 0

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

buttons_list = []
c = 0
r = 0
for img in object_images:
    buttons_list.append(
        Button(
            WIDTH + 20 + c * 80,
            10 + r  * 80,
            img,
            "object"
        )
    )
    c +=1
    if c == 5:
        r += 1
        c = 0
for img in tile_images:
    buttons_list.append(
        Button(
            WIDTH + 20 + c * 80,
            10 + r  * 80,
            img,
            "tile"
        )
    )
    c +=1
    if c == 5:
        r += 1
        c = 0

level = 1

f = pygame.font.Font("./Pygame Test/Bruce Forever.ttf", 20)
level_text = f.render(f"level{level}", True, "black")
level_rect = level_text.get_rect(center=(50, HEIGHT + 50))

world_data = []
scroll = 0
scroll_speed = 1
scroll_left, scroll_right = (False, False)
for i in range(ROWS):
    temp = [-1] * COLS
    world_data.append(temp)

def draw_world(level):
    for i in range(len(world_data)):
        for j in range(len(world_data[i])):
            if world_data[i][j] != -1:
                screen.blit(buttons_list[world_data[i][j]].image, (j * TILE_SIZE - scroll, i * TILE_SIZE))


def draw_lines():
    for i in range(COLS + 1):
        pygame.draw.line(screen, "brown", (i * TILE_SIZE - scroll, 0), (i * TILE_SIZE - scroll, HEIGHT))
    for j in range(ROWS + 1):
        pygame.draw.line(screen, "brown", ( 0, j * TILE_SIZE), (WIDTH, j * TILE_SIZE))

screen = pygame.display.set_mode((WIDTH + SIDE_MARGIN, HEIGHT+ LOWER_MARGIN))
pygame.display.set_caption("Simple Game")
clock = pygame.time.Clock() 


up_arrow_btn = Button(
    300, HEIGHT + 30,
    pygame.transform.scale_by(
        pygame.image.load("./Pygame Test/arrow.png"),
        0.2
    ),
    "button"
)
down_arrow_btn = Button(
    350, HEIGHT + 30,
    pygame.transform.rotate(
        pygame.transform.scale_by(
        pygame.image.load("./Pygame Test/arrow.png"),
        0.2
    ), 180
    ),
    "button"
)

save_btn = Button(
    500, HEIGHT + 30,
    pygame.transform.scale_by(
        pygame.image.load("./Pygame Test/save.png"),
        0.1
    ),
    "button"
)
load_btn = Button(
    550, HEIGHT + 30,
    pygame.transform.rotate(
        pygame.transform.scale_by(
        pygame.image.load("./Pygame Test/load.png"),
        0.1
    ), 180
    ),
    "button"
)


def save_level(level):
    with open(f"./Pygame Test/level{level}", "wb") as f:
        pickle.dump(world_data, f)


def load_level(level):
    global world_data
    with open(f"./Pygame Test/level{level}", "rb") as f:
        world_data = pickle.load(f)




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_LSHIFT :
                scroll_speed = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1
    if scroll_left:
        scroll -= 5 * scroll_speed
    elif scroll_right:
        scroll += 5 * scroll_speed
    if scroll < 0:
        scroll = 0
    screen.fill((255,255,255))
    level_text = f.render(f"level  {level}", True, "black")
    draw_lines()
    pygame.draw.rect(screen, "lightblue", (WIDTH, 0, SIDE_MARGIN, HEIGHT + LOWER_MARGIN))
    pygame.draw.rect(screen, "lightblue", (0, HEIGHT, SIDE_MARGIN + WIDTH, LOWER_MARGIN))
    screen.blit(level_text, level_rect)
    for i,btn in enumerate(buttons_list):
        if btn.update(screen):
            selected_btn_index = i
    mouse_pos = pygame.mouse.get_pos()
    r = mouse_pos[1]//TILE_SIZE
    c = (mouse_pos[0] + scroll)//TILE_SIZE
    if mouse_pos[0] < WIDTH and mouse_pos[1] < HEIGHT:
        if pygame.mouse.get_pressed()[0]:
            world_data[r][c] = selected_btn_index
        elif pygame.mouse.get_pressed()[2]:
            world_data[r][c] = -1
    draw_world(level)

    if up_arrow_btn.update(screen):
        level += 1
    elif down_arrow_btn.update(screen):
        level -= 1
        if level < 0:
            level = 0        

    if save_btn.update(screen):
        save_level(level)
    if load_btn.update(screen):
        load_level(level)
    pygame.draw.rect(screen, "red", buttons_list[selected_btn_index].rect, 3)
    pygame.display.update()
    clock.tick(FPS)