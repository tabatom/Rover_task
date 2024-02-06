# -*- coding: utf-8 -*-
"""
@author: Tommaso
"""

from random import random

DEFAULT_DIMENSION_GRID_X= 100
DEFAULT_DIMENSION_GRID_Y = 100

class rover:
    """
    Class to represent rover moving on the planet (represented by a grid)
      - x,y: are the initial coordinates.
        Default to [0,0] if not provided or if out of grid range.
        Assuming the coordinates can only be positive integers.
        Coordinates can vary in range [0, dimension_grid_coord).
        If after a move the rover is outside the grid, it is wrapped to the other side.
      - orientation: is the direction the rover is facing.
        Allowed orientations are ['N', 'S', 'E', 'W'].
        Default to 'N' if unprovided or invalid.
      - dimension_grid_x, dimension_grid_y: represent the grid dimensions.
        Default to 100 if invalid (< 0) or not provided.
        Conventionally setting constants as global variables (in this module).
      - prob_obstacles: represents the probability to find obstacles: [0, 1]
        Default value is 0
    """
    def __init__(self,
               x_init = 0,
               y_init = 0,
               orientation_init = 'N',
               prob_obstacles_init = 0.,
               dimension_grid_x_init = DEFAULT_DIMENSION_GRID_X,
               dimension_grid_y_init = DEFAULT_DIMENSION_GRID_Y):
        
        if (dimension_grid_x_init <= 0): # NOTE: also a 1x1 grid has no meaning, but for now it will be allowed
            print("Warning: x grid dimension cannot be < 0. Setting it to MAX_GRID_X (100).")
            self.dimension_grid_x = DEFAULT_DIMENSION_GRID_X
        else:
            self.dimension_grid_x = dimension_grid_x_init
        if (dimension_grid_y_init <= 0):
            print("Warning: y grid dimension cannot be < 0. Setting it to MAX_GRID_Y (100).")
            self.dimension_grid_y = DEFAULT_DIMENSION_GRID_Y
        else:
            self.dimension_grid_y = dimension_grid_y_init
        
        if (x_init >= self.dimension_grid_x or x_init < 0):
            print("Warning: x coordinate out of grid range [0, MAX_GRID_X). Setting x = 0")
            self.x = 0
        else:
            self.x = x_init

        if (y_init >= self.dimension_grid_y or y_init < 0):
            print("Warning: y coordinate out of grid range [0, MAX_GRID_X). Setting y = 0")
            self.y = 0
        else:                    
            self.y = y_init
        
        if (orientation_init != 'N' and
            orientation_init != 'S' and
            orientation_init != 'E' and
            orientation_init != 'W'):
            print("Warning: unrecognized orientation. Allowed orientations are ['N', 'S', 'E', 'W'].\nSetting orientation = 'N'")
            self.orientation = 'N'
        else:
            self.orientation = orientation_init
            
        self.prob_obstacles = prob_obstacles_init
        
        self.known_commands = "fblr"
        
    # Using this shared class variable to compact the code for turning command ('l', 'r')
    ordered_orientations = "NESW"
    
    def execute_command_string(self, command_string):
        """
        Function that tries to execute the commands in the command string.
        Allowed commands are ['f', 'b', 'l', 'r']
        If an invalid command is found, the execution is not performed.
        The execution starts and goes until the command string ends or an obstacle is found.
        
        Parameters
        ----------
        command_string : string
            The string representing the list of commands.

        Returns
        -------
        string
            Message describing a successful execution or obstacle detection details

        """
        check, details = self.check_valid_command_string(command_string)
        if not(check):
            return "Error: invalid command.", details + "\nExiting execution (no command has been executed)."
        
        for command in command_string:
            # If moving (commands 'f' or 'b' received), checking for obstacles
            #  See check_for_obstacles method for details and obstacles assumptions
            if command == 'f' or command == 'b':
                if self.check_for_obstacle():
                    # evaluating the obstacle position
                    x_obstacle, y_obstacle = self.obstacle_position(command)
                    response = "ABORTING. Reason: Found obstacle."
                    details = "Obstacle position:"
                    details += "[x = " + str(x_obstacle) + ", y = " + str(y_obstacle) + "]\n"
                    details += "Current state:\n"
                    details += "\tx: " + str(self.x) + "\n"
                    details += "\ty: " + str(self.y) + "\n"
                    details += "\torientation: " + str(self.orientation) + "\n"
                    details += "\tTrying to execute command: " + command + "\n"
                    details += "\tGrid dimensions:\n"
                    details += "\tx dimension: " + str(self.dimension_grid_x)
                    details += "\ty dimension: " + str(self.dimension_grid_y)
                    return response, details
            
            self.move(command)
        
        return "All commands successfully executed.", ""
                    
    def check_valid_command_string(self, command_string):
        """
        Method that checks for invalid commands in the string before the execution.
        If it finds some, it interrupt the execution and exit printing a warning.

        Parameters
        ----------
        command_string : STRING
            The string representing the list of commands.

        Returns
        -------
        bool
            True if the command string has only valid commands
            False otherwise
        string
            Returning an empty string if command is valid.
            Returning some feedback if command is invalid.

        """
        for command in command_string:
            if not(self.check_known_command(command)):
                details = "Unknown command: " + str(command)
                details += "\nAllowed commands are: [f, b, l, r]"
                return False, details
        return True, ""
        
    def check_known_command(self, command):
        """
        Check if a single command is valid (known) or not.

        Parameters
        ----------
        command : character
            The caracter representing a single command.

        Returns
        -------
        bool
            True if the command is valid (known)
            False otherwise.

        """
        return (command in self.known_commands)
    
    def move(self, command):
        """
        Method that changes the coordinates or the orientation of the rover
         instance based on the given command.
        If after the command execution the rover is outside the grid limits,
         it is wrapped to the other side of the grid.
        
        Parameters
        ----------
        command : CHARACTER
            the command code passed to the rover.
            Allowed commands are:
                - f --> istruct the rover to move forward of 1 tile in the current direction
                - b --> istruct the rover to move backward of 1 tile in the current direction
                - l --> istruct the rover to turn left
                - r --> istruct the rover to turn right

        Returns
        -------
        None.


        """
        if command == 'f':
            if self.orientation == 'N':
                self.y += 1
            elif self.orientation == 'S':
                self.y -= 1
            elif self.orientation == 'E':
                self.x += 1
            elif self.orientation == 'W':
                self.x -= 1
            else:
                # Should never enter this branch
                print("Error: unknow orientation found while executing 'f' command.")
        elif command == 'b':
            if self.orientation == 'N':
                self.y -= 1
            elif self.orientation == 'S':
                self.y += 1
            elif self.orientation == 'E':
                self.x -= 1
            elif self.orientation == 'W':
                self.x += 1
            else:
                # Should never enter this branch
                print("Error: unknow orientation found while executing 'b' command.")
        elif command == 'l':
            self.orientation = rover.ordered_orientations[rover.ordered_orientations.find(self.orientation) - 1]
        elif command == 'r':
            self.orientation = rover.ordered_orientations[(rover.ordered_orientations.find(self.orientation) + 1) % len(rover.ordered_orientations)]
        
        # Checking if a wrap is needed
        # NOTE: moves are only made by 1 step, but the update step is more general
        #  (eg: going beyond grid by 5 would result in wrapping 5 units, not just
        #  restarting from beginning/end of the grid)
        if (self.x < 0):
            self.x = (self.dimension_grid_x + self.x) % self.dimension_grid_x
        if (self.y < 0):
            self.y = (self.dimension_grid_y + self.y) % self.dimension_grid_y;
        if (self.x >= self.dimension_grid_x):
            self.x = self.x % self.dimension_grid_x;
        if (self.y >= self.dimension_grid_y):
            self.y = self.y % self.dimension_grid_y;
        
        return

    
    def check_for_obstacle(self):
        """
        Method to simulate obstacles.
        Simulating obstacles using random numbers
         Arbitrariry choosing prob obstacle = 1/10
        Assuming obstacles are only visible when approaching the new location
         from a nearby one (cannot detect obstacles from far away)
        NOTE: with this approach the assumption is that new obstacle can arise
        in already explored places (and can disappear where already found).
        
        Returns
        -------
        BOOLEAN
        

        """
        return random() < self.prob_obstacles
    
    def obstacle_position(self, command):
        if command == 'f':
            if self.orientation == 'N':
                y_obstacle = (self.y + 1) if (self.y != self.dimension_grid_y - 1) else 0
                return self.x, y_obstacle
            elif self.orientation == 'S':
                y_obstacle = (self.y - 1) if (self.y != 0) else self.dimension_grid_y - 1
                return self.x, y_obstacle
            elif self.orientation == 'E':
                x_obstacle = (self.x + 1) if (self.x != self.dimension_grid_x - 1) else 0
                return x_obstacle, self.y
            elif self.orientation == 'W':
                x_obstacle = (self.x - 1) if (self.x != 0) else self.dimension_grid_x - 1
                return x_obstacle, self.y
            else:
                # Should never enter this branch
                print("Error: unknow orientation found while computing obstacle position for 'f' command.")
        elif command == 'b':
            if self.orientation == 'N':
                y_obstacle = (self.y - 1) if (self.y != 0) else self.dimension_grid_y - 1
                return self.x, y_obstacle
            elif self.orientation == 'S':
                y_obstacle = (self.y + 1) if (self.y != self.dimension_grid_y - 1) else 0
                return self.x, y_obstacle
            elif self.orientation == 'E':
                x_obstacle = (self.x - 1) if (self.x != 0) else self.dimension_grid_x - 1
                return x_obstacle, self.y
            elif self.orientation == 'W':
                x_obstacle = (self.x + 1) if (self.x != self.dimension_grid_x - 1) else 0
                return x_obstacle, self.y
            else:
                # Should never enter this branch
                print("Error: unknow orientation found while computing obstacle position for 'b' command.")
        
        