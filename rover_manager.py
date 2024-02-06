# -*- coding: utf-8 -*-
"""
@author: Tommaso
"""

from rover import rover, DEFAULT_DIMENSION_GRID_X, DEFAULT_DIMENSION_GRID_Y
from bottle import get, post, request, Bottle, run, response
from random import seed

# Setting seed for tests
seed(1234)

# Supposing there is already 1 rover initialized
r1 = rover(0, 0, 'N', 0.1)
# Using in-memory variables for simplicity
#  (in a real world scenario there would be an online database, or other things)
managed_rovers = {"r1": r1}

# Initializing application
rover_manager = Bottle()

# Function to return available rovers
@rover_manager.get('/available_rovers')
def return_rovers():
    print("Rovers:", str(managed_rovers))
    return str(managed_rovers)


# Function to send to an existing rover a command string
@rover_manager.post('/send_commands')
def apply_command_string():
    data_pairs = str(request.body.read().decode("UTF-8")).split('&')
    info_dictio = {}
    command_string = ""
    for pair in data_pairs:
        key, value = pair.split("=")
        # Possible TODO: check for duplicated keys
        info_dictio[key] = value
    
    if "rover_name" not in info_dictio:
        response.status = "400 Bad request"
        return "'rover_name' key not found."

    if "command_string" in info_dictio.keys():
        command_string = info_dictio["command_string"]
    else:
        response.status = "400 Bad request"
        return "'command_string' key-value not found."
    
    rover_status = ""
    
    if info_dictio["rover_name"] not in managed_rovers:
        response.status = "400 Bad request"
        return "Rover name not found in managed rovers list."
    
    acting_rover = managed_rovers[info_dictio["rover_name"]]
    r, d = acting_rover.execute_command_string(command_string)
    rover_status = {"Result": r,
                    "Details": d, 
                    "x": acting_rover.x,
                    "y": acting_rover.y,
                    "orientation": acting_rover.orientation}

    
    return str(rover_status)


run(rover_manager, host='localhost', port=8080)