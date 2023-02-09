import mesa
from rescue_robots.random_explore import RandomExplore
import time
                
class ExplorerDrone(RandomExplore):
    """
    These robots move in 6 directions: front, back, left, right, up and down.
    Drones locate the persons to be rescued and wait for the first-aid terrain
    robots to reach and deliver first-aid kit , once done, they all return to their base stations.
    """

    battery_level = 100

    def __init__(self, unique_id, pos, model, moore, battery_level= 100):
        super().__init__(unique_id, pos, model, moore=moore)
        self.battery_level = battery_level

    def step(self):
        """
        A model step. Move in random direction in search of patients. 
        """
        self.random_move()
        searching = True

        if self.model.bad_health_status:

            # If there is patient available and First-aid robot has come 
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            patient = [obj for obj in this_cell if isinstance(obj, Patient )]
            terrainRobot = [obj for obj in this_cell if isinstance(obj, FirstAidRobot )]
            if len(patient) > 0:
                if len(terrainRobot) > 0:
                    patient_to_heal = self.random.choice(patient)        
                    self.model.grid.remove_agent(patient_to_heal)
                    self.model.schedule.remove(patient_to_heal)
            else:
                # Reduce energy 
                self.battery_level -= 1
                # If energy is low stop searching, call new Explorer Drone 

                if self.battery_level <= 0:
                    self.model.grid.remove_agent(self)
                    self.model.schedule.remove(self)
                    searching = False

                # Call a new drone:
                if not searching and self.random.random() < self.model.robot_available:
                    explorer_drone = ExplorerDrone(
                        self.model.next_id(), self.pos, self.model, self.moore, self.battery_level
                    )
                    self.model.grid.place_agent(explorer_drone, self.pos)
                    self.model.schedule.add(explorer_drone)
                
class FirstAidRobot(RandomExplore):
    """
    A First-aid terrain robot that moves to explorer drone's location to supply first-aid services.
    On recieval the patient is removed from rescue mission
    """

    battery_level = 100
    patients_found = 0
    timer = 0

    def __init__(self, unique_id, pos, model, moore, battery_level=100,patients_found = 0,timer = 0):
        super().__init__(unique_id, pos, model, moore=moore)
        self.battery_level = battery_level
        self.patients_found = patients_found
        self.timer = timer
    def step(self):
        """
        A model step. Move in random direction in search of patients. 
        """
        self.random_move()
        tic = time.perf_counter()
        searching = True

        if self.model.bad_health_status:

            # If there is patient available
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            patient = [obj for obj in this_cell if isinstance(obj, Patient )]
            #aerialDrone = [obj for obj in this_cell if isinstance(obj, ExplorerDrone )]
            if len(patient) > 0:
                #if len(aerialDrone) > 0:
                    patient_to_heal = self.random.choice(patient)        
                    self.model.grid.remove_agent(patient_to_heal)
                    self.model.schedule.remove(patient_to_heal)
                    self.patients_found += 1
                    if self.patients_found == 3:
                        toc = time.perf_counter()
                        self.timer = toc - tic
                        
            else:
                # Reduce energy 
                self.battery_level -= 1
                # If energy is low stop searching, call new Explorer Drone 

                if self.battery_level <= 0:
                    self.model.grid.remove_agent(self)
                    self.model.schedule.remove(self)
                    # searching = False

                # # Call a new drone:
                # if not searching and self.random.random() < self.model.robot_available:
                #     firstAidRobot = FirstAidRobot(
                #         self.model.next_id(), self.pos, self.model, self.moore, self.battery_level
                #     )
                #     self.model.grid.place_agent(firstAidRobot, self.pos)
                #     self.model.schedule.add(firstAidRobot)
            
        
class Patient(mesa.Agent):
    """
    A patient that is searched by the explorer drones and terrain robots 
    """

    def __init__(self, unique_id, pos, model, not_critical_patient, countdown):
        
        super().__init__(unique_id, model)
        self.not_critical_patient = not_critical_patient
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if self.not_critical_patient:
            if self.countdown <= 0:
                self.not_critical_patient = False
                self.countdown = self.model.time_to_bad_state
            else:
                self.countdown -= 1


