# -*- coding: utf-8 -*-
"""
@author: Tommaso
"""

from random import seed
from rover import rover, DEFAULT_DIMENSION_GRID_X, DEFAULT_DIMENSION_GRID_Y

# setting seed for tests
seed(123)

def test_rover():
    """
    Function to test the rover funcionalities are working as expected.
    
    The following tests will be carried out (without obstacles):
        1. Standard/default initialization
        2. Correct non-default initializations
        3. Overflowing dimensions initialization
        4. Bad orientation initialization
        5. Wrong grid initialization (grid dim < 0)
        6. Wrong command
        7. Correct single commands
        8. Wrapping coordinates after move
        9. Long path with no obstacles
        10. Prob obstacles = 1

    Returns
    -------
    int
        The number of the test that is failing.
        0 is returned if all tests are ok.

    """
    
    def test_rover_status(test_rover,
                          expected_x = 0,
                          expected_y = 0,
                          expected_orientation = 'N',
                          expected_obstacles = 0.,
                          expected_dimension_grid_x = DEFAULT_DIMENSION_GRID_X,
                          expected_dimension_grid_y = DEFAULT_DIMENSION_GRID_Y):
        """
        Function to wrap the check

        Parameters
        ----------
        test_rover : rover
            The rover to check
        expected_x : int
        expected_y : int
        expected_orientation : char
        expected_obstacles : float
        expected_grid_dimension_x : int
        expected_grid_dimension_y : int

        Returns
        -------
        bool
            The test result

        """
        return (test_rover.x == expected_x and
                test_rover.y == expected_y and
                test_rover.orientation == expected_orientation and
                test_rover.orientation == expected_orientation and
                test_rover.dimension_grid_x == expected_dimension_grid_x and
                test_rover.dimension_grid_y == expected_dimension_grid_y)
    
    
    
    def check_move_response(response, details, expected_response, expected_details):
        """
        

        Parameters
        ----------
        response : string
            Rover main feedback from function executing command string.
        details : string
            Eventually, details of the previous status response.
        expected_response : string
        expected_details : string

        Returns
        -------
        bool
            True if the response and the details are as expected.
            False otherwise.

        """
        return (response == expected_response and
                details == expected_details)
    
    
    # 1. Checking default initialization
    print("\nStarting test 1...\n")
    r1 = rover()
    if not(test_rover_status(r1) and
           r1.known_commands == 'fblr'):
        print("Failed test 1: default initialization.\n")
        return 1
    else:
        print("\nPassed!\n")
    
    
    # 2. Checking correct non-default initialization
    print("\nStarting test 2...\n")
    r2 = rover(2, 2, 'N', 0., 150, 100)
    if not(test_rover_status(r2, 2, 2, 'N', False, 150, 100)):
        print("Failed test 2: correct non-default initialization.\n")
        return 2
    else:
        print("\nPassed!\n")

    # 3. Checking overflowing dimensions initialization
    print("\nStarting test 3...\n")
    r3 = rover(333, 333, 'N', 0., 100, 100)
    if not(test_rover_status(r3, 0, 0, 'N')):
        print("Failed test 3: overflowing dimensions initialization.\n")
        return 3
    else:
        print("\nPassed!\n")
    
    # 4. Checking bad orientation initialization
    print("\nStarting test 4...\n")
    r4 = rover(0, 0, 'A')
    if not(test_rover_status(r4, 0, 0, 'N')):
        print("Failed test 4: bad orientation initialization.\n")
        return 4
    else:
        print("\nPassed!\n")
    
    # 5. Wrong grid initialization (grid dim < 0)
    print("\nStarting test 5...\n")
    r5 = rover(0, 0, 'N', 0., -1, -1)
    if not(test_rover_status(r5)):
        print("Failed test 5: wrong grid initialization (grid dim < 0).\n")
        return 5
    else:
        print("\nPassed!\n")
    
    # 6. Wrong command
    print("\nStarting test 6...\n")
    r6 = rover()
    r, d = r6.execute_command_string("a")
    exp_r = "Error: invalid command."
    exp_d = "Unknown command: a\nAllowed commands are: [f, b, l, r]"
    exp_d += "\nExiting execution (no command has been executed)."
    if (not(test_rover_status(r6)) or
        not(check_move_response(r, d, exp_r, exp_d))):
        print("Failed test 6: wrong command.\n")
        return 6
    else:
        print("\nPassed!\n")
    
    # 7. Correct single commands
    print("\nStarting test 7...\n")
    r7 = rover()
    r, d = r7.execute_command_string("f")
    if (not(test_rover_status(r7, 0, 1, 'N')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 7.1: correct single commands (command 'f')\n")
        return 7
    r, d = r7.execute_command_string("b")
    if (not(test_rover_status(r7, 0, 0, 'N')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 7.2: correct single commands (command 'b')\n")
        return 7
    # For 'l' and 'r', testing also the correct wrapping from the class list "ordered_orientations"
    r, d = r7.execute_command_string("l")
    if (not(test_rover_status(r7, 0, 0, 'W')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 7.3: correct single commands (command 'l')\n")
        return 7
    r, d = r7.execute_command_string("l")
    if (not(test_rover_status(r7, 0, 0, 'S')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 7.4: correct single commands (command 'l')\n")
        return 7
    r, d = r7.execute_command_string("r")
    if (not(test_rover_status(r7, 0, 0, 'W')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 7.5: correct single commands (command 'r')\n")
        return 7
    r, d = r7.execute_command_string("r")
    if (not(test_rover_status(r7, 0, 0, 'N')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 7.6: correct single commands (command 'r')\n")
        return 7
    else:
        print("\nPassed!\n")
    
    # 8. Wrapping coordinates after move
    print("\nStarting test 8...\n")
    r8 = rover(0, DEFAULT_DIMENSION_GRID_Y - 1, 'N')
    r, d = r8.execute_command_string("f")
    if (not(test_rover_status(r8, 0, 0, 'N')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 8.1: wrapping coordinates after move.\n")
        return 8
    r, d = r8.execute_command_string("b")
    if (not(test_rover_status(r8, 0, DEFAULT_DIMENSION_GRID_Y - 1, 'N')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 8.2: wrapping coordinates after move.\n")
        return 8
    
    r8 = rover(0, 0, 'S')
    r, d = r8.execute_command_string("f")
    if (not(test_rover_status(r8, 0, DEFAULT_DIMENSION_GRID_Y - 1, 'S')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 8.3: wrapping coordinates after move.\n")
        return 8
    r, d = r8.execute_command_string("b")
    if (not(test_rover_status(r8, 0, 0, 'S')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 8.4: wrapping coordinates after move.\n")
        return 8
    
    r8 = rover(0, 0, 'W')
    r, d = r8.execute_command_string("f")
    if (not(test_rover_status(r8, DEFAULT_DIMENSION_GRID_X - 1, 0, 'W')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 8.5: wrapping coordinates after move.\n")
        return 8
    r, d = r8.execute_command_string("b")
    if (not(test_rover_status(r8, 0, 0, 'W')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 8.6: wrapping coordinates after move.\n")
        return 8
    
    r8 = rover(DEFAULT_DIMENSION_GRID_X - 1, 0, 'E')
    r, d = r8.execute_command_string("f")
    if (not(test_rover_status(r8, 0, 0, 'E')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 8.7: wrapping coordinates after move.\n")
        return 8
    r, d = r8.execute_command_string("b")
    if (not(test_rover_status(r8, DEFAULT_DIMENSION_GRID_X - 1, 0, 'E')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 8.8: wrapping coordinates after move.\n")
        return 8
    else:
        print("\nPassed!\n")
    
    # 9. Long path with no obstacles
    print("\nStarting test 9...\n")
    r9 = rover(0, 0, 'E')
    r, d = r9.execute_command_string("ffffffflfffffffrbbbbbblbbbbbb")
    if (not(test_rover_status(r9, 1, 1, 'N')) or
        not(check_move_response(r, d, "All commands successfully executed.", ""))):
        print("Failed test 9: long path with no obstacles.\n")
        return 9
    else:
        print("\nPassed!\n")
        
    # 10. Prob obstacles = 1
    print("\nStarting test 10...\n")
    r10 = rover(0, 0, 'N', 1.)
    r, d = r10.execute_command_string("f")
    exp_r = "ABORTING. Reason: Found obstacle."
    exp_d = "Obstacle position:[x = 0, y = 1]\n"
    exp_d += "Current state:\n"
    exp_d += "\tx: 0\n"
    exp_d += "\ty: 0\n"
    exp_d += "\torientation: N\n"
    exp_d += "\tTrying to execute command: f\n"
    exp_d += "\tGrid dimensions:\n"
    exp_d += "\tx dimension: 100	y dimension: 100"
    if (not(test_rover_status(r10)) or
        not(check_move_response(r, d, exp_r, exp_d))):
        print("Failed test 10: prob obstacles = 1.\n")
        return 10
    
    r, d = r10.execute_command_string("b")
    exp_r = "ABORTING. Reason: Found obstacle."
    exp_d = "Obstacle position:[x = 0, y = 99]\n"
    exp_d += "Current state:\n"
    exp_d += "\tx: 0\n"
    exp_d += "\ty: 0\n"
    exp_d += "\torientation: N\n"
    exp_d += "\tTrying to execute command: b\n"
    exp_d += "\tGrid dimensions:\n"
    exp_d += "\tx dimension: 100	y dimension: 100"
    if (not(test_rover_status(r10)) or
        not(check_move_response(r, d, exp_r, exp_d))):
        print("Failed test 10: prob obstacles = 1.\n")
        return 10
    else:
        print("\nPassed!\n")
    
    return 0



if __name__ == '__main__':
    print("Testing rover funcionalities...")
    
    test_rover()