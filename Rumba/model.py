from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import Floor, Rumba

class rumbaModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height, density, max_time):

        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 
        self.density = density
        self.max_time = max_time

        self.datacollector = DataCollector(
            {
                "Clean": lambda m: self.count_type(m, "Clean"),
                "Dirty": lambda m: self.count_type(m, "Dirty"),
            }
        )
       
        for i in range (self.num_agents):
           agent = Rumba(i, (1,1), self)
           self.grid._place_agent((1,1), agent)
           self.schedule.add(agent)

        for (contents, x, y) in self.grid.coord_iter():
            state = "Dirty"
            if self.random.random() < density:
                state = "Clean"
            
            new_floor = Floor((x,y),state,self)

            self.grid._place_agent((x,y),new_floor)
            self.schedule.add(new_floor)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)

        if self.count_type(self, "Dirty") == 0 or self.max_time == 0:
            self.running = False
        self.max_time -=1

    @staticmethod
    def count_type(model, state):
        count = 0
        for floor in model.schedule.agents:
            if isinstance(floor, Floor) and floor.state == state:
                count +=1
        return count