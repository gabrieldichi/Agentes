from model import rumbaModel
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from agent import Floor, Rumba

colors = {"Dirty":"#A18262", "Clean" : "#DDDDDD"} 

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Filled": "true"}
                 
    if (isinstance(agent, Rumba)):
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        portrayal["Color"] = "green"
    else:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 0
        portrayal["Color"] = colors[agent.state]
        portrayal["w"] = 1
        portrayal["h"] = 1


    return portrayal

model_params = {
    "N" : UserSettableParameter("slider", "Agent density", 5, 1, 20, 1),
    "height" : 10,
    "width" : 10,
    "density" : UserSettableParameter("slider", "Cell density", 0.5, 0.01, 1.0, 0.1),
    "max_time" : UserSettableParameter("slider", "Time / Steps", 100, 10, 150, 1)
}

tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in colors.items()]
)
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(rumbaModel, [grid,  tree_chart], "Random Agents", model_params)

                       
server.port = 8521 # The default
server.launch()