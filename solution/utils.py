import logging 
import operator

class position:
    
    # list of 4 directions; will be used for computing rotation
    _rotation_list = ["N","E","S","W"]
    # normalized vectors will be used to move the rover
    _orientation_coord = {
        "N" : (0,1),
        "E" : (1,0),
        "S" : (0,-1),
        "W" : (-1,0)
    }

    def __init__(self, x, y, orientation=None):
        self._current_position=(x,y)
        self._current_orientation=orientation
        self._orientation_index=self._rotation_list.index(orientation) if orientation else None

    def __eq__(self, other):
        return self._current_position == other._current_position
    
    def __lt__(self, other):
        return self._current_position < other._current_position
    
    def rotate_left(self):
        # counterclockwise rotation
        self._orientation_index = (self._orientation_index - 1)%len(self._rotation_list)
        self._current_orientation=self._rotation_list[self._orientation_index]

    def rotate_right(self):
        # clockwise rotation
        self._orientation_index = (self._orientation_index + 1)%len(self._rotation_list)
        self._current_orientation=self._rotation_list[self._orientation_index]

    def move_forward(self):
        new_position = self.simulate_move_forward()
        self._current_position = new_position.current_position
        del new_position

    def simulate_move_forward(self):
        # get current orientation
        direction_module = self._current_orientation_module()
        # computer rover movement 
        temp_position = tuple(map(operator.add, self._current_position, direction_module))
        return position(temp_position[0],temp_position[1])

    def _current_orientation_module(self):
        return self._orientation_coord[self.current_orientation]
    def position_to_string(self):
        return "{x} {y} {o}".format(x=self._current_position[0], y=self._current_position[1], o=self.current_orientation)
    @property
    def current_orientation(self):
        return self._current_orientation
    @property
    def current_position(self):
        return self._current_position
    @property
    def current_position_x(self):
        return self._current_position[0]
    @property
    def current_position_y(self):
        return self._current_position[1]
    

class rover:
    _min_coord = position(0,0)
    _stop_coord = position(-1,-1)

    def __init__(self, name, start_position, orientation, coord_limit_xy):
        self._rover_n=name
        self._current_position=position(start_position[0],start_position[1],orientation)
        self._max_coord = position(coord_limit_xy[0],coord_limit_xy[1])

    def __call__(self, rover_instructions):
        new_position=None

        for command in rover_instructions:
            # take new position after moving the rover
            new_position = self._next_step(command)
            # position (-1,-1) is red flag signaling rover has overcome area limits
            if new_position == self._stop_coord:
                break
            logging.info("Rover {rover_name} is now at {position}".format(rover_name=self._rover_n, position=new_position.position_to_string()))
        
        if new_position == self._stop_coord:
            logging.info("{name} has NOT completed the track!".format(name=self._rover_n))
        else:
            logging.info("{name} has completed the track!".format(name=self._rover_n))
        return self.position_to_string()

    def _next_step(self, direction):
        if direction == 'M':
            # compute rover movement 
            temp_position = self._current_position.simulate_move_forward()
            # check if the new position overcomes the area limit
            if self.within_area_limits(temp_position):
                logging.warning("{name} cannot overcome the area limit. Exploration will stop here.".format(name=self.name))
                return self._stop_coord
            else:
                # if the new position is within area limits, it is then confirmed
                self._current_position.move_forward()
                logging.info("Rover {name} moved {orientation}".format(name=self.name,orientation=self.current_orientation))
        elif direction == 'L':
            # counterclockwise rotation
            self._current_position.rotate_left()
            logging.info("Rover {name} rotated left to {orientation}".format(name=self.name,orientation=self.current_orientation))
        else:
            # clockwise rotation
            self._current_position.rotate_right()
            logging.info("Rover {name} rotated right to {orientation}".format(name=self.name,orientation=self.current_orientation))
        return self.current_position

    def within_area_limits(self, temp_position):
         return temp_position < self._min_coord or temp_position > self._max_coord
    def position_to_string(self):
        return self._current_position.position_to_string()
    @property
    def min_coord(self):
        return self._min_coord
    @property
    def name(self):
        return self._rover_n
    @property
    def current_position(self):
        return self._current_position
    @property
    def current_orientation(self):
        return self._current_position.current_orientation
