from RouthCriterionScreen import *
from GUI_modules.node import Node
from Logic.CalculateTransferFunction import *
from RouthCriterionScreen import *


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def increment_one_recursive(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.append(increment_one_recursive(item))
        elif isinstance(item, int):
            result.append(item + 1)
        else:
            result.append(item)
    return result

def result_screen(paths_loops, deltas, tf):
    result_dims = 1280, 720
    res_screen = pygame.display.set_mode(result_dims)
    res_screen.fill((0, 0, 0))

    headline_text = get_font(30).render("Results", True, (255, 255, 255))
    headline_text_rect = headline_text.get_rect(center=(result_dims[0] // 2, result_dims[1] // 2 - 300))

    paths_loops_text = get_font(16).render("The Paths and Loops are: " + paths_loops, True, (255, 255, 255))
    paths_loops_text_rect = headline_text.get_rect(center=(result_dims[0] // 2 - 450, result_dims[1] // 2 - 150))
    
    deltas_text = get_font(16).render("The Deltas are: " + deltas, True, (255, 255, 255))
    deltas_text_rect = headline_text.get_rect(center=(result_dims[0] // 2 - 450, result_dims[1] // 2 + 100))

    
    tf_text = get_font(16).render("The Transfer function is: " + tf, True, (255, 255, 255))
    tf_text_rect = headline_text.get_rect(center=(result_dims[0] // 2 - 450, result_dims[1] // 2 + 150 + 100))
    
    ret_text = get_font(16).render("PRESS ESC TO RETURN", True, (204, 0, 0))
    ret_text_rect = headline_text.get_rect(center=(result_dims[0] // 2 - 40, result_dims[1] // 2 + 300))


    res_screen.blit(headline_text, headline_text_rect)
    res_screen.blit(deltas_text, deltas_text_rect)
    res_screen.blit(paths_loops_text, paths_loops_text_rect)
    res_screen.blit(tf_text, tf_text_rect)
    res_screen.blit(ret_text, ret_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Close the pop-up screen

        pygame.display.update()

def SigFlowGraph():
    vertexCount = 0
    Vertices = []
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
    
    CLEAR = Button(image=pygame.image.load("assets/CLEAR Rect.png"), pos=(200, 650), 
                            text_input="CLEAR", font=get_font(15), base_color="#cc0000", hovering_color="White")
    
    SFG_BACK = Button(image = None, pos=(80, 50), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")


    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 20)



    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(dims)


    while True:
        screen.fill(black)

        if not editing:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if SFG_BACK.checkForInput((mouse_x, mouse_y)):
                        main_menu()
                        
                    if getTransferFunction.checkForInput(MENU_MOUSE_POS):

                        paths_loops , deltas ,tf = calculateTransferFunction(Vertices)
                        paths_loops = increment_one_recursive(paths_loops)
                        
                        deltas_string = "Δ =" + str(deltas[0]) + "\n\n"

                        loops = ""

                        loopsCount = 0
                        for x in paths_loops[1]:
                            nodesCount = 0
                            loopsCount += 1 
                            loops += "Loop_" + str(loopsCount) + ": "
                            for y in x[0]:
                                nodesCount += 1
                                loops += str(y)
                                if(nodesCount < len(x[0])):
                                    loops += " -> "

                            loops += " -> "
                            loops += str(x[0][0])
                            
                            if(loopsCount < len(paths_loops[1])):
                                loops += " && "

                            if(loopsCount % 2 == 0):
                                loops += "\n\n"



                        index = 1
                        for x in deltas[1]:
                            deltas_string += "Δ_" + str(index) + " = " + str(x)

                            if(index < len(deltas[1])):
                                deltas_string += ", "
                            
                            if(index % 2 == 0):
                                deltas_string += "\n\n"
                            
                            index += 1 

                        result_string = ""
                        pathsCount = 0

                        for paths in paths_loops[0]:
                            count = 0
                            for node in paths[0]:
                                count += 1
                                result_string += str(node)

                                if count < len(paths[0]):
                                    result_string += " -> "
                            
                            pathsCount += 1

                            if(pathsCount < len(paths_loops[0])):   
                                result_string += " || "
                            
                            if(pathsCount % 2 == 0):
                                result_string += "\n\n"

                        result_string += "\n\n" + loops
                        
                        result_screen(result_string,deltas_string,str(tf))
                        pass
                    
                    if CLEAR.checkForInput(MENU_MOUSE_POS):
                        vertexCount = 0
                        Vertices = []
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
                        connecting = False

                    elif event.button == 3:
                        selected = []
                        mouse_x, mouse_y = event.pos
                        vertexCount += 1
                        Vertices.append(Node(vertexCount, mouse_x, mouse_y))

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
            instruction_text = get_font(16).render("PRESS ENTER TO CONFIRM", True, (204, 0, 0))
            instruction_text_rect = instruction_text.get_rect(center=(dims[0] // 2, dims[1] // 2 - 300))
            screen.blit(instruction_text, instruction_text_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        editing = False
                    elif event.key == pygame.K_BACKSPACE:
                        current_value = current_value[:-1]
                    else:
                        if(event.unicode in ['0','1','2','3','4','5','6','7','8','9','+','-','*','/','(',')','^', 's']):
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
        CLEAR.changeColor(MENU_MOUSE_POS)
        CLEAR.update(screen)
        SFG_BACK.changeColor(MENU_MOUSE_POS)
        SFG_BACK.update(screen)
        pygame.display.update()
        clock.tick(60)

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.jpg")

def get_font(size):
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
                    RouthScreen()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()