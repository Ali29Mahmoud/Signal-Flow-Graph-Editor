import pygame, sys
from signal_flow_graph import *
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0)) 

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#FFFFFF")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        SFG = Button(image=pygame.image.load("assets/SFG Rect.png"), pos=(640, 250), 
                            text_input="SIGNAL FLOW GRAPH", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        RCriteria = Button(image=pygame.image.load("assets/RCriteria Rect.png"), pos=(640, 400), 
                            text_input="ROUTH CRITERIA", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [SFG, RCriteria, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SFG.checkForInput(MENU_MOUSE_POS):
                    SigFlowGraph()
                if RCriteria.checkForInput(MENU_MOUSE_POS):
                    pass
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()