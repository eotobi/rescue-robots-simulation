# A Simulation of Explorer Drones and Firstaid Terrain Robots Model

## Summary

A simple  model, consisting of three agent types: Explorer drones, Firstaid Terrain Robots, and Patients. The Explorer drones fly over the drid at random in search of patients. When they find one checks if condition is critical if so call the Firstaid Terrain Robots to deliver first aid supplies. If not, the Explorer drones keeps searching.

When the battery level goes low the two robots abandon the mission and call for back up robots.

The model is tests and demonstrates several Mesa concepts and features:
 - MultiGrid
 - Multiple agent types (Explorer drones, Firstaid Terrain Robots, and Patients.)
 - Overlay arbitrary text (battery level) on agent's shapes while drawing on CanvasGrid
 - Agents inheriting a behavior (random movement) from an abstract parent
 - Writing a model composed of multiple files.
 - Dynamically adding and removing agents from the schedule

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

###### First, we clone the rescue-robots-simulation repo
          ```bash
             git clone https://github.com/rescue-robots-simulation.git
          ```bash
              cd RescueRobots
       
###### activate the virtual environment
- On Windows : 
    ```bash
    rescueenv\Scripts\activate
- On Linux : 
    ```bash
    source rescuenv/bin/activate
- then 
    ```bash
    cd RescueRobots
    ```bash
    pip install -r requirements.txt

## How to Run

To run the model interactively, run ``mesa runserver`` in the root directory

```bash
    $ mesa runserver
Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

## Files

* ``rescue_robots/random_walk.py``: Defines the ``RandomWalker`` agent, which implements the behavior of moving randomly across a grid, one cell at a time. Both the ExplorerDrone and FirstAidRobot agents will inherit from it.
* ``rescue_robots/test_random_walk.py``: Defines a simple model and a text-only visualization intended to make sure the RandomWalk class was working as expected. This doesn't actually model anything, but serves as an ad-hoc unit test. To run it, ``cd`` into the ``rescue_robots`` directory and run ``python test_random_walk.py``. You'll see a series of ASCII grids, one per model step, with each cell showing a count of the number of agents in it.
* ``rescue_robots/agents.py``: Defines the ExplorerDrone, FirstAidRobot, and Patient agent classes.
* ``rescue_robots/scheduler.py``: Defines a custom variant on the RandomActivationByType scheduler, where we can define filters for the `get_type_count` function.
* ``rescue_robots/model.py``: Defines the RescueRobots model itself
* ``rescue_robots/server.py``: Sets up the interactive visualization server
* ``run.py``: Launches a model visualization server.

Multiagent System Analysis.ipynb is a jupyter file notebook that has some analysis from the simulation
