from QuadTree import QuadTree, Boundary, Entity
import math
import pygame, sys, random


def draw_tree_boundaries(quadtree, surface):
    rect_dim = [quadtree.boundary.x, quadtree.boundary.y, quadtree.boundary.w, quadtree.boundary.h]
    pygame.draw.rect(surface, [150, 0, 0], pygame.Rect(rect_dim), width=1)


def draw_tree_entities(quadtree, contained_entities, surface):
    for i in range(0, len(quadtree.entities)):
        if quadtree.divided:
            color = [0, 255, 0]
        else:
            color = [0, 0, 255]

        if quadtree.entities[i] in contained_entities:
            color = [255, 255, 255]

        pygame.draw.circle(surface, color, [quadtree.entities[i].x, quadtree.entities[i].y], 3)



def show(quadtree, surface, search_boundary, contained_entities, draw_NN):

    

    # If top-level of tree draw black screen
    if quadtree.level == 0:        
        pygame.Surface.fill(surface, [0,0,0])
    

    # Draw boundary of tree node
    draw_tree_boundaries(quadtree, surface)


    # Draw entities in different colors
    draw_tree_entities(quadtree, contained_entities, surface)

    # Perform recursion if tree node has child nodes
    if quadtree.divided:
        show(quadtree.northeast, surface, search_boundary, contained_entities, draw_NN)
        show(quadtree.northwest, surface, search_boundary, contained_entities, draw_NN)
        show(quadtree.southeast, surface, search_boundary, contained_entities, draw_NN)
        show(quadtree.southwest, surface, search_boundary, contained_entities, draw_NN)



    # Finally, draw search_boundary and nearest-neighbor search
    if quadtree.level == 0:

        if draw_NN:
            entity_list = quadtree.return_contained_entities(search_boundary, contained_entities=[])

            if entity_list != None:
                for entity in entity_list:
                    closest_entity, min_distance = quadtree.return_nearest_neighbor(entity, search_boundary, entity_list)
                    if closest_entity != None:
                        pygame.draw.line(surface, [255, 255, 0], [closest_entity.x, closest_entity.y], [entity.x, entity.y])
            print(len(entity_list))


        if search_boundary.type == 'rect':
            pygame.draw.rect(surface, [0, 255, 255], pygame.Rect(search_boundary.x, search_boundary.y, search_boundary.w, search_boundary.h), width=1)
        elif search_boundary.type == 'circle':
            pygame.draw.circle(surface, [0, 255, 255], [search_boundary.x, search_boundary.y], search_boundary.r, width=1)
    
                




def quadtree_test():
    WIDTH = 1400
    HEIGHT = 800
    boundary = Boundary(0, 0, WIDTH, HEIGHT)
    
    pygame.init()
    surface = pygame.display.set_mode((WIDTH,HEIGHT))
    search_boundary = Boundary(-10, -10, 0, 0)
    myTree = QuadTree(boundary, 10, 0)
    redraw = True
    draw_NN = False
    contained_entities = []
    clock = pygame.time.Clock()
    init_pos = [0, 0]

    boundary_type = 'rect'
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Get mouse position
            pos = pygame.mouse.get_pos()

            # If left click, make new entity
            if pygame.mouse.get_pressed()[0]:
                myTree.insert_entity(Entity(pos[0], pos[1]))
                redraw = True

            # If middle mouse button is pressed, calculate nearest-neighbor
            if pygame.mouse.get_pressed()[1]:
                for i in range(0,1000):            
                    myTree.insert_entity(Entity(random.randint(0,WIDTH), random.randint(0,HEIGHT)))
                redraw = True

                draw_NN = True


            # If right-click button gets pressed, get initial position of search boundary
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                init_pos = pos

            # If right-click is held, update search boundary
            if pygame.mouse.get_pressed()[2]:
                if boundary_type == 'rect':
                    search_boundary = Boundary(init_pos[0], init_pos[1], pos[0]-init_pos[0], pos[1]-init_pos[1])
                elif boundary_type == 'circle':
                    search_boundary = Boundary(init_pos[0], init_pos[1], math.sqrt((pos[0] - init_pos[0]) ** 2 + (pos[1] - init_pos[1]) ** 2), type='circle')
                redraw = True

            # Select between search boundary shape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    boundary_type = 'circle'
                elif event.key == pygame.K_r:
                    boundary_type = 'rect'




        # Re-draw if necessary
        if redraw:
            contained_entities = myTree.return_contained_entities(search_boundary, contained_entities=[])
            show(myTree, surface, search_boundary, contained_entities, draw_NN)
            pygame.display.flip()
            redraw = False    
            draw_NN = False
                

        clock.tick()
        #print(clock.get_fps())




if __name__ == "__main__":
    import cProfile

    cProfile.run('quadtree_test()')
    