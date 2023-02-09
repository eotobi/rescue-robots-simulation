import mesa

from rescue_robots.agents import FirstAidRobot, ExplorerDrone, Patient
from rescue_robots.model import RescueRobots


def rescue_robot_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is ExplorerDrone:
        portrayal["Shape"] = "rescue_robots/resources/droned.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1


    elif type(agent) is FirstAidRobot:
        portrayal["Shape"] = "rescue_robots/resources/terrain.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.battery_level, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is Patient:
        if agent.not_critical_patient:
            portrayal["Shape"] = "rescue_robots/resources/person.png"
        else:
            portrayal["Shape"] = "rescue_robots/resources/personcritical.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 0
        
    return portrayal


canvas_element = mesa.visualization.CanvasGrid(rescue_robot_portrayal, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "FirstAid Terrain Robots", "Color": "#AA0000"},
        {"Label": "Explorer Drones", "Color": "#666666"},
        {"Label": "Patients", "Color": "#00AA00"},
    ],
    data_collector_name='datacollector'
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "bad_health_status": mesa.visualization.Checkbox("Patient are in bad status", True),
    "initial_explorer_drones": mesa.visualization.Slider("Initial Number of Explorer Drones", 3, 0, 20),
    "initial_firstaid_robots": mesa.visualization.Slider("Initial Number of FirstAid Robots", 3, 0, 20),
    "initial_patients": mesa.visualization.Slider(
        "Initial Number of Patients", 3,0,10
    ),
    
}

server = mesa.visualization.ModularServer(
    RescueRobots, [canvas_element, chart_element], "Mount Green Rescue Mission", model_params
)
server.port = 8521
