

class Boundary():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        if self.w < 0:
            self.x = x + w
            self.w = abs(w)
        
        if self.h < 0:
            self.y = y + h
            self.h = abs(h)
        


class QuadTree():
    def __init__(self, boundary, capacity, level):
        self.boundary = boundary
        self.points = []
        self.capacity = capacity
        self.divided = False
        self.num_points = 0
        self.level = level

    def subdivide(self):
        boundary = Boundary(self.boundary.x + self.boundary.w/2, self.boundary.y, self.boundary.w/2, self.boundary.h/2)
        self.northeast = QuadTree(boundary, self.capacity, self.level+1)

        boundary = Boundary(self.boundary.x, self.boundary.y, self.boundary.w/2, self.boundary.h/2)
        self.northwest = QuadTree(boundary, self.capacity, self.level+1)

        boundary = Boundary(self.boundary.x + self.boundary.w/2, self.boundary.y + self.boundary.h/2, self.boundary.w/2, self.boundary.h/2)
        self.southeast = QuadTree(boundary, self.capacity, self.level+1)

        boundary = Boundary(self.boundary.x, self.boundary.y + self.boundary.h/2, self.boundary.w/2, self.boundary.h/2)
        self.southwest = QuadTree(boundary, self.capacity, self.level+1)


    def within_bounds(self, boundary, point):
        if (point[0] >= boundary.x and point[0] <= boundary.x + boundary.w) and (point[1] >= boundary.y and point[1] <= boundary.y + boundary.h):
            return True
        
        return False



    def insert_point(self, point):

        if self.within_bounds(self.boundary, point):
            self.num_points += 1
        else:
            return

        if len(self.points) < self.capacity:
            self.points.append(point)
        else: # If over capacity, sub-divide
            if not self.divided:
                self.subdivide()
                self.divided = True
            
            self.northeast.insert_point(point)
            self.northwest.insert_point(point)
            self.southeast.insert_point(point)
            self.southwest.insert_point(point)

    def return_contained_points(self, search_boundary, contained_points):
        def check_range(quadtree, search_boundary, contained_points):
            for i in range(0, len(quadtree.points)):
                if quadtree.within_bounds(search_boundary, quadtree.points[i]):
                    contained_points.append(quadtree.points[i])
            return contained_points

        contained_points = check_range(self, search_boundary, contained_points)

        if self.divided:
            contained_points = self.northeast.return_contained_points(search_boundary, contained_points)
            contained_points = self.northwest.return_contained_points(search_boundary, contained_points)
            contained_points = self.southeast.return_contained_points(search_boundary, contained_points)
            contained_points = self.southwest.return_contained_points(search_boundary, contained_points)

        return contained_points






    
def show(quadtree, surface, search_boundary, contained_points, pygame):

    # If top-level of tree
    if quadtree.level == 0:
        contained_points = quadtree.return_contained_points(search_boundary, [])
        pygame.Surface.fill(surface, [0,0,0])
    

    # Draw boundary of tree node
    rect_dim = [quadtree.boundary.x, quadtree.boundary.y, quadtree.boundary.w, quadtree.boundary.h]
    pygame.draw.rect(surface, [255, 0, 0], pygame.Rect(rect_dim), width=1)


    # Draw points in different colors
    for i in range(0, len(quadtree.points)):
        if quadtree.divided:
            color = [0, 255, 0]
        else:
            color = [0, 0, 255]

        if quadtree.points[i] in contained_points:
            color = [255, 255, 255]

        pygame.draw.circle(surface, color, quadtree.points[i], 2)

    # Perform recursion if tree node has child nodes
    if quadtree.divided:
        show(quadtree.northeast, surface, search_boundary, contained_points, pygame)
        show(quadtree.northwest, surface, search_boundary, contained_points, pygame)
        show(quadtree.southeast, surface, search_boundary, contained_points, pygame)
        show(quadtree.southwest, surface, search_boundary, contained_points, pygame)

    if quadtree.level == 0:
        print(search_boundary.x, search_boundary.y, search_boundary.w, search_boundary.h)
        pygame.draw.rect(surface, [0, 255, 255], pygame.Rect(search_boundary.x, search_boundary.y, search_boundary.w, search_boundary.h), width=1)
    
                




def quadtree_test():
    WIDTH = 1200
    HEIGHT = 600
    boundary = Boundary(0, 0, WIDTH, HEIGHT)


    import pygame, sys
    pygame.init()
    surface = pygame.display.set_mode((WIDTH,HEIGHT))
    search_boundary = Boundary(-10, -10, 0, 0)
    myTree = QuadTree(boundary, 1, 0)
    redraw = True
    contained_points = []
    fps = 60
    clock = pygame.time.Clock()
    init_pos = [0, 0]

    


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


            pos = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()[0]:
                myTree.insert_point(pos)
                redraw = True

            if pygame.mouse.get_pressed()[1]:
                search_boundary = Boundary(init_pos[0], init_pos[1], pos[0]-init_pos[0], pos[1]-init_pos[1])
                redraw = True


            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]:
                init_pos = pos
                search_boundary = Boundary(init_pos[0], init_pos[1], 0, 0)


            if redraw:
                show(myTree, surface, search_boundary, contained_points, pygame)  
                pygame.display.flip()
                redraw = False              
                

        clock.tick(fps)


if __name__ == "__main__":

    quadtree_test()