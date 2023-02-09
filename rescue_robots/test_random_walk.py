"""
Testing the RandomExplore by having an ABM composed only of random walker
agents.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.TextVisualization import TextVisualization, TextGrid

from rescue_robots.random_explore import RandomExplore


class ExplorerAgent(RandomExplore):
    """
    Agent which only explores around.
    """

    def step(self):
        self.random_move()


class MountainExplorer(Model):
    """
    Random mountain  explorer world.
    """

    height = 10
    width = 10

    def __init__(self, width, height, agent_count):
        """
        Create a new Explorer World.

        Args:
            width, height: Mountain size.
            agent_count: How many agents to create.
        """
        self.height = height
        self.width = width
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.agent_count = agent_count

        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.agent_count):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            a = ExplorerAgent(i, (x, y), self, True)
            self.schedule.add(a)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()


class MountainExplorerVisualization(TextVisualization):
    """
    ASCII Visualization for a Mt.Green explorer agent.
    Each cell is displayed as the number of agents currently in that cell.
    """

    def __init__(self, model):
        """
        Create a new visualization for a MountainExplorer instance.

        args:
            model: An instance of a MountainExplorer model.
        """
        self.model = model
        grid_visualization = TextGrid(self.model.grid, None)
        grid_visualization.converter = lambda x: str(len(x))
        self.elements = [grid_visualization]


if __name__ == "__main__":
    print("Testing 10x10 Mt. Green, with 50 random walkers, for 10 steps.")
    model = MountainExplorer(10, 10, 50)
    visualize = MountainExplorerVisualization(model)
    for i in range(10):
        print("Step:", str(i))
        visualize.step()
