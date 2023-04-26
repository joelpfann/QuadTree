

class Boundary():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        


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






    
def show(quadtree, surface, pygame):

    rect_dim = [quadtree.boundary.x, quadtree.boundary.y, quadtree.boundary.w, quadtree.boundary.h]

    color = [255, 0, 0]

    pygame.draw.rect(surface, color, pygame.Rect(rect_dim), width=1)
    
    for i in range(0, len(quadtree.points)):
        if quadtree.divided:
            color = [0, 255, 0]
        else:
            color = [0, 0, 255]
        pygame.draw.circle(surface, color, quadtree.points[i], 2)

    if quadtree.divided:
        show(quadtree.northeast, surface, pygame)
        show(quadtree.northwest, surface, pygame)
        show(quadtree.southeast, surface, pygame)
        show(quadtree.southwest, surface, pygame)

                




def quadtree_test():
    WIDTH = 1200
    HEIGHT = 600
    boundary = Boundary(0, 0, WIDTH, HEIGHT)
    search_boundary = Boundary(100, 70, 300, 200)



    import pygame, sys
    pygame.init()
    surface = pygame.display.set_mode((WIDTH,HEIGHT))

    myTree = QuadTree(boundary, 1, 0)
    

    


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


            pos = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()[0]:
                myTree.insert_point(pos)
                show(myTree, surface, pygame)
                pygame.display.flip()

            if pygame.mouse.get_pressed()[2]:
                pygame.draw.rect(surface, [0, 255, 255], pygame.Rect(search_boundary.x, search_boundary.y, search_boundary.w, search_boundary.h), width=1)
                pygame.display.flip()
                contained_points = myTree.return_contained_points(search_boundary, [])
                print(contained_points)


if __name__ == "__main__":

    quadtree_test()