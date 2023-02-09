import mesa
import pandas as pd
import numpy as np

from rescue_robots.scheduler import RandomActivationByTypeFiltered
from rescue_robots.agents import ExplorerDrone, FirstAidRobot, Patient

            
class RescueRobots(mesa.Model):
    """
    Rescue Robots Mission Model
    """

    height = 10
    width = 10

    initial_firstaid_robots = 4
    
    initial_explorer_drones = 3
    
    initial_patients = 3
    
    battery_level = 10
    
    bad_health_status = False
    time_to_bad_state = 20

    robot_available = 0.05

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating rescue mission for patients in MT GREEN by coordination of aerial explorer drones and land terrain firstaid robots."
    )

    def __init__(
        self,
        width=20,
        height=20,
        initial_explorer_drones =3,
        initial_firstaid_robots =4,
        initial_patients = 3,
        battery_level = 100,
        bad_health_status = True,
        time_to_bad_state = 5,
        robot_available = 0.05
    ):
        """
            initial_explorer_drones: Number of Explorer Drones to start with
            initial_firstaid_robots: Number of FirstAid Robots to start with
            initial_patients = Number of Patients to start with 
            bad_health_status: Whether to have the Explorer Drones call FirstAid Robots
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_explorer_drones = initial_explorer_drones
        self.initial_firstaid_robots = initial_firstaid_robots
        self.bad_health_status = bad_health_status
        self.time_to_bad_state = time_to_bad_state
        self.battery_level = battery_level
        self.robot_available = robot_available
        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Explorer Drone": lambda m: m.schedule.get_type_count(ExplorerDrone),
                "FirstAid Robot": lambda m: m.schedule.get_type_count(FirstAidRobot),
                "Patient": lambda m: m.schedule.get_type_count(
                    Patient , lambda x: x.not_critical_patient
                ),
            }
        )

        # Create Explorer Drone:
        for i in range(self.initial_explorer_drones):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.battery_level)
            explorerDrone = ExplorerDrone(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(explorerDrone, (x, y))
            self.schedule.add(explorerDrone)

        # Create Terrain FirstAid Robot
        for i in range(self.initial_firstaid_robots):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.battery_level)
            firstAidRobot  = FirstAidRobot(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(firstAidRobot, (x, y))
            self.schedule.add(firstAidRobot)

        # Create patients
        for i in range(self.initial_patients):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            if self.bad_health_status:
                    not_critical_patient = self.random.choice([True, False])

                    if not_critical_patient:
                        countdown = self.time_to_bad_state
                    else:
                        countdown = self.random.randrange(self.time_to_bad_state)

                    patient_location = Patient(self.next_id(), (x, y), self, not_critical_patient, countdown)
                    self.grid.place_agent(patient_location, (x, y))
                    self.schedule.add(patient_location)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(FirstAidRobot ),
                    self.schedule.get_type_count(ExplorerDrone),
                    self.schedule.get_type_count(Patient , lambda x: x.not_critical_patient),
                ]
            )

    def grid_stats(model, it):
        df = pd.DataFrame(np.zeros((model.grid.height)))
        for (states, x, y) in model.grid.coord_iter():
            c = None
            for i in states:
                c = i.model
            df.loc[x,y] = c
        df = pd.DataFrame(df.stack(), columns=['value']).reset_index()
        df['iter'] = [it]*len(df)
        return df

    def run_model(self, step_count=5):

        if self.verbose:
            print("Initial number firstaid terrain robots : ", self.schedule.get_type_count(FirstAidRobot))
            print("Initial number explorer drones : ", self.schedule.get_type_count(ExplorerDrone))
            print(
                "Initial number patients: ",
                self.schedule.get_type_count(Patient, lambda x: x.not_critical_patient),
            )

        if self.verbose:
            print("Final number firstaid terrain robots: ", self.schedule.get_type_count(FirstAidRobot))
            print("Final number explorer drones: ", self.schedule.get_type_count(ExplorerDrone))
            print(
                "Final number patients in risk: ",
                self.schedule.get_type_count(Patient, lambda x: x.not_critical_patient),
            )
