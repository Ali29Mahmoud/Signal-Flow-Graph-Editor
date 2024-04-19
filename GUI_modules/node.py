import pygame
import math


WHITE = 255,255,255

class Node:
    def __init__(self, id, pos_x, pos_y):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = 15
        self.arc_radius = 12
        self.edges = []
        self.hl_rzcs = []

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Arial', 20)
        self.textFont = pygame.font.SysFont('Arial', 30)
        self.rect = pygame.Rect(pos_x - self.radius, pos_y - self.radius, self.radius * 2, self.radius * 2)
        
    def render(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.pos_x, self.pos_y), self.radius, 0)
        
        # Render text
        text_surface = self.myfont.render(str(self.id), False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.pos_x, self.pos_y))
        screen.blit(text_surface, text_rect)


    def get_edge_weight(self, dest_obj):
        for a in self.edges:
            if a[0] == dest_obj:
                return a[1]
        return None
    
    def translate(self, comp_x, comp_y):
        self.pos_x += comp_x
        self.pos_y += comp_y


    def get_position(self):
        return (self.pos_x, self.pos_y)
    
    def is_inside_selection(self, rect):
        l = rect.x-self.radius
        t = rect.y-self.radius
        r = rect.x+rect.w+self.radius
        b = rect.y+rect.h+self.radius

        if l > r:
            l,r = r,l
        if t > b:
            t,b = b,t

        if self.pos_x < l or self.pos_x > r:
            return False
        if self.pos_y < t or self.pos_y > b:
            return False
        return True
    
    def is_inside(self, point_x, point_y):
        d = math.sqrt((point_x - self.pos_x)**2 + (point_y - self.pos_y)**2)

        if d > self.radius:
            return False

        return True
    
    
    def add_edge(self, dest_obj, weight, displayed):
        self.edges.append([dest_obj, weight, displayed])

        
    def edit_edge(self, dest_obj, weight, displayed):

        found = False
        for a in self.edges:
            if a[0] == dest_obj:
                found = True
                a[1] = weight  # Update the weight
                a[2] = displayed
                break

        if not found:
            self.add_edge(dest_obj, weight, displayed)

    def highlight_arc(self, destination=None,callback=True):
        if destination == None:
            self.hl_arcs = []
        else:
            if callback:
                destination.highlight_arc(self,False)

            for a in self.arcs:
                if a[0] == destination:
                    self.hl_arcs.append(a)

    def render_edge(self, screen, mouse_pos):
        cx = 0
        cy = 0
        for a in self.edges:
            if a[2]:  # Checking if the edge should be rendered
                if self.id == a[0].id:  # Circular edge
                    x1, y1 = self.get_position()
                    loopRadius = 40
                    y1 -= loopRadius
                    pygame.draw.circle(screen, WHITE, (x1, y1), loopRadius, 2)
                    
                    # Render the weight text for circular edge
                    cx = int(x1)
                    cy = int(y1 - loopRadius - 10)
                    text_surface = self.textFont.render(str(a[1]), False, (255, 255, 40))
                    text_rect = text_surface.get_rect(center=(cx, cy))
                    screen.blit(text_surface, text_rect)
                else:
                    x1, y1 = self.get_position()
                    x2, y2 = a[0].get_position()
                    c1, c2 = ((x1+x2)/2, (y1+y2)/2 - 50 * (x2-x1)/200)

                    # Draw the curve
                    self.draw_curve(screen, (x1, y1), (x2, y2), (c1, c2), WHITE)

                    # Draw the arrowhead at the end of the curve
                    arrow_length = 10

                    temp_x1, temp_y1 = self.get_edge_points(x1,x2,y1,y2,0.94)
                    temp_x2, temp_y2 = self.get_edge_points(x1,x2,y1,y2,0.96)
                    angle = math.atan2(temp_y2 - temp_y1, temp_x2 - temp_x1)

                    t = 0.95  # Adjust this value to change the position of the weight along the curve
                    end_x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * c1 + t ** 2 * x2
                    end_y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * c2 + t ** 2 * y2
                    arrow_angle = math.pi / 6  # Angle of the arrowhead
                    arrowhead_points = [
                        (end_x - arrow_length * math.cos(angle - arrow_angle), end_y - arrow_length * math.sin(angle - arrow_angle)),
                        (end_x, end_y),
                        (end_x - arrow_length * math.cos(angle + arrow_angle), end_y - arrow_length * math.sin(angle + arrow_angle))
                    ]
                    pygame.draw.polygon(screen, (255, 255, 255), arrowhead_points)

                    cx, cy = mid_x, mid_y = self.get_edge_points(x1,x2,y1,y2,0.5)


                    # Draw the weight text along the curve
                    text_surface = self.textFont.render(str(a[1]), False, (255, 255, 40))
                    text_rect = text_surface.get_rect(center=(int(mid_x), int(mid_y)))
                    screen.blit(text_surface, text_rect)

        d = math.sqrt((cx - mouse_pos[0])**2 + (cy - mouse_pos[1])**2)
        if d < self.arc_radius:
                    pygame.draw.circle(screen, (255,255,255), (cx, cy),self.arc_radius, 0)





    def get_selected_arc_destination(self, pos_x, pos_y):
        for a in self.edges:
            if a[2]:
                # Check if the edge is a circular edge
                if self.id == a[0].id:
                    # Calculate the center and radius of the circular arc
                    arc_center_x, arc_center_y = self.get_position()
                    arc_radius = 10  # Adjust as needed
                    # Calculate the distance between the click and the center of the arc
                    d = math.sqrt((arc_center_x - pos_x)**2 + ((arc_center_y - 90) - pos_y)**2)
                    # If the distance is within the radius of the circular arc, return the current node
                    if d < arc_radius:
                        return self
                else:
                    # For normal edges, calculate if the click falls within the bounding box of the edge
                    x1, y1 = self.get_position()
                    x2, y2 = a[0].get_position()
                    c1, c2 = ((x1+x2)/2, (y1+y2)/2 - 50 * (x2-x1)/200)
                    t = 0.5  # Adjust this value to change the position of the weight along the curve
                    mid_x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * c1 + t ** 2 * x2
                    mid_y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * c2 + t ** 2 * y2

                    d = math.sqrt((mid_x - pos_x)**2 + (mid_y - pos_y)**2)
                    if d < self.arc_radius:
                        return a[0]

        return None
    
    def draw_curve(self, screen, start, end, control, color):
    # Draw curve using quadratic Bezier curve
        for t in range(0, 501, 1):
            t /= 500.0
            x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0] 
            y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1] 
            pygame.draw.circle(screen, color, (int(x), int(y)), 1)

    def get_edge_points(self,x1,x2,y1,y2,t):
        c1, c2 = ((x1+x2)/2, (y1+y2)/2 - 50 * (x2-x1)/200)
        point_x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * c1 + t ** 2 * x2
        point_y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * c2 + t ** 2 * y2

        return point_x, point_y



        
