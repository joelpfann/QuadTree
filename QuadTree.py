import math

class Boundary():
    # Creates either a circular or rectangular (default) shaped boundary

    def __init__(self, x, y, w, h=0, type='rect'):
        self.x = x
        self.y = y
        self.type = type

        if self.type == 'rect':
            self.w = w
            self.h = h

            if self.w < 0:
                self.x = x + w
                self.w = abs(w)
            
            if self.h < 0:
                self.y = y + h
                self.h = abs(h)

        elif self.type =='circle':
            self.r = abs(w)



class Entity():
    # Creates a point entity

    def __init__(self, x, y, entity=None):
        self.x = x
        self.y = y



class QuadTree():
    # Creates a recursive quadtree that divides into four child quadtrees when the defined capacity is reached.
    
    def __init__(self, boundary, capacity, level):
        self.boundary = boundary
        self.entities = []
        self.capacity = capacity
        self.divided = False
        self.num_entities = 0
        self.level = level
        self.num_checks = 0



    def subdivide(self):
        # When called, quadtree will create four child quadtrees

        boundary = Boundary(self.boundary.x + self.boundary.w/2, self.boundary.y, self.boundary.w/2, self.boundary.h/2)
        self.northeast = QuadTree(boundary, self.capacity, self.level+1)

        boundary = Boundary(self.boundary.x, self.boundary.y, self.boundary.w/2, self.boundary.h/2)
        self.northwest = QuadTree(boundary, self.capacity, self.level+1)

        boundary = Boundary(self.boundary.x + self.boundary.w/2, self.boundary.y + self.boundary.h/2, self.boundary.w/2, self.boundary.h/2)
        self.southeast = QuadTree(boundary, self.capacity, self.level+1)

        boundary = Boundary(self.boundary.x, self.boundary.y + self.boundary.h/2, self.boundary.w/2, self.boundary.h/2)
        self.southwest = QuadTree(boundary, self.capacity, self.level+1)



    def insert_entity(self, entity):
        # Inserts an entity into the quadtree if it is within its bounds
        
        if self.within_bounds(self.boundary, entity):
            self.num_entities += 1
        else:
            return

        if len(self.entities) < self.capacity:
            self.entities.append(entity)
        else:   # If over capacity, sub-divide
            if not self.divided:
                self.subdivide()
                self.divided = True
            
            # Perform recusion in order to place entity in proper child quadtree
            self.northeast.insert_entity(entity)
            self.northwest.insert_entity(entity)
            self.southeast.insert_entity(entity)
            self.southwest.insert_entity(entity)



    def within_bounds(self, boundary, entity):
        # Determines if an entity is located within the rectangular or circular bounds of the quadtree

        if boundary.type == 'rect':
            if (entity.x >= boundary.x and entity.x <= boundary.x + boundary.w) and (entity.y >= boundary.y and entity.y <= boundary.y + boundary.h):
                return True
        
        if boundary.type == 'circle':
            if (math.sqrt((entity.x - boundary.x) ** 2 + (entity.y - boundary.y) ** 2) <= boundary.r):
                return True
        
        return False
    
    

    def intersects(self, search_boundary):
        # Determines if a search boundary intersects the bounds of the quadtree

        if search_boundary.type == 'rect':
            if (search_boundary.x < self.boundary.x + self.boundary.w) and (search_boundary.x + search_boundary.w > self.boundary.x):
                if (search_boundary.y < self.boundary.y + self.boundary.h) and (search_boundary.y + search_boundary.h > self.boundary.y):
                    return True
        
        if search_boundary.type == 'circle': # To reduce computational strain, the circle is approximated to be the smallest square that still contains the circle
            if (search_boundary.x - search_boundary.r < self.boundary.x + self.boundary.w) and (search_boundary.x + search_boundary.r > self.boundary.x):
                if (search_boundary.y - search_boundary.r < self.boundary.y + self.boundary.h) and (search_boundary.y + search_boundary.r > self.boundary.y):
                    return True
               
        return False
    
    

    def return_contained_entities(self, search_boundary):
        # Returns all entities that are within the search boundary given

        contained_entities = []

        # If search boundary doesn't intersect quadtree boundary, return empty list
        if not self.intersects(search_boundary):    
            return contained_entities
        
        # For each quadtree entity, append entity if within searach bounds
        for entity in self.entities:    
            if self.within_bounds(search_boundary, entity):
                contained_entities.append(entity)

        # Perform recursion to append contained entities from all child quadtrees
        if self.divided:
            contained_entities.extend(self.northeast.return_contained_entities(search_boundary))
            contained_entities.extend(self.northwest.return_contained_entities(search_boundary))
            contained_entities.extend(self.southeast.return_contained_entities(search_boundary))
            contained_entities.extend(self.southwest.return_contained_entities(search_boundary))
        
        return contained_entities



    def return_nearest_neighbor(self, entity, search_boundary, entity_list):
        # Returns the nearest entity from a given list that falls within the search boundary

        def calc_distance(entity, pos, min_distance, entity_found):
            # Determines if the given entity is closer than any previously checked entity
            distance = math.sqrt((entity.x - pos[0]) ** 2 + (entity.y - pos[1]) ** 2)
            self.num_checks += 1
            if distance < min_distance and distance > 0:
                entity_found = entity
                min_distance = distance                
            return entity_found, min_distance


        if entity_list == None:
            entity_list = self.return_contained_entities(search_boundary)

        min_distance = float('inf')
        entity_found = None
        pos = [entity.x, entity.y]
        for entity in entity_list:
            entity_found, min_distance = calc_distance(entity, pos, min_distance, entity_found)

        return entity_found, min_distance



    def get_all_entities(self):
        # Return all entities contained within this quadtree and all child quadtrees
        entity_list = []

        for entity in self.entities:            
            entity_list.append(entity)

        if self.divided:
            entity_list.extend(self.northeast.get_all_entities())
            entity_list.extend(self.northwest.get_all_entities())
            entity_list.extend(self.southeast.get_all_entities())
            entity_list.extend(self.southwest.get_all_entities())

        return entity_list
    
    