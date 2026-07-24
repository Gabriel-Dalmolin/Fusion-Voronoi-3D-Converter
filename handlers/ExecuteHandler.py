import adsk.core 
import adsk.fusion

from ..scripts import convert_to_voronoi

class ExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, root):
        super().__init__()

        self.root = root


    def notify(self, args: adsk.core.CommandEventArgs) -> None:
        command = args.command
        inputs = command.commandInputs
        
        selection = adsk.core.SelectionCommandInput.cast(inputs.itemById("body")).selection(0)
        body = adsk.fusion.BRepBody.cast(selection.entity)

        radius = float(adsk.core.ValueCommandInput.cast(inputs.itemById("radius")).value)

        n_seeds = int(adsk.core.IntegerSpinnerCommandInput.cast(inputs.itemById("seeds")).value)
        
        convert_to_voronoi(self.root, body, radius, n_seeds)
