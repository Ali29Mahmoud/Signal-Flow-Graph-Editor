import pygame
import sys
from GUI_modules.button import Button
from Logic.RouthHerwitzCriterion import *

black = 0, 0, 0
white = 255, 255, 255


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def get_input(screen):
    text = ''
    input_font = get_font(15)
    input_rect = pygame.Rect(pygame.display.Info().current_w // 2 - 300, pygame.display.Info().current_h // 2 - 250,
                             600, 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        pygame.draw.rect(screen, black, input_rect)

        input_surface = input_font.render("Input: " + text, True, white)

        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()


def RouthScreen():
    dims = 1280, 720
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(dims)
    stabilityCheck = Button(image=pygame.image.load("assets/GTF Rect.png"), pos=(650, 400),
                            text_input="CHECK FOR STABILITY", font=get_font(20), base_color="#d7fcd4",
                            hovering_color="White")

    insertEquation = Button(image=pygame.image.load("assets/EQN Rect.png"), pos=(650, 300),
                            text_input="ADD CHARACTERISTIC EQUATION", font=get_font(20), base_color="#d7fcd4",
                            hovering_color="White")

    result = ''
    while True:
        instruction = "PRESS ENTER WHEN YOU FINISH"
        screen.fill(black)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        stabilityCheck.changeColor(MENU_MOUSE_POS)
        stabilityCheck.update(screen)
        insertEquation.changeColor(MENU_MOUSE_POS)
        insertEquation.update(screen)

        text_surface = get_font(20).render("Enter The Characteristic Equation:", True, white)

        text_rect = text_surface.get_rect()

        text_rect.center = (dims[0] // 2, dims[1] // 2 - 300)

        screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if stabilityCheck.checkForInput(MENU_MOUSE_POS):
                    result = checkResult(user_input)
                elif insertEquation.checkForInput(MENU_MOUSE_POS):
                    result = ""
                    screen.blit(text_surface2, text_rect2)
                    user_input = get_input(screen)
                    print("User input:", user_input)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        lines = result.split('\n')
        line_height = get_font(20).get_linesize()
        y = dims[1] // 2 + 150 - (len(lines) - 1) * line_height // 2
        for line in lines:
            text_surface1 = get_font(17).render(line, True, white)
            text_rect1 = text_surface1.get_rect()
            text_rect1.centerx = dims[0] // 2
            text_rect1.y = y
            screen.blit(text_surface1, text_rect1)
            y += line_height



        text_surface2 = get_font(17).render(instruction, True, (204,0,0))
        text_rect2 = text_surface2.get_rect()
        text_rect2.center = (dims[0] // 2, dims[1] // 2 - 200)


        pygame.display.update()
        clock.tick(20)
