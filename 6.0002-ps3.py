# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: James Quigley
# Collaborators (discussion): None
# Time: 11 hours :(

import math
import random
import matplotlib
matplotlib.use('TkAgg', warn=False)

import ps3_visualize
import pylab

from ps3_verify_movement3 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # find change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add to existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        #initialize parameters 
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        #keep track of the dirt on each tile represented by coordinates
        #initialize dictionary
        self.tiles = {}
        #keys are tiles' coordinates in the room
        for i in range(width):
            for k in range(height):
                #the values are the corresponding dirt amount on each tile
                self.tiles[(i,k)] = dirt_amount
    
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        #set the values of x and y coordinates
        x, y = math.floor(pos.get_x()), math.floor(pos.get_y())
        #update the dirt amount by subtracting the amount of dirt cleaned each step
        self.tiles[(x,y)] -= capacity
        #since the dirt amount cannot be negative, we set it to be 0 if it is
        if self.tiles[(x,y)] < 0:
            self.tiles[(x,y)] = 0

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        #check if the tile is completely cleaned; by checking if the dirt amount is 0
        if self.tiles[(m,n)] == 0:
            #return True if it is
            return True
        #false otherwise
        return False

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        #initialize a counter that keeps track of the number of cleaned tiles
        count = 0
        #iterate over each tile (through the x and y coordinates) 
        for i in range(self.width):
            for k in range(self.height):
                #if the tile is completely cleaned
                if self.tiles[(i,k)] == 0:
                    #increment the counter by 1
                    count += 1
        return count
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        #check if the position is in range of the height and width of the room
        return 0 <= pos.get_x() < self.width and 0 <= pos.get_y() < self.height
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        #return the value of the key of the dictionary of tiles in the given coordinates m, ns
        return self.tiles[(m,n)]
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        #return the number of tiles defined by the product of the height and width of the room
        return self.height * self.width 

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        #get random values for the x and y coordinates in the range of the height and width of the room
        rand_x = random.uniform(0, self.width)
        rand_y = random.uniform(0, self.height)
        #return a Position object with the random coordinates
        return Position(rand_x, rand_y)         

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive integer; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        #initialize the parameters of the class Robot
        self.room = room
        self.speed = speed
        self.capacity = capacity
        #initialize a random position using the get_random_position function implemented above
        self.position = self.room.get_random_position()
        #initialize a random direction in the range 0-360 angle degrees
        self.angle = random.uniform(0, 360)

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        #return the position
        return self.position

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        #returns angle of direction
        return self.angle

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        #sets the position of the robot
        self.position = position 

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        #sets the direction of the robot
        self.angle = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        - Determine the new position of the robot.
        - If the new position is invalid, rotate once to a random 
        new direction, and stay stationary. 
        - If the new position is valid, move the robot there and 
        clean the tile under the robot.
        """
        #get the current position of the robot
        currentPosition = self.get_robot_position()
        #move robot to new position
        newPosition = currentPosition.get_new_position(self.get_robot_direction(), self.speed)
        #check whether the position is valid or not, aka for the walls in the room
        if not self.room.is_position_in_room(newPosition):
            #if it isn't valid, then change the direction of the robot
            self.set_robot_direction(random.uniform(0, 360))
        #if valid  
        else:
            #set new position and clean
            self.set_robot_position(newPosition)
            self.room.clean_tile_at_position(newPosition, self.capacity)

# Uncomment this line to see your implementation of StandardRobot in action!
# Note to comment it again before running the tester.
#test_robot_movement(StandardRobot, RectangularRoom)

# === Problem 3
class CatOnARobot(Robot):
    """
    A CatOnARobot is a robot with a cat mounted on it. A CatOnARobot will 
    not clean the tile it moves to and pick a new, random direction for itself 
    with probability p rather than simply cleaning the tile it moves to.
    """
    p = 0.15
    
    @staticmethod
    def set_cat_probability(prob):
        """
        Sets the probability of the cat messing with the controls equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        CatOnARobot.p = prob
    
    def gets_cat_interference(self):
        """
        Answers the question: Does the cat mess with this CatOnARobot's controls
        at this timestep?
        The cat messes with the CatOnARobot's controls with probability p.

        returns: True if the cat messes with CatOnARobot's controls, False otherwise.
        """
        return random.random() < CatOnARobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.
        
        Check if the cat messes with the controls. If the robot does get cat
        interference, do not clean the current tile and change its direction randomly.

        If the cat does not mess with the controls, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        moving there if it can, picking a new direction and stay stationary if it can't)
        """
        #Check if the robot interferes with the cat by calling gets_cat_interference
        if self.gets_cat_interference():
            #if yes, change direction but don't clean the tile
            self.set_robot_direction(random.uniform(0, 360))
        #if the cat doesn't interfere, then its the same steps are with Standard
        else:
            #get the current position of the robot
            currentPosition = self.get_robot_position()
            #move the robot and get a new position
            newPosition = currentPosition.get_new_position(self.get_robot_direction(), self.speed)
            #check whether the position is valid or not, aka for the walls in the room
            if not self.room.is_position_in_room(newPosition):
                #if it isn't, change the direction again
                self.set_robot_direction(random.uniform(0, 360))
            #if valid  
            else:
                #set the new position and cleans
                self.set_robot_position(newPosition)
                self.room.clean_tile_at_position(newPosition, self.capacity)
        
    
#test_robot_movement(CatOnARobot, RectangularRoom)

# === Problem 4
class SuperRobot(Robot):
    """
    A SuperRobot is a robot that moves extra fast and cleans two tiles in one timestep.

    It moves in its current direction, cleans the tile it lands on, and continues 
    moving in that direction and cleans the second tile it lands on, all in one unit of time. 

    If the SuperRobot hits a wall when it attempts to move in its current direction,
    it may dirty the current tile by one unit because it moves very fast and can knock dust off of the wall.
    
    There are three possible cases:

    1. The robot tries to move. If it would hit the wall on the first move, it 
    does not move. Instead, it turns to face a random direction and stops for this timestep. 
    
    2. If it can move, it moves and cleans the tile it moves to. Then, it tries to move a second time. 
        
        a. If it hits the wall, it dirties the tile it is on with probability
           p. Regardless of whether it dirties the tile, the robot turns to a random
           direction. Then it stops. 

        b. If it does not hit the wall, it moves and cleans the tile it moves to. 

    """
    p = 0.1337

    @staticmethod
    def set_dirty_probability(prob):
        """
        Sets the probability of getting the tile dirty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        SuperRobot.p = prob
    
    def dirties_tile(self):
        """
        Answers the question: Does this SuperRobot dirty the tile if it hits the wall at full speed?
        A SuperRobot dirties a tile with probability p.

        returns: True if the SuperRobot dirties the tile, False otherwise.
        """
        return random.random() < SuperRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.
 
        Follow the instructions provided in the pset and the class docstring above.
        """
         #move the robot
        currentPosition = self.get_robot_position()
        #update position
        newPosition = currentPosition.get_new_position(self.get_robot_direction(), self.speed)
        #check if the new position is valid; aka if it is in range
        if not self.room.is_position_in_room(newPosition):
            #if it isn't, change the direction
            self.set_robot_direction(random.uniform(0, 360))
        #if in range
        else: 
            
            #update position
            self.set_robot_position(newPosition)
            #clean the tile
            self.room.clean_tile_at_position(newPosition, self.capacity)
            currentPosition = self.get_robot_position()
            #get the new position 
            newPosition = currentPosition.get_new_position(self.get_robot_direction(), self.speed)
            #check again if the new position is in range
            if not self.room.is_position_in_room(newPosition):
            #if not, change direction again
                self.set_robot_direction(random.uniform(0, 360))
                if self.dirties_tile():
                    #if robot dirties the room (by our probability function), clean the tile by -1; aka dirty it by 1
                    self.room.clean_tile_at_position(self.position, -1)
            #if in range
            else:
                #update position and clean
                self.set_robot_position(newPosition)
                self.room.clean_tile_at_position(newPosition, self.capacity)


#test_robot_movement(SuperRobot, RectangularRoom)
        
# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room. For example,
    if we want to test the amount of time it takes to clean 75% of the room, min_coverage
    would be 0.75.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0), the number of robots in the simulation
    speed: a float (speed > 0), how fast the robots move at each timestep
    capacity: an int (capacity >0), how much dirt the robots pick up at a time
    width: an int (width > 0), the width of the room
    height: an int (height > 0), the height of the room
    dirt_amount: an int, the dirt amount all the tiles start with
    min_coverage: a float (0 <= min_coverage <= 1.0), how much of the room the 
        robots should clean before stopping the simulation
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                CatOnARobot)
    """
     #initialize the counter for total number of steps in trials
    stepSum = 0
    #mean average of time-steps needed to clean the minimum of the room
    mean = 0
    #iterate through each trial
    for i in range(num_trials):
        #initialize an enmpty list to hold the robots for each trial
        robotList = []
        #initialize a room of RectangularRoom object type
        room = RectangularRoom(width, height, dirt_amount)
        #for every robot in the trials
        for k in range(num_robots):
            #get the features of the robots
            robot = robot_type(room, speed, capacity)
            #append the robot to the list of robots
            robotList.append(robot)
        #initialize the number of steps for each particular trial as 0
        stepCount = 0
        #while the rate of the cleaned tiles is less than the minimum coverage
        while room.get_num_cleaned_tiles()/room.get_num_tiles() < min_coverage:
            #every robot of the list of robots
            for i in range(num_robots):
                #cleans and new position 
                robotList[i].update_position_and_clean()
            #b/c the robots in the list clean the tiles at the same time, increment stepCount
            stepCount += 1
        #add the number of steps of each trial to stepSum
        stepSum += stepCount
    #calculate and return the mean average time-steps needed to finish cleaning
    mean = stepSum/num_trials
    return mean


#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the three robot types compare when cleaning 80%
#       of a 20x20 room? SuperRobot is the obviously fastest with the best 
#   performance. 
#   The StandardRobot is a tad faster than the CatOnRobot. This makes sense because
#   both robots are similar except that for with specific probability
#   CatOnRobot cannot clean a tile it's on, therefore it's slower overall 
#
#
#
# 2) How does the performance of the three robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6? All robots have do their best when the room
#       is a square. The time steps increases with the ratio of the room which will
#       hinder the robots b/c you hit the wall less in a square room.  Performance
#       is still Super > Standard > Cat

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the three robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, CatOnARobot))
        times3.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, SuperRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'CatOnARobot', 'SuperRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, CatOnARobot))
        times3.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, SuperRobot))
    pylab.plot(aspect_ratios, times1, 'o-')
    pylab.plot(aspect_ratios, times2, 'o-')
    pylab.plot(aspect_ratios, times3, 'o-')
    pylab.title(title)
    pylab.legend(('StandardRobot', 'CatOnARobot', 'SuperRobot'), fancybox=True, framealpha=0.5)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
#