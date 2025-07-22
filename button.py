import pygame

class Button:
    def __init__(self, x,y, image, type):
        self.image = image
        self.rect = self.image.get_rect(topleft= (x,y))
        self.type = type
        self.clicked = False


    def update(self, screen):
        click= False
        screen.blit(self.image, self.rect)

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image.set_alpha(180)
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                click = True
                self.clicked = True
            elif not pygame.mouse.get_pressed()[0]:
                self.clicked = False
            
        else:
            self.image.set_alpha(255)
        return click