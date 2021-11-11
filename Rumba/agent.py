from mesa import Agent

class Rumba(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, pos, model):

        super().__init__(pos, model)
        self.direction = 4
        self.unique_id = unique_id
        self.pos = pos
        self.cleaned = 0

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False) 

        self.direction = self.random.randint(0,len(possible_steps)-1)
        self.model.grid.move_agent(self, possible_steps[self.direction])
        
        # Checks which grid cells are dirty
        #freeSpaces = list(map(lambda x, y : True if self.model.grid[x][y].state == "Dirty" else False, possible_steps))

        # If the cell is dirty, moves the agent to that cell;
        # if freeSpaces[self.direction]:
        #     self.model.grid.move_agent(self, possible_steps[self.direction])
        #     print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        # else:
        #     print(f"No se puede mover de {self.pos} en esa direccion.")

    def clean(self):

        (x,y) = self.pos
        cell = self.model.grid.get_cell_list_contents([self.pos])
        if cell[0].state == "Dirty":
            cell[0].state = "Clean"
            self.cleaned += 1

    
        


    def step(self):
        self.move()
        self.clean()

class Floor(Agent):

    def __init__(self, pos, state, model):
        super().__init__(pos, model)
        self.pos = pos
        self.state = state



    def step(self):
        pass  
