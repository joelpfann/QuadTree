import math

class Boundary():
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
    def __init__(self, x, y, entity=None):
        self.x = x
        self.y = y
        self.entity = entity



class QuadTree():
    def __init__(self, boundary, capacity, level):
        self.boundary = boundary
        self.entities = []
        self.capacity = capacity
        self.divided = False
        self.num_entities = 0
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


    def insert_entity(self, entity):

        if self.within_bounds(self.boundary, entity):
            self.num_entities += 1
        else:
            return

        if len(self.entities) < self.capacity:
            self.entities.append(entity)
        else: # If over capacity, sub-divide
            if not self.divided:
                self.subdivide()
                self.divided = True
            
            self.northeast.insert_entity(entity)
            self.northwest.insert_entity(entity)
            self.southeast.insert_entity(entity)
            self.southwest.insert_entity(entity)






    def within_bounds(self, boundary, entity):
        if boundary.type == 'rect':
            if (entity.x >= boundary.x and entity.x <= boundary.x + boundary.w) and (entity.y >= boundary.y and entity.y <= boundary.y + boundary.h):
                return True
        
        if boundary.type == 'circle':
            if (math.sqrt((entity.x - boundary.x) ** 2 + (entity.y - boundary.y) ** 2) <= boundary.r):
                return True
        
        return False
    
    

    def intersects(self, search_boundary):
        if self.boundary.type == 'rect':
            if (search_boundary.x > self.boundary.x) and (search_boundary.x < self.boundary.x + self.boundary.w):
                if (search_boundary.y > self.boundary.y) and (search_boundary.y < self.boundary.y + self.boundary.h):
                    return True
               
        return False
    
    

    def return_contained_entities(self, search_boundary):
        contained_entities = []

        if not self.intersects(search_boundary):
            return contained_entities
        
        for entity in self.entities:
            contained_entities.append(entity)


        if self.divided:
            contained_entities.extend(self.northeast.return_contained_entities(search_boundary))
            contained_entities.extend(self.northwest.return_contained_entities(search_boundary))
            contained_entities.extend(self.southeast.return_contained_entities(search_boundary))
            contained_entities.extend(self.southwest.return_contained_entities(search_boundary))

        return contained_entities



    def return_nearest_neighbor(self, entity, search_boundary, entity_list):

        if search_boundary != None:
            pass
            #entity_list = self.return_contained_entities(search_boundary, contained_entities=[])


        def calc_distance(entity, pos, min_distance, entity_found):
            distance = math.sqrt((entity.x - pos[0]) ** 2 + (entity.y - pos[1]) ** 2)
            #distance = (entity.x - pos[0]) + (entity.y - pos[1])
            if distance < min_distance and distance > 0:
                entity_found = entity
                min_distance = distance                
            return entity_found, min_distance
        

        min_distance = float('inf')
        entity_found = None
        pos = [entity.x, entity.y]
        for entity in entity_list:
            entity_found, min_distance = calc_distance(entity, pos, min_distance, entity_found)

        return entity_found, min_distance


    def get_all_entities(self):
        entity_list = []

        for entity in self.entities:            
            entity_list.append(entity)

        if self.divided:
            entity_list.extend(self.northeast.get_all_entities(entity_list))
            entity_list.extend(self.northwest.get_all_entities(entity_list))
            entity_list.extend(self.southeast.get_all_entities(entity_list))
            entity_list.extend(self.southwest.get_all_entities(entity_list))

        return entity_list
    
    

    
