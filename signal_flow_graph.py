import pygame
import sys
from node import Node
from button import Button
from CalculateTransferFunction import *

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def SigFlowGraph():
    vertexCount = 0
    Vertices = []
    Edges = []

    dims = 1280, 720
    black = 0, 0, 0
    white = 255, 255, 255

    connecting = False
    drawing = False
    dragging = False
    moved = False
    dragging_index = 0
    selecting = False
    selecting_pos = None
    selected = []
    editing = False
    editing_weight = False
    editing_information = (0, 0)
    current_value = ""
    current_weight_value = ""

    getTransferFunction = Button(image=pygame.image.load("assets/GTF Rect.png"), pos=(650, 650), 
                            text_input="GET TRANSFER FUNCTION", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 20)



    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(dims)

    while True:
        screen.fill(black)
        
        if not editing:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if getTransferFunction.checkForInput(MENU_MOUSE_POS):
                        calculateTransferFunction(Vertices)
                        pass
                    
                    elif event.button == 1:
                        mouse_x, mouse_y = event.pos
        
                        i = 0

                        if connecting:
                            starting_index = dragging_index

                        dragging_index = None

                        f = False
                        for ver in Vertices:
                            if ver.is_inside(mouse_x, mouse_y):
                                if not connecting:
                                    dragging = True
                                    moved = False
                                    dragging_index = i
                                    starting_x = mouse_x
                                    starting_y = mouse_y
                                else:
                                    dragging_index = i
                                f = True
                                break
                            i += 1

                        if not f:
                            for ver in Vertices:
                                x = ver.get_selected_arc_destination(mouse_x, mouse_y)
                                if x != None:
                                    selected = []
                                    editing = True
                                    editing_information = (ver, x)
                                    current_value = str(ver.get_edge_weight(x))
                                    break

                            if not editing:
                                selecting = True
                                selecting_pos = event.pos
                                selected = []

                    if connecting:
                        if dragging_index != None:
                            Vertices[starting_index].edit_edge(Vertices[dragging_index], 1, True)
                            print(starting_index, dragging_index)
                        connecting = False

                    elif event.button == 3:
                        selected = []
                        mouse_x, mouse_y = event.pos
                        vertexCount += 1
                        Vertices.append(Node(vertexCount, mouse_x, mouse_y))

                    elif event.button == 2:
                        pass

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if dragging and not moved:
                            connecting = True
                            selected = []

                        dragging = False
                        selecting = False
                elif event.type == pygame.MOUSEMOTION:
                    if drawing:
                        mouse_x, mouse_y = event.pos
                        drawing_w = mouse_x - starting_x
                        drawing_h = mouse_y - starting_y 
                    if dragging:
                        moved = True
                        mouse_x, mouse_y = event.pos
                        vec_x = mouse_x - starting_x
                        vec_y = mouse_y - starting_y
                        
                        if Vertices[dragging_index] in selected:
                            for n in selected:
                                n.translate(vec_x, vec_y)
                        else:
                            selected = []
                            Vertices[dragging_index].translate(vec_x, vec_y)

                        starting_x = mouse_x
                        starting_y = mouse_y
                    if selecting:
                        selected = []
                        for a in Vertices:
                            if a.is_inside_selection(pygame.Rect(selecting_pos, (mouse_x-selecting_pos[0],mouse_y-selecting_pos[1]))):
                                selected.append(a)
                
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        editing = False
                    elif event.key == pygame.K_BACKSPACE:
                        current_value = current_value[:-1]
                    else:
                        if(event.unicode in ['1','2','3','4','5','6','7','8','9','+','-','*','/','(',')','^', 's']):
                            current_value += event.unicode

            editing_information[0].edit_edge(editing_information[1], current_value, True)

            if editing_weight:
                if isinstance(editing_information[0], Node):
                    pygame.draw.rect(screen, white, (editing_information[0].pos_x - 40, editing_information[0].pos_y - 30, 80, 20))
                    weight_text_surface = myfont.render(current_weight_value, False, black)
                    weight_text_rect = weight_text_surface.get_rect(center=(editing_information[0].pos_x, editing_information[0].pos_y - 20))

                    # Check if the mouse is hovering over the weight text
                    if weight_text_rect.collidepoint(pygame.mouse.get_pos()):
                        weight_text_surface = myfont.render(current_weight_value, False, (255, 255, 0))  # Highlight the weight text
                    
                    screen.blit(weight_text_surface, weight_text_rect)
                else:
                    # Handle case when editing_information[0] is an integer
                    pass



        for ver in Vertices:
            ver.highlight_arc()
        
        if selecting:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pygame.draw.rect(screen, (200,200,200), pygame.Rect(selecting_pos, (mouse_x-selecting_pos[0],mouse_y-selecting_pos[1])),1)

        for ver in Vertices:
            ver.render_edge(screen, pygame.mouse.get_pos())
            ver.render(screen)

            if connecting:
                pygame.draw.line(screen, white, (starting_x, starting_y), pygame.mouse.get_pos())

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        getTransferFunction.changeColor(MENU_MOUSE_POS)
        getTransferFunction.update(screen)
        pygame.display.update()
        clock.tick(60)




