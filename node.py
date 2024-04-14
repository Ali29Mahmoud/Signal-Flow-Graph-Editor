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
        for a in self.edges:
            if a[2]:
                if self.id == a[0].id:
                    # Circular edge
                    x1, y1 = self.get_position()
                    loopRadius = 40
                    y1 -= loopRadius
                    pygame.draw.circle(screen, WHITE, (x1, y1), loopRadius, 2)
                    
                    # Render the weight text for circular edge
                    cx = int(x1)
                    cy = int(y1 - loopRadius - 10)
                    text_surface = self.myfont.render(str(a[1]), False, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(cx, cy))
                    screen.blit(text_surface, text_rect)
                else:
                    # Normal edge
                    x1, y1 = self.get_position()
                    x2, y2 = a[0].get_position()

                    # Calculate angle of the edge
                    angle = math.atan2(y2 - y1, x2 - x1)

                    # Calculate the endpoint of the arrowhead at the border of the destination node
                    arrow_length = 10
                    end_x = x2 - (a[0].radius + arrow_length) * math.cos(angle)
                    end_y = y2 - (a[0].radius + arrow_length) * math.sin(angle)

                    # Draw the edge line
                    pygame.draw.line(screen, (255, 255, 255), (x1, y1), (end_x, end_y), 2)

                    # Draw the arrowhead
                    arrow_angle = math.pi / 6  # Angle of the arrowhead
                    arrowhead_points = [
                        (end_x - arrow_length * math.cos(angle - arrow_angle), end_y - arrow_length * math.sin(angle - arrow_angle)),
                        (end_x, end_y),
                        (end_x - arrow_length * math.cos(angle + arrow_angle), end_y - arrow_length * math.sin(angle + arrow_angle))
                    ]
                    pygame.draw.polygon(screen, (255, 255, 255), arrowhead_points)

                    # Draw the weight text
                    cx = int((x1 + end_x) / 2)
                    cy = int((y1 + end_y) / 2)
                    text_surface = self.myfont.render(str(a[1]), False, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(cx, cy))
                    screen.blit(text_surface, text_rect)



    def get_selected_arc_destination(self, pos_x, pos_y):
        for a in self.edges:
            if a[2]:
                # Check if the edge is a circular edge
                if self.id == a[0].id:
                    # Calculate the center and radius of the circular arc
                    arc_center_x, arc_center_y = self.get_position()
                    arc_radius = 40  # Adjust as needed
                    # Calculate the distance between the click and the center of the arc
                    d = math.sqrt((arc_center_x - pos_x)**2 + (arc_center_y - pos_y)**2)
                    # If the distance is within the radius of the circular arc, return the current node
                    if d < arc_radius:
                        return self
                else:
                    # For normal edges, calculate if the click falls within the bounding box of the edge
                    x1, y1 = self.get_position()
                    x2, y2 = a[0].get_position()
                    cx = int((x1 + x2)/2)
                    cy = int((y1 + y2)/2)
                    d = math.sqrt((cx - pos_x)**2 + (cy - pos_y)**2)
                    if d < self.arc_radius:
                        return a[0]

        return None

        
