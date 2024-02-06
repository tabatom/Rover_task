# -*- coding: utf-8 -*-
"""
@author: Tommaso
"""

import requests

def test_rover_manager():
    """
    Function to test the rover_manager server.    
    
    Tests:
        1. Fetching rovers
        2. Sending correct data via POST request
        3. Sending wrong rover name
        4. Missing data in request

    Returns
    -------
    int
        The number of the test that is failing.
        0 is returned if all tests are ok.

    """
    
    # 1. Fetching rovers
    print("\nStarting test 1...\n")
    response = requests.get("http://localhost:8080/available_rovers")
    if (response.status_code != 200):
        print("Failed test 1: fetching rovers.\n")
        return 1
    
    print(response.content.decode("UTF-8"))
    
    print("\nPassed!\n")


    # 2. Sending correct data via POST request
    print("\nStarting test 2...\n")
    data_post = {"rover_name": "r1", "command_string": "ffrffrflb"}
    response = requests.post("http://localhost:8080/send_commands", data=data_post)
    if (response.status_code != 200):
        print("Failed test 2: sending correct data via POST request.\n")
        return 2
    
    print(response.content.decode("UTF-8"))

    print("\nPassed!\n")
    
    # 3. Sending wrong rover name
    print("\nStarting test 3...\n")
    data_post = {"rover_name": "wrong_name", "command_string": "ffrffrflb"}
    response = requests.post("http://localhost:8080/send_commands", data=data_post)
    if (response.status_code != 400 or
        response.content.decode("UTF-8") != "Rover name not found in managed rovers list."):
        print("Failed test 3: sending wrong rover name.\n")
        return 3
    
    print("\nPassed!\n")

    
    # 4. Missing data in request
    print("\nStarting test 4...\n")
    data_post = {"rover_name": "wrong_name"}
    response = requests.post("http://localhost:8080/send_commands", data=data_post)
    if (response.status_code != 400 or
        response.content.decode("UTF-8") != "'command_string' key-value not found."):
        print("Failed test 4.1: missing 'command_string' key.\n")
        return 4
    
    data_post = {"command_string": "ffrffrflb"}
    response = requests.post("http://localhost:8080/send_commands", data=data_post)
    if (response.status_code != 400 or
        response.content.decode("UTF-8") != "'rover_name' key not found."):
        print("Failed test 4.2: missing 'rover_name' key.\n")
        return 4

    print("\nPassed!\n")

if __name__=='__main__':
    
    test_rover_manager()