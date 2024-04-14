import pygame

class Button():
    def __init__(self, pos, width, height, value):
        self.pos_x, self.pos_y = pos
        self.height = height
        self.width = width
        self.value = value
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Arial', 20)
        self.over_time = 0

    def is_inside(self, pos):
        tempx, tempy = pos
        if tempx < self.pos_x:
            return False
        if tempx > self.pos_x + self.width:
            return False
        if tempy < self.pos_y:
            return False
        if tempy >= self.pos_y + self.height:
            return False
        return True

    def render(self, screen, mouse_pos ,clicked):
        
        if not clicked:
            pygame.draw.rect(screen, (max(100, 255-self.over_time),max(100, 255-self.over_time),max(100, 255-self.over_time)), pygame.Rect(self.pos_x, self.pos_y, self.width, self.height), 0, 4)
            
            if self.is_inside(mouse_pos):    
                self.over_time = min(155,self.over_time + 20)
            else:
                self.over_time = max(0,self.over_time - 20)
        else:
            pygame.draw.rect(screen, (100,100,100), pygame.Rect(self.pos_x, self.pos_y, self.width, self.height), 0, 4)

        cx = self.pos_x + int(self.width/2)
        cy = self.pos_y + int(self.height/2)
        
        texts = self.myfont.render(str(self.value), False, (0,0,0))
                
        offset_x = int(texts.get_rect().width/2)
        offset_y = int(texts.get_rect().height/2)
        screen.blit(texts,(cx-offset_x, cy-offset_y))