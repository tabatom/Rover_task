# Rover_task
Mini project developed for interview

The code is written in Python.
Used packages are:
- random
- bottle
- requests

Tests are written in the "test" files.

After downloading all files in the same folder, to run the tests:
- test_rover.py : run the file in a command line\\

  `python test_rover.py`

- test_rover_manager.py : run the program simulating an online server with

  `python rover_manager.py`

  (NB: make sure that port 8080 on localhost is free for use)
  then, run the tests using

  `python test_rover_manager.py`
  

Results in the tests for the rover_manager can vary as obstacles are simulated with a certain probability using random numbers.
